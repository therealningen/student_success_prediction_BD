"""
Duomenų normalizavimo skriptas
Konvertuoja originalų apklausos CSV į tinkamą formatą modelio treniravimui
"""
import pandas as pd
import re

def clean_percentage(value):
    """Išvalo procentus ir konvertuoja į skaičių"""
    if pd.isna(value):
        return None
    value = str(value).replace('%', '').replace(',', '.').strip()
    try:
        result = float(value)
        if result > 100:
            return 100
        if result < 0:
            return 0
        return result
    except:
        return None

def clean_number(value):
    """Išvalo skaičius"""
    if pd.isna(value):
        return None
    value = str(value).replace(',', '.').replace('-', '').strip()
    # Jei yra range (pvz "2-3"), imame vidurkį
    if '-' in value or '/' in value:
        parts = re.findall(r'\d+\.?\d*', value)
        if parts:
            return sum(float(p) for p in parts) / len(parts)
    try:
        return float(value)
    except:
        return None

def normalize_survey_data(input_file, output_file='data/students_data.csv'):
    """
    Normalizuoja apklausos duomenis į modelio formatą
    """
    print("=" * 60)
    print("DUOMENŲ NORMALIZAVIMAS")
    print("=" * 60)
    
    # Įkeliame duomenis
    print(f"\n1. Įkeliami duomenys iš: {input_file}")
    df = pd.read_csv(input_file)
    print(f"   Įrašų skaičius: {len(df)}")
    
    # Sukuriame naują DataFrame su reikiamais stulpeliais
    print("\n2. Konvertuojami stulpeliai...")
    
    normalized_df = pd.DataFrame()
    
    # Lankomumas
    normalized_df['lankomumas_proc'] = df['18. Lankomumas šiame semestre (%)'].apply(clean_percentage)
    
    # Savarankiško mokymosi valandos
    normalized_df['savarankisko_mokymosi_val'] = df['20. Savarankiško mokymosi valandos per savaitę'].apply(clean_number)
    
    # Streso lygis
    normalized_df['streso_lygis'] = df['23. Patiriu stiprų stresą'].apply(clean_number)
    
    # Darbo valandos
    normalized_df['darbo_valandos'] = df['9. Darbo valandos per savaitę'].apply(clean_number)
    
    # Miego valandos
    normalized_df['miego_valandos'] = df['21. Miego valandos per parą'].apply(clean_number)
    
    # Socialinių tinklų valandos
    normalized_df['socialiniu_tinklu_val'] = df['22. Laikas socialiniuose tinkluose per dieną (val.)'].apply(clean_number)
    
    # Studijų vidurkis
    normalized_df['studiju_vidurkis'] = df['13. Koks yra jūsų bendras visų studijų semestrų vidurkis (1–10)?'].apply(clean_number)
    
    # 12 klasės vidurkis
    normalized_df['dvyliktos_klases_vidurkis'] = df['17. 12 klasės metinis vidurkis (1–10)'].apply(clean_number)
    
    # Brandos egzaminai
    normalized_df['brandos_egzaminas_1'] = df['14. Brandos egzaminas: Matematika (1–100, 0=nelaikiau)'].apply(clean_number)
    normalized_df['brandos_egzaminas_2'] = df['15. Brandos egzaminas: Lietuvių kalba (1–100, 0=nelaikiau)'].apply(clean_number)
    normalized_df['brandos_egzaminas_3'] = df['16. Brandos egzaminas: Anglų kalba (1–100, 0=nelaikiau)'].apply(clean_number)
    
    # Finansinis stresas
    normalized_df['finansinis_stresas'] = df['7. Finansinis stresas (1–5)'].apply(clean_number)
    
    # Ketinu mesti studijas (TARGET)
    normalized_df['ketinu_mesti_studijas'] = df['24. Ketinu nutraukti studijas'].apply(clean_number)
    
    print("   [OK] Visi stulpeliai konvertuoti")
    
    # Pašaliname eilutes su trūkstamomis reikšmėmis
    print("\n3. Valymas...")
    before_count = len(normalized_df)
    
    # Užpildome trūkstamas reikšmes vidurkiais
    for col in normalized_df.columns:
        if col != 'ketinu_mesti_studijas':
            mean_val = normalized_df[col].mean()
            normalized_df[col] = normalized_df[col].fillna(mean_val)
    
    # Ketinu mesti studijas - pašaliname jei trūksta
    normalized_df = normalized_df.dropna(subset=['ketinu_mesti_studijas'])
    
    after_count = len(normalized_df)
    print(f"   Prieš valymą: {before_count} įrašų")
    print(f"   Po valymo: {after_count} įrašų")
    print(f"   Pašalinta: {before_count - after_count} įrašų")
    
    # Statistika
    print("\n4. Statistika:")
    print(f"   Rizikos grupė (4-5): {(normalized_df['ketinu_mesti_studijas'] >= 4).sum()} ({(normalized_df['ketinu_mesti_studijas'] >= 4).sum()/len(normalized_df)*100:.1f}%)")
    print(f"   Nerizikos grupė (1-3): {(normalized_df['ketinu_mesti_studijas'] < 4).sum()} ({(normalized_df['ketinu_mesti_studijas'] < 4).sum()/len(normalized_df)*100:.1f}%)")
    
    # Išsaugome
    print(f"\n5. Išsaugoma į: {output_file}")
    normalized_df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 60)
    print("NORMALIZAVIMAS BAIGTAS!")
    print("=" * 60)
    print(f"\nDabar galite treniruoti modelį:")
    print(f"  python train_model.py")
    
    return normalized_df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'data/Studentų akademinės sėkmės apklausa (Atsakymai).csv'
    
    try:
        df = normalize_survey_data(input_file)
        print(f"\n[OK] Sėkmingai normalizuota {len(df)} įrašų!")
    except FileNotFoundError:
        print(f"\n❌ Klaida: Nerastas failas {input_file}")
    except Exception as e:
        print(f"\n❌ Klaida: {e}")
        import traceback
        traceback.print_exc()
