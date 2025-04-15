import sqlite3
from datetime import datetime
import os

DB_FILE = "faceaccess.db"

def opprett_database():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            navn TEXT NOT NULL,
            bildemappe TEXT NOT NULL,
            opprettet_tid TEXT NOT NULL
        )
        """)
        conn.commit()

def lagre_bruker(navn, bildemappe):
    opprett_database()
    tidspunkt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (navn, bildemappe, opprettet_tid) VALUES (?, ?, ?)",
                  (navn, bildemappe, tidspunkt))
        conn.commit()
        print(f"[DB] Bruker '{navn}' registrert i databasen.")
