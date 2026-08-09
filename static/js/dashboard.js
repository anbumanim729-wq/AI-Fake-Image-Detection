```javascript
// =========================================================
// TRUTHLENS AI DASHBOARD
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("===================================");
    console.log("TruthLens Dashboard Loaded");
    console.log("===================================");

    showWelcome();
    animateCards();
    uploadValidation();
    imagePreview();
    logoutConfirmation();

});


// =========================================================
// WELCOME GREETING
// =========================================================

function showWelcome() {

    const hour = new Date().getHours();

    let greeting;

    if (hour < 12) {

        greeting = "☀️ Good Morning";

    } else if (hour < 18) {

        greeting = "🌤️ Good Afternoon";

    } else {

        greeting = "🌙 Good Evening";

    }

    console.log(greeting);
}


// =========================================================
// CARD ANIMATION
// =========================================================

function animateCards() {

    const cards = document.querySelectorAll(
        ".stat-card, .card"
    );

    cards.forEach(function (card, index) {

        card.style.opacity = "0";
        card.style.transform = "translateY(25px)";

        setTimeout(function () {

            card.style.transition =
                "opacity 0.5s ease, transform 0.5s ease";

            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, index * 100);

    });
}


// =========================================================
// IMAGE UPLOAD VALIDATION
// =========================================================

function uploadValidation() {

    const form = document.getElementById(
        "uploadForm"
    );

    const fileInput = document.getElementById(
        "image"
    );


    if (!form) {

        console.error(
            "ERROR: uploadForm not found!"
        );

        return;
    }


    if (!fileInput) {

        console.error(
            "ERROR: image input not found!"
        );

        return;
    }


    form.addEventListener(
        "submit",
        function (event) {

            console.log(
                "==================================="
            );

            console.log(
                "UPLOAD FORM SUBMITTED"
            );


            // -------------------------------------------------
            // CHECK FILE
            // -------------------------------------------------

            if (
                !fileInput.files ||
                fileInput.files.length === 0
            ) {

                event.preventDefault();

                alert(
                    "Please select an image."
                );

                console.error(
                    "No image selected."
                );

                return;
            }


            const file =
                fileInput.files[0];


            console.log(
                "Selected file:",
                file.name
            );

            console.log(
                "File type:",
                file.type
            );

            console.log(
                "File size:",
                file.size,
                "bytes"
            );


            // -------------------------------------------------
            // ALLOWED TYPES
            // -------------------------------------------------

            const allowedTypes = [
                "image/jpeg",
                "image/png",
                "image/jpg",
                "image/webp"
            ];


            if (
                !allowedTypes.includes(
                    file.type
                )
            ) {

                event.preventDefault();

                alert(
                    "Only JPG, JPEG, PNG and WEBP images are allowed."
                );

                console.error(
                    "Invalid image type:",
                    file.type
                );

                return;
            }


            // -------------------------------------------------
            // FILE SIZE
            // -------------------------------------------------

            const maxSize =
                10 * 1024 * 1024;


            if (file.size > maxSize) {

                event.preventDefault();

                alert(
                    "Image size must be less than 10 MB."
                );

                console.error(
                    "Image too large."
                );

                return;
            }


            // -------------------------------------------------
            // IMPORTANT
            // -------------------------------------------------

            console.log(
                "Validation successful."
            );

            console.log(
                "Submitting image to /predict..."
            );

            console.log(
                "==================================="
            );


            // DO NOT USE preventDefault()
            // Browser will submit normally to Flask.
        }
    );
}


// =========================================================
// IMAGE PREVIEW
// =========================================================

function imagePreview() {

    const input =
        document.getElementById("image");


    if (!input) {

        return;
    }


    input.addEventListener(
        "change",
        function () {

            if (
                !this.files ||
                this.files.length === 0
            ) {

                return;
            }


            const file =
                this.files[0];


            console.log(
                "Image selected:",
                file.name
            );


            // -------------------------------------------------
            // REMOVE OLD PREVIEW
            // -------------------------------------------------

            const oldPreview =
                document.getElementById(
                    "clientImagePreview"
                );


            if (oldPreview) {

                oldPreview.remove();
            }


            // -------------------------------------------------
            // CREATE PREVIEW
            // -------------------------------------------------

            const reader =
                new FileReader();


            reader.onload =
                function (event) {

                    const img =
                        document.createElement(
                            "img"
                        );


                    img.id =
                        "clientImagePreview";


                    img.src =
                        event.target.result;


                    img.alt =
                        "Selected Image";


                    img.style.maxWidth =
                        "250px";


                    img.style.maxHeight =
                        "250px";


                    img.style.marginTop =
                        "15px";


                    img.style.borderRadius =
                        "12px";


                    img.style.display =
                        "block";


                    input.parentElement.appendChild(
                        img
                    );
                };


            reader.readAsDataURL(
                file
            );

        }
    );
}


// =========================================================
// LOGOUT CONFIRMATION
// =========================================================

function logoutConfirmation() {

    const logoutLink =
        document.querySelector(
            'a[href="/logout"]'
        );


    if (!logoutLink) {

        return;
    }


    logoutLink.addEventListener(
        "click",
        function (event) {

            const confirmed =
                confirm(
                    "Are you sure you want to logout?"
                );


            if (!confirmed) {

                event.preventDefault();
            }

        }
    );
}


// =========================================================
// REFRESH DASHBOARD
// =========================================================

function refreshDashboard() {

    window.location.reload();

}


// =========================================================
// DEBUG HELPER
// =========================================================

console.log(
    "TruthLens dashboard.js loaded successfully."
);


// =========================================================
// FUTURE FEATURES
// =========================================================

// Live Charts
// Detection History Search
// Dark Mode
// Profile Update
// Download Report PDF
// Export History
// Notification System
```
