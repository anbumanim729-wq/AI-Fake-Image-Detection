// ==========================
// TruthLens Dashboard
// ==========================

document.addEventListener("DOMContentLoaded", () => {

    console.log("TruthLens Dashboard Loaded");

    showWelcome();

    animateCards();

    uploadValidation();

    imagePreview();

});

// ==========================
// Welcome Greeting
// ==========================

function showWelcome() {

    const hour = new Date().getHours();

    let greeting = "";

    if (hour < 12) {

        greeting = "☀️ Good Morning";

    }

    else if (hour < 18) {

        greeting = "🌤️ Good Afternoon";

    }

    else {

        greeting = "🌙 Good Evening";

    }

    console.log(greeting);

}

// ==========================
// Card Animation
// ==========================

function animateCards() {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(40px)";

        setTimeout(() => {

            card.style.transition = "0.6s ease";

            card.style.opacity = "1";

            card.style.transform = "translateY(0px)";

        }, index * 150);

    });

}

// ==========================
// Upload Validation
// ==========================

function uploadValidation() {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function(e) {

        const fileInput = document.querySelector('input[type="file"]');

        if (!fileInput.files.length) {

            e.preventDefault();

            alert("Please select an image.");

            return;

        }

        const file = fileInput.files[0];

        const allowed = [

            "image/jpeg",
            "image/png",
            "image/jpg"

        ];

        if (!allowed.includes(file.type)) {

            e.preventDefault();

            alert("Only JPG, JPEG and PNG images are allowed.");

            return;

        }

    });

}

// ==========================
// Image Preview
// ==========================

function imagePreview() {

    const input = document.querySelector('input[type="file"]');

    if (!input) return;

    input.addEventListener("change", function() {

        if (this.files.length > 0) {

            console.log("Selected File :", this.files[0].name);

        }

    });

}

// ==========================
// Logout Confirmation
// ==========================

const logoutLink = document.querySelector('a[href="/logout"]');

if (logoutLink) {

    logoutLink.addEventListener("click", function(e) {

        const ok = confirm("Are you sure you want to logout?");

        if (!ok) {

            e.preventDefault();

        }

    });

}

// ==========================
// Refresh Dashboard
// ==========================

function refreshDashboard() {

    location.reload();

}

// ==========================
// Future Features
// ==========================

// ✅ Live Charts
// ✅ Detection History Search
// ✅ Dark Mode
// ✅ Profile Update
// ✅ Download Report (PDF)
// ✅ Export History to Excel
// ✅ Notification System