"""
Duomenų paruošimo ir išvalymo skriptas
"""
import pandas as pd
import numpy as np
from utils import create_risk_label, get_feature_columns

def prepare_dataset(input_file='data/students_data.csv', output_file='data/students_prepared.csv'):
    """
    Paruošia duomenų rinkinį modelio treniravimui
    """
    print("Įkeliami duomenys...")
    df = pd.read_csv(input_file)
    
    print(f"Įkelta įrašų: {len(df)}")
    print(f"Stulpeliai: {df.columns.tolist()}")
    
    # Sukuriame rizikos kintamąjį
    if 'ketinu_mesti_studijas' in df.columns:
        df['rizika'] = df['ketinu_mesti_studijas'].apply(create_risk_label)
        print(f"\nRizikos pasiskirstymas:")
        print(df['rizika'].value_counts())
    
    # Patikriname trūkstamas reikšmes
    print(f"\nTrūkstamos reikšmės:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # Užpildome trūkstamas reikšmes
    feature_columns = get_feature_columns()
    for col in feature_columns:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mean(), inplace=True)
            print(f"Užpildyta {col} vidurkiu: {df[col].mean():.2f}")
    
    # Pašaliname outliers (pasirenkite pagal poreikį)
    print("\nDuomenų statistika:")
    print(df[feature_columns].describe())
    
    # Išsaugome paruoštus duomenis
    df.to_csv(output_file, index=False)
    print(f"\nParuošti duomenys išsaugoti: {output_file}")
    
    return df

if __name__ == "__main__":
    # Jei turite pradinį CSV failą, paleiskite šį skriptą
    # prepare_dataset('data/students_data.csv', 'data/students_prepared.csv')
    print("Duomenų paruošimo skriptas paruoštas.")
    print("Įdėkite savo CSV failą į data/students_data.csv")
    print("Tada paleiskite: python data_preparation.py")
