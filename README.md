# 🎓 Studentų Akademinės Sėkmės Prognozė

Sistema prognozuoja studentų studijų nutraukimo riziką naudojant mašininį mokymąsi.

## 📋 Technologijos

- Python 3.10+
- scikit-learn (ML modeliai)
- pandas, numpy (duomenų apdorojimas)
- Streamlit (UI)
- MySQL (duomenų bazė)
- joblib (modelio išsaugojimas)
- matplotlib, plotly (grafikai)

## 🚀 Greitas startas

### 1. Įdiegti priklausomybes

```bash
pip install -r requirements.txt
```

### 2. Paruošti duomenis

Įdėkite savo CSV failą į `data/students_data.csv` su šiais stulpeliais:
- lankomumas_proc
- savarankisko_mokymosi_val
- streso_lygis
- darbo_valandos
- miego_valandos
- socialiniu_tinklu_val
- dvyliktos_klases_vidurkis
- brandos_egzaminas_1
- brandos_egzaminas_2
- brandos_egzaminas_3
- finansinis_stresas
- ketinu_mesti_studijas (1-5)

### 3. Treniruoti modelį

```bash
python train_model.py
```

Tai sukurs:
- `models/random_forest_model.pkl`
- `models/random_forest_scaler.pkl`
- `models/feature_importance.csv`
- `models/feature_importance.png`
- `models/model_comparison.csv`
- `models/confusion_matrix_*.png` (visiems modeliams)

### 4. Paleisti Streamlit aplikaciją

```bash
streamlit run streamlit_app.py
```

Aplikacija atidarys naršyklėje adresu: http://localhost:8501

## 📁 Projekto struktūra

```
student_success_prediction/
│
├── data/
│   └── students_data.csv          # Jūsų duomenų failas
│
├── models/
│   ├── random_forest_model.pkl    # Išsaugotas modelis
│   ├── random_forest_scaler.pkl   # Normalizavimo scaler
│   └── feature_importance.csv     # Požymių svarba
│
├── data_preparation.py            # Duomenų paruošimas
├── train_model.py                 # Modelių treniravimas
├── predict.py                     # Prognozavimo funkcijos
├── streamlit_app.py               # UI aplikacija
├── utils.py                       # Pagalbinės funkcijos
├── requirements.txt               # Python bibliotekos
├── database.sql                   # MySQL schema
└── README.md                      # Ši instrukcija
```

## 🎯 Modeliai

Sistema trenruoja 3 modelius:
1. **Logistinė regresija**
2. **Sprendimų medis**
3. **Random Forest** (pagrindinis)

## 📊 Metrikos

Sistema vertina modelius pagal:
- Accuracy (tikslumas)
- F1 Score
- ROC-AUC
- Cross-validation score
- Confusion Matrix (klaidų matrica)

## 💡 Naudojimas

### Prognozė vienam studentui

```python
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
```

### Prognozė keliems studentams

```python
from predict import predict_batch

predict_batch('data/students_data.csv', output_file='predictions.csv')
```

## 🗄️ MySQL duomenų bazė (pasirenkite)

```bash
mysql -u root -p < database.sql
```

## 🐛 Troubleshooting

### Klaida: "Modelis nerastas"
Paleiskite: `python train_model.py`

### Klaida: "Nerastas failas students_data.csv"
Įdėkite CSV failą į `data/` katalogą

### Klaida: "Module not found"
Įdiekite: `pip install -r requirements.txt`

## 📈 Rezultatų interpretacija

- **Rizikos grupė (1)**: Studentas ketina mesti studijas (4-5 balai)
- **Nerizikos grupė (0)**: Studentas tęs studijas (1-3 balai)

## 🔧 Papildomi patobulinimai

1. **Hiperparametrų optimizavimas**: GridSearchCV
2. **SMOTE**: Duomenų balanso gerinimas
3. **Daugiau požymių**: Pridėti naujus kintamuosius
4. **Deep Learning**: Neural network modelis
5. **API**: REST API su Flask/FastAPI
6. **Dashboard**: Išplėstinė analitika su Plotly Dash

## 📝 Licencija

Šis projektas skirtas akademiniams tikslams.
