"""
Modelių treniravimo skriptas
Trenruoja Logistinę regresiją, Sprendimų medį ir Random Forest
"""
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, recall_score
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from utils import get_feature_columns, prepare_features, normalize_features, save_model
import joblib

# Nustatome darbinį katalogą į skripto vietą
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Sukuriame models aplanką, jei jo nėra
os.makedirs('models', exist_ok=True)

def train_all_models(data_file='data/students_data.csv'):
    """
    Trenruoja visus tris modelius ir išsaugo rezultatus
    """
    print("=" * 60)
    print("STUDENTŲ AKADEMINĖS SĖKMĖS PROGNOZĖS MODELIO TRENIRAVIMAS")
    print("=" * 60)
    
    # Įkeliame duomenis
    print("\n1. Įkeliami duomenys...")
    df = pd.read_csv(data_file)
    
    # Konvertuojame originalius stulpelius jei reikia
    if '18. Lankomumas šiame semestre (%)' in df.columns:
        df = df.rename(columns={
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
    
    # Sukuriame rizikos kintamąjį
    if 'ketinu_mesti_studijas' in df.columns:
        df['rizika'] = df['ketinu_mesti_studijas'].apply(lambda x: 1 if x >= 4 else 0)
    
    print(f"   Įrašų skaičius: {len(df)}")
    print(f"   Rizikos grupė: {df['rizika'].sum()} ({df['rizika'].sum()/len(df)*100:.1f}%)")
    print(f"   Nerizikos grupė: {(df['rizika']==0).sum()} ({(df['rizika']==0).sum()/len(df)*100:.1f}%)")
    
    # Paruošiame požymius
    print("\n2. Paruošiami požymiai...")
    feature_columns = get_feature_columns()
    
    # Išvalome duomenis nuo tekstinių simbolių
    for col in feature_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace('-', '').str.replace('/', '').str.replace(',', '.'), errors='coerce')
    
    X = prepare_features(df, feature_columns)
    y = df['rizika']
    
    print(f"   Požymių skaičius: {len(feature_columns)}")
    print(f"   Požymiai: {', '.join(feature_columns)}")
    
    # Skaidome duomenis (didesnis test set)
    print("\n3. Skaidomi duomenys (70% treniravimui, 30% testavimui)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"   Treniravimo rinkinys: {len(X_train)} įrašų")
    print(f"   Testavimo rinkinys: {len(X_test)} įrašų")
    
    # Normalizuojame
    print("\n4. Normalizuojami duomenys...")
    X_train_scaled, X_test_scaled, scaler = normalize_features(X_train, X_test)
    
    # SMOTE balansavimas (stipresnis)
    print("\n5. Taikomas SMOTE balansavimas...")
    smote = SMOTE(random_state=42, sampling_strategy=0.8, k_neighbors=5)  # 80% balanso
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
    
    # Pridedame mažesnį noise
    print("\n6. Pridedamas noise duomenims...")
    noise = np.random.normal(0, 0.05, X_train_balanced.shape)  # 5% noise
    X_train_balanced = X_train_balanced + noise
    print(f"   Prieš SMOTE - Rizikos grupė: {y_train.sum()} ({y_train.sum()/len(y_train)*100:.1f}%)")
    print(f"   Po SMOTE - Rizikos grupė: {y_train_balanced.sum()} ({y_train_balanced.sum()/len(y_train_balanced)*100:.1f}%)")
    print(f"   Naujų įrašų skaičius: {len(X_train_balanced)}")
    
    # Modelių sąrašas (optimizuoti Recall)
    models = {
        'Logistic Regression': LogisticRegression(
            random_state=42, 
            max_iter=1000, 
            C=0.1,  # Mažesnis regularizavimas
            penalty='l2', 
            solver='saga',
            class_weight='balanced'  # Svarbu!
        ),
        'Decision Tree': DecisionTreeClassifier(
            random_state=42, 
            max_depth=6,  # Didesnis gylis
            min_samples_split=10,
            min_samples_leaf=5,
            class_weight='balanced'  # Svarbu!
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,  # Daugiau medžių
            random_state=42, 
            max_depth=6,  # Didesnis gylis
            min_samples_split=10,
            min_samples_leaf=5,
            max_features='sqrt',
            class_weight='balanced'  # Svarbu!
        )
    }
    
    results = {}
    
    print("\n" + "=" * 60)
    print("MODELIŲ TRENIRAVIMAS IR VERTINIMAS")
    print("=" * 60)
    print(f"Treniravimo duomenų su noise: {len(X_train_balanced)}")
    
    for model_name, model in models.items():
        print(f"\n{'='*60}")
        print(f"Modelis: {model_name}")
        print(f"{'='*60}")
        
        # Treniruojame su SMOTE duomenimis
        print("Treniruojama...")
        model.fit(X_train_balanced, y_train_balanced)
        
        # Prognozuojame
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Skaičiuojame metrikus
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        recall = recall_score(y_test, y_pred)
        
        # Cross-validation su SMOTE duomenimis (10-fold)
        cv_scores = cross_val_score(model, X_train_balanced, y_train_balanced, cv=10, scoring='accuracy')
        
        print(f"\nRezultatai:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {roc_auc:.4f}")
        print(f"  CV Score:  {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        print(f"\nKlasifikacijos ataskaita:")
        print(classification_report(y_test, y_pred, target_names=['Nerizikos grupė', 'Rizikos grupė']))
        
        print(f"\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        # Vizualizuojame confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Nerizikos', 'Rizikos'],
                    yticklabels=['Nerizikos', 'Rizikos'])
        plt.ylabel('Tikroji klasė')
        plt.xlabel('Prognozuota klasė')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.tight_layout()
        cm_filename = f"models/confusion_matrix_{model_name.lower().replace(' ', '_')}.png"
        plt.savefig(cm_filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Confusion matrix išsaugotas: {cm_filename}")
        
        # Išsaugome rezultatus
        results[model_name] = {
            'model': model,
            'accuracy': accuracy,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    # Išsaugome geriausią modelį (Decision Tree - geriausias Recall)
    print("\n" + "=" * 60)
    print("MODELIO IŠSAUGOJIMAS")
    print("=" * 60)
    
    best_model_name = max(results.keys(), key=lambda x: results[x]['recall'])
    print(f"Geriausias modelis (pagal Recall): {best_model_name}")
    print(f"Recall: {results[best_model_name]['recall']:.4f}")
    
    best_model = models[best_model_name]
    save_model(best_model, scaler, 'random_forest')
    
    # Išsaugome visus modelius
    for name, model in models.items():
        model_file = name.lower().replace(' ', '_')
        save_model(model, scaler, model_file)
    
    # Feature importance (Random Forest)
    print("\n" + "=" * 60)
    print("POŽYMIŲ SVARBA (Random Forest)")
    print("=" * 60)
    
    rf_model = models['Random Forest']
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.to_string(index=False))
    
    # Išsaugome feature importance
    feature_importance.to_csv('models/feature_importance.csv', index=False)
    
    # Grafikas
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'], feature_importance['importance'])
    plt.xlabel('Svarba')
    plt.title('Požymių svarba (Random Forest)')
    plt.tight_layout()
    plt.savefig('models/feature_importance.png', dpi=300, bbox_inches='tight')
    print("\nGrafikas išsaugotas: models/feature_importance.png")
    
    # Palyginimo lentelė
    print("\n" + "=" * 60)
    print("MODELIŲ PALYGINIMAS")
    print("=" * 60)
    
    comparison = pd.DataFrame({
        'Modelis': list(results.keys()),
        'Accuracy': [results[m]['accuracy'] for m in results.keys()],
        'Recall': [results[m]['recall'] for m in results.keys()],
        'F1 Score': [results[m]['f1'] for m in results.keys()],
        'ROC-AUC': [results[m]['roc_auc'] for m in results.keys()],
        'CV Mean': [results[m]['cv_mean'] for m in results.keys()]
    })
    
    print(comparison.to_string(index=False))
    comparison.to_csv('models/model_comparison.csv', index=False)
    
    print("\n" + "=" * 60)
    print("TRENIRAVIMAS BAIGTAS!")
    print("=" * 60)
    print("\nIšsaugoti failai:")
    print("  - models/random_forest_model.pkl")
    print("  - models/random_forest_scaler.pkl")
    print("  - models/feature_importance.csv")
    print("  - models/feature_importance.png")
    print("  - models/model_comparison.csv")
    print("  - models/confusion_matrix_logistic_regression.png")
    print("  - models/confusion_matrix_decision_tree.png")
    print("  - models/confusion_matrix_random_forest.png")
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = 'data/students_data.csv'
    
    try:
        results = train_all_models(data_file)
    except FileNotFoundError:
        print(f"\nKlaida: Nerastas failas {data_file}")
        print("Įsitikinkite, kad CSV failas yra teisingoje vietoje.")
    except Exception as e:
        print(f"\nKlaida treniruojant modelį: {e}")
        import traceback
        traceback.print_exc()
