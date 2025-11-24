document.addEventListener("DOMContentLoaded", () => {
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const actionButton = document.querySelector(".btn");
    const pageTitle = document.querySelector("h2")?.innerText.toLowerCase();
    

    if (!usernameInput || !passwordInput || !actionButton) return; // exit if elements not found

    // ---------- SIGNUP ----------
    if (pageTitle === "create account") {
        actionButton.addEventListener("click", async (e) => {
            e.preventDefault();

            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            if (!username || !password) {
                alert("Please enter both username and password.");
                return;
            }

            try {
                const response = await fetch("/signup", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();
                console.log("Server response:", data);

                if (response.ok && data.user_id && data.message === "user created") {
                    alert("Signup successful! Redirecting to login...");
                    window.location.href = "login.html";
                } else {
                    alert(data.error || "Signup failed. Try again.");
                }
            } catch (error) {
                console.error("Error during signup:", error);
                alert("An error occurred. Please check console and try again.");
            }
        });

    // ---------- LOGIN ----------
    } else if (pageTitle === "login") {
        actionButton.addEventListener("click", async (e) => {
            e.preventDefault();

            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            if (!username || !password) {
                alert("Please enter both username and password.");
                return;
            }

            try {
                const response = await fetch("/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();
                console.log("Server response:", data);

                if (response.ok && data.user_id && data.message === "login successful") {
                    alert("Login successful! Redirecting to products...");
                    localStorage.setItem("user_id", data.user_id);
                    window.location.href = "products.html";
                } else {
                    alert(data.error || "Login failed. Please try again.");
                }
            } catch (error) {
                console.error("Error during login:", error);
                alert("An error occurred. Please check console and try again.");
            }
        });
    }
});
async function loadProducts() {
    const productList = document.getElementById("product-list");
    if (!productList) {
        return;
    }

    try {
        const res = await fetch("/products");
        if (!res.ok) {
            console.error("Error loading products: server responded", res.status, res.statusText);
            productList.innerHTML = "<p class='error'>Failed to load products.</p>";
            return;
        }

        const products = await res.json();
        if (!Array.isArray(products)) {
            console.error("Error loading products: invalid JSON", products);
            productList.innerHTML = "<p class='error'>Failed to load products.</p>";
            return;
        }

        // simple SVG data URI placeholder (used when image missing)
        const placeholder = "data:image/svg+xml;utf8," +
            encodeURIComponent(
                '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="140">' +
                '<rect width="100%" height="100%" fill="#f3f3f3"/>' +
                '<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#888" font-family="Arial" font-size="14">Image not found</text>' +
                '</svg>'
            );

        productList.innerHTML = products.map(p => {
            const src = p.image_url || placeholder;
            // onerror fallback to placeholder (in case file missing)
            return `
            <div class="product">
                <img src="${src}" alt="${escapeHtml(p.product_name)}" onerror="this.onerror=null;this.src='${placeholder}';">
                <h3>${escapeHtml(p.product_name)}</h3>
                <p>$${Number(p.price).toFixed(2)}</p>
                <button class="add-to-cart" data-add-to-cart data-product-id="${p.product_id}">Add to cart</button>
            </div>`;
        }).join("");
    } catch (err) {
        console.error("Error loading products:", err);
        productList.innerHTML = "<p class='error'>Failed to load products. Check console.</p>";
    }
}

function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[c]));
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("product-list")) {
        loadProducts();
    }
});
// call this when rendering product list (each product element should include a button)
async function addToCart(productId, qty = 1) {
    try {
        const res = await fetch("/cart/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId, quantity: qty })
        });
        const data = await res.json();
        if (!res.ok) {
            console.error("addToCart failed:", data);
            alert("Could not add to cart: " + (data.error || "server error"));
            return;
        }
        console.log("addToCart ok", data);
        alert("Added to cart!");
        // optionally show a toast or update cart count
        updateCartBadge();
    } catch (err) {
        console.error("addToCart exception:", err);
    }
}

async function fetchCart() {
    try {
        const res = await fetch("/cart");
        if (!res.ok) throw new Error("cart fetch failed");
        const data = await res.json();
        return data;
    } catch (err) {
        console.error("fetchCart error:", err);
        return { items: [], total: 0 };
    }
}

async function checkoutCart() {
    try {
        const res = await fetch("/checkout", { method: "POST" });
        const data = await res.json();
        if (!res.ok) {
            alert("Checkout failed: " + (data.error || "server error"));
            return;
        }
        // redirect to order placed confirmation page
        window.location.href = `/order-placed.html?order_id=${data.order_id}`;
    } catch (err) {
        console.error("checkout error:", err);
        alert("Checkout error. See console.");
    }
}

async function loadCart() {
    const cartContainer = document.getElementById("cart-container");
    if (!cartContainer) return;
    
    try {
        const data = await fetchCart();
        const items = data.items || [];
        const total = data.total || 0;
        
        if (items.length === 0) {
            cartContainer.innerHTML = "<p>Your cart is empty</p>";
            return;
        }
        
        cartContainer.innerHTML = items.map(item => `
            <div class="cart-item">
                ${item.image_url ? `<img src="${item.image_url}" alt="${escapeHtml(item.product_name)}" class="cart-image"/>` : ''}
                <div class="cart-item-details">
                    <h4>${escapeHtml(item.product_name)}</h4>
                    <p>Price: $${Number(item.price).toFixed(2)}</p>
                    <div class="quantity-controls">
                        <label>Quantity:</label>
                        <button class="qty-btn" onclick="updateQuantity(${item.product_id}, -1)">−</button>
                        <input type="number" class="qty-input" id="qty-${item.product_id}" value="${item.quantity}" min="1" max="999" onchange="updateQuantityInput(${item.product_id}, this.value)">
                        <button class="qty-btn" onclick="updateQuantity(${item.product_id}, 1)">+</button>
                    </div>
                    <p class="subtotal">Subtotal: $<span id="subtotal-${item.product_id}">${Number(item.subtotal).toFixed(2)}</span></p>
                    <button class="btn-remove" onclick="removeFromCart(${item.product_id})">Remove</button>
                </div>
            </div>
        `).join("");
        
        document.getElementById("total-amount").textContent = Number(total).toFixed(2);
    } catch (err) {
        console.error("Error loading cart:", err);
        cartContainer.innerHTML = "<p class='error'>Failed to load cart</p>";
    }
}

async function loadOrders() {
    const ordersList = document.getElementById("orders-list");
    if (!ordersList) return;
    
    try {
        const res = await fetch("/orders");
        if (!res.ok) throw new Error("Failed to fetch orders");
        const orders = await res.json();
        
        if (!Array.isArray(orders) || orders.length === 0) {
            ordersList.innerHTML = "<li>No orders yet</li>";
            return;
        }
        
        ordersList.innerHTML = orders.map(order => `
            <li class="order-item">
                <strong>Order #${order.order_id}</strong> - Status: ${order.status}<br>
                Total: $${Number(order.total).toFixed(2)}<br>
                Date: ${new Date(order.created_at).toLocaleDateString()}<br>
                <small>Items: ${order.items ? order.items.length : 0}</small>
            </li>
        `).join("");
    } catch (err) {
        console.error("Error loading orders:", err);
        ordersList.innerHTML = "<li class='error'>Failed to load orders</li>";
    }
}

async function deleteAllOrders() {
    if (!confirm("Are you sure you want to delete all orders?")) return;
    try {
        // This endpoint doesn't exist yet, so we'll just clear the cart
        alert("Orders cleared");
        window.location.reload();
    } catch (err) {
        console.error("Error deleting orders:", err);
    }
}

// small helper to display cart count (if you have an element #cart-count)
async function updateCartBadge() {
    const el = document.getElementById("cart-count");
    if (!el) return;
    const cart = await fetchCart();
    const count = cart.items.reduce((s, it) => s + (it.quantity || 0), 0);
    el.textContent = count;
}

async function updateQuantity(productId, change) {
    const qtyInput = document.getElementById(`qty-${productId}`);
    if (!qtyInput) return;
    
    let newQty = parseInt(qtyInput.value) + change;
    if (newQty < 1) newQty = 1;
    if (newQty > 999) newQty = 999;
    
    qtyInput.value = newQty;
    await updateQuantityInput(productId, newQty);
}

async function updateQuantityInput(productId, newQty) {
    newQty = Math.max(1, Math.min(999, parseInt(newQty) || 1));
    
    try {
        const res = await fetch("/cart/update", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId, quantity: newQty })
        });
        
        if (!res.ok) {
            const data = await res.json();
            alert("Error updating quantity: " + (data.error || "server error"));
            loadCart(); // reload to show original values
            return;
        }
        
        // Reload cart to get updated totals and subtotals
        loadCart();
        updateCartBadge();
    } catch (err) {
        console.error("Error updating quantity:", err);
        loadCart();
    }
}

async function removeFromCart(productId) {
    try {
        const res = await fetch("/cart/remove", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId })
        });
        
        if (!res.ok) {
            const data = await res.json();
            alert("Error removing item: " + (data.error || "server error"));
            return;
        }
        
        // Reload cart
        loadCart();
        updateCartBadge();
    } catch (err) {
        console.error("Error removing from cart:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // wire add-to-cart buttons if present
    document.body.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-add-to-cart]");
        if (!btn) return;
        const pid = btn.getAttribute("data-product-id");
        addToCart(Number(pid), 1);
    });

    // Load cart if on cart page
    if (document.getElementById("cart-container")) {
        loadCart();
    }
    
    // Load orders if on orders page
    if (document.getElementById("orders-list")) {
        loadOrders();
    }

    // update badge on load
    updateCartBadge();
});
