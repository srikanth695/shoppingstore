# Shopping Store - E-commerce Application

A simple yet functional e-commerce shopping cart application built with Flask (Python) backend and HTML/CSS/JavaScript frontend.

## Features

- ✅ User Authentication (Signup/Login)
- ✅ User Profile & Details View
- ✅ Product Catalog with Images
- ✅ Shopping Cart Management
- ✅ Quantity Control with Dynamic Price Updates
- ✅ Order Placement & Confirmation
- ✅ Order History with Item Details View
- ✅ Session-based Cart Management
- ✅ SQLite Database

## Technology Stack

- **Backend:** Flask, SQLite3, Werkzeug
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database:** SQLite

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/srikanth695/shoppingstore.git
cd shoppingstore
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# On Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- Flask >= 2.2
- Flask-Cors >= 3.0

### 4. Initialize the Database

```bash
python init_db.py
```

This creates the SQLite database with the necessary tables:
- `users` - User accounts with hashed passwords
- `products` - Product catalog
- `orders` - Order records
- `order_items` - Individual items in orders

### 5. Add Sample Products (Optional)

```bash
python add_products.py
```

This adds sample products to the database:
- Apple iPhone 14
- Samsung Galaxy S23
- Sony WH-1000XM5 Headphones
- Apple MacBook Air M2
- Logitech MX Master 3
- Instant Pot Duo 7-in-1

### 6. Run the Application

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

## File Structure

```
shoppingstore/
├── app.py                 # Main Flask application
├── db.py                  # Database connection and initialization
├── init_db.py             # Database schema setup
├── add_products.py        # Sample products loader
├── requirements.txt       # Python dependencies
│
├── index.html             # Home page (Login/Signup redirect)
├── login.html             # Login page
├── signup.html            # Registration page
├── products.html          # Products catalog
├── cart.html              # Shopping cart
├── orders.html            # Order history
├── order-placed.html      # Order confirmation
│
├── script.js              # Main application logic
├── login.js               # Login form handler
├── signup.js              # Signup form handler
├── style.css              # Application styling
│
├── shopping.db            # SQLite database (created after init_db.py)
└── README.md              # This file
```

## Usage

### 1. Home Page
- Navigate to `http://127.0.0.1:5000/`
- Click "Login" or "Sign Up"

### 2. Create Account (Sign Up)
- Enter username and password
- Account is created with email (optional)
- Redirects to login page

### 3. Login
- Enter your username and password
- After successful login, redirected to products page

### 4. Browse Products
- View all available products with images
- Each product shows name, price, and description
- Cart count badge shows items in cart

### 5. Add to Cart
- Click "Add to cart" button on any product
- Item added to session-based cart
- Cart count updates automatically

### 6. Manage Cart
- Go to cart page (click cart icon)
- **Change Quantity:** Use +/- buttons or type directly
- **Prices Update:** Subtotal and total update in real-time
- **Remove Items:** Click Remove button
- View total cart amount

### 7. Checkout
- Click "Place Order" button
- Order is created and saved to database
- Redirected to order confirmation page
- Cart is cleared

### 8. View Orders
- Click "Orders" in navigation
- See all previous orders with:
  - Order ID
  - Order Status
  - Total Amount
  - Date Placed
  - Number of Items
- Click "View Items" to see order details:
  - Product IDs ordered
  - Quantity per item
  - Unit price
  - Item subtotals

### 9. View User Profile
- On Orders page, click "User Details" button
- See profile information:
  - Username
  - Email address
  - Account creation date
  - Total orders placed

## API Endpoints

### Authentication
- `POST /signup` - Create new user account
- `POST /login` - User login
- `GET /user/profile` - Get logged-in user profile details

### Products
- `GET /products` - Get all products

### Cart (Session-based)
- `POST /cart/add` - Add item to cart
- `GET /cart` - Get cart contents
- `POST /cart/update` - Update item quantity
- `POST /cart/remove` - Remove item from cart
- `POST /cart/clear` - Clear entire cart

### Checkout & Orders
- `POST /checkout` - Place order
- `GET /orders` - Get all orders

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Products Table
```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT
)
```

### Orders Table
```sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
```

### Order Items Table
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
```

## Configuration

### Secret Key
The Flask secret key is set from environment variable `FLASK_SECRET`. For production, set this:

```bash
# Windows PowerShell
$env:FLASK_SECRET = "your-secret-key-here"

# macOS/Linux
export FLASK_SECRET="your-secret-key-here"
```

If not set, defaults to `"dev-secret-change-me"` (not for production).

### CORS
CORS is enabled to allow cross-origin requests from the frontend.

## Troubleshooting

### Database Error: "Cannot operate on a closed database"
- Make sure database operations are completed before closing the connection
- Use `try/finally` blocks to ensure proper cleanup

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)
```

### Module Not Found Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Image Not Found
Product images are expected in an `images/` folder. Currently using image_url from database without actual image files. Update paths in `add_products.py` if adding real images.

## Security Notes

⚠️ **For Development Only:**
- This is a learning project and not production-ready
- Passwords are hashed using Werkzeug security
- No CSRF protection implemented
- Secret key should be changed for production
- Use HTTPS in production
- Implement proper session timeout
- Add input validation and sanitization

## Future Enhancements

- [ ] Admin dashboard for product management
- [ ] User profile management
- [ ] Product search and filtering
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Inventory management
- [ ] Order tracking

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the GitHub repository:
https://github.com/srikanth695/shoppingstore/issues

## Author

Created by [srikanth695](https://github.com/srikanth695)

---

**Happy Shopping! 🛒**
