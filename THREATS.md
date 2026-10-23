# TrustVault — Threat Model

## 1. Introduction

TrustVault is a Flask-based document-sharing application. It handles user accounts, uploaded documents, document integrity checks, and audit records.

This threat model identifies possible security risks, their impact, and the mitigations implemented or planned.

## 2. Assets to Protect

- User account credentials
- Uploaded confidential documents
- Document integrity
- User and document ownership information
- Audit records
- Application secret key
- Database and private file storage

## 3. Threats and Mitigations

### Threat 1: Unauthorized Access

**Risk:** An unauthenticated person attempts to access protected pages.

**Impact:** Private documents or application information could be exposed.

**Mitigation:** Require login for protected routes and verify the current user's session.

**Status:** Basic authentication checks are implemented. Additional automated tests are required.

### Threat 2: Privilege Escalation

**Risk:** A normal user attempts to access administrator-only audit logs.

**Impact:** Confidential activity records could be exposed.

**Mitigation:** Check the authenticated user's role on the server before returning audit logs.

**Status:** The administrator-only audit-log route has been manually tested; normal-user access was denied.

### Threat 3: Insecure Document Access

**Risk:** A user changes a document ID in a URL to access another user's file.

**Impact:** Confidential documents could be disclosed.

**Mitigation:** Verify document ownership or explicitly authorized sharing on every document access request.

**Status:** Basic owner checks are implemented. Broader access-control tests are still required.

### Threat 4: Document Tampering

**Risk:** A stored document is changed without authorization.

**Impact:** Users could receive altered or unreliable documents.

**Mitigation:** Calculate a SHA-256 hash at upload and compare it with the stored hash before download.

**Status:** Integrity verification is implemented. Additional tampering tests are required.

### Threat 5: Malicious File Upload

**Risk:** An attacker uploads a dangerous or unexpected file.

**Impact:** Malicious content could be stored or potentially abused.

**Mitigation:** Use safe server-generated storage names, restrict upload size, keep files outside public web directories, and validate allowed file types where appropriate.

**Status:** Secure storage names and a 5 MB size limit are implemented. File-type validation and malware scanning are not yet implemented.

### Threat 6: Password Attacks

**Risk:** Attackers guess passwords or repeatedly attempt to log in.

**Impact:** User accounts could be compromised.

**Mitigation:** Hash passwords securely, require reasonable password strength, and add login rate limiting and monitoring.

**Status:** Password hashing and a minimum password length are implemented. Rate limiting remains to be implemented.

### Threat 7: Cross-Site Request Forgery (CSRF)

**Risk:** A malicious website tricks an authenticated user into submitting an unwanted request.

**Impact:** Unauthorized actions could be performed using the user's session.

**Mitigation:** Add CSRF tokens to state-changing forms and validate them on the server.

**Status:** CSRF protection still needs to be implemented and tested.

### Threat 8: Secret Key Exposure

**Risk:** The Flask secret key is exposed or a weak development key is used in deployment.

**Impact:** Session security could be compromised.

**Mitigation:** Use a strong secret key supplied through environment configuration and never commit secrets to version control.

**Status:** Environment-variable configuration is supported, but the development fallback must be removed or rejected in production.

### Threat 9: Organization or Tenant Data Leakage

**Risk:** If multiple organizations use the application, one organization may access another organization's documents or records.

**Impact:** Confidential business information could be exposed.

**Mitigation:** Introduce organization identifiers and enforce tenant-scoped authorization on every relevant database query and file operation.

**Status:** Full organization-level tenant isolation is not yet implemented.

### Threat 10: Audit Log Manipulation

**Risk:** An unauthorized person attempts to change or delete audit records.

**Impact:** The record of document activity may become unreliable.

**Mitigation:** Restrict audit-log access, minimize modification permissions, and consider append-only or externally protected audit storage.

**Status:** Administrator-only viewing and basic event recording are implemented. Tamper-resistant audit storage is not yet implemented.

## 4. Security Testing Plan

The following tests should be performed:

1. Confirm unauthenticated users cannot access protected routes.
2. Confirm normal users cannot view administrator audit logs.
3. Confirm one user cannot download another user's document.
4. Modify a test document and confirm the integrity check rejects it.
5. Attempt to upload an oversized file.
6. Test invalid login attempts and password validation.
7. Verify that secret keys, database files, and private documents are excluded from the public repository.
8. Test CSRF protection after it is implemented.
9. Test organization-level isolation after tenant support is implemented.

## 5. Residual Risks

TrustVault is a development prototype, not a production-ready secure document platform. CSRF protection, tenant isolation, rate limiting, comprehensive automated tests, and tamper-resistant audit storage remain outstanding security tasks.

## 6. Conclusion

TrustVault implements several foundational security controls, including password hashing, owner checks, SHA-256 integrity verification, and administrator-only audit-log access. The remaining risks must be addressed and tested before production use.
