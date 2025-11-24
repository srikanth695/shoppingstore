document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form") || document.querySelector('form[action="/signup"]');
    const msg = document.getElementById("signup-msg");

    if (!form) return; // nothing to do on pages without the signup form

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (msg) msg.textContent = "Signing up...";
        const fd = new FormData(form);
        const body = new URLSearchParams();
        for (const [k, v] of fd.entries()) body.append(k, v);

        try {
            const res = await fetch("/signup", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: body.toString()
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                const err = data.error || data.detail || res.statusText;
                if (msg) msg.textContent = "Signup failed: " + err;
                console.error("Signup error:", res.status, err, data);
                return;
            }
            if (msg) msg.textContent = "Signup successful";
            console.log("Signup success:", data);
            // optionally redirect after signup:
            // window.location.href = "/login.html";
        } catch (err) {
            if (msg) msg.textContent = "Signup failed. Check console.";
            console.error("Signup exception:", err);
        }
    });
});