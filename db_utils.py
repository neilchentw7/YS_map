import sqlite3
import pandas as pd
import os

DB_PATH = 'site_locations.db'
CSV_PATH = 'site_locations.csv'

def init_db():
    first_time = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                url TEXT NOT NULL,
                supervisor TEXT,
                phone TEXT
        )"""
    )
    conn.commit()
    if first_time and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, dtype={'聯絡電話': str})
        for _, row in df.iterrows():
            cursor.execute(
                'INSERT INTO locations (name, address, url, supervisor, phone) VALUES (?, ?, ?, ?, ?)',
                (row['工地名稱'], row['地址'], row['GoogleMap網址'], row['工地主任'], row['聯絡電話'])
            )
        conn.commit()
    conn.close()


def get_all_locations():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('SELECT * FROM locations', conn)
    conn.close()
    df.rename(
        columns={
            'name': '工地名稱',
            'address': '地址',
            'url': 'GoogleMap網址',
            'supervisor': '工地主任',
            'phone': '聯絡電話',
        },
        inplace=True,
    )
    return df


def add_location(name, address, url, supervisor, phone):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO locations (name, address, url, supervisor, phone) VALUES (?, ?, ?, ?, ?)',
        (name, address, url, supervisor, phone)
    )
    conn.commit()
    conn.close()


def delete_location(row_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM locations WHERE id = ?', (row_id,))
    conn.commit()
    conn.close()
