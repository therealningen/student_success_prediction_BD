"""
Geresnių sintetinių duomenų generavimas
Bazuojasi ant 15 tikrų rizikos studentų iš originalios apklausos
"""
import pandas as pd
import numpy as np

def generate_realistic_from_real_15(real_risk_df, n=40):
    """
    Generuoja sintetinius studentus bazuojantis ant tikrų 15 rizikos studentų
    Išlaiko požymių svarbą ir natūralius ryšius
    """
    synthetic = []
    
    print(f"Generuojama {n} sintetinių studentų iš {len(real_risk_df)} tikrų rizikos studentų...")
    
    for i in range(n):
        # Pasirinkti atsitiktinį tikrą studentą kaip bazę
        base = real_risk_df.sample(1, random_state=42+i).iloc[0].copy()
        
        new_student = {}
        
        # SVARBŪS požymiai - mažas noise (išlaikyti tikslumą)
        new_student['brandos_egzaminas_1'] = np.clip(
            base['brandos_egzaminas_1'] + np.random.normal(0, 5), 0, 100
        )
        new_student['brandos_egzaminas_2'] = np.clip(
            base['brandos_egzaminas_2'] + np.random.normal(0, 5), 0, 100
        )
        new_student['brandos_egzaminas_3'] = np.clip(
            base['brandos_egzaminas_3'] + np.random.normal(0, 5), 0, 100
        )
        new_student['savarankisko_mokymosi_val'] = np.clip(
            base['savarankisko_mokymosi_val'] + np.random.normal(0, 2), 0, 60
        )
        new_student['socialiniu_tinklu_val'] = np.clip(
            base['socialiniu_tinklu_val'] + np.random.normal(0, 1), 0, 24
        )
        new_student['lankomumas_proc'] = np.clip(
            base['lankomumas_proc'] + np.random.normal(0, 5), 0, 100
        )
        new_student['dvyliktos_klases_vidurkis'] = np.clip(
            base['dvyliktos_klases_vidurkis'] + np.random.normal(0, 0.3), 0, 10
        )
        
        # MAŽIAU SVARBŪS - didesnis noise
        new_student['darbo_valandos'] = np.clip(
            base['darbo_valandos'] + np.random.normal(0, 5), 0, 60
        )
        new_student['miego_valandos'] = np.clip(
            base['miego_valandos'] + np.random.normal(0, 1), 3, 12
        )
        new_student['streso_lygis'] = np.clip(
            int(base['streso_lygis'] + np.random.choice([-1, 0, 1])), 1, 5
        )
        new_student['finansinis_stresas'] = np.clip(
            int(base['finansinis_stresas'] + np.random.choice([-1, 0, 1])), 1, 5
        )
        
        # Studijų vidurkis (jei yra)
        if 'studiju_vidurkis' in base.index:
            new_student['studiju_vidurkis'] = np.clip(
                base['studiju_vidurkis'] + np.random.normal(0, 0.5), 0, 10
            )
        
        # Rizika lieka 1 (ketina mesti - 4 arba 5)
        new_student['ketinu_mesti_studijas'] = np.random.choice([4, 5], p=[0.7, 0.3])
        new_student['rizika'] = 1
        
        synthetic.append(new_student)
    
    return pd.DataFrame(synthetic)


def main():
    print("=" * 60)
    print("GERESNIŲ SINTETINIŲ DUOMENŲ GENERAVIMAS")
    print("=" * 60)
    
    # 1. Įkelti originalius 334 duomenis
    print("\n1. Įkeliami originalūs apklausos duomenys...")
    original_file = 'data/Studentų akademinės sėkmės apklausa (Atsakymai).csv'
    df_original = pd.read_csv(original_file)
    print(f"   Įkelta: {len(df_original)} įrašų")
    
    # 2. Konvertuoti stulpelius
    print("\n2. Konvertuojami stulpeliai...")
    df = df_original.rename(columns={
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
    
    # Išvalyti duomenis
    feature_columns = [
        'lankomumas_proc', 'savarankisko_mokymosi_val', 'streso_lygis',
        'darbo_valandos', 'miego_valandos', 'socialiniu_tinklu_val',
        'dvyliktos_klases_vidurkis', 'brandos_egzaminas_1',
        'brandos_egzaminas_2', 'brandos_egzaminas_3', 'finansinis_stresas'
    ]
    
    for col in feature_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace('%', '').str.replace('-', '').str.replace('/', '').str.replace(',', '.'),
                errors='coerce'
            )
    
    # Pridėti studiju_vidurkis jei yra
    if 'studiju_vidurkis' in df.columns:
        df['studiju_vidurkis'] = pd.to_numeric(df['studiju_vidurkis'], errors='coerce')
        feature_columns.append('studiju_vidurkis')
    
    # Sukurti rizikos kintamąjį
    df['rizika'] = df['ketinu_mesti_studijas'].apply(lambda x: 1 if x >= 4 else 0)
    
    print(f"   Konvertuota {len(feature_columns)} požymių")
    
    # 3. Išfiltruoti 15 tikrų rizikos studentų
    print("\n3. Išfiltruojami tikri rizikos studentai...")
    real_risk = df[df['rizika'] == 1][feature_columns + ['ketinu_mesti_studijas', 'rizika']].copy()
    print(f"   Rasta: {len(real_risk)} tikrų rizikos studentų")
    print(f"   Nerizikos: {(df['rizika']==0).sum()} studentų")
    
    if len(real_risk) == 0:
        print("\n❌ KLAIDA: Nerasta rizikos studentų!")
        return
    
    # 4. Generuoti 80 sintetinių
    print("\n4. Generuojami sintetiniai duomenys...")
    synthetic_risk = generate_realistic_from_real_15(real_risk, n=80)
    print(f"   Sugeneruota: {len(synthetic_risk)} sintetinių rizikos studentų")
    
    # 5. Paruošti galutinį dataset
    print("\n5. Ruošiamas galutinis dataset...")
    
    # Pasiimti tik reikalingus stulpelius iš originalių
    df_clean = df[feature_columns + ['ketinu_mesti_studijas', 'rizika']].copy()
    
    # Sujungti su sintetiniais
    df_final = pd.concat([df_clean, synthetic_risk], ignore_index=True)
    
    print(f"   Galutinis dataset: {len(df_final)} įrašų")
    print(f"   - Nerizikos: {(df_final['rizika']==0).sum()} ({(df_final['rizika']==0).sum()/len(df_final)*100:.1f}%)")
    print(f"   - Rizikos: {(df_final['rizika']==1).sum()} ({(df_final['rizika']==1).sum()/len(df_final)*100:.1f}%)")
    
    # 6. Išsaugoti
    print("\n6. Išsaugoma...")
    output_file = 'data/students_data.csv'
    df_final.to_csv(output_file, index=False)
    print(f"   Issaugota: {output_file}")
    
    print("\n" + "=" * 60)
    print("BAIGTA!")
    print("=" * 60)
    print("\nDabar galite paleisti: python train_model.py")
    print("\nPožymių svarba turėtų būti panaši į originalią!")


if __name__ == "__main__":
    main()
