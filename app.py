from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

import os
import uuid
import psycopg2

from dotenv import load_dotenv

load_dotenv()

from werkzeug.utils import secure_filename

from predict import predict_image
from pdf_generator import create_pdf


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "truthlens_secret_key"
)


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = os.path.join(
    "static",
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# DATABASE CONNECTION
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
# GET DASHBOARD DATA
# =========================================================

def get_dashboard_data(user_id):

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                image_name,
                result,
                confidence,
                created_at
            FROM public.truthlens_history
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

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

        return {
            "history": history,
            "total_images": total_images,
            "real_count": real_count,
            "fake_count": fake_count,
            "error": None
        }

    except Exception as e:

        print(
            "DASHBOARD DATABASE ERROR:",
            str(e)
        )

        return {
            "history": [],
            "total_images": 0,
            "real_count": 0,
            "fake_count": 0,
            "error": "Database Error: " + str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# RENDER DASHBOARD
# =========================================================

def render_dashboard(
    error=None,
    result=None,
    confidence=None,
    image=None
):

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    data = get_dashboard_data(
        session["user_id"]
    )

    # -----------------------------------------------------
    # SESSION RESULT
    # -----------------------------------------------------

    if result is None:

        result = session.get(
            "last_result"
        )

    if confidence is None:

        confidence = session.get(
            "last_confidence"
        )

    if image is None:

        image = session.get(
            "last_image"
        )

    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    final_error = error

    if not final_error:

        final_error = data.get(
            "error"
        )

    return render_template(
        "dashboard.html",

        fullname=session.get(
            "fullname",
            ""
        ),

        email=session.get(
            "email",
            ""
        ),

        result=result,

        confidence=confidence,

        image=image,

        history=data["history"],

        total_images=data["total_images"],

        real_count=data["real_count"],

        fake_count=data["fake_count"],

        error=final_error
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# SIGN UP
# =========================================================

@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if request.method == "POST":

        fullname = request.form.get(
            "fullname",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

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

            cursor.execute(
                """
                SELECT id
                FROM public.truthlens_users
                WHERE LOWER(TRIM(email)) =
                      LOWER(TRIM(%s))
                LIMIT 1
                """,
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                return render_template(
                    "signup.html",
                    error="Email already registered!"
                )

            cursor.execute(
                """
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
                """,
                (
                    fullname,
                    email,
                    password
                )
            )

            conn.commit()

            return render_template(
                "signup.html",
                success="Sign Up Successful!"
            )

        except Exception as e:

            if conn:
                conn.rollback()

            print(
                "SIGNUP ERROR:",
                str(e)
            )

            return render_template(
                "signup.html",
                error="Database Error: " + str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    return render_template(
        "signup.html"
    )


# =========================================================
# CREATE ACCOUNT
# =========================================================

@app.route(
    "/create-account",
    methods=["GET", "POST"]
)
def create_account():

    if request.method == "POST":

        fullname = request.form.get(
            "fullname",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        dob = request.form.get(
            "dob",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not fullname or not email or not password:

            return render_template(
                "create_account.html",
                error="Please fill all required fields!"
            )

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

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id
                FROM public.truthlens_users
                WHERE LOWER(TRIM(email)) =
                      LOWER(TRIM(%s))
                LIMIT 1
                """,
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                return render_template(
                    "create_account.html",
                    error="Email already registered!"
                )

            phone_value = phone if phone else None
            dob_value = dob if dob else None

            cursor.execute(
                """
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
                """,
                (
                    fullname,
                    email,
                    phone_value,
                    dob_value,
                    password
                )
            )

            conn.commit()

            return render_template(
                "create_account.html",
                success="Account Created Successfully!"
            )

        except Exception as e:

            if conn:
                conn.rollback()

            print(
                "CREATE ACCOUNT ERROR:",
                str(e)
            )

            return render_template(
                "create_account.html",
                error="Database Error: " + str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    return render_template(
        "create_account.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["POST"]
)
def login():

    email = request.form.get(
        "email",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    ).strip()

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

        cursor.execute(
            """
            SELECT
                id,
                fullname,
                email,
                password
            FROM public.truthlens_users
            WHERE LOWER(TRIM(email)) =
                  LOWER(TRIM(%s))
            LIMIT 1
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            return render_template(
                "index.html",
                error="Email not registered!"
            )

        stored_password = str(
            user[3]
        ).strip()

        entered_password = str(
            password
        ).strip()

        if stored_password != entered_password:

            return render_template(
                "index.html",
                error="Incorrect password!"
            )

        # -------------------------------------------------
        # LOGIN SUCCESS
        # -------------------------------------------------

        session.clear()

        session["user_id"] = user[0]
        session["fullname"] = user[1]
        session["email"] = user[2]
        session.permanent = True

        print("LOGIN SUCCESS")
        print("USER ID:", session["user_id"])
        print("FULLNAME:", session["fullname"])

        return redirect(
            url_for("dashboard")
        )

    except Exception as e:

        print(
            "LOGIN ERROR:",
            str(e)
        )

        return render_template(
            "index.html",
            error="Database Error: " + str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    return render_dashboard()


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

        fullname=session.get(
            "fullname",
            ""
        ),

        email=session.get(
            "email",
            ""
        )
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
# IMAGE PREDICTION
# =========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    if "user_id" not in session:

        return redirect(
            url_for("home")
        )

    # -----------------------------------------------------
    # CHECK IMAGE
    # -----------------------------------------------------

    if "image" not in request.files:

        return render_dashboard(
            error="Please select an image!"
        )

    file = request.files["image"]

    if file.filename == "":

        return render_dashboard(
            error="No image selected!"
        )

    # -----------------------------------------------------
    # SECURE FILE NAME
    # -----------------------------------------------------

    original_filename = secure_filename(
        file.filename
    )

    if not original_filename:

        return render_dashboard(
            error="Invalid image filename!"
        )

    # -----------------------------------------------------
    # UNIQUE FILE NAME
    # -----------------------------------------------------

    file_extension = os.path.splitext(
        original_filename
    )[1]

    safe_filename = (
        str(uuid.uuid4())
        + file_extension
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        safe_filename
    )

    # -----------------------------------------------------
    # SAVE IMAGE
    # -----------------------------------------------------

    try:

        file.save(
            filepath
        )

    except Exception as e:

        print(
            "IMAGE UPLOAD ERROR:",
            str(e)
        )

        return render_dashboard(
            error="Image Upload Error: " + str(e)
        )

    # -----------------------------------------------------
    # AI PREDICTION
    # -----------------------------------------------------

    try:

        result, confidence = predict_image(
            filepath
        )

        confidence = float(
            confidence
        )

    except Exception as e:

        print(
            "PREDICTION ERROR:",
            str(e)
        )

        return render_dashboard(
            error="Prediction Error: " + str(e)
        )

    # -----------------------------------------------------
    # SAVE HISTORY
    # -----------------------------------------------------

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
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
            """,
            (
                session["user_id"],
                safe_filename,
                result,
                confidence
            )
        )

        conn.commit()

    except Exception as e:

        if conn:
            conn.rollback()

        print(
            "HISTORY DATABASE ERROR:",
            str(e)
        )

        return render_dashboard(
            error="History Database Error: " + str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    # -----------------------------------------------------
    # SAVE LAST RESULT
    # -----------------------------------------------------

    session["last_image"] = safe_filename

    session["last_result"] = result

    session["last_confidence"] = confidence

    # -----------------------------------------------------
    # SHOW DASHBOARD
    # -----------------------------------------------------

    return render_dashboard(
        result=result,
        confidence=confidence,
        image=safe_filename
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

    image_name = session.get(
        "last_image"
    )

    result = session.get(
        "last_result"
    )

    confidence = session.get(
        "last_confidence"
    )

    print("========================================")
    print("PDF DOWNLOAD REQUEST")
    print("USER ID:", session.get("user_id"))
    print("IMAGE:", image_name)
    print("RESULT:", result)
    print("CONFIDENCE:", confidence)
    print("========================================")

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not image_name:

        return (
            "Image data not found. "
            "Please upload and predict again.",
            400
        )

    if not result:

        return (
            "Prediction result not found. "
            "Please predict again.",
            400
        )

    if confidence is None:

        return (
            "Confidence data not found. "
            "Please predict again.",
            400
        )

    # -----------------------------------------------------
    # CREATE PDF
    # -----------------------------------------------------

    try:

        pdf_file = create_pdf(
            image_name,
            result,
            confidence
        )

        print(
            "PDF FILE CREATED:",
            pdf_file
        )

        # -------------------------------------------------
        # CHECK PDF
        # -------------------------------------------------

        if not pdf_file:

            return (
                "PDF file path is empty.",
                500
            )

        if not os.path.exists(pdf_file):

            print(
                "PDF FILE DOES NOT EXIST:",
                pdf_file
            )

            return (
                "PDF file was not created.",
                500
            )

        # -------------------------------------------------
        # SEND PDF
        # -------------------------------------------------

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name="TruthLens_AI_Report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:

        print(
            "PDF DOWNLOAD ERROR:",
            repr(e)
        )

        return (
            f"PDF Error: {str(e)}",
            500
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

        cursor.execute(
            """
            SELECT
                current_user,
                current_database()
            """
        )

        info = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM public.truthlens_users
            """
        )

        user_count = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM public.truthlens_history
            """
        )

        history_count = cursor.fetchone()[0]

        return f"""
        <html>

        <head>

            <title>
                TruthLens Database Test
            </title>

            <style>

                body {{
                    font-family: Arial;
                    background: #111827;
                    color: white;
                    padding: 50px;
                }}

                .box {{
                    max-width: 700px;
                    margin: auto;
                    background: #1f2937;
                    padding: 35px;
                    border-radius: 15px;
                }}

                h2 {{
                    color: #22c55e;
                }}

                .value {{
                    color: #60a5fa;
                    font-weight: bold;
                }}

            </style>

        </head>

        <body>

            <div class="box">

                <h2>
                    Database Test Successful
                </h2>

                <p>
                    Database User:
                    <span class="value">
                        {info[0]}
                    </span>
                </p>

                <p>
                    Database:
                    <span class="value">
                        {info[1]}
                    </span>
                </p>

                <p>
                    Users:
                    <span class="value">
                        {user_count}
                    </span>
                </p>

                <p>
                    History Records:
                    <span class="value">
                        {history_count}
                    </span>
                </p>

            </div>

        </body>

        </html>
        """

    except Exception as e:

        return f"""
        <h2>
            Database Error
        </h2>

        <pre>
{e}
        </pre>
        """

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        debug=False,
        host="0.0.0.0",
        port=port
    )