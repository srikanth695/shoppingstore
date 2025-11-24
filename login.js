// Placeholder login script to avoid 404. Add login logic here if needed.
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form") || document.querySelector('form[action="/login"]');
    const msg = document.getElementById("login-msg");

    if (!form) {
        console.warn("login.js: no login form found on page");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (msg) msg.textContent = "Logging in...";
        console.log("login.js: submit intercepted");

        const fd = new FormData(form);
        const body = new URLSearchParams();
        for (const [k, v] of fd.entries()) body.append(k, v);

        try {
            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: body.toString()
            });

            console.log("login.js: fetch complete", res.status, res.statusText);

            // try parse JSON, fall back to text
            let data;
            try { data = await res.json(); } catch (e) { data = await res.text(); }

            console.log("login.js: response body:", data);

            if (!res.ok) {
                const err = (data && data.error) ? data.error : (typeof data === "string" ? data : res.statusText);
                if (msg) msg.textContent = "Login failed: " + err;
                console.error("login.js: login failed:", res.status, err);
                return;
            }

            // success -> redirect to products page
            console.log("login.js: login successful, redirecting to /products.html");
            window.location.href = "/products.html";
        } catch (err) {
            if (msg) msg.textContent = "Login failed. Check console.";
            console.error("login.js: fetch exception:", err);
        }
    });
});