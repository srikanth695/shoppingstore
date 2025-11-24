import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "shopping.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create minimal schema and a sample product if DB doesn't exist or is empty."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        image_url TEXT
    );
    """)
    # optional sample row if table empty
    cur.execute("SELECT COUNT(1) as cnt FROM products")
    if cur.fetchone()["cnt"] == 0:
        cur.execute(
            "INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)",
            ("Sample Product", 9.99, "sample.jpg")
        )
    conn.commit()
    conn.close()
