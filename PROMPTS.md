# TrustVault — AI Prompt Log

This file records AI assistance used during TrustVault development. The entries below should reflect actual prompts and work performed. Commit links must be added after the corresponding changes have been committed to the public GitHub repository.

## Prompt 1 — Flask Application Setup

**Date:** 2026-10-22

**Purpose:** Create the initial Flask application structure and configure the database.

**Prompt used:** "Help me build the TrustVault secure document-sharing project from scratch using Python and Flask. Guide me step by step and prepare the required source code and documentation."

**Outcome:** Created the initial application structure and database models.

**Related commit:** TODO — add the actual Git commit URL.

## Prompt 2 — Authentication

**Date:** 2026-10-22

**Purpose:** Implement user registration and login.

**Prompt used:** "Help me implement user registration and login in Flask using securely hashed passwords and session-based authentication."

**Outcome:** Implemented registration, password hashing, login, and session handling.

**Related commit:** TODO — add the actual Git commit URL.

## Prompt 3 — Document Access Control

**Date:** 2026-10-23

**Purpose:** Restrict document access to authorized users.

**Prompt used:** "Help me implement document upload and download in Flask, ensuring that users can access only their own documents and that uploaded files are stored privately."

**Outcome:** Implemented document upload, private file storage, and basic owner checks for document access.

**Related commit:** TODO — add the actual Git commit URL.

## Prompt 4 — Document Integrity and Audit Logging

**Date:** 2026-10-23

**Purpose:** Detect unexpected document changes and record document activity.

**Prompt used:** "Help me implement SHA-256 document integrity verification and audit logs for document uploads and downloads in my Flask TrustVault project."

**Outcome:** Implemented SHA-256 verification and basic upload/download audit records. The audit-log page was manually checked.

**Related commit:** TODO — add the actual Git commit URL.

## Prompt 5 — Administrator-Only Audit Logs

**Date:** 2026-10-23

**Purpose:** Restrict audit-log access to administrators.

**Prompt used:** "Help me restrict the TrustVault audit-log page to administrators and test that normal users receive a 403 response."

**Outcome:** Implemented an administrator role check and manually verified that a normal user was denied access to the audit-log page.

**Related commit:** TODO — add the actual Git commit URL.

## Prompt 6 — Security Documentation

**Date:** 2026-10-23

**Purpose:** Document security risks and mitigations.

**Prompt used:** "Help me create a threat model for TrustVault that identifies security risks, their impact, implemented mitigations, and outstanding security work."

**Outcome:** Created the initial threat-model documentation in THREATS.md.

**Related commit:** TODO — add the actual Git commit URL.

## Notes

- These entries are a draft based on the development work described in the project conversation. Review the dates, wording, and outcomes so they accurately represent your work.
- Replace every TODO with a real commit URL after committing the corresponding changes.
- Do not invent commit hashes, repository URLs, or claim that unimplemented security controls are complete.
- Continue updating this file when additional AI-assisted development work is performed.
