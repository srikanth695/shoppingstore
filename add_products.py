from db import get_db_connection

PRODUCTS = [
    ("Apple iPhone 14", 699.00, "iphone14.jpg"),
    ("Samsung Galaxy S23", 649.00, "galaxy_s23.jpg"),
    ("Sony WH-1000XM5 Headphones", 349.00, "sony_wh1000xm5.jpg"),
    ("Apple MacBook Air M2", 1099.00, "macbook_air_m2.jpg"),
    ("Logitech MX Master 3", 99.99, "logitech_mx_master_3.jpg"),
    ("Instant Pot Duo 7-in-1", 89.99, "instant_pot_duo.jpg")
]

def add_products():
    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0
    skipped = 0
    for name, price, image in PRODUCTS:
        cur.execute("SELECT 1 FROM products WHERE product_name = ?", (name,))
        if cur.fetchone():
            skipped += 1
            continue
        cur.execute(
            "INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)",
            (name, price, image)
        )
        inserted += 1
    conn.commit()
    conn.close()
    print(f"Inserted: {inserted}, Skipped (already present): {skipped}")

if __name__ == "__main__":
    add_products()