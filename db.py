import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------- USERS ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # ---------- TASKS ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        date TEXT,
        task TEXT,
        focus TEXT,
        completed INTEGER DEFAULT 0,
        self_score INTEGER DEFAULT 0,
        mentor_score INTEGER DEFAULT 0,
        olq_score INTEGER DEFAULT 0,
        notes TEXT,
        improvement TEXT
    )
    """)

    # ---------- NOTES ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        date TEXT,
        content TEXT
    )
    """)

    # ---------- SCHEDULE ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        task TEXT,
        focus TEXT
    )
    """)

    # ---------- DEFAULT ADMIN ----------
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )
        print("✅ Default admin created (admin / admin123)")

    conn.commit()
    conn.close()