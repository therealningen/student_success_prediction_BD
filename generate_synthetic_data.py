"""
Sintetinių duomenų generavimas rizikos grupei
"""
import pandas as pd
import numpy as np

def generate_risk_students(n=50):
    """
    Generuoja sintetinius rizikos grupės studentų duomenis su variacijomis
    """
    np.random.seed(42)
    
    data = []
    for i in range(n):
        # Pasirenkame rizikos tipą
        risk_type = np.random.choice(['classic', 'burnout', 'financial', 'edge_case'], p=[0.5, 0.25, 0.15, 0.1])
        
        if risk_type == 'classic':  # Klasikinis rizikos studentas
            lankomumas = np.random.randint(20, 60)
            mokymasis = np.random.randint(0, 5)
            stresas = np.random.randint(3, 6)
            darbas = np.random.randint(30, 50)
            miegas = np.random.randint(4, 6)
            socialiniai = np.random.randint(5, 12)
            vidurkis = round(np.random.uniform(5.0, 7.0), 1)
            finansinis = np.random.randint(4, 6)
            
        elif risk_type == 'burnout':  # Perdegęs studentas (buvo geras, dabar blogai)
            lankomumas = np.random.randint(40, 75)
            mokymasis = np.random.randint(5, 15)  # Dar bando mokytis
            stresas = 5  # Labai aukštas
            darbas = np.random.randint(20, 40)
            miegas = np.random.randint(3, 6)  # Labai mažai
            socialiniai = np.random.randint(1, 4)  # Mažai laiko
            vidurkis = round(np.random.uniform(6.5, 8.0), 1)  # Buvo geresnis
            finansinis = np.random.randint(2, 5)
            
        elif risk_type == 'financial':  # Finansinės problemos
            lankomumas = np.random.randint(50, 80)  # Bando lankyti
            mokymasis = np.random.randint(3, 10)
            stresas = np.random.randint(4, 6)
            darbas = np.random.randint(35, 60)  # Labai daug dirba
            miegas = np.random.randint(4, 7)
            socialiniai = np.random.randint(1, 5)  # Nėra laiko
            vidurkis = round(np.random.uniform(6.0, 8.0), 1)
            finansinis = 5  # Labai aukštas
            
        else:  # edge_case - keistas atvejis
            lankomumas = np.random.randint(10, 90)  # Bet kas
            mokymasis = np.random.randint(0, 20)
            stresas = np.random.randint(2, 6)
            darbas = np.random.randint(0, 50)
            miegas = np.random.randint(4, 9)
            socialiniai = np.random.randint(1, 12)
            vidurkis = round(np.random.uniform(5.0, 8.5), 1)
            finansinis = np.random.randint(1, 6)
        
        # Koreliacijos: daug dirba -> mažai mokosi
        if darbas > 35:
            mokymasis = max(0, mokymasis - np.random.randint(2, 5))
        
        # Koreliacijos: mažai miega -> aukštas stresas
        if miegas < 6:
            stresas = min(5, stresas + 1)
        
        student = {
            'lankomumas_proc': lankomumas,
            'savarankisko_mokymosi_val': mokymasis,
            'streso_lygis': stresas,
            'darbo_valandos': darbas,
            'miego_valandos': miegas,
            'socialiniu_tinklu_val': socialiniai,
            'studiju_vidurkis': vidurkis,
            'dvyliktos_klases_vidurkis': round(np.random.uniform(6.0, 8.5), 1),
            'brandos_egzaminas_1': np.random.randint(20, 70),
            'brandos_egzaminas_2': np.random.randint(20, 70),
            'brandos_egzaminas_3': np.random.randint(20, 70),
            'finansinis_stresas': finansinis,
            'ketinu_mesti_studijas': np.random.choice([4, 5], p=[0.6, 0.4]),
            'rizika': 1
        }
        data.append(student)
    
    return pd.DataFrame(data)

def generate_no_risk_students(n=50):
    """
    Generuoja sintetinius nerizikos grupės studentų duomenis su variacijomis
    """
    np.random.seed(43)
    
    data = []
    for i in range(n):
        # Pasirenkame nerizikos tipą
        student_type = np.random.choice(['excellent', 'good', 'average', 'edge_case'], p=[0.3, 0.4, 0.2, 0.1])
        
        if student_type == 'excellent':  # Puikus studentas
            lankomumas = np.random.randint(90, 101)
            mokymasis = np.random.randint(15, 35)
            stresas = np.random.randint(1, 3)
            darbas = np.random.randint(0, 15)
            miegas = np.random.randint(7, 10)
            socialiniai = np.random.randint(1, 5)
            vidurkis = round(np.random.uniform(8.5, 10.0), 1)
            finansinis = np.random.randint(1, 3)
            egzaminai_range = (70, 100)
            
        elif student_type == 'good':  # Geras studentas
            lankomumas = np.random.randint(80, 95)
            mokymasis = np.random.randint(10, 25)
            stresas = np.random.randint(2, 4)
            darbas = np.random.randint(10, 25)
            miegas = np.random.randint(6, 9)
            socialiniai = np.random.randint(2, 6)
            vidurkis = round(np.random.uniform(7.5, 9.0), 1)
            finansinis = np.random.randint(1, 4)
            egzaminai_range = (60, 85)
            
        elif student_type == 'average':  # Vidutinis studentas
            lankomumas = np.random.randint(70, 90)
            mokymasis = np.random.randint(5, 15)
            stresas = np.random.randint(2, 4)
            darbas = np.random.randint(15, 30)
            miegas = np.random.randint(6, 8)
            socialiniai = np.random.randint(3, 8)
            vidurkis = round(np.random.uniform(7.0, 8.5), 1)
            finansinis = np.random.randint(2, 4)
            egzaminai_range = (50, 75)
            
        else:  # edge_case - keistas bet sėkmingas
            lankomumas = np.random.randint(50, 100)  # Žemas bet sėkmingas
            mokymasis = np.random.randint(5, 30)
            stresas = np.random.randint(1, 5)  # Gali būti aukštas bet tvarkosi
            darbas = np.random.randint(0, 40)
            miegas = np.random.randint(5, 10)
            socialiniai = np.random.randint(1, 10)
            vidurkis = round(np.random.uniform(7.0, 9.5), 1)
            finansinis = np.random.randint(1, 5)
            egzaminai_range = (55, 90)
        
        # Koreliacijos: daug mokosi -> geresnis vidurkis
        if mokymasis > 20:
            vidurkis = min(10.0, vidurkis + round(np.random.uniform(0.2, 0.8), 1))
        
        # Koreliacijos: geras miegas -> mažesnis stresas
        if miegas >= 8:
            stresas = max(1, stresas - 1)
        
        student = {
            'lankomumas_proc': lankomumas,
            'savarankisko_mokymosi_val': mokymasis,
            'streso_lygis': stresas,
            'darbo_valandos': darbas,
            'miego_valandos': miegas,
            'socialiniu_tinklu_val': socialiniai,
            'studiju_vidurkis': vidurkis,
            'dvyliktos_klases_vidurkis': round(np.random.uniform(7.0, 9.5), 1),
            'brandos_egzaminas_1': np.random.randint(*egzaminai_range),
            'brandos_egzaminas_2': np.random.randint(*egzaminai_range),
            'brandos_egzaminas_3': np.random.randint(*egzaminai_range),
            'finansinis_stresas': finansinis,
            'ketinu_mesti_studijas': np.random.choice([1, 2, 3], p=[0.6, 0.25, 0.15]),
            'rizika': 0
        }
        data.append(student)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generuojami sintetiniai duomenys...")
    
    # Įkeliame esamus duomenis
    try:
        existing_df = pd.read_csv('data/students_data.csv')
        print(f"Esami duomenys: {len(existing_df)} įrašų")
        
        # Konvertuojame originalius stulpelius jei reikia
        if '18. Lankomumas šiame semestre (%)' in existing_df.columns:
            print("Konvertuojami originalaus CSV stulpeliai...")
            existing_df = existing_df.rename(columns={
                '18. Lankomumas šiame semestre (%)': 'lankomumas_proc',
                '20. Savarankiško mokymosi valandos per savaitę': 'savarankisko_mokymosi_val',
                '23. Patiriu stiprų stresą': 'streso_lygis',
                '9. Darbo valandos per savaitę': 'darbo_valandos',
                '21. Miego valandos per parą': 'miego_valandos',
                '22. Laikas socialiniuose tinkluose per dieną (val.)': 'socialiniu_tinklu_val',
                '13. Koks yra jūsų bendras visų studijų semestrų vidurkis (1–10)?': 'studiju_vidurkis',
                '17. 12 klasės metinis vidurkis (1–10)': 'dvyliktos_klases_vidurkis',
                '14. Brandos egzaminas: Matematika (1–100, 0=nelaikiau)': 'brandos_egzaminas_1',
                '15. Brandos egzaminas: Lietuvių kalba (1–100, 0=nelaikiau)': 'brandos_egzaminas_2',
                '16. Brandos egzaminas: Anglų kalba (1–100, 0=nelaikiau)': 'brandos_egzaminas_3',
                '7. Finansinis stresas (1–5)': 'finansinis_stresas',
                '24. Ketinu nutraukti studijas': 'ketinu_mesti_studijas'
            })
        
        # Sukuriame rizika stulpelį jei jo nėra
        if 'rizika' not in existing_df.columns and 'ketinu_mesti_studijas' in existing_df.columns:
            existing_df['rizika'] = existing_df['ketinu_mesti_studijas'].apply(lambda x: 1 if x >= 4 else 0)
        
        if 'rizika' in existing_df.columns:
            print(f"  Rizikos grupė: {existing_df['rizika'].sum()}")
            print(f"  Nerizikos grupė: {(existing_df['rizika']==0).sum()}")
    except Exception as e:
        existing_df = pd.DataFrame()
        print(f"Esami duomenys nerasti: {e}")
        print("Kuriami nauji...")
    
    # Generuojame tik rizikos studentus (nerizikos jau užtenka)
    risk_df = generate_risk_students(100)  # 100 rizikos studentų
    
    print(f"\nSugeneruota:")
    print(f"  Rizikos grupė: {len(risk_df)}")
    
    # Sujungiame su esamais duomenimis
    if not existing_df.empty:
        # Pasiimame tik bendrus stulpelius (be rizika)
        common_cols = [col for col in risk_df.columns if col in existing_df.columns and col != 'rizika']
        existing_df_filtered = existing_df[common_cols]
        risk_df_filtered = risk_df[common_cols]
        
        combined_df = pd.concat([existing_df_filtered, risk_df_filtered], ignore_index=True)
    else:
        combined_df = risk_df
    
    # Sukuriame rizika stulpelį jei jo nėra
    if 'rizika' not in combined_df.columns and 'ketinu_mesti_studijas' in combined_df.columns:
        combined_df['rizika'] = combined_df['ketinu_mesti_studijas'].apply(lambda x: 1 if x >= 4 else 0)
    
    # Išsaugome
    combined_df.to_csv('data/students_data.csv', index=False)
    
    print(f"\n✅ Išsaugota į data/students_data.csv")
    print(f"Iš viso: {len(combined_df)} įrašų")
    
    if 'rizika' in combined_df.columns:
        print(f"  Rizikos grupė: {combined_df['rizika'].sum()} ({combined_df['rizika'].sum()/len(combined_df)*100:.1f}%)")
        print(f"  Nerizikos grupė: {(combined_df['rizika']==0).sum()} ({(combined_df['rizika']==0).sum()/len(combined_df)*100:.1f}%)")
    
    print("\n🚀 Dabar paleiskite: python train_model.py")
