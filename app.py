from flask import Flask, render_template, request, redirect, url_for, session
import os
import oracledb
from predict import predict_image
from pdf_generator import create_pdf
from flask import send_file

# ==========================
# Flask App
# ==========================

app = Flask(__name__)
app.secret_key = "truthlens_secret_key"

# ==========================
# Upload Folder
# ==========================

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# Oracle Database Connection
# ==========================

def get_connection():

    return oracledb.connect(
        user="system",
        password="anbu123",
        dsn="localhost:1521/XE"
    )

# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================
# SIGN UP
# ==========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT NVL(MAX(ID),0)+1 FROM TRUTHLENS_USERS"
            )

            new_id = cursor.fetchone()[0]

            cursor.execute("""

                INSERT INTO TRUTHLENS_USERS
                (
                    ID,
                    FULLNAME,
                    EMAIL,
                    PASSWORD,
                    CREATED_AT
                )

                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    SYSDATE
                )

            """,
            (
                new_id,
                fullname,
                email,
                password
            ))

            conn.commit()

            cursor.close()
            conn.close()

            return render_template(
                "signup.html",
                success="Sign Up Successful!"
            )

        except Exception as e:

            return render_template(
                "signup.html",
                error=str(e)
            )

    return render_template("signup.html")


# ==========================
# CREATE ACCOUNT
# ==========================

@app.route("/create-account", methods=["GET", "POST"])
def create_account():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        dob = request.form.get("dob")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            return render_template(
                "create_account.html",
                error="Passwords do not match!"
            )

        if len(password) < 6:

            return render_template(
                "create_account.html",
                error="Password must contain at least 6 characters!"
            )

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT NVL(MAX(ID),0)+1 FROM TRUTHLENS_USERS"
            )

            new_id = cursor.fetchone()[0]

            cursor.execute("""

                INSERT INTO TRUTHLENS_USERS
                (
                    ID,
                    FULLNAME,
                    EMAIL,
                    PHONE,
                    DOB,
                    PASSWORD,
                    CREATED_AT
                )

                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    TO_DATE(:5,'YYYY-MM-DD'),
                    :6,
                    SYSDATE
                )

            """,
            (
                new_id,
                fullname,
                email,
                phone,
                dob,
                password
            ))

            conn.commit()

            cursor.close()
            conn.close()

            return render_template(
                "create_account.html",
                success="Account Created Successfully!"
            )

        except Exception as e:

            return render_template(
                "create_account.html",
                error=str(e)
            )

    return render_template("create_account.html")
   
# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"].strip()
    password = request.form["password"].strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ID,
            FULLNAME,
            EMAIL
        FROM TRUTHLENS_USERS
        WHERE TRIM(LOWER(EMAIL)) = TRIM(LOWER(:1))
        AND TRIM(PASSWORD) = TRIM(:2)
    """, (email, password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:

        session["user_id"] = user[0]
        session["fullname"] = user[1]
        session["email"] = user[2]

        return redirect(url_for("dashboard"))

    return render_template(
        "index.html",
        error="Invalid Email or Password!"
    )
# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            IMAGE_NAME,
            RESULT,
            CONFIDENCE,
            CREATED_AT
        FROM TRUTHLENS_HISTORY
        WHERE USER_ID = :1
        ORDER BY ID DESC
    """, (session["user_id"],))

    history = cursor.fetchall()

    total_images = len(history)
    real_count = sum(1 for h in history if h[1] == "REAL")
    fake_count = sum(1 for h in history if h[1] == "FAKE")
    
    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        email=session["email"],
        history=history,
        total_images=total_images,
        real_count=real_count,
        fake_count=fake_count,
      
    )

# ==========================
# PROFILE
# ==========================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template(
        "profile.html",
        fullname=session["fullname"]
    )
# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ==========================
# DOWNLOAD PDF REPORT
# ==========================

@app.route("/download-report")
def download_report():

    if "user_id" not in session:
        return redirect(url_for("home"))

    image_name = session.get("last_image")
    result = session.get("last_result")
    confidence = session.get("last_confidence")

    if image_name is None:
        return redirect(url_for("dashboard"))

    pdf_file = create_pdf(
        image_name,
        result,
        confidence
    )

    return send_file(
        pdf_file,
        as_attachment=True
    )


# ==========================
# IMAGE PREDICTION
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if "image" not in request.files:
        return redirect(url_for("dashboard"))

    file = request.files["image"]

    if file.filename == "":
        return redirect(url_for("dashboard"))


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)


    # ==========================
    # CAPCHECK AI PREDICTION
    # ==========================

    try:

        result, confidence = predict_image(filepath)
        confidence = float(confidence)

    except Exception as e:

        return render_template(
            "dashboard.html",
            error=str(e)
        )


    print("===================================")
    print("IMAGE :", file.filename)
    print("RESULT :", result)
    print("CONFIDENCE :", confidence)
    print("===================================")


    # ==========================
    # SAVE HISTORY DATABASE
    # ==========================

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT NVL(MAX(ID),0)+1
        FROM TRUTHLENS_HISTORY
    """)

    history_id = cursor.fetchone()[0]


    cursor.execute("""
        INSERT INTO TRUTHLENS_HISTORY
        (
            ID,
            USER_ID,
            IMAGE_NAME,
            RESULT,
            CONFIDENCE,
            CREATED_AT
        )

        VALUES
        (
            :1,
            :2,
            :3,
            :4,
            :5,
            SYSDATE
        )

    """,
    (
        history_id,
        session["user_id"],
        file.filename,
        result,
        confidence
    ))


    conn.commit()



    # ==========================
    # GET HISTORY
    # ==========================

    cursor.execute("""
        SELECT
            IMAGE_NAME,
            RESULT,
            CONFIDENCE,
            CREATED_AT
        FROM TRUTHLENS_HISTORY
        WHERE USER_ID=:1
        ORDER BY ID DESC
    """,
    (
        session["user_id"],
    ))


    history = cursor.fetchall()



    total_images = len(history)

    real_count = sum(
        1 for h in history if h[1]=="REAL"
    )

    fake_count = sum(
        1 for h in history if h[1]=="FAKE"
    )

 



    cursor.close()
    conn.close()



    # ==========================
    # PDF SESSION DATA
    # ==========================

    session["last_image"] = file.filename
    session["last_result"] = result
    session["last_confidence"] = confidence



    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        email=session["email"],
        result=result,
        confidence=confidence,
        image=file.filename,
        history=history,
        total_images=total_images,
        real_count=real_count,
        fake_count=fake_count,
       
    )

# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )