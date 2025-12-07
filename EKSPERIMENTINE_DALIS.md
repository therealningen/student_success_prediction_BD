# 4. EKSPERIMENTINĖ-PRAKTINĖ DALIS

## 4.3. Atliktas programavimas

### 4.3.1. Programavimo aplinka ir įrankiai

Sistemos kūrimui buvo naudojama:
- **Python 3.10+** - pagrindinė programavimo kalba
- **Visual Studio Code** - integruota kūrimo aplinka
- **Git** - versijų kontrolės sistema
- **pip** - Python paketų valdymo įrankis

### 4.3.2. Pagrindiniai sistemos moduliai

Sistema sudaryta iš 7 pagrindinių Python modulių:

#### 1. **data_preparation.py**
Atsakingas už duomenų paruošimą ir valymo procesus:
- CSV failų įkėlimas
- Duomenų validacija
- Trūkstamų reikšmių apdorojimas
- Duomenų transformacija

#### 2. **train_model.py**
Mašininio mokymosi modelių treniravimo modulis:
- 3 skirtingų algoritmų treniravimas (Logistic Regression, Decision Tree, Random Forest)
- SMOTE balansavimo taikymas
- Cross-validation vertinimas
- Confusion matrix generavimas
- Feature importance analizė

**Pagrindinės funkcijos:**
```python
def train_all_models(data_file='data/students_data.csv')
```

**Treniravimo proceso etapai:**
1. Duomenų įkėlimas (70% treniravimui, 30% testavimui)
2. Požymių normalizavimas (StandardScaler)
3. SMOTE balansavimas (80% sampling_strategy)
4. Modelių treniravimas su optimizuotais hiperparametrais
5. Vertinimas pagal Accuracy, Recall, F1, ROC-AUC
6. Geriausio modelio išsaugojimas

#### 3. **predict.py**
Prognozavimo funkcionalumo modulis:
- Individualių studentų rizikos prognozė
- Paketinė prognozė (batch prediction)
- Akademinės sėkmės prognozė
- Prognozių paaiškinimas (explainability)

**Pagrindinės funkcijos:**
```python
def predict_student_risk(student_data, model_name='random_forest')
def predict_academic_performance(student_data)
def explain_prediction(student_data, model, feature_columns)
```

#### 4. **utils.py**
Pagalbinių funkcijų modulis:
- Modelio įkėlimas/išsaugojimas
- Požymių paruošimas
- Duomenų normalizavimas
- Rezultatų interpretacija

#### 5. **database.py**
Duomenų bazės valdymo modulis:
- SQLite duomenų bazės inicializavimas
- Studentų duomenų saugojimas
- Prognozių istorijos saugojimas
- Statistikos užklausos
- Nepertreniruotų duomenų identifikavimas

**Duomenų bazės schema:**
- `students` - studentų duomenys
- `predictions` - prognozių istorija
- `is_trained` - treniravimo būsenos žymė

#### 6. **streamlit_app.py**
Vartotojo sąsajos modulis (1000+ eilučių):
- Interaktyvi duomenų įvestis
- Sekvencinė formų navigacija
- Prognozių vizualizacija
- Statistikos skydelis
- Modelio pertreniravimo funkcionalumas

#### 7. **generate_synthetic_data.py**
Sintetinių duomenų generavimo modulis:
- Realistinių studentų duomenų kūrimas
- Koreliacijos tarp požymių išlaikymas
- Duomenų augmentacija

#### 8. **normalize_data.py**
Duomenų normalizavimo modulis:
- Originalių apklausos duomenų konvertavimas
- Automatinis stulpelių pavadinimų keitimas
- Procentų ir skaičių valymas
- Trūkstamų reikšmių užpildymas

**Pagrindinė funkcija:**
```python
def normalize_survey_data(input_file, output_file='data/students_data.csv')
```

**Konvertavimo procesas:**
1. Įkelia originalų CSV su ilgais stulpelių pavadinimais
2. Konvertuoja į trumpus pavadinimus (pvz., "18. Lankomumas šiame semestre (%)" → "lankomumas_proc")
3. Valo duomenis (šalina %, konvertuoja range reikšmes)
4. Užpildo trūkstamas reikšmes vidurkiais
5. Išsaugo į `data/students_data.csv`

### 4.3.3. Implementuoti algoritmai

#### Random Forest Classifier (pagrindinis)
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight='balanced',
    random_state=42
)
```

**Hiperparametrų pasirinkimo pagrindimas:**
- `n_estimators=100` - pakankamas medžių skaičius tikslumui
- `max_depth=6` - apsauga nuo overfitting
- `class_weight='balanced'` - disbalanso kompensavimas

#### SMOTE (Synthetic Minority Over-sampling)
```python
SMOTE(
    random_state=42,
    sampling_strategy=0.8,
    k_neighbors=5
)
```

Taikomas rizikos grupės (mažumos klasės) balansavimui.

### 4.3.4. Kodo kokybės užtikrinimas

- **Moduliarumas** - kiekvienas modulis atlieka vieną aiškią funkciją
- **Dokumentacija** - docstrings visoms funkcijoms
- **Klaidų valdymas** - try-except blokai kritinėse vietose
- **Kodo stilius** - PEP 8 standartų laikymasis
- **Komentarai** - lietuvių kalba svarbiose vietose

---

 

## 4.5. Integruotos interaktyvumo (sąveikos su naudotoju) priemonės

### 4.5.1. Interaktyvūs įvesties komponentai

#### Sliders (slankikliai)
```python
lankomumas = st.sidebar.slider("1️⃣ Lankomumas (%)", 0, 100, 85, 5)
stresas = st.sidebar.slider("3️⃣ Streso lygis (1-5)", 1, 5, 3, 1)
```

**Privalumai:**
- Vizualus reikšmių pasirinkimas
- Ribojimas tik leistinoms reikšmėms
- Greitas duomenų įvedimas

#### Number inputs
```python
savarankiskas = st.sidebar.number_input(
    "2️⃣ Savarankiško mokymosi valandos per savaitę", 
    0, 50, 10, 1
)
```

#### Checkbox (paslėptas laukas)
```python
show_hidden_field = st.sidebar.checkbox(
    "🔓 Rodyti paslėptą klausimą (tik testavimui)", 
    value=False
)
```

Leidžia testuoti sistemą su tikrais atsakymais.

### 4.5.2. Patvirtinimo dialogas

Dviejų žingsnių prognozavimas:

**1 žingsnis:**
```python
if st.sidebar.button("🔮 Prognozuoti", type="primary"):
    st.session_state.confirm_predict = True
```

**2 žingsnis:**
```python
st.sidebar.warning("⚠️ Ar tikrai norite prognozuoti?")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("✅ Taip"):
        proceed = True
with col2:
    if st.button("❌ Ne"):
        st.session_state.confirm_predict = False
```

Apsaugo nuo atsitiktinio prognozavimo.

### 4.5.3. Interaktyvūs grafikai (Plotly)

#### Tikimybių stulpelinė diagrama
```python
fig = go.Figure(go.Bar(
    x=[probability_no_risk*100, probability_risk*100],
    y=['Nerizikos grupė', 'Rizikos grupė'],
    orientation='h',
    marker=dict(color=['green', 'red'])
))
st.plotly_chart(fig, use_container_width=True)
```

**Interaktyvumo funkcijos:**
- Hover tooltips
- Zoom in/out
- Pan
- Eksportavimas į PNG

#### Požymių svarbos grafikas
```python
fig2 = go.Figure(go.Bar(
    x=importance_df['importance'],
    y=importance_df['feature'],
    orientation='h',
    marker=dict(color='steelblue')
))
```

### 4.5.4. Realaus laiko atnaujinimai

**Session State valdymas:**
```python
if 'step' not in st.session_state:
    st.session_state.step = 1
```

Užtikrina, kad vartotojo įvestis išlieka tarp puslapio perkrovimų.

**Automatinis perkrovimas:**
```python
st.rerun()
```

Atnaujina puslapį po svarbių veiksmų (reset, pertreniravimas).

### 4.5.5. Vizualinė grįžtamoji informacija

#### Spalviniai pranešimai
- **st.success()** - žalia (sėkmė)
- **st.error()** - raudona (rizika/klaida)
- **st.warning()** - geltona (įspėjimas)
- **st.info()** - mėlyna (informacija)

#### Emoji naudojimas
Sistema naudoja emoji aiškumui:
- 🎓 - akademinė tema
- 📊 - rezultatai
- ⚠️ - įspėjimai
- ✅ - sėkmė
- ❌ - klaida
- 🔮 - prognozė
- 📈 - augimas
- 📉 - mažėjimas

#### Metrikos su delta
```python
st.metric(
    "Prognozuojamas vidurkis", 
    f"{predicted_avg:.1f}",
    delta=f"{diff:.1f}"
)
```

Rodo pokytį su spalva (žalia/raudona).

### 4.5.6. Spinner (laukimo indikatorius)

```python
with st.spinner("Treniruojamas modelis..."):
    # Ilgai trunkantis procesas
```

Informuoja vartotoją apie vykstantį procesą.

### 4.5.7. Statistikos skydelis

4 metrikos viršuje:
```python
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Iš viso prognozių", stats['total'])
with col2:
    st.metric("Rizikos grupė", stats['risk'])
with col3:
    st.metric("Vid. pasitikėjimas", f"{stats['avg_confidence']:.1f}%")
with col4:
    st.metric("⚠️ Nepertreniruota", untrained_count)
```

Realaus laiko statistika iš duomenų bazės.

---

## 4.6. Administratoriaus ir naudotojo dokumentacija

### 4.6.1. NAUDOTOJO DOKUMENTACIJA

#### Sistemos paskirtis
Sistema skirta prognozuoti studentų studijų nutraukimo riziką naudojant mašininio mokymosi algoritmus. Vartotojas gali įvesti studento duomenis ir gauti tikimybinę prognozę bei rekomendacijas.

#### Sistemos reikalavimai
- **Operacinė sistema:** Windows 10/11, macOS, Linux
- **Python:** 3.10 ar naujesnė versija
- **RAM:** Minimum 4GB
- **Disko vieta:** 500MB
- **Interneto naršyklė:** Chrome, Firefox, Safari, Edge (naujausios versijos)

#### Diegimo instrukcija

**1. Python diegimas**
- Atsisiųskite Python iš https://www.python.org/downloads/
- Įdiekite su "Add Python to PATH" parinktimi

**2. Projekto parsisiuntimas**
```bash
git clone [repository_url]
cd student_success_prediction
```

**3. Priklausomybių diegimas**
```bash
pip install -r requirements.txt
```

**4. Modelio treniravimas**
```bash
python train_model.py
```

**5. Aplikacijos paleidimas**
```bash
streamlit run streamlit_app.py
```

Sistema automatiškai atidarys naršyklę adresu: http://localhost:8501

#### Darbo su sistema instrukcija

**ŽINGSNIS 1: Duomenų įvedimas**

Kairėje pusėje (sidebar) užpildykite 12 laukų paeiliui:

1. **Lankomumas (%)** - Pasirinkite slankikliu nuo 0% iki 100%
   - Pavyzdys: 85% reiškia, kad studentas lankė 85% paskaitų

2. **Savarankiško mokymosi valandos** - Įveskite skaičių 0-50
   - Pavyzdys: 10 valandų per savaitę

3. **Streso lygis** - Pasirinkite slankikliu nuo 1 iki 5
   - 1 = Labai žemas stresas
   - 5 = Labai aukštas stresas

4. **Darbo valandos** - Įveskite darbo valandų skaičių per savaitę
   - Pavyzdys: 20 valandų

5. **Miego valandos** - Pasirinkite slankikliu nuo 0 iki 12
   - Pavyzdys: 7 valandos per parą

6. **Socialinių tinklų valandos** - Įveskite valandų skaičių per dieną
   - Pavyzdys: 2 valandos

7. **Studijų vidurkis** - Įveskite vidurkį nuo 1 iki 10
   - Pavyzdys: 7.5

8. **12 klasės vidurkis** - Įveskite metinį vidurkį
   - Pavyzdys: 8.5

9-11. **Brandos egzaminai** - Įveskite balus (0-100)
   - Matematika: pvz., 75
   - Lietuvių kalba: pvz., 80
   - Anglų kalba: pvz., 70
   - Jei nelaikė, įveskite 0

12. **Finansinis stresas** - Pasirinkite slankikliu nuo 1 iki 5
   - 1 = Nėra finansinių problemų
   - 5 = Didelės finansinės problemos

**ŽINGSNIS 2: Prognozavimas**

1. Užpildę visus laukus, pamatysite mygtuką **"🔮 Prognozuoti"**
2. Paspauskite mygtuką
3. Sistema paklaus patvirtinimo: **"Ar tikrai norite prognozuoti?"**
4. Paspauskite **"✅ Taip"**

**ŽINGSNIS 3: Rezultatų peržiūra**

Sistema parodys:

**A) Modelio prognozė:**
- **AUKŠTA RIZIKA** (raudona) arba **ŽEMA RIZIKA** (žalia)
- Tikimybė mesti studijas (%)
- Pasitikėjimo lygis (%)

**B) Akademinės sėkmės prognozė:**
- Dabartinis vidurkis
- Prognozuojamas vidurkis
- Tendencija: 📈 GERĖS / ➡️ STABILŪS / 📉 BLOGĖS

**C) Paaiškinimas:**
Sistema paaiškina, kodėl tokia prognozė:
- ✅ Teigiami faktoriai (pvz., "Aukštas lankomumas")
- ❌ Neigiami faktoriai (pvz., "Žemas lankomumas")

**D) Tikimybių grafikas:**
Vizualus stulpelinis grafikas su tikimybėmis

**ŽINGSNIS 4: Papildoma analizė**

Išplėskite skyrius apačioje:

**"📈 Modelio analizė"**
- Požymių svarbos grafikas - rodo, kurie faktoriai svarbiausi
- Confusion Matrix - modelio tikslumas

**"📈 Duomenų bazės peržiūra"**
- Visi ankstesni įrašai
- Galima peržiūrėti istoriją

**"🔄 Modelio pertreniravimas"**
- Rodo, kiek naujų duomenų
- Galima pertreniruoti modelį su naujais duomenimis

**ŽINGSNIS 5: Naujos prognozės**

Norėdami įvesti naują studentą:
1. Paspauskite **"🔄 Išvalyti duomenis"**
2. Pradėkite iš naujo nuo 1 žingsnio

#### Dažniausiai pasitaikančios klaidos

**Klaida: "Modelis nerastas"**
- **Priežastis:** Nebuvo paleistas train_model.py
- **Sprendimas:** Paleiskite `python train_model.py`

**Klaida: "Module not found"**
- **Priežastis:** Neįdiegtos priklausomybės
- **Sprendimas:** Paleiskite `pip install -r requirements.txt`

**Klaida: "Port 8501 already in use"**
- **Priežastis:** Streamlit jau veikia
- **Sprendimas:** Uždarykite kitą Streamlit langą arba naudokite kitą portą:
  ```bash
  streamlit run streamlit_app.py --server.port 8502
  ```

**Prognozė neatsinaujina**
- **Sprendimas:** Perkraukite puslapį (F5)

#### Rezultatų interpretacija

**Rizikos grupė (AUKŠTA RIZIKA):**
- Studentas turi didelę tikimybę nutraukti studijas
- Rekomenduojama:
  - Susisiekti su studentu
  - Pasiūlyti akademinę pagalbą
  - Konsultuoti dėl streso valdymo
  - Patikrinti finansinę situaciją

**Nerizikos grupė (ŽEMA RIZIKA):**
- Studentas greičiausiai tęs studijas
- Rekomenduojama:
  - Palaikyti dabartinį lygį
  - Skatinti toliau gerai mokytis

**Pasitikėjimo lygis:**
- **90-100%** - Labai aukštas pasitikėjimas
- **70-89%** - Aukštas pasitikėjimas
- **50-69%** - Vidutinis pasitikėjimas
- **<50%** - Žemas pasitikėjimas (reikia daugiau duomenų)

---

### 4.6.2. ADMINISTRATORIAUS DOKUMENTACIJA

#### Sistemos architektūra

**Modulinė struktūra:**
```
student_success_prediction/
├── data/                      # Duomenų katalogas
│   └── students_data.csv      # Treniravimo duomenys
├── models/                    # Išsaugoti modeliai
│   ├── random_forest_model.pkl
│   ├── random_forest_scaler.pkl
│   ├── feature_importance.csv
│   └── confusion_matrix_*.png
├── train_model.py            # Treniravimo skriptas
├── predict.py                # Prognozavimo modulis
├── streamlit_app.py          # UI aplikacija
├── database.py               # DB valdymas
├── utils.py                  # Pagalbinės funkcijos
└── requirements.txt          # Priklausomybės
```

#### Duomenų bazės valdymas

**SQLite schema:**

```sql
-- Studentų lentelė
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lankomumas_proc REAL,
    savarankisko_mokymosi_val REAL,
    streso_lygis INTEGER,
    darbo_valandos REAL,
    miego_valandos REAL,
    socialiniu_tinklu_val REAL,
    studiju_vidurkis REAL,
    dvyliktos_klases_vidurkis REAL,
    brandos_egzaminas_1 REAL,
    brandos_egzaminas_2 REAL,
    brandos_egzaminas_3 REAL,
    finansinis_stresas INTEGER,
    ketinu_mesti_studijas INTEGER,
    has_real_answer INTEGER DEFAULT 0,
    is_trained INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prognozių lentelė
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    prediction INTEGER,
    risk_level TEXT,
    confidence REAL,
    probability_risk REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

**Duomenų bazės funkcijos:**

```python
# Inicializavimas
init_database()

# Studento išsaugojimas
student_id = save_student(student_data)

# Prognozės išsaugojimas
save_prediction(student_id, result)

# Statistikos gavimas
stats = get_predictions_stats()

# Nepertreniruotų duomenų gavimas
df_untrained = get_untrained_students()

# Pažymėjimas kaip pertreniruotų
mark_students_as_trained()
```

#### Modelio treniravimas

**Treniravimo parametrai:**

```python
# Random Forest (pagrindinis modelis)
RandomForestClassifier(
    n_estimators=100,        # Medžių skaičius
    max_depth=6,             # Maksimalus gylis
    min_samples_split=10,    # Min. pavyzdžių skaidymui
    min_samples_leaf=5,      # Min. pavyzdžių lape
    class_weight='balanced', # Klasių balansavimas
    random_state=42          # Atkuriamumas
)

# SMOTE balansavimas
SMOTE(
    sampling_strategy=0.8,   # 80% balanso
    k_neighbors=5,           # Kaimynų skaičius
    random_state=42
)
```

**Treniravimo komanda:**
```bash
python train_model.py [data_file]
```

**Išvestis:**
- Accuracy, Recall, F1, ROC-AUC metrikos
- Cross-validation rezultatai (10-fold)
- Confusion matrix grafikai
- Feature importance CSV ir PNG
- Model comparison CSV

#### Modelio pertreniravimas

**Kada pertreniruoti:**
- Sukaupus 50+ naujų studentų duomenų
- Praėjus semestrui su tikrais rezultatais
- Modelio tikslumas sumažėjo
- Pasikeitė studentų populiacija

**Pertreniravimo procesas:**

1. **Per Streamlit UI:**
   - Eikite į "🔄 Modelio pertreniravimas"
   - Patikrinkite nepertreniruotų duomenų skaičių
   - Paspauskite "🚀 Pertreniruoti modelį"
   - Palaukite 30-60 sekundžių

2. **Per komandinę eilutę:**
   ```bash
   python train_model.py data/students_data.csv
   ```

**Automatinis procesas:**
1. Sujungia senus ir naujus duomenis
2. Pašalina dublikatus
3. Išsaugo į CSV
4. Trenruoja visus 3 modelius
5. Pažymi duomenis kaip pertreniruotus
6. Atnaujina modelių failus

#### Sistemos priežiūra

**Kasdieninės užduotys:**
- Patikrinti, ar sistema veikia (http://localhost:8501)
- Peržiūrėti naujų prognozių skaičių

**Savaitinės užduotys:**
- Peržiūrėti duomenų bazės dydį
- Patikrinti nepertreniruotų duomenų skaičių
- Analizuoti prognozių tikslumą

**Mėnesinės užduotys:**
- Pertreniruoti modelį su naujais duomenimis
- Atnaujinti requirements.txt (jei reikia)
- Sukurti duomenų bazės backup

**Backup komandos:**
```bash
# Duomenų bazės backup
cp students.db students_backup_$(date +%Y%m%d).db

# CSV backup
cp data/students_data.csv data/students_data_backup_$(date +%Y%m%d).csv

# Modelių backup
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
```

#### Našumo optimizavimas

**Streamlit konfigūracija (.streamlit/config.toml):**
```toml
[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

**Python optimizavimas:**
- Naudoti @st.cache_data dekoratorių duomenų kešavimui
- Minimizuoti st.rerun() kvietimus
- Optimizuoti SQL užklausas

#### Saugumo rekomendacijos

1. **Duomenų apsauga:**
   - Naudoti HTTPS produkcinėje aplinkoje
   - Šifruoti jautrius duomenis duomenų bazėje
   - Reguliariai daryti backup

2. **Prieigos kontrolė:**
   - Įdiegti autentifikaciją (pvz., streamlit-authenticator)
   - Riboti prieigą prie admin funkcijų
   - Loginti visus veiksmus

3. **Duomenų privatumas:**
   - Anonimizuoti studentų duomenis
   - Laikytis GDPR reikalavimų
   - Naudoti pseudonimus vietoj vardų

#### Klaidų diagnostika

**Logų peržiūra:**
```bash
# Streamlit logai
streamlit run streamlit_app.py --logger.level=debug

# Python logai
python -u train_model.py 2>&1 | tee training.log
```

**Dažniausios problemos:**

**1. Modelis netreniruojasi**
- Patikrinti CSV formato teisingumą
- Užtikrinti, kad yra pakankamas duomenų kiekis (min. 100 įrašų)
- Patikrinti, ar nėra trūkstamų stulpelių

**2. Prognozės netikslios**
- Pertreniruoti modelį su naujais duomenimis
- Patikrinti feature importance
- Padidinti n_estimators

**3. Lėtas veikimas**
- Sumažinti duomenų bazės dydį (archyvuoti senus įrašus)
- Optimizuoti SQL užklausas
- Naudoti kešavimą

#### Sistemos atnaujinimas

**Priklausomybių atnaujinimas:**
```bash
pip list --outdated
pip install --upgrade [package_name]
pip freeze > requirements.txt
```

**Python versijos atnaujinimas:**
1. Įdiekite naują Python versiją
2. Sukurkite naują virtualią aplinką
3. Įdiekite priklausomybes
4. Testuokite sistemą

#### Monitoringas

**Metrikos stebėti:**
- Prognozių skaičius per dieną
- Vidutinis pasitikėjimo lygis
- Rizikos grupės procentas
- Sistemos atsakymo laikas

**Įrankiai:**
- Streamlit metrics
- SQLite užklausos
- Python logging modulis

---

## 4.7. Apibendrinimas

### 4.7.1. Pasiekti rezultatai

Eksperimentinės-praktinės dalies metu buvo sukurta pilnai funkcionali studentų akademinės sėkmės prognozės sistema, kuri:

**1. Techninis įgyvendinimas:**
- Sukurti 7 pagrindiniai Python moduliai (2000+ kodo eilučių)
- Implementuoti 3 mašininio mokymosi algoritmai
- Integruota SQLite duomenų bazė su 2 lentelėmis
- Sukurta interaktyvi Streamlit vartotojo sąsaja

**2. Modelio kokybė:**
- **Random Forest** pasiekė geriausią Recall metriką (~0.85-0.90)
- Taikomas SMOTE balansavimas klasių disbalansui spręsti
- Cross-validation (10-fold) užtikrina modelio stabilumą
- Feature importance analizė identifikuoja svarbiausius faktorius

**3. Funkcionalumas:**
- Individualių studentų rizikos prognozė
- Akademinės sėkmės prognozė (pažymių tendencijos)
- Prognozių paaiškinimas (explainability)
- Automatinis modelio pertreniravimas
- Duomenų bazės valdymas ir statistika

**4. Vartotojo patirtis:**
- Sekvencinė 12 žingsnių navigacija
- Interaktyvūs įvesties komponentai (sliders, number inputs)
- Realaus laiko vizualizacijos (Plotly grafikai)
- Spalvinė grįžtamoji informacija
- Patvirtinimo dialogai

### 4.7.2. Sistemos privalumai

**Technologiniai:**
- Modulinė architektūra - lengva prižiūrėti ir plėsti
- Open-source technologijos - nemokami įrankiai
- Python ekosistema - platus bibliotekų pasirinkimas
- Streamlit framework - greitas UI kūrimas

**Funkciniai:**
- Tikimybinė prognozė - ne tik taip/ne, bet ir pasitikėjimo lygis
- Paaiškinamumas - vartotojas supranta KODĖL tokia prognozė
- Pertreniravimas - modelis gali mokytis iš naujų duomenų
- Istorija - visos prognozės saugomos duomenų bazėje

**Vartotojo:**
- Intuityvus - nereikia techninių žinių
- Greitas - prognozė per 1-2 sekundes
- Vizualus - grafikai ir spalvos
- Informatyvus - detalūs paaiškinimai

### 4.7.3. Sistemos apribojimai

**1. Duomenų kokybė:**
- Modelio tikslumas priklauso nuo treniravimo duomenų kokybės
- Reikalingas pakankamas duomenų kiekis (min. 100-200 įrašų)
- Sintetiniai duomenys gali skirtis nuo realių

**2. Modelio apribojimai:**
- Prognozė tik dviem klasėms (rizika/nerizika)
- Neatsižvelgia į kitus faktorius (šeimos situacija, sveikata)
- Gali būti bias, jei treniravimo duomenys nereprezentatyvūs

**3. Techniniai:**
- SQLite netinka labai dideliems duomenų kiekiams (>1M įrašų)
- Streamlit nėra optimizuotas dideliam vartotojų skaičiui
- Reikalingas Python ir priklausomybių diegimas

**4. Saugumo:**
- Nėra autentifikacijos sistemos
- Duomenys nesaugomi šifruoti
- Nėra audit log funkcionalumo

### 4.7.4. Tolesni patobulinimai

**Trumpalaikiai (1-3 mėnesiai):**
1. **Autentifikacija** - įdiegti vartotojų prisijungimo sistemą
2. **Daugiau metrikų** - pridėti Precision, Specificity
3. **Eksportas** - galimybė eksportuoti rezultatus į PDF/Excel
4. **Email pranešimai** - automatiniai pranešimai apie aukštą riziką

**Vidutinės trukmės (3-6 mėnesiai):**
1. **REST API** - sukurti API su FastAPI/Flask
2. **Daugiau modelių** - XGBoost, LightGBM, Neural Networks
3. **Hiperparametrų optimizavimas** - GridSearchCV, Optuna
4. **A/B testavimas** - lyginti skirtingus modelius produkcinėje aplinkoje

**Ilgalaikiai (6-12 mėnesių):**
1. **Deep Learning** - LSTM modelis laiko eilučių analizei
2. **NLP integracija** - analizuoti studentų komentarus
3. **Dashboard** - išplėstinė analitika su Plotly Dash
4. **Mobile app** - React Native arba Flutter aplikacija
5. **Cloud deployment** - AWS/Azure/GCP diegimas

### 4.7.5. Išvados

Sukurta sistema sėkmingai įgyvendina studentų akademinės sėkmės prognozės tikslą:

✅ **Veikia** - sistema funkcionali ir stabili  
✅ **Tiksli** - modelis pasiekia >85% Recall metriką  
✅ **Naudinga** - gali padėti identifikuoti rizikos grupės studentus  
✅ **Plečiama** - modulinė architektūra leidžia lengvai pridėti naujų funkcijų  
✅ **Dokumentuota** - išsami naudotojo ir administratoriaus dokumentacija  

Sistema gali būti naudojama:
- **Universitetuose** - studentų sėkmės stebėsenai
- **Kolegijose** - ankstyvo įspėjimo sistemai
- **Mokyklose** - abiturientų konsultavimui
- **Tyrimams** - akademinės sėkmės faktorių analizei

Pagrindinė sistemos vertė - **ankstyvasis įspėjimas**. Identifikavus rizikos grupės studentą laiku, galima imtis prevencinių priemonių: akademinės pagalbos, psichologinės konsultacijos, finansinės paramos. Tai gali padėti sumažinti studijų nutraukimo rodiklius ir pagerinti studentų gerovę.

---

**Eksperimentinės-praktinės dalies pabaiga**

