from flask import Flask,  jsonify
from db import get_db_connection
from flask_cors import CORS 




app = Flask(__name__, static_folder="../frontend",static_url_path="")
CORS(app)
'''
# ---------------- SIGN UP ----------------
@app.post("/signup")
def signup():
    data = request.json
    username = data['username'].strip()
    password = data['password'].strip()

    db = get_db_connection()
    cursor = db.cursor()
    # Check if username exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        db.close()
        return jsonify({"message": "Username already exists"}), 400

    cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, password))
    db.commit()
    user_id = cursor.lastrowid  # Get inserted user id
    db.close()
    return jsonify({"message": "Signup successful", "user_id": user_id})


# ---------------- LOGIN ----------------
@app.post("/login")
def login():
    data = request.json
    username = data['username'].strip()
    password = data['password'].strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()
    db.close()
    if user:
        return jsonify({"message": "Login successful", "user_id": user['user_id']})
    return jsonify({"message": "Invalid credentials"}), 400
'''
# ---------------- GET PRODUCTS ----------------
@app.route("/<path:page>")
def serve_page(page):
    return app.send_static_file(page)


# Get products from database
@app.get("/products")
def get_products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT product_id, product_name, price, image_url FROM products")
    products = cursor.fetchall()
    db.close()

    # Prepend folder path for images
    for p in products:
         p["image_url"] = f"static/images/{p['image_url']}"
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)
'''
# ---------------- PLACE ORDER ----------------

@app.post("/orders")
def place_order():
    data = request.json
    user_id = data['user_id']
    items = data['items']  # [{product_id, quantity, price}, ...]

    if not items:
        return jsonify({"message": "Cart is empty"}), 400

    total_amount = sum([item['quantity'] * item['price'] for item in items])

    db = get_db_connection()
    cursor = db.cursor()

    # Insert order
    cursor.execute(
        "INSERT INTO orders (user_id, order_date, total_amount) VALUES (%s, %s, %s)",
        (user_id, date.today(), total_amount)
    )
    order_id = cursor.lastrowid

    # Insert order details
    for item in items:
        cursor.execute(
            "INSERT INTO orderdetails (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_id, item['product_id'], item['quantity'], item['price'])
        )

    db.commit()
    db.close()
    return jsonify({"message": "Order placed successfully", "order_id": order_id})

# ---------------- GET USER ORDERS ----------------
@app.get("/orders/<int:user_id>")
def get_user_orders(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    # Get orders
    cursor.execute("SELECT * FROM orders WHERE user_id=%s", (user_id,))
    orders = cursor.fetchall()

    # Get order details for each order
    for order in orders:
        cursor.execute(
            "SELECT od.orderdetail_id, p.product_name, od.quantity,p.image_url, od.price "
            "FROM orderdetails od JOIN products p ON od.product_id = p.product_id "
            "WHERE od.order_id=%s", (order['order_id'],)
        )
        order['items'] = cursor.fetchall()
       
    db.close()
    return jsonify(orders)
@app.delete("/orders/<int:user_id>")
def delete_orders(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    
    # Delete order details first
    cursor.execute(
        "DELETE od FROM orderdetails od JOIN orders o ON od.order_id = o.order_id WHERE o.user_id=%s",
        (user_id,)
    )
    
    # Delete orders
    cursor.execute("DELETE FROM orders WHERE user_id=%s", (user_id,))
    
    db.commit()
    db.close()
    return jsonify({"message": "All orders deleted successfully"})


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
'''