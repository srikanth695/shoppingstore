import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_db_connection, init_db

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Initialize sqlite DB on startup (creates shopping.db in project folder)
init_db()

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:page>")
def serve_page(page):
    return app.send_static_file(page)

@app.get("/products")
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, product_name, price, image_url FROM products")
    rows = cur.fetchall()
    products = []
    for r in rows:
        products.append({
            "product_id": r["product_id"],
            "product_name": r["product_name"],
            "price": r["price"],
            "image_url": f"images/{r['image_url']}" if r["image_url"] else None
        })
    conn.close()
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)