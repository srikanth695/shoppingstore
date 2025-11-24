import sqlite3, os
db = os.path.join(os.path.dirname(__file__), "shopping.db")
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT COUNT(1) as cnt FROM products")
print("products count:", cur.fetchone()["cnt"])
cur.execute("SELECT product_id, product_name FROM products LIMIT 5")
print(cur.fetchall())
conn.close()