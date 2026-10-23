
import os
import hashlib
import secrets
from pathlib import Path

from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    session,
    send_file
)
from werkzeug.utils import secure_filename
from markupsafe import escape

from models import db, User, Document, AuditLog


# --------------------------------------------------
# Application setup
# --------------------------------------------------

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("Set the SECRET_KEY environment variable before starting TrustVault.")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trustvault.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = Path(app.instance_path) / "private_uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    return """
    <h1>Welcome to TrustVault</h1>
    <p>Secure Document Sharing Platform</p>
    <a href="/register">Register</a> |
    <a href="/login">Login</a>
    """


# --------------------------------------------------
# Registration
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or len(password) < 8:
            return (
                "Enter a name, email, and password of at least 8 characters.",
                400
            )

        if User.query.filter_by(email=email).first():
            return "An account with this email already exists.", 409

        user = User(name=name, email=email, role="user")
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))

        return "Invalid email or password.", 401

    return render_template("login.html")


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return redirect(url_for("login"))

    safe_name = escape(user.name)
    safe_role = escape(user.role)

    admin_link = ""
    if user.role == "admin":
        admin_link = '<p><a href="/admin/audit-logs">View Audit Logs</a></p>'

    return f"""
    <h1>TrustVault Dashboard</h1>
    <p>Welcome, {safe_name}!</p>
    <p>Your role: {safe_role}</p>
    <p><a href="/upload">Upload a Document</a></p>
    <p><a href="/my-documents">My Documents</a></p>
    {admin_link}
    <form method="POST" action="/logout">
        <button type="submit">Logout</button>
    </form>
    """


# --------------------------------------------------
# Upload document and record audit event
# --------------------------------------------------

@app.route("/upload", methods=["GET", "POST"])
def upload():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return redirect(url_for("login"))

    if request.method == "POST":
        uploaded_file = request.files.get("document")

        if not uploaded_file or not uploaded_file.filename:
            return "Please choose a file.", 400

        original_filename = secure_filename(uploaded_file.filename)

        if not original_filename:
            return "Invalid filename.", 400

        file_data = uploaded_file.read(5 * 1024 * 1024 + 1)

        if not file_data:
            return "The file is empty.", 400

        if len(file_data) > 5 * 1024 * 1024:
            return "File is too large. Maximum size is 5 MB.", 413

        stored_name = secrets.token_hex(16)
        file_path = UPLOAD_FOLDER / stored_name

        try:
            file_hash = hashlib.sha256(file_data).hexdigest()

            with open(file_path, "xb") as saved_file:
                saved_file.write(file_data)

            document = Document(
                filename=original_filename,
                stored_name=stored_name,
                sha256_hash=file_hash,
                owner_id=user_id
            )

            db.session.add(document)
            db.session.flush()

            audit = AuditLog(
                user_id=user_id,
                action="UPLOAD",
                document_id=document.id,
                details="Document uploaded successfully"
            )

            db.session.add(audit)
            db.session.commit()

        except Exception:
            db.session.rollback()

            if file_path.exists():
                file_path.unlink()

            app.logger.exception("Document upload failed")
            return "Upload failed. Please try again.", 500

        return redirect(url_for("my_documents"))

    return render_template("upload.html")


# --------------------------------------------------
# List only the logged-in user's documents
# --------------------------------------------------

@app.route("/my-documents")
def my_documents():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return redirect(url_for("login"))

    documents = (
        Document.query
        .filter_by(owner_id=user_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    rows = "".join(
        (
            f"<li>Document ID: {doc.id} | "
            f"{escape(doc.filename)} — "
            f"SHA-256: {doc.sha256_hash} "
            f'<a href="/download/{doc.id}">Download</a></li>'
        )
        for doc in documents
    )

    return f"""
    <h1>My Documents</h1>
    <ul>{rows or '<li>No documents uploaded yet.</li>'}</ul>
    <p><a href="/upload">Upload another document</a></p>
    <p><a href="/dashboard">Back to Dashboard</a></p>
    """


# --------------------------------------------------
# Download with ownership and integrity checks
# --------------------------------------------------

@app.route("/download/<int:document_id>")
def download_document(document_id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return redirect(url_for("login"))

    document = Document.query.filter_by(
        id=document_id,
        owner_id=user_id
    ).first()

    if not document:
        return "Document not found.", 404

    file_path = UPLOAD_FOLDER / document.stored_name

    if not file_path.is_file():
        return "Stored document is unavailable.", 404

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as stored_file:
        for chunk in iter(lambda: stored_file.read(8192), b""):
            sha256.update(chunk)

    if sha256.hexdigest() != document.sha256_hash:
        app.logger.error(
            "Integrity check failed for document ID %s",
            document.id
        )
        return "Document integrity check failed.", 409

    audit = AuditLog(
        user_id=user_id,
        action="DOWNLOAD",
        document_id=document.id,
        details="Document download requested after integrity check"
    )

    try:
        db.session.add(audit)
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Download audit logging failed")
        return "Download could not be completed. Please try again.", 500

    return send_file(
        file_path,
        as_attachment=True,
        download_name=document.filename
    )


# --------------------------------------------------
# Admin-only audit logs
# --------------------------------------------------

@app.route("/admin/audit-logs")
def admin_audit_logs():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if not user or user.role != "admin":
        return "Access denied: Admins only.", 403

    logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).all()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TrustVault Audit Logs</title>
    </head>
    <body>
        <h1>TrustVault Audit Logs</h1>
        <p>Administrator access only</p>

        <table border="1" cellpadding="8">
            <tr>
                <th>Log ID</th>
                <th>User ID</th>
                <th>Action</th>
                <th>Document ID</th>
                <th>Timestamp</th>
                <th>Details</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ log.id }}</td>
                <td>{{ log.user_id }}</td>
                <td>{{ log.action }}</td>
                <td>{{ log.document_id or "-" }}</td>
                <td>{{ log.timestamp }}</td>
                <td>{{ log.details or "-" }}</td>
            </tr>
            {% endfor %}
        </table>

        <p><a href="{{ url_for('dashboard') }}">Back to Dashboard</a></p>
    </body>
    </html>
    """, logs=logs)


# --------------------------------------------------
# Logout
# --------------------------------------------------

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


# --------------------------------------------------
# File-size error
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):
    return "File is too large. Maximum size is 5 MB.", 413


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
