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
                const response = await fetch("http://127.0.0.1:5000/signup", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();
                console.log("Server response:", data);

                if (response.ok && data.user_id && data.message === "Signup successful") {
                    alert("Signup successful! Redirecting to login...");
                    window.location.href = "login.html";
                } else {
                    alert(data.message || "Signup failed. Try again.");
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
                const response = await fetch("http://127.0.0.1:5000/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();
                console.log("Server response:", data);

                if (response.ok && data.user_id && data.message === "Login successful") {
                    alert("Login successful! Redirecting to products...");
                    localStorage.setItem("user_id", data.user_id);
                    window.location.href = "products.html";
                } else {
                    alert(data.message || "Login failed. Please try again.");
                }
            } catch (error) {
                console.error("Error during login:", error);
                alert("An error occurred. Please check console and try again.");
            }
        });
    }
});
const productList = document.getElementById("product-list");

async function loadProducts() {
    try {
        const response = await fetch("/products");
        const products = await response.json();

        productList.innerHTML = "";

        products.forEach(product => {
            const div = document.createElement("div");
            div.className = "product-card";

            div.innerHTML = `
                <img src="${product.image_url}" alt="${product.product_name}" class="product-img">
                <h3>${product.product_name}</h3>
                <p>Price: $${product.price}</p>
                <button>Add to Cart</button>
            `;

            productList.appendChild(div);
        });

    } catch (err) {
        console.error("Error loading products:", err);
        alert("Failed to load products. Check console.");
    }
}

document.addEventListener("DOMContentLoaded", loadProducts);
