import sqlite3

DB_FILE = "passwords.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT,
                username TEXT,
                password TEXT
            )
        """)
        conn.commit()

def insert_account(site, username, password):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO accounts (site, username, password) VALUES (?, ?, ?)",
                  (site, username, password))
        conn.commit()

def get_all_accounts():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT site, username, password FROM accounts")
        return c.fetchall()
