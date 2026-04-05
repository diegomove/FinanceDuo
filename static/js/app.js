/* Els Nostres Dobbers — UI helpers */

document.addEventListener("DOMContentLoaded", () => {
    /* Add CSRF token to every POST form */
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute("content");
    if (csrfToken) {
        document.querySelectorAll('form[method="POST"], form[method="post"]').forEach((form) => {
            if (!form.querySelector('input[name="_csrf_token"]')) {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = "_csrf_token";
                input.value = csrfToken;
                form.appendChild(input);
            }
        });
    }

    /* Auto-dismiss alerts after 4 seconds */
    document.querySelectorAll(".alert-dismissible").forEach((alert) => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    /* ---- Theme switcher ---- */
    const currentTheme = localStorage.getItem("theme") || "warm";

    document.querySelectorAll(".theme-option").forEach((btn) => {
        if (btn.dataset.theme === currentTheme) {
            btn.classList.add("active");
        }

        btn.addEventListener("click", () => {
            const theme = btn.dataset.theme;
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
            document.querySelectorAll(".theme-option").forEach((b) => b.classList.remove("active"));
            document.querySelectorAll('.theme-option[data-theme="' + theme + '"]').forEach((b) => b.classList.add("active"));
        });
    });

    /* ---- Loading state on form submit ---- */
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const btn = form.querySelector('button[type="submit"]');
            if (btn && !btn.classList.contains("btn-outline-danger")) {
                btn.classList.add("btn-loading");
            }
        });
    });
});
