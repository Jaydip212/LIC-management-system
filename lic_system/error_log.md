# Resolved Errors Log - LIC Management System

This document logs the technical issues encountered and resolved during the project setup and deployment.

### 1. Configuration Type Inconsistency
- **Error**: Potential linter warnings and runtime issues due to inconsistent types for `SECRET_KEY` and `MYSQL_CA_PATH` in `config.py`.
- **Resolution**: Ensured `Config` and `ProductionConfig` use consistent string types and default values.

### 2. Missing Dependencies / IDE Sync Issues
- **Error**: IDE reported missing imports for `flask`, `pymysql`, `bcrypt`, etc.
- **Resolution**: Verified installations in the virtual environment and system Python. Updated `extensions.py` to trigger a re-parse.

### 3. Database Authentication Error (Access Denied)
- **Error**: `pymysql.err.OperationalError: (1045, "Access denied for user 'avnadmin'@'...'")`.
- **Resolution**: Created a `.env` file with the correct Aiven MySQL credentials provided by the user.

### 4. SSL Certificate Corruption
- **Error**: `ssl.SSLError: [X509] PEM lib (_ssl.c:4411)` when connecting to Aiven.
- **Resolution**: Identified illegal characters (`^e-`) in the `ca.pem` base64 string. Replaced it with a clean certificate provided by the user.

### 5. Environment Variable Precedence
- **Error**: App was defaulting to `localhost/root` even with `.env` present.
- **Resolution**: Moved `load_dotenv()` call in `app.py` to the very top, before the `config` module is imported.

### 6. Vercel TemplateNotFound Conflict
- **Error**: `jinja2.exceptions.TemplateNotFound: public/index.html` on Vercel.
- **Resolution**: Renamed `templates/public` to `templates/main_site` to avoid Vercel's special handling of the `public/` directory name. Updated all routing and template `extends`/`include` references.

### 7. Vercel Entry Point
- **Error**: Deployment issues or path resolution errors on Vercel.
- **Resolution**: Created `index.py` as a standardized entry point for Vercel's `@vercel/python` builder.
