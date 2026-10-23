# TrustVault — Secure Document Sharing

## 1. Project Overview

TrustVault is a web application built using Python and Flask to support secure document sharing. It allows registered users to upload and download their own documents while maintaining an audit trail of document activities.

The project focuses on authentication, access control, document integrity, and accountability.

## 2. Problem Statement

Organizations frequently share confidential documents such as contracts, employee records, and business reports. Unauthorized access, document tampering, and a lack of activity records can create serious security risks.

TrustVault aims to address these challenges through user authentication, document access restrictions, SHA-256 integrity verification, and audit logging.

## 3. Features

- User registration and login
- Password hashing using Werkzeug
- Document upload and download
- Private local file storage
- SHA-256 document integrity verification
- User-specific document access restrictions
- Audit records for document uploads and downloads
- Administrator-only audit log access
- Maximum upload size of 5 MB
- SQLite database for application data

## 4. Technologies Used

- Python 3.11
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- Werkzeug password hashing
- SHA-256 hashing
- Pytest for automated testing

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

**Note:** The `instance/` directory may be created locally when the application runs. Local database files and uploaded documents contain application data and should not be committed to the public repository.

## 6. Installation and Setup

### Prerequisites

- Python 3.11 or a compatible Python version
- pip
- Git
- Visual Studio Code or another code editor

### Step 1: Clone the Repository

```bash
git clone https://github.com/Alla-Poojitha/TrustVault.git
cd TrustVault
```

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure the Secret Key

The application requires a `SECRET_KEY` environment variable. Generate a strong, random secret key and configure it in your local environment.

For Windows PowerShell, you can generate a key with Python:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value locally and set it for your current PowerShell session:

```powershell
$env:SECRET_KEY = "paste-your-generated-secret-here"
```

Replace the example text with your generated key. Never commit your real secret key to GitHub or share it publicly.

### Step 5: Run the Application

```powershell
python app.py
```

Open the application in your browser:

http://127.0.0.1:5000/

This address is for local development on your computer. It is not a public deployment URL.

## 7. How to Test the Application

Follow these steps to perform a basic manual test:

1. Start the Flask application.
2. Register a test user.
3. Log in using the registered account.
4. Upload a small test document.
5. Open the document list and confirm that the uploaded document appears.
6. Download the document and check whether the integrity verification succeeds.
7. Attempt to access `/admin/audit-logs` as a normal user. The expected result is HTTP 403 if the route and authorization check are configured as described.
8. Using an appropriately configured administrator account, check whether upload and download audit records are displayed.

Use only test documents and test accounts during development.

## 8. Automated Tests

The project includes a `tests/` directory for automated tests.

Install the project dependencies, activate the virtual environment, configure `SECRET_KEY`, and run:

```powershell
python -m pytest -q
```

Review the test output to confirm which tests pass or fail. Passing tests provide evidence only for the cases they cover; they do not establish that the application is completely secure.

## 9. Security Features

### Authentication

The application supports user registration and login. Passwords are hashed using Werkzeug password-hashing utilities rather than being stored as plain text.

### Access Control

Protected functionality checks the logged-in user. Document access is intended to be restricted to the document owner, while administrator audit-log access is restricted by role.

### Document Integrity

TrustVault calculates a SHA-256 hash for uploaded documents and compares it during download to detect unexpected changes to stored files.

### Audit Logging

The application records document upload and download activity, including relevant user and document references and timestamps.

### Private File Storage

Uploaded documents are stored locally rather than being served directly from a public static directory. Access should be provided only through authorized application routes.

## 10. Threat Modeling

`THREATS.md` documents relevant security threats, potential impacts, and mitigation approaches for the TrustVault prototype.

The threat model should be reviewed alongside the source code and updated whenever security controls or application behavior change.

## 11. AI Assistance and Development Notes

`PROMPTS.md` records prompts used during development and the related development work.

Any commit references or descriptions should correspond to actual work performed in the repository. AI-assisted code should be reviewed, tested, and understood by the project author.

## 12. Security Limitations and Future Improvements

TrustVault is a development prototype and is **not production-ready**.

Further work is needed to implement and verify:

- CSRF protection for state-changing requests
- Secure production configuration and session-cookie settings
- Rate limiting and stronger authentication protections
- Comprehensive automated security tests
- Robust organization-level tenant isolation and authorized document sharing
- Stronger file validation and upload security controls
- Production deployment using HTTPS
- Persistent storage, backups, monitoring, and secure operational practices

The current application uses a local SQLite database and local file storage. A local development setup should not be treated as proof of production security.

## 13. Project Status

The project implements core registration, login, document upload and download, SHA-256 integrity checking, and administrator audit-log functionality.

Automated test coverage, additional security hardening, deployment, and operational safeguards should be evaluated separately. Features and tests should be described as complete only after verifying them in the current repository.

## 14. Author

**Alla Poojitha**

GitHub: https://github.com/Alla-Poojitha/TrustVault
