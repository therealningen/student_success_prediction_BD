"""
Streamlit UI aplikacija studentų rizikos prognozei
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from predict import predict_student_risk, predict_academic_performance
from utils import load_model, get_feature_columns
from database import init_database, save_student, save_prediction, get_all_students, get_predictions_stats, get_untrained_students, mark_students_as_trained
import joblib

st.set_page_config(page_title="Studentų Rizikos Prognozė", layout="wide")

# Inicializuojame duomenų bazę
init_database()

st.title("🎓 Studentų Akademinės Sėkmės Prognozė")
st.markdown("Sistema prognozuoja studijų nutraukimo riziką naudojant mašininį mokymąsi")

# Statistikos skydelis
stats = get_predictions_stats()
df_all = get_all_students()
df_untrained = get_untrained_students()
total_in_db = len(df_all)
untrained_count = len(df_untrained)

if stats['total'] > 0 or total_in_db > 0:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Iš viso prognozių", stats['total'])
    with col2:
        st.metric("Rizikos grupė", stats['risk'])
    with col3:
        st.metric("Vid. pasitikėjimas", f"{stats['avg_confidence']:.1f}%")
    with col4:
        st.metric("⚠️ Nepertreniruota", untrained_count, help="Naujų duomenų, kurie dar nenaudoti modelio treniravimui")

# Sidebar su įvesties laukais
st.sidebar.header("📝 Studento duomenys")
st.sidebar.markdown("*Užpildykite laukus paeiliui*")

# Inicializuojame session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'confirm_predict' not in st.session_state:
    st.session_state.confirm_predict = False

# Sekvenciniai įvesties laukai
lankomumas = st.sidebar.slider("1️⃣ Lankomumas (%)", 0, 100, 85, 5, key="lankomumas")
if lankomumas != 85:
    st.session_state.step = max(st.session_state.step, 2)

savarankiskas = None
if st.session_state.step >= 2:
    savarankiskas = st.sidebar.number_input("2️⃣ Savarankiško mokymosi valandos per savaitę", 0, 50, 10, 1, key="savarankiskas")
    if savarankiskas != 10:
        st.session_state.step = max(st.session_state.step, 3)

stresas = None
if st.session_state.step >= 3:
    stresas = st.sidebar.slider("3️⃣ Streso lygis (1-5)", 1, 5, 3, 1, key="stresas")
    if stresas != 3:
        st.session_state.step = max(st.session_state.step, 4)

darbas = None
if st.session_state.step >= 4:
    darbas = st.sidebar.number_input("4️⃣ Darbo valandos per savaitę", 0, 60, 20, 1, key="darbas")
    if darbas != 20:
        st.session_state.step = max(st.session_state.step, 5)

miegas = None
if st.session_state.step >= 5:
    miegas = st.sidebar.slider("5️⃣ Miego valandos per parą", 0, 12, 7, 1, key="miegas")
    if miegas != 7:
        st.session_state.step = max(st.session_state.step, 6)

socialiniai = None
if st.session_state.step >= 6:
    socialiniai = st.sidebar.number_input("6️⃣ Socialinių tinklų valandos per dieną", 0, 12, 2, 1, key="socialiniai")
    if socialiniai != 2:
        st.session_state.step = max(st.session_state.step, 7)

studiju_vidurkis = None
if st.session_state.step >= 7:
    studiju_vidurkis = st.sidebar.number_input("7️⃣ Studijų vidurkis (1-10)", 0.0, 10.0, 7.5, 0.1, key="studiju_vidurkis")
    if studiju_vidurkis != 7.5:
        st.session_state.step = max(st.session_state.step, 8)

vidurkis = None
if st.session_state.step >= 8:
    vidurkis = st.sidebar.number_input("8️⃣ 12 klasės metinis vidurkis", 1.0, 10.0, 8.5, 0.1, key="vidurkis")
    if vidurkis != 8.5:
        st.session_state.step = max(st.session_state.step, 9)

egzaminas1 = None
if st.session_state.step >= 9:
    egzaminas1 = st.sidebar.number_input("9️⃣ Brandos egzaminas (Matematika)", 0, 100, 75, 1, key="egzaminas1")
    if egzaminas1 != 75:
        st.session_state.step = max(st.session_state.step, 10)

egzaminas2 = None
if st.session_state.step >= 10:
    egzaminas2 = st.sidebar.number_input("🔟 Brandos egzaminas (Lietuvių kalba)", 0, 100, 80, 1, key="egzaminas2")
    if egzaminas2 != 80:
        st.session_state.step = max(st.session_state.step, 11)

egzaminas3 = None
if st.session_state.step >= 11:
    egzaminas3 = st.sidebar.number_input("1️⃣1️⃣ Brandos egzaminas (Anglų kalba)", 0, 100, 70, 1, key="egzaminas3")
    if egzaminas3 != 70:
        st.session_state.step = max(st.session_state.step, 12)

finansinis = None
if st.session_state.step >= 12:
    finansinis = st.sidebar.slider("1️⃣2️⃣ Finansinis stresas (1-5)", 1, 5, 2, 1, key="finansinis")
    if finansinis != 2:
        st.session_state.step = max(st.session_state.step, 13)

# Paslėptas laukas su checkbox
ketinu_mesti = None
has_real_answer = False
show_hidden_field = st.sidebar.checkbox("🔓 Rodyti paslėptą klausimą (tik testavimui)", value=False)

if show_hidden_field and st.session_state.step >= 13:
    ketinu_mesti = st.sidebar.slider("1️⃣3️⃣ Ar ketini mesti studijas? (1-5)", 1, 5, 1, 1, key="ketinu_mesti",
                                      help="1 = Tikrai ne, 5 = Tikrai taip")
    has_real_answer = True  # Studentas tikrai atsakė
else:
    # Jei paslėptas, naudojame default reikšmę (nežinoma)
    ketinu_mesti = 1  # Default reikšmė
    has_real_answer = False  # Neatsakyta

# Tikrinimas ar visi laukai užpildyti (be paslėpto lauko)
all_filled = st.session_state.step >= 13

if not all_filled:
    st.sidebar.info(f"Užpildyta: {st.session_state.step-1}/12")

# Reset mygtukas
if st.sidebar.button("🔄 Išvalyti duomenis"):
    for key in ['lankomumas', 'savarankiskas', 'stresas', 'darbas', 'miegas', 'socialiniai', 'studiju_vidurkis', 'vidurkis', 'egzaminas1', 'egzaminas2', 'egzaminas3', 'finansinis', 'ketinu_mesti']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.step = 1
    st.session_state.confirm_predict = False
    st.rerun()

# Prognozavimo mygtukas (rodomas tik kai visi laukai užpildyti)
proceed = False
if all_filled:
    if not st.session_state.confirm_predict:
        if st.sidebar.button("🔮 Prognozuoti", type="primary"):
            st.session_state.confirm_predict = True
            st.rerun()
    else:
        st.sidebar.warning("⚠️ Ar tikrai norite prognozuoti?")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("✅ Taip", key="confirm_yes"):
                proceed = True
        with col2:
            if st.button("❌ Ne", key="confirm_no"):
                st.session_state.confirm_predict = False
                st.rerun()
else:
    st.session_state.confirm_predict = False

if proceed:
    student_data = {
        'lankomumas_proc': lankomumas,
        'savarankisko_mokymosi_val': savarankiskas,
        'streso_lygis': stresas,
        'darbo_valandos': darbas,
        'miego_valandos': miegas,
        'socialiniu_tinklu_val': socialiniai,
        'studiju_vidurkis': studiju_vidurkis,
        'dvyliktos_klases_vidurkis': vidurkis,
        'brandos_egzaminas_1': egzaminas1,
        'brandos_egzaminas_2': egzaminas2,
        'brandos_egzaminas_3': egzaminas3,
        'finansinis_stresas': finansinis,
        'ketinu_mesti_studijas': ketinu_mesti,
        'has_real_answer': 1 if has_real_answer else 0
    }
    
    # Išsaugome duomenis
    student_id = save_student(student_data)
    
    try:
        result = predict_student_risk(student_data, 'random_forest')
        performance = predict_academic_performance(student_data)
        
        # Išsaugome prognozę
        save_prediction(student_id, result)
        
        # Išvalome patvirtinimo būseną
        st.session_state.confirm_predict = False
        
        # Rezultatų rodymas
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("📊 Rezultatai")
            
            # Modelio prognozė
            st.subheader("🤖 Modelio prognozė")
            if result['prediction'] == 1:
                st.error(f"### ⚠️ {result['risk_level']}")
                st.metric("Tikimybė mesti studijas", f"{result['probability_risk']*100:.1f}%")
            else:
                st.success(f"### ✅ {result['risk_level']}")
                st.metric("Tikimybė tęsti studijas", f"{result['probability_no_risk']*100:.1f}%")
            
            # Akademinė sėkmė
            st.subheader("📚 Akademinės sėkmės prognozė")
            if performance['color'] == 'success':
                st.success(f"### {performance['trend']}")
            elif performance['color'] == 'error':
                st.error(f"### {performance['trend']}")
            else:
                st.info(f"### {performance['trend']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Dabartinis vidurkis", f"{performance['current_avg']:.1f}")
            with col_b:
                st.metric("Prognozuojamas vidurkis", f"{performance['predicted_avg']:.1f}", 
                         delta=f"{performance['diff']:.1f}")
            st.write(performance['trend_msg'])
            
            # Paaiškinimas KODĖL
            st.subheader("🔍 Kodėl modelis taip prognozavo?")
            for reason in result['reasons']:
                st.write(reason)
        
        with col2:
            # Tikimybių grafikas
            fig = go.Figure(go.Bar(
                x=[result['probability_no_risk']*100, result['probability_risk']*100],
                y=['Nerizikos grupė', 'Rizikos grupė'],
                orientation='h',
                marker=dict(color=['green', 'red'])
            ))
            fig.update_layout(
                title="Tikimybės",
                xaxis_title="Tikimybė (%)",
                height=250
            )
            st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.error("❌ Modelis nerastas! Pirmiausia paleiskite: python train_model.py")
    except Exception as e:
        st.error(f"❌ Klaida: {e}")

# Modelio analizė
with st.expander("📈 Modelio analizė"):
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Požymių svarba")
        try:
            importance_df = pd.read_csv('models/feature_importance.csv')
            
            fig2 = go.Figure(go.Bar(
                x=importance_df['importance'],
                y=importance_df['feature'],
                orientation='h',
                marker=dict(color='steelblue')
            ))
            fig2.update_layout(
                xaxis_title="Svarba",
                yaxis_title="Požymis",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        except:
            st.info("Feature importance grafikas nepasiekiamas. Paleiskite train_model.py")
    
    with col_right:
        st.subheader("Confusion Matrix")
        try:
            st.image('models/confusion_matrix_random_forest.png', use_container_width=True)
        except:
            st.info("Confusion matrix nepasiekiamas. Paleiskite train_model.py")

# Duomenų peržiūros skyrius
with st.expander("📈 Duomenų bazės peržiūra"):
    if st.button("Rodyti visus įrašus"):
        df = get_all_students()
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("Nėra įrašų duomenų bazėje")

# Modelio pertreniravimas
with st.expander("🔄 Modelio pertreniravimas"):
    st.markdown("""
    **Pertreniruokite modelį su naujais duomenimis iš duomenų bazės.**
    
    ⚠️ Rekomenduojama pertreniruoti kai:
    - Turite bent 50+ naujų studentų duomenų
    - Praėjo semestras ir turite tikrų rezultatų
    """)
    
    df = get_all_students()
    df_untrained_local = get_untrained_students()
    st.info(f"Duomenų bazėje: {len(df)} įrašai (iš jų {len(df_untrained_local)} nepertreniruoti)")
    
    if len(df_untrained_local) > 0:
        st.warning(f"⚠️ Turite {len(df_untrained_local)} naujų įrašų, kurie dar nenaudoti treniravimui!")
    
    if st.button("🚀 Pertreniruoti modelį", type="primary"):
        if len(df_untrained_local) == 0:
            st.info("ℹ️ Nėra naujų duomenų treniravimui.")
        elif len(df_untrained_local) < 10:
            st.warning("⚠️ Per mažai naujų duomenų! Rekomenduojama turėti bent 50+ naujų įrašų.")
        else:
            with st.spinner("Treniruojamas modelis..."):
                try:
                    import os
                    import sqlite3
                    
                    # Skaitome senus duomenis ir pridedame tik nepertreniruotus
                    if os.path.exists('data/students_data.csv'):
                        old_df = pd.read_csv('data/students_data.csv')
                        combined_df = pd.concat([old_df, df_untrained_local], ignore_index=True)
                        combined_df = combined_df.drop_duplicates()
                    else:
                        combined_df = df_untrained_local
                    
                    # Išsaugome atnaujintus duomenis
                    combined_df.to_csv('data/students_data.csv', index=False)
                    
                    # Paleidžiame treniravimą
                    import subprocess
                    result = subprocess.run(['python', 'train_model.py'], 
                                          capture_output=True, text=True, cwd=os.getcwd())
                    
                    if result.returncode == 0:
                        # Pažymime studentus kaip pertreniruotus
                        mark_students_as_trained()
                        
                        st.success("✅ Modelis sėkmingai pertreniruotas!")
                        st.info(f"Iš viso duomenų: {len(combined_df)} studentų")
                        st.info(f"✅ Pažymėta {len(df_untrained_local)} įrašų kaip pertreniruotų.")
                        st.code(result.stdout[-500:])
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"❌ Klaida: {result.stderr}")
                        
                except Exception as e:
                    st.error(f"❌ Klaida: {e}")

# Informacija apie modelį
with st.expander("ℹ️ Apie modelį"):
    st.markdown("""
    **Naudojamas modelis:** Random Forest Classifier
    
    **Požymiai:**
    - Lankomumas (%)
    - Savarankiško mokymosi valandos
    - Streso lygis (1-5)
    - Darbo valandos
    - Miego valandos
    - Socialinių tinklų valandos
    - 12 klasės metinis vidurkis
    - Brandos egzaminų balai (3)
    - Finansinis stresas (1-5)
    
    **Rizikos grupė:** Studentai, kurie ketina mesti studijas (4-5 balai)
    """)
