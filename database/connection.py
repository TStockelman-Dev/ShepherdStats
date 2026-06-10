import sqlite3

database_name = "shepherdstats.db"

def get_connection():
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                service_type TEXT NOT NULL,
                count INTEGER NOT NULL CHECK(count >= 0),
                note TEXT,
                UNIQUE(date, service_type)
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0.0),
                category TEXT NOT NULL,
                note TEXT
            )
        """)
