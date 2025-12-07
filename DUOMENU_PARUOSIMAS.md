# 📊 Duomenų paruošimo instrukcija

## Greitas startas

Jei turite originalų apklausos CSV failą, tiesiog paleiskite:

```bash
python normalize_data.py "data/Studentų akademinės sėkmės apklausa (Atsakymai).csv"
```

Sistema automatiškai:
1. ✅ Konvertuos stulpelių pavadinimus
2. ✅ Išvalys duomenis (%, range reikšmės)
3. ✅ Užpildys trūkstamas reikšmes
4. ✅ Sukurs `data/students_data.csv`

## Kas vyksta viduje?

### Stulpelių konvertavimas

| Originalus pavadinimas | Naujas pavadinimas |
|------------------------|-------------------|
| 18. Lankomumas šiame semestre (%) | lankomumas_proc |
| 20. Savarankiško mokymosi valandos per savaitę | savarankisko_mokymosi_val |
| 23. Patiriu stiprų stresą | streso_lygis |
| 9. Darbo valandos per savaitę | darbo_valandos |
| 21. Miego valandos per parą | miego_valandos |
| 22. Laikas socialiniuose tinkluose per dieną (val.) | socialiniu_tinklu_val |
| 13. Koks yra jūsų bendras visų studijų semestrų vidurkis (1–10)? | studiju_vidurkis |
| 17. 12 klasės metinis vidurkis (1–10) | dvyliktos_klases_vidurkis |
| 14. Brandos egzaminas: Matematika (1–100, 0=nelaikiau) | brandos_egzaminas_1 |
| 15. Brandos egzaminas: Lietuvių kalba (1–100, 0=nelaikiau) | brandos_egzaminas_2 |
| 16. Brandos egzaminas: Anglų kalba (1–100, 0=nelaikiau) | brandos_egzaminas_3 |
| 7. Finansinis stresas (1–5) | finansinis_stresas |
| 24. Ketinu nutraukti studijas | ketinu_mesti_studijas |

### Duomenų valymas

**Procentai:**
- `"100%"` → `100`
- `"0.82"` → `82`
- `"100"` → `100`

**Range reikšmės:**
- `"2-3"` → `2.5` (vidurkis)
- `"1-2"` → `1.5`
- `"4-5"` → `4.5`

**Neteisingi įrašai:**
- `"-"` → `None` (užpildoma vidurkiu)
- `""` → `None` (užpildoma vidurkiu)
- Tekstas → `None` (užpildoma vidurkiu)

### Trūkstamų reikšmių valdymas

Sistema automatiškai užpildo trūkstamas reikšmes:
- **Skaitiniai laukai** - užpildoma stulpelio vidurkiu
- **ketinu_mesti_studijas** - jei trūksta, eilutė pašalinama

## Pavyzdys

**Prieš normalizavimą:**
```csv
Laiko žymė,1. Vardas,...,18. Lankomumas šiame semestre (%),24. Ketinu nutraukti studijas
9/12/2025 14:38:45,Guste,...,100,1
9/12/2025 14:39:14,Vanesa,...,75,2
```

**Po normalizavimo:**
```csv
lankomumas_proc,savarankisko_mokymosi_val,...,ketinu_mesti_studijas
100,5,...,1
75,15,...,2
```

## Statistika

Po normalizavimo sistema parodo:
```
====================================================================
DUOMENŲ NORMALIZAVIMAS
====================================================================

1. Įkeliami duomenys iš: data/Studentų akademinės sėkmės apklausa (Atsakymai).csv
   Įrašų skaičius: 250

2. Konvertuojami stulpeliai...
   ✓ Visi stulpeliai konvertuoti

3. Valymas...
   Prieš valymą: 250 įrašų
   Po valymo: 248 įrašų
   Pašalinta: 2 įrašų

4. Statistika:
   Rizikos grupė (4-5): 15 (6.0%)
   Nerizikos grupė (1-3): 233 (94.0%)

5. Išsaugoma į: data/students_data.csv

====================================================================
NORMALIZAVIMAS BAIGTAS!
====================================================================

Dabar galite treniruoti modelį:
  python train_model.py
```

## Dažniausios klaidos

### Klaida: "Nerastas failas"
```bash
❌ Klaida: Nerastas failas data/Studentų akademinės sėkmės apklausa (Atsakymai).csv
```

**Sprendimas:**
- Patikrinkite failo pavadinimą
- Įsitikinkite, kad failas yra `data/` kataloge
- Naudokite kabutes jei pavadinime yra tarpų

### Klaida: "Encoding error"
```bash
❌ Klaida: 'charmap' codec can't decode byte...
```

**Sprendimas:**
Atverkite `normalize_data.py` ir pakeiskite:
```python
df = pd.read_csv(input_file, encoding='utf-8')
```

### Klaida: "Per mažai duomenų"
```bash
⚠️ Po valymo liko tik 10 įrašų
```

**Sprendimas:**
- Patikrinkite ar CSV turi visus reikalingus stulpelius
- Įsitikinkite, kad "24. Ketinu nutraukti studijas" stulpelis užpildytas

## Tolimesni žingsniai

Po sėkmingo normalizavimo:

1. **Treniruokite modelį:**
   ```bash
   python train_model.py
   ```

2. **Paleiskite aplikaciją:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Testuokite prognozę:**
   - Atidarykite http://localhost:8501
   - Įveskite studento duomenis
   - Gaukite prognozę

## Papildoma informacija

Jei norite modifikuoti normalizavimo logiką:
1. Atidarykite `normalize_data.py`
2. Redaguokite `clean_percentage()` arba `clean_number()` funkcijas
3. Paleiskite iš naujo

Jei turite kitokį CSV formatą, galite sukurti savo konvertavimo skriptą pagal `normalize_data.py` pavyzdį.
