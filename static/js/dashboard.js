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

    const form =
        document.getElementById("uploadForm");

    const fileInput =
        document.getElementById("image");

    const analyzeBtn =
        document.getElementById("analyzeBtn");

    const analyzeBtnText =
        document.getElementById("analyzeBtnText");


    console.log("Upload Form:", form);
    console.log("Image Input:", fileInput);
    console.log("Analyze Button:", analyzeBtn);


    // -------------------------------------------------
    // CHECK ELEMENTS
    // -------------------------------------------------

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


    // =================================================
    // FORM SUBMIT
    // =================================================

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
                !allowedTypes.includes(file.type)
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


            // =================================================
            // VALIDATION SUCCESS
            // =================================================

            console.log(
                "Validation successful."
            );


            console.log(
                "Submitting image to /predict..."
            );


            // =================================================
            // SHOW ANALYSING ANIMATION
            // =================================================

            if (analyzeBtn) {

                // Disable button
                analyzeBtn.disabled = true;

                // Add loading class
                analyzeBtn.classList.add(
                    "loading"
                );

            }


            if (analyzeBtnText) {

                analyzeBtnText.innerHTML =
                    '<span class="loading-spinner"></span> Analysing...';

            }


            console.log(
                "Analysis started..."
            );

            console.log(
                "==================================="
            );


            // IMPORTANT:
            // DO NOT USE preventDefault()
            //
            // Flask /predict will receive the image normally.

        }
    );

}


// =========================================================
// IMAGE PREVIEW + ORIGINAL FILENAME
// =========================================================

function imagePreview() {

    const input =
        document.getElementById("image");

    const fileNameBox =
        document.getElementById(
            "selectedFileName"
        );


    console.log(
        "Image Preview Initialized"
    );


    if (!input) {

        console.error(
            "Image input not found for preview!"
        );

        return;
    }


    // =================================================
    // FILE CHANGE EVENT
    // =================================================

    input.addEventListener(
        "change",
        function () {

            console.log(
                "==================================="
            );

            console.log(
                "FILE CHANGE EVENT TRIGGERED"
            );


            // -------------------------------------------------
            // NO FILE
            // -------------------------------------------------

            if (
                !this.files ||
                this.files.length === 0
            ) {

                console.log(
                    "No file selected."
                );


                if (fileNameBox) {

                    fileNameBox.textContent =
                        "No image selected";

                    fileNameBox.classList.remove(
                        "has-file"
                    );

                }

                return;
            }


            // -------------------------------------------------
            // GET FILE
            // -------------------------------------------------

            const file =
                this.files[0];


            console.log(
                "Selected Image:",
                file.name
            );


            // =================================================
            // SHOW ORIGINAL FILE NAME
            // =================================================

            if (fileNameBox) {

                fileNameBox.textContent =
                    "📁 Selected: " + file.name;

                fileNameBox.classList.add(
                    "has-file"
                );

            } else {

                console.error(
                    "selectedFileName element not found!"
                );

            }


            // =================================================
            // REMOVE OLD PREVIEW
            // =================================================

            const oldPreview =
                document.getElementById(
                    "clientImagePreview"
                );


            if (oldPreview) {

                oldPreview.remove();

            }


            // =================================================
            // CREATE IMAGE PREVIEW
            // =================================================

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


                    img.style.width =
                        "auto";


                    img.style.height =
                        "auto";


                    img.style.margin =
                        "15px auto 0";


                    img.style.borderRadius =
                        "12px";


                    img.style.display =
                        "block";


                    img.style.objectFit =
                        "contain";


                    img.style.border =
                        "2px solid #334155";


                    // Add preview after filename
                    input.parentElement.appendChild(
                        img
                    );


                    console.log(
                        "Image preview created successfully."
                    );

                };


            reader.onerror =
                function () {

                    console.error(
                        "Failed to read image file."
                    );

                };


            reader.readAsDataURL(file);


            console.log(
                "==================================="
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
// DEBUG
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
