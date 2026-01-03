"""
Pagalbinės funkcijos duomenų tvarkymui ir modelio valdymui
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

def create_risk_label(ketinu_mesti):
    """
    Sukuria rizikos etiketę pagal 'ketinu mesti studijas' reikšmę
    4-5 = rizikos grupė (1)
    1-3 = nerizikos grupė (0)
    """
    return 1 if ketinu_mesti >= 4 else 0

def load_and_prepare_data(filepath):
    """
    Įkelia ir paruošia duomenis iš CSV failo
    """
    df = pd.read_csv(filepath)
    
    # Sukuriame rizikos kintamąjį
    if 'ketinu_mesti_studijas' in df.columns:
        df['rizika'] = df['ketinu_mesti_studijas'].apply(create_risk_label)
    
    return df

def get_feature_columns():
    """
    Grąžina požymių stulpelių sąrašą
    """
    return [
        'lankomumas_proc',
        'savarankisko_mokymosi_val',
        'streso_lygis',
        'darbo_valandos',
        'miego_valandos',
        'socialiniu_tinklu_val',
        'studiju_vidurkis',
        'dvyliktos_klases_vidurkis',
        'brandos_egzaminas_1',
        'brandos_egzaminas_2',
        'brandos_egzaminas_3',
        'finansinis_stresas'
    ]

def prepare_features(df, feature_columns):
    """
    Paruošia požymius modeliui
    """
    X = df[feature_columns].copy()
    
    # Užpildome trūkstamas reikšmes vidurkiu
    X = X.fillna(X.mean())
    
    return X

def normalize_features(X_train, X_test=None):
    """
    Normalizuoja požymius naudojant StandardScaler
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    
    return X_train_scaled, scaler

def save_model(model, scaler, model_name='random_forest'):
    """
    Išsaugo modelį ir scaler į models katalogą
    """
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, f'models/{model_name}_model.pkl')
    joblib.dump(scaler, f'models/{model_name}_scaler.pkl')
    print(f"Modelis išsaugotas: models/{model_name}_model.pkl")

def load_model(model_name='random_forest'):
    """
    Įkelia modelį ir scaler iš models katalogo
    """
    model = joblib.load(f'models/{model_name}_model.pkl')
    scaler = joblib.load(f'models/{model_name}_scaler.pkl')
    return model, scaler

def interpret_prediction(prediction, probability, risk_probability=None):
    """
    Interpretuoja prognozės rezultatą su 3 lygiais
    """
    # Jei perduota tikimybė rizikos grupei
    if risk_probability is not None:
        prob = risk_probability
    else:
        prob = probability
    
    # 3 rizikos lygiai pagal tikimybę
    if prob >= 0.60:
        risk_level = "AUKŠTA RIZIKA"
        message = "Studentas priklauso aukštos rizikos grupei. Rekomenduojama skirti papildomą dėmesį."
    elif prob >= 0.30:
        risk_level = "VIDUTINĖ RIZIKA"
        message = "Studentas priklauso vidutinės rizikos grupei. Rekomenduojama stebėti situaciją."
    else:
        risk_level = "ŽEMA RIZIKA"
        message = "Studentas nepriklauso rizikos grupei. Studijų tęsimo tikimybė aukšta."
    
    confidence = prob * 100
    
    return {
        'risk_level': risk_level,
        'message': message,
        'confidence': confidence,
        'prediction': prediction
    }
