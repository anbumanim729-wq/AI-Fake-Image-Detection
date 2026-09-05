// ===============================
// IMAGE PREVIEW
// ===============================

const imageInput = document.getElementById("imageInput");
const previewBox = document.getElementById("previewBox");
const previewImage = document.getElementById("previewImage");
const fileName = document.getElementById("fileName");

if (imageInput) {

    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (file) {

            // Show file name
            if (fileName) {
                fileName.textContent = "Selected: " + file.name;
            }

            // Image preview
            if (previewImage && previewBox) {

                const reader = new FileReader();

                reader.onload = function (event) {

                    previewImage.src = event.target.result;

                    previewImage.style.display = "block";

                    previewBox.style.display = "block";
                };

                reader.readAsDataURL(file);
            }

        } else {

            if (fileName) {
                fileName.textContent = "";
            }

            if (previewImage) {
                previewImage.style.display = "none";
            }

        }

    });

}


// ===============================
// IMAGE ANALYSIS ANIMATION
// ===============================

const uploadForm = document.getElementById("uploadForm");
const analyseBtn = document.getElementById("analyseBtn");
const btnText = document.getElementById("btnText");
const btnIcon = document.getElementById("btnIcon");

if (uploadForm) {

    uploadForm.addEventListener("submit", function () {

        // Prevent multiple clicks
        if (analyseBtn) {
            analyseBtn.disabled = true;
            analyseBtn.classList.add("analysing");
        }

        // Change button icon
        if (btnIcon) {
            btnIcon.innerHTML = `
                <span class="loading-spinner"></span>
            `;
        }

        // Change button text
        if (btnText) {
            btnText.textContent = "Analysing...";
        }

    });

}


// ===============================
// LOGIN MODAL
// ===============================

function openLogin() {

    const modal = document.getElementById("loginModal");

    if (modal) {

        modal.style.display = "flex";

        document.body.style.overflow = "hidden";

    }

}


function closeLogin() {

    const modal = document.getElementById("loginModal");

    if (modal) {

        modal.style.display = "none";

        document.body.style.overflow = "auto";

    }

}


// ===============================
// CLOSE LOGIN WHEN CLICKING OUTSIDE
// ===============================

window.addEventListener("click", function (event) {

    const modal = document.getElementById("loginModal");

    if (modal && event.target === modal) {

        closeLogin();

    }

});


// ===============================
// ESC KEY - CLOSE LOGIN
// ===============================

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        closeLogin();

    }

});


// ===============================
// SIGN UP
// ===============================

function showSignup() {

    window.location.href = "/signup";

}