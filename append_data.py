"""
Duomenų pridėjimo skriptas
Prideda naujus normalizuotus duomenis prie esamo students_data.csv
"""
import pandas as pd
from normalize_data import normalize_survey_data

def append_normalized_data(input_file, target_file='data/students_data.csv'):
    """
    Normalizuoja naujus duomenis ir prideda prie esamo failo
    """
    print("=" * 60)
    print("DUOMENŲ PRIDĖJIMAS")
    print("=" * 60)
    
    # Normalizuojame naujus duomenis į laikinį failą
    print(f"\n1. Normalizuojami nauji duomenys iš: {input_file}")
    new_df = normalize_survey_data(input_file, 'data/temp_normalized.csv')
    
    # Įkeliame esamą failą
    print(f"\n2. Įkeliamas esamas failas: {target_file}")
    try:
        existing_df = pd.read_csv(target_file)
        print(f"   Esamų įrašų: {len(existing_df)}")
    except FileNotFoundError:
        print(f"   Failas nerastas, bus sukurtas naujas")
        existing_df = pd.DataFrame()
    
    # Sujungiame
    print(f"\n3. Sujungiami duomenys...")
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        print(f"   Esamų įrašų: {len(existing_df)}")
        print(f"   Naujų įrašų: {len(new_df)}")
        print(f"   Iš viso: {len(combined_df)}")
    else:
        combined_df = new_df
    
    # Išsaugome
    print(f"\n4. Išsaugoma į: {target_file}")
    combined_df.to_csv(target_file, index=False)
    
    print("\n" + "=" * 60)
    print("PRIDĖJIMAS BAIGTAS!")
    print("=" * 60)
    print(f"\nBendra statistika:")
    print(f"  Iš viso įrašų: {len(combined_df)}")
    print(f"  Naujų pridėta: {len(new_df)}")
    print(f"  Rizikos grupė: {(combined_df['ketinu_mesti_studijas'] >= 4).sum()} ({(combined_df['ketinu_mesti_studijas'] >= 4).sum()/len(combined_df)*100:.1f}%)")
    
    # Išvalome laikinį failą
    import os
    if os.path.exists('data/temp_normalized.csv'):
        os.remove('data/temp_normalized.csv')
    
    return combined_df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'data/Studentų akademinės sėkmės apklausa (Atsakymai).csv'
    
    try:
        df = append_normalized_data(input_file)
        print(f"\n[OK] Sėkmingai pridėta!")
    except Exception as e:
        print(f"\n[KLAIDA] {e}")
        import traceback
        traceback.print_exc()
