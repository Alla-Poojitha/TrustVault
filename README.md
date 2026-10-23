# TrustVault — Secure Document Sharing

## 1. Project Overview

TrustVault is a web application developed using Python and Flask to support secure document sharing. It allows registered users to upload and download their own documents while recording document activity in an audit log.

The project focuses on authentication, access control, document integrity, and accountability.

## 2. Problem Statement

Organizations frequently share confidential documents such as contracts, employee records, and business reports. Unauthorized access, document tampering, and a lack of activity records can create security risks.

TrustVault aims to address these challenges through user authentication, document access restrictions, SHA-256 integrity verification, and audit logging.

## 3. Features

- User registration and login
- Password hashing
- Document upload and download
- Private local file storage
- SHA-256 document integrity verification
- Users can access their own documents
- Audit records for document uploads and downloads
- Administrator-only audit log access
- Maximum upload size of 5 MB

## 4. Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- Werkzeug password hashing
- SHA-256

## 5. Project Structure

```text
TrustVault/
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── THREATS.md
├── PROMPTS.md
├── tests/
├── templates/
└── instance/
    └── private_uploads/
```

Note: Some documentation and test files in this structure are planned and must be created before submission. Local database files and private uploads should not be published.

## 6. Installation and Setup

### Prerequisites

- Python 3.11 or a compatible Python version
- pip
- Visual Studio Code or another code editor

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TrustVault
```

Replace the placeholder with the actual repository URL.

### Step 2: Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure the Secret Key

Set a strong, randomly generated `SECRET_KEY` environment variable. Never publish real secret keys in the repository.

### Step 5: Start the Application

```powershell
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000/

## 7. How to Test the Application

1. Register a test user.
2. Log in with the registered account.
3. Upload a small test document.
4. Open My Documents.
5. Download the uploaded document and verify that the integrity check succeeds.
6. Attempt to access `/admin/audit-logs` as a normal user. The expected result is HTTP 403.
7. Log in as an administrator and verify that upload and download audit records are displayed.

## 8. Security Features

### Authentication

Passwords are hashed using Werkzeug password-hashing utilities instead of being stored as plain text.

### Access Control

The application checks the logged-in user before allowing access to protected pages. Administrator audit logs are restricted to accounts with the administrator role.

### Document Integrity

TrustVault calculates a SHA-256 hash when a document is uploaded and compares the hash during download to detect unexpected file changes.

### Audit Logging

The application records document upload and download events with user and document references and timestamps.

## 9. Security Limitations

TrustVault is currently a development prototype and is not production-ready.

Further work is required to implement and verify:

- CSRF protection
- Secure production configuration and session-cookie settings
- Rate limiting and stronger authentication protections
- Comprehensive automated security tests
- Organization-level tenant isolation and secure document sharing between authorized users
- Production deployment, persistent storage, backups, and monitoring

The current application uses a local SQLite database and local file storage.

## 10. Project Status

The core registration, login, document upload and download, SHA-256 integrity checking, and administrator audit-log features have been implemented and manually tested.

Additional security hardening, automated testing, documentation, and deployment remain part of the project work.

## Author
Alla Poojitha
