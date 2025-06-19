import pandas as pd
import sqlite3

def create_database(db_name='loblow_bio.sqlite'):
    # connect to database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # create tables if they don't already exist in the database
    cur.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id TEXT PRIMARY KEY,
            project TEXT,
            age INTEGER,
            sex TEXT,
            condition TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS samples (
            sample_id TEXT PRIMARY KEY,
            subject_id TEXT,
            sample_type TEXT,
            time_from_treatment_start INTEGER,
            FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            sample_id TEXT PRIMARY KEY,
            treatment TEXT,
            response TEXT,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER,
            FOREIGN KEY(sample_id) REFERENCES samples(sample_id)
        )
    ''')

    conn.commit()
    conn.close()

def load_data(csv_file='cell-count.csv', db_name='loblow_bio.sqlite'):
    # read in data and connect to database
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute('''
            INSERT OR IGNORE INTO subjects (subject_id, project, age, sex, condition)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['subject'], row['project'], row['age'], row['sex'], row['condition']))

        cur.execute('''
            INSERT OR REPLACE INTO samples (sample_id, subject_id, sample_type, time_from_treatment_start)
            VALUES (?, ?, ?, ?)
        ''', (row['sample'], row['subject'], row['sample_type'], row['time_from_treatment_start']))

        cur.execute('''
            INSERT OR REPLACE INTO treatments (sample_id, treatment, response, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['sample'], row['treatment'], row['response'],
            row['b_cell'], row['cd8_t_cell'], row['cd4_t_cell'],
            row['nk_cell'], row['monocyte']
        ))

    conn.commit()
    conn.close()

def remove_sample(sample_id, db_name='loblow_bio.sqlite'):
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute("DELETE FROM treatments WHERE sample_id = ?", (sample_id,))
    c.execute("DELETE FROM samples WHERE sample_id = ?", (sample_id,))
    conn.commit()
    conn.close()


def add_sample(sample_dict, db_name='loblow_bio.sqlite'):
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute('''
        INSERT OR IGNORE INTO subjects (subject_id, project, age, sex, condition)
        VALUES (?, ?, ?, ?, ?)
    ''', (sample_dict['subject'], sample_dict['project'], sample_dict['age'], sample_dict['sex'], sample_dict['condition']))

    cur.execute('''
        INSERT OR REPLACE INTO samples (sample_id, subject_id, sample_type, time_from_treatment_start)
        VALUES (?, ?, ?, ?)
    ''', (sample_dict['sample'], sample_dict['subject'], sample_dict['sample_type'], sample_dict['time_from_treatment_start']))

    cur.execute('''
        INSERT OR REPLACE INTO treatments (sample_id, treatment, response, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sample_dict['sample'], sample_dict['treatment'], sample_dict['response'],
        sample_dict['b_cell'], sample_dict['cd8_t_cell'], sample_dict['cd4_t_cell'],
        sample_dict['nk_cell'], sample_dict['monocyte']
    ))

    conn.commit()
    conn.close()