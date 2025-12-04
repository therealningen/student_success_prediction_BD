"""
SQLite duomenų bazės funkcijos
"""
import sqlite3
import pandas as pd
from datetime import datetime

def init_database():
    """Sukuria duomenų bazę ir lenteles"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Studentų duomenų lentelė
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lankomumas_proc INTEGER,
        savarankisko_mokymosi_val INTEGER,
        streso_lygis INTEGER,
        darbo_valandos INTEGER,
        miego_valandos INTEGER,
        socialiniu_tinklu_val INTEGER,
        studiju_vidurkis REAL,
        dvyliktos_klases_vidurkis REAL,
        brandos_egzaminas_1 INTEGER,
        brandos_egzaminas_2 INTEGER,
        brandos_egzaminas_3 INTEGER,
        finansinis_stresas INTEGER,
        ketinu_mesti_studijas INTEGER,
        is_trained INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Prognozių lentelė
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        prediction INTEGER,
        confidence REAL,
        risk_level TEXT,
        model_used TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def save_student(student_data):
    """Išsaugo studento duomenis"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO students (
        lankomumas_proc, savarankisko_mokymosi_val, streso_lygis,
        darbo_valandos, miego_valandos, socialiniu_tinklu_val,
        studiju_vidurkis, dvyliktos_klases_vidurkis,
        brandos_egzaminas_1, brandos_egzaminas_2, brandos_egzaminas_3,
        finansinis_stresas, ketinu_mesti_studijas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_data['lankomumas_proc'],
        student_data['savarankisko_mokymosi_val'],
        student_data['streso_lygis'],
        student_data['darbo_valandos'],
        student_data['miego_valandos'],
        student_data['socialiniu_tinklu_val'],
        student_data['studiju_vidurkis'],
        student_data['dvyliktos_klases_vidurkis'],
        student_data['brandos_egzaminas_1'],
        student_data['brandos_egzaminas_2'],
        student_data['brandos_egzaminas_3'],
        student_data['finansinis_stresas'],
        student_data['ketinu_mesti_studijas']
    ))
    
    student_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return student_id

def save_prediction(student_id, prediction_result):
    """Išsaugo prognozės rezultatą"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO predictions (
        student_id, prediction, confidence, risk_level, model_used
    ) VALUES (?, ?, ?, ?, ?)
    ''', (
        student_id,
        prediction_result['prediction'],
        prediction_result['confidence'],
        prediction_result['risk_level'],
        'random_forest'
    ))
    
    conn.commit()
    conn.close()

def get_all_students():
    """Gauna visus studentus"""
    conn = sqlite3.connect('students.db')
    df = pd.read_sql_query('SELECT * FROM students ORDER BY created_at DESC', conn)
    conn.close()
    
    # Pridedame rizikos stulpelį treniravimui
    if 'ketinu_mesti_studijas' in df.columns:
        df['rizika'] = df['ketinu_mesti_studijas'].apply(lambda x: 1 if x >= 4 else 0)
    
    return df

def get_untrained_students():
    """Gauna tik nepertreniruotus studentus"""
    conn = sqlite3.connect('students.db')
    df = pd.read_sql_query('SELECT * FROM students WHERE is_trained = 0 ORDER BY created_at DESC', conn)
    conn.close()
    
    if 'ketinu_mesti_studijas' in df.columns:
        df['rizika'] = df['ketinu_mesti_studijas'].apply(lambda x: 1 if x >= 4 else 0)
    
    return df

def mark_students_as_trained():
    """Pažymi visus studentus kaip pertreniruotus"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET is_trained = 1 WHERE is_trained = 0')
    conn.commit()
    conn.close()

def get_predictions_stats():
    """Gauna prognozių statistikas"""
    conn = sqlite3.connect('students.db')
    
    stats = {}
    cursor = conn.cursor()
    
    # Bendras skaičius
    cursor.execute('SELECT COUNT(*) FROM predictions')
    stats['total'] = cursor.fetchone()[0]
    
    # Rizikos grupė
    cursor.execute('SELECT COUNT(*) FROM predictions WHERE prediction = 1')
    stats['risk'] = cursor.fetchone()[0]
    
    # Vidutinis pasitikėjimas
    cursor.execute('SELECT AVG(confidence) FROM predictions')
    result = cursor.fetchone()[0]
    stats['avg_confidence'] = result if result else 0
    
    conn.close()
    return stats