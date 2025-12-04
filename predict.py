"""
Prognozavimo funkcijos
"""
import pandas as pd
import numpy as np
from utils import load_model, interpret_prediction, get_feature_columns

def predict_student_risk(student_data, model_name='random_forest'):
    """
    Prognozuoja studento rizikos lygį
    
    Args:
        student_data: dict arba DataFrame su studento duomenimis
        model_name: modelio pavadinimas (default: 'random_forest')
    
    Returns:
        dict su prognozės rezultatais
    """
    # Įkeliame modelį
    model, scaler = load_model(model_name)
    
    # Paruošiame duomenis
    if isinstance(student_data, dict):
        df = pd.DataFrame([student_data])
    else:
        df = student_data.copy()
    
    # Užtikriname, kad visi požymiai yra
    feature_columns = get_feature_columns()
    
    # Patikriname ar visi stulpeliai yra
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Trūksta stulpelių: {missing_cols}")
    
    X = df[feature_columns]
    
    # Užpildome trūkstamas reikšmes (jei yra)
    X = X.fillna(X.mean())
    
    # Normalizuojame
    X_scaled = scaler.transform(X)
    
    # Prognozuojame su žemesniu slenksčiu
    probability = model.predict_proba(X_scaled)[0]
    
    # Naudojame žemesnį slenkstį rizikos grupei (0.25 vietoj 0.5)
    RISK_THRESHOLD = 0.25
    prediction = 1 if probability[1] >= RISK_THRESHOLD else 0
    
    # Interpretuojame rezultatą
    result = interpret_prediction(prediction, probability[prediction])
    
    # Pridedame tikimybes
    result['probability_no_risk'] = probability[0]
    result['probability_risk'] = probability[1]
    
    # Pridedame paaiškinimą KODĖL
    result['reasons'] = explain_prediction(student_data, model, feature_columns)
    
    return result

def predict_academic_performance(student_data):
    """
    Prognozuoja akademinę sėkmę (pažymių prognozė)
    """
    # Skaičiuojame akademinį indeksą
    current_avg = student_data.get('studiju_vidurkis', 7)
    study_hours = student_data.get('savarankisko_mokymosi_val', 10)
    attendance = student_data.get('lankomumas_proc', 85)
    stress = student_data.get('streso_lygis', 3)
    sleep = student_data.get('miego_valandos', 7)
    work_hours = student_data.get('darbo_valandos', 20)
    
    # Prognozuojame vidurkį
    predicted_avg = current_avg
    
    # Teigiami faktoriai
    if study_hours >= 10:
        predicted_avg += 0.5
    elif study_hours >= 7:
        predicted_avg += 0.2
    
    if attendance >= 90:
        predicted_avg += 0.3
    elif attendance >= 80:
        predicted_avg += 0.1
    elif attendance < 70:
        predicted_avg -= 0.4
    
    if sleep >= 7:
        predicted_avg += 0.2
    elif sleep < 6:
        predicted_avg -= 0.3
    
    # Neigiami faktoriai
    if stress >= 4:
        predicted_avg -= 0.4
    elif stress >= 3:
        predicted_avg -= 0.2
    
    if work_hours > 30:
        predicted_avg -= 0.5
    elif work_hours > 20:
        predicted_avg -= 0.2
    
    # Ribojame 1-10
    predicted_avg = max(1, min(10, predicted_avg))
    
    # Nustatome tendenciją
    diff = predicted_avg - current_avg
    if diff > 0.3:
        trend = "📈 GERĖS"
        trend_msg = f"Pažymiai turėtų pagerėti ~{diff:.1f} balo"
        color = "success"
    elif diff < -0.3:
        trend = "📉 BLOGĖS"
        trend_msg = f"Pažymiai gali pablogėti ~{abs(diff):.1f} balo"
        color = "error"
    else:
        trend = "➡️ STABILŪS"
        trend_msg = "Pažymiai išliks panašūs"
        color = "info"
    
    return {
        'current_avg': current_avg,
        'predicted_avg': predicted_avg,
        'trend': trend,
        'trend_msg': trend_msg,
        'color': color,
        'diff': diff
    }

def explain_prediction(student_data, model, feature_columns):
    """
    Paaiškina kodėl studentas rizikos/nerizikos grupėje
    """
    reasons = []
    
    # Gauname feature importance
    if hasattr(model, 'feature_importances_'):
        importance = dict(zip(feature_columns, model.feature_importances_))
        top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Analizuojame kiekvieną požymį
    if student_data.get('lankomumas_proc', 100) < 70:
        reasons.append(f"❌ Žemas lankomumas ({student_data['lankomumas_proc']:.0f}%)")
    elif student_data.get('lankomumas_proc', 0) >= 90:
        reasons.append(f"✅ Aukštas lankomumas ({student_data['lankomumas_proc']:.0f}%)")
    
    if student_data.get('streso_lygis', 1) >= 4:
        reasons.append(f"❌ Aukštas streso lygis ({student_data['streso_lygis']}/5)")
    elif student_data.get('streso_lygis', 5) <= 2:
        reasons.append(f"✅ Žemas streso lygis ({student_data['streso_lygis']}/5)")
    
    if student_data.get('miego_valandos', 8) < 6:
        reasons.append(f"❌ Per mažai miega ({student_data['miego_valandos']:.0f}h)")
    elif student_data.get('miego_valandos', 0) >= 7:
        reasons.append(f"✅ Pakankamas miegas ({student_data['miego_valandos']:.0f}h)")
    
    if student_data.get('darbo_valandos', 0) > 30:
        reasons.append(f"❌ Daug dirba ({student_data['darbo_valandos']:.0f}h/savaitę)")
    elif student_data.get('darbo_valandos', 40) <= 15:
        reasons.append(f"✅ Nedaug dirba ({student_data['darbo_valandos']:.0f}h/savaitę)")
    
    if student_data.get('savarankisko_mokymosi_val', 20) < 5:
        reasons.append(f"❌ Mažai mokosi savarankiškai ({student_data['savarankisko_mokymosi_val']:.0f}h/savaitę)")
    elif student_data.get('savarankisko_mokymosi_val', 0) >= 10:
        reasons.append(f"✅ Daug mokosi savarankiškai ({student_data['savarankisko_mokymosi_val']:.0f}h/savaitę)")
    
    avg_exam = (student_data.get('brandos_egzaminas_1', 0) + 
                student_data.get('brandos_egzaminas_2', 0) + 
                student_data.get('brandos_egzaminas_3', 0)) / 3
    if avg_exam > 0 and avg_exam < 60:
        reasons.append(f"❌ Žemi brandos egzaminų balai ({avg_exam:.0f})")
    elif avg_exam >= 75:
        reasons.append(f"✅ Geri brandos egzaminų balai ({avg_exam:.0f})")
    
    if student_data.get('finansinis_stresas', 1) >= 4:
        reasons.append(f"❌ Aukštas finansinis stresas ({student_data['finansinis_stresas']}/5)")
    
    if not reasons:
        reasons.append("ℹ️ Visi rodikliai vidutiniški")
    
    return reasons

def predict_batch(data_file, model_name='random_forest', output_file='predictions.csv'):
    """
    Prognozuoja keliems studentams iš CSV failo
    """
    print(f"Įkeliami duomenys iš {data_file}...")
    df = pd.read_csv(data_file)
    
    print(f"Prognozuojama {len(df)} studentams...")
    
    predictions = []
    for idx, row in df.iterrows():
        try:
            result = predict_student_risk(row.to_dict(), model_name)
            predictions.append({
                'index': idx,
                'prediction': result['prediction'],
                'risk_level': result['risk_level'],
                'confidence': result['confidence'],
                'probability_risk': result['probability_risk']
            })
        except Exception as e:
            print(f"Klaida eilutėje {idx}: {e}")
            predictions.append({
                'index': idx,
                'prediction': None,
                'risk_level': 'ERROR',
                'confidence': 0,
                'probability_risk': 0
            })
    
    # Išsaugome rezultatus
    results_df = pd.DataFrame(predictions)
    results_df.to_csv(output_file, index=False)
    
    print(f"\nPrognozės išsaugotos: {output_file}")
    print(f"Rizikos grupė: {(results_df['prediction']==1).sum()} studentų")
    print(f"Nerizikos grupė: {(results_df['prediction']==0).sum()} studentų")
    
    return results_df

if __name__ == "__main__":
    # Pavyzdys kaip naudoti
    print("Prognozavimo modulis paruoštas.")
    print("\nPavyzdys:")
    print("""
    from predict import predict_student_risk
    
    student = {
        'lankomumas_proc': 85,
        'savarankisko_mokymosi_val': 10,
        'streso_lygis': 3,
        'darbo_valandos': 20,
        'miego_valandos': 7,
        'socialiniu_tinklu_val': 2,
        'dvyliktos_klases_vidurkis': 8.5,
        'brandos_egzaminas_1': 75,
        'brandos_egzaminas_2': 80,
        'brandos_egzaminas_3': 70,
        'finansinis_stresas': 2
    }
    
    result = predict_student_risk(student)
    print(result)
    """)
