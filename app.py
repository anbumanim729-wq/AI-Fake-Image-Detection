from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename

from predict import predict_image
from pdf_generator import create_pdf


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

# IMPORTANT:
# Render-la SECRET_KEY environment variable set pannala na
# local development-ku this value use aagum.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "truthlens_secret_key"
)


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# SUPABASE / POSTGRESQL DATABASE CONNECTION
# =========================================================

def get_connection():

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not configured."
        )

    return psycopg2.connect(
        database_url,
        sslmode="require",
        connect_timeout=10
    )


# =========================================================
# DATABASE TEST
# =========================================================

@app.route("/db-test")
def db_test():

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # -------------------------------------------------
        # DATABASE INFORMATION
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                current_user,
                current_database(),
                version()
        """)

        info = cursor.fetchone()

        # -------------------------------------------------
        # CHECK USERS TABLE
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM public.truthlens_users
        """)

        user_count = cursor.fetchone()[0]

        # -------------------------------------------------
        # CHECK HISTORY TABLE
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM public.truthlens_history
        """)

        history_count = cursor.fetchone()[0]

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        cursor.close()
        conn.close()

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>TruthLens Database Test</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: #111827;
                    color: white;
                    padding: 50px;
                }}

                .box {{
                    max-width: 800px;
                    margin: auto;
                    background: #1f2937;
                    padding: 35px;
                    border-radius: 15px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.4);
                }}

                h2 {{
                    color: #22c55e;
                }}

                p {{
                    font-size: 18px;
                    margin: 15px 0;
                }}

                .value {{
                    color: #60a5fa;
                    font-weight: bold;
                }}

            </style>

        </head>

        <body>

            <div class="box">

                <h2>Database Test Successful</h2>

                <p>
                    Database User:
                    <span class="value">{info[0]}</span>
                </p>

                <p>
                    Database:
                    <span class="value">{info[1]}</span>
                </p>

                <p>
                    Users:
                    <span class="value">{user_count}</span>
                </p>

                <p>
                    History Records:
                    <span class="value">{history_count}</span>
                </p>

            </div>

        </body>

        </html>
        """

    except Exception as e:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Database Error</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: #111827;
                    color: white;
                    padding: 50px;
                }}

                .box {{
                    max-width: 800px;
                    margin: auto;
                    background: #7f1d1d;
                    padding: 30px;
                    border-radius: 15px;
                }}

                h2 {{
                    color: #fecaca;
                }}

                pre {{
                    white-space: pre-wrap;
                    color: #fecaca;
                }}

            </style>

        </head>

        <body>

            <div class="box">

                <h2>Database Error</h2>

                <pre>{e}</pre>

            </div>

        </body>

        </html>
        """


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# SIGN UP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not fullname or not email or not password:

            return render_template(
                "signup.html",
                error="Please fill all required fields!"
            )

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            # -------------------------------------------------
            # CHECK EXISTING EMAIL
            # -------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM public.truthlens_users
                WHERE LOWER(email) = LOWER(%s)
                LIMIT 1
            """, (email,))

            existing_user = cursor.fetchone()

            if existing_user:

                return render_template(
                    "signup.html",
                    error="Email already registered!"
                )

            # -------------------------------------------------
            # INSERT USER
            # ID IS AUTO GENERATED
            # -------------------------------------------------

            cursor.execute("""
                INSERT INTO public.truthlens_users
                (
                    fullname,
                    email,
                    password,
                    created_at
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    NOW()
                )
            """, (
                fullname,
                email,
                password
            ))

            conn.commit()

            return render_template(
                "signup.html",
                success="Sign Up Successful!"
            )

        except Exception as e:

            if conn:
                conn.rollback()

            return render_template(
                "signup.html",
                error="Database Error: " + str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    return render_template("signup.html")


# =========================================================
# CREATE ACCOUNT
# =========================================================

@app.route("/create-account", methods=["GET", "POST"])
def create_account():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        dob = request.form.get("dob", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # -------------------------------------------------
        # REQUIRED FIELDS
        # -------------------------------------------------

        if not fullname or not email or not password:

            return render_template(
                "create_account.html",
                error="Please fill all required fields!"
            )

        # -------------------------------------------------
        # PASSWORD MATCH
        # -------------------------------------------------

        if password != confirm_password:

            return render_template(
                "create_account.html",
                error="Passwords do not match!"
            )

        # -------------------------------------------------
        # PASSWORD LENGTH
        # -------------------------------------------------

        if len(password) < 6:

            return render_template(
                "create_account.html",
                error="Password must contain at least 6 characters!"
            )

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            # -------------------------------------------------
            # CHECK EMAIL
            # -------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM public.truthlens_users
                WHERE LOWER(email) = LOWER(%s)
                LIMIT 1
            """, (email,))

            existing_user = cursor.fetchone()

            if existing_user:

                return render_template(
                    "create_account.html",
                    error="Email already registered!"
                )

            # -------------------------------------------------
            # OPTIONAL VALUES
            # -------------------------------------------------

            phone_value = phone if phone else None
            dob_value = dob if dob else None

            # -------------------------------------------------
            # INSERT ACCOUNT
            # ID AUTO GENERATED
            # -------------------------------------------------

            cursor.execute("""
                INSERT INTO public.truthlens_users
                (
                    fullname,
                    email,
                    phone,
                    dob,
                    password,
                    created_at
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    NOW()
                )
            """, (
                fullname,
                email,
                phone_value,
                dob_value,
                password
            ))

            conn.commit()

            return render_template(
                "create_account.html",
                success="Account Created Successfully!"
            )

        except Exception as e:

            if conn:
                conn.rollback()

            return render_template(
                "create_account.html",
                error="Database Error: " + str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    return render_template("create_account.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not email or not password:

        return render_template(
            "index.html",
            error="Please enter Email and Password!"
        )

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # -------------------------------------------------
        # LOGIN QUERY
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                fullname,
                email
            FROM public.truthlens_users
            WHERE LOWER(TRIM(email)) = LOWER(TRIM(%s))
            AND TRIM(password) = TRIM(%s)
            LIMIT 1
        """, (
            email,
            password
        ))

        user = cursor.fetchone()

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        cursor.close()
        conn.close()

        # -------------------------------------------------
        # LOGIN SUCCESS
        # -------------------------------------------------

        if user:

            session["user_id"] = user[0]
            session["fullname"] = user[1]
            session["email"] = user[2]

            return redirect(
                url_for("dashboard")
            )

        # -------------------------------------------------
        # LOGIN FAILED
        # -------------------------------------------------

        return render_template(
            "index.html",
            error="Invalid Email or Password!"
        )

    except Exception as e:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        return render_template(
            "index.html",
            error="Database Error: " + str(e)
        )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # -------------------------------------------------
        # GET USER HISTORY
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                image_name,
                result,
                confidence,
                created_at
            FROM public.truthlens_history
            WHERE user_id = %s
            ORDER BY id DESC
        """, (
            session["user_id"],
        ))

        history = cursor.fetchall()

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        total_images = len(history)

        real_count = sum(
            1
            for h in history
            if str(h[1]).upper() == "REAL"
        )

        fake_count = sum(
            1
            for h in history
            if str(h[1]).upper() == "FAKE"
        )

        cursor.close()
        conn.close()

        return render_template(
            "dashboard.html",
            fullname=session["fullname"],
            email=session["email"],
            history=history,
            total_images=total_images,
            real_count=real_count,
            fake_count=fake_count
        )

    except Exception as e:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        return render_template(
            "dashboard.html",
            fullname=session.get("fullname", ""),
            email=session.get("email", ""),
            history=[],
            total_images=0,
            real_count=0,
            fake_count=0,
            error="Database Error: " + str(e)
        )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    return render_template(
        "profile.html",
        fullname=session["fullname"]
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================

@app.route("/download-report")
def download_report():

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    image_name = session.get("last_image")
    result = session.get("last_result")
    confidence = session.get("last_confidence")

    if image_name is None:

        return redirect(
            url_for("dashboard")
        )

    try:

        pdf_file = create_pdf(
            image_name,
            result,
            confidence
        )

        return send_file(
            pdf_file,
            as_attachment=True
        )

    except Exception as e:

        return render_template(
            "dashboard.html",
            fullname=session.get("fullname", ""),
            email=session.get("email", ""),
            history=[],
            total_images=0,
            real_count=0,
            fake_count=0,
            error="PDF Error: " + str(e)
        )


# =========================================================
# IMAGE PREDICTION
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    # -------------------------------------------------
    # CHECK IMAGE
    # -------------------------------------------------

    if "image" not in request.files:

        return redirect(
            url_for("dashboard")
        )

    file = request.files["image"]

    if file.filename == "":

        return redirect(
            url_for("dashboard")
        )

    # -------------------------------------------------
    # SECURE FILE NAME
    # -------------------------------------------------

    original_filename = file.filename

    safe_filename = secure_filename(
        original_filename
    )

    if not safe_filename:

        return redirect(
            url_for("dashboard")
        )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        safe_filename
    )

    file.save(filepath)

    # -------------------------------------------------
    # AI PREDICTION
    # -------------------------------------------------

    try:

        result, confidence = predict_image(
            filepath
        )

        confidence = float(
            confidence
        )

    except Exception as e:

        return render_template(
            "dashboard.html",
            fullname=session.get("fullname", ""),
            email=session.get("email", ""),
            history=[],
            total_images=0,
            real_count=0,
            fake_count=0,
            error="Prediction Error: " + str(e)
        )

    print("===================================")
    print("IMAGE :", safe_filename)
    print("RESULT :", result)
    print("CONFIDENCE :", confidence)
    print("===================================")

    # -------------------------------------------------
    # SAVE HISTORY
    # -------------------------------------------------

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO public.truthlens_history
            (
                user_id,
                image_name,
                result,
                confidence,
                created_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                NOW()
            )
        """, (
            session["user_id"],
            safe_filename,
            result,
            confidence
        ))

        conn.commit()

        # -------------------------------------------------
        # GET UPDATED HISTORY
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                image_name,
                result,
                confidence,
                created_at
            FROM public.truthlens_history
            WHERE user_id = %s
            ORDER BY id DESC
        """, (
            session["user_id"],
        ))

        history = cursor.fetchall()

        total_images = len(history)

        real_count = sum(
            1
            for h in history
            if str(h[1]).upper() == "REAL"
        )

        fake_count = sum(
            1
            for h in history
            if str(h[1]).upper() == "FAKE"
        )

        cursor.close()
        conn.close()

    except Exception as e:

        if conn:
            conn.rollback()

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        return render_template(
            "dashboard.html",
            fullname=session.get("fullname", ""),
            email=session.get("email", ""),
            history=[],
            total_images=0,
            real_count=0,
            fake_count=0,
            error="History Database Error: " + str(e)
        )

    # -------------------------------------------------
    # SAVE SESSION DATA FOR PDF
    # -------------------------------------------------

    session["last_image"] = safe_filename
    session["last_result"] = result
    session["last_confidence"] = confidence

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        email=session["email"],
        result=result,
        confidence=confidence,
        image=safe_filename,
        history=history,
        total_images=total_images,
        real_count=real_count,
        fake_count=fake_count
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        debug=True,
        host="0.0.0.0",
        port=port
    )