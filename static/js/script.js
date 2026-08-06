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

            const reader = new FileReader();

            reader.onload = function (event) {

                previewImage.src = event.target.result;

                previewBox.style.display = "block";

            };

            reader.readAsDataURL(file);

            fileName.textContent = file.name;

        }

    });

}


// ===============================
// LOGIN MODAL
// ===============================

function openLogin() {

    const modal = document.getElementById("loginModal");

    modal.style.display = "flex";

    document.body.style.overflow = "hidden";

}


function closeLogin() {

    const modal = document.getElementById("loginModal");

    modal.style.display = "none";

    document.body.style.overflow = "auto";

}


// Close when clicking outside

window.addEventListener("click", function (event) {

    const modal = document.getElementById("loginModal");

    if (event.target === modal) {

        closeLogin();

    }

});


// ESC key

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        closeLogin();

    }

});


// ===============================
// SIGN UP
// ===============================

function showSignup() {

    alert("Sign Up page will be added next!");

}