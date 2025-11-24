import os
from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from db import get_db_connection, init_db
from werkzeug.security import generate_password_hash, check_password_hash
import traceback, sys

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# IMPORTANT: set a secret key (use env var in production)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")

# Initialize sqlite DB on startup
init_db()

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:page>")
def serve_page(page):
    return send_from_directory(app.static_folder, page)

@app.post("/signup")
def signup():
    try:
        # Accept JSON or form-encoded
        if request.is_json:
            data = request.get_json()
            username = (data.get("username") or "").strip()
            password = data.get("password") or ""
            email = data.get("email")
        else:
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            email = request.form.get("email")

        if not username or not password:
            return jsonify({"error": "username and password required"}), 400

        pw_hash = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, pw_hash)
            )
            conn.commit()
            
            # Get the user_id immediately after insert
            cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_row = cur.fetchone()
            user_id = user_row["user_id"] if user_row else None
        except Exception as e:
            # unique constraint or other DB error
            conn.rollback()
            if "UNIQUE constraint failed" in str(e):
                return jsonify({"error": "username already exists"}), 409
            raise
        finally:
            conn.close()

        return jsonify({"message": "user created", "username": username, "user_id": user_id}), 201
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": "internal error", "detail": str(e)}), 500

@app.get("/products")
def get_products():
    try:
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
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": "Failed to load products", "detail": str(e)}), 500

@app.post("/login")
def login():
    try:
        # accept JSON or form-encoded
        if request.is_json:
            data = request.get_json()
            username = (data.get("username") or "").strip()
            password = data.get("password") or ""
        else:
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

        if not username or not password:
            return jsonify({"error": "username and password required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()

        if not row or not check_password_hash(row["password_hash"], password):
            return jsonify({"error": "invalid credentials"}), 401

        session["user_id"] = row["user_id"]
        return jsonify({"message": "login successful", "username": row["username"], "user_id": row["user_id"]}), 200
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": "internal error", "detail": str(e)}), 500

# --- Cart endpoints (session-based) ---
@app.post("/cart/add")
def add_to_cart():
    try:
        data = request.get_json() or request.form
        pid = int(data.get("product_id") or 0)
        qty = int(data.get("quantity") or 1)
        if pid <= 0 or qty <= 0:
            return jsonify({"error": "invalid product_id or quantity"}), 400

        cart = session.get("cart", {})
        cart[str(pid)] = cart.get(str(pid), 0) + qty
        session["cart"] = cart
        return jsonify({"message": "added", "cart": cart}), 200
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

@app.get("/cart")
def get_cart():
    try:
        cart = session.get("cart", {})
        if not cart:
            return jsonify({"items": [], "total": 0.0})
        conn = get_db_connection()
        cur = conn.cursor()
        items = []
        total = 0.0
        for pid_str, qty in cart.items():
            cur.execute("SELECT product_id, product_name, price, image_url FROM products WHERE product_id = ?", (int(pid_str),))
            p = cur.fetchone()
            if not p:
                continue
            subtotal = p["price"] * qty
            total += subtotal
            items.append({
                "product_id": p["product_id"],
                "product_name": p["product_name"],
                "price": p["price"],
                "quantity": qty,
                "subtotal": subtotal,
                "image_url": f"images/{p['image_url']}" if p["image_url"] else None
            })
        conn.close()
        return jsonify({"items": items, "total": total})
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

@app.post("/cart/clear")
def clear_cart():
    session["cart"] = {}
    return jsonify({"message": "cart cleared"}), 200

@app.post("/cart/update")
def update_cart():
    try:
        data = request.get_json() or request.form
        pid = int(data.get("product_id") or 0)
        qty = int(data.get("quantity") or 1)
        if pid <= 0 or qty < 0:
            return jsonify({"error": "invalid product_id or quantity"}), 400

        cart = session.get("cart", {})
        if qty == 0:
            # Remove item if quantity is 0
            cart.pop(str(pid), None)
        else:
            cart[str(pid)] = qty
        session["cart"] = cart
        return jsonify({"message": "updated", "cart": cart}), 200
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

@app.post("/cart/remove")
def remove_from_cart():
    try:
        data = request.get_json() or request.form
        pid = int(data.get("product_id") or 0)
        if pid <= 0:
            return jsonify({"error": "invalid product_id"}), 400

        cart = session.get("cart", {})
        cart.pop(str(pid), None)
        session["cart"] = cart
        return jsonify({"message": "removed", "cart": cart}), 200
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

# --- Checkout: persist order and order_items, clear session cart ---
@app.post("/checkout")
def checkout():
    try:
        # Optionally accept user_id or customer info in request
        # For now use anonymous orders (user_id NULL)
        cart = session.get("cart", {})
        if not cart:
            return jsonify({"error": "cart is empty"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # compute total and validate products exist
        total = 0.0
        items = []
        for pid_str, qty in cart.items():
            cur.execute("SELECT product_id, price FROM products WHERE product_id = ?", (int(pid_str),))
            p = cur.fetchone()
            if not p:
                conn.close()
                return jsonify({"error": f"product {pid_str} not found"}), 400
            unit_price = p["price"]
            subtotal = unit_price * qty
            total += subtotal
            items.append((int(pid_str), qty, unit_price))

        # create order
        cur.execute("INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)", (None, total, "placed"))
        order_id = cur.lastrowid

        # insert order_items
        for product_id, qty, unit_price in items:
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, qty, unit_price)
            )

        conn.commit()
        conn.close()

        # clear cart
        session["cart"] = {}
        return jsonify({"message": "order placed", "order_id": order_id}), 201
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

# --- List orders (simple) ---
@app.get("/orders")
def list_orders():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT order_id, user_id, total, status, created_at FROM orders ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
        orders = []
        for r in rows:
            cur2 = conn.cursor()
            cur2.execute("SELECT product_id, quantity, unit_price FROM order_items WHERE order_id = ?", (r["order_id"],))
            items = [dict(x) for x in cur2.fetchall()]
            orders.append({
                "order_id": r["order_id"],
                "user_id": r["user_id"],
                "total": r["total"],
                "status": r["status"],
                "created_at": r["created_at"],
                "items": items
            })
        conn.close()
        return jsonify(orders)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)