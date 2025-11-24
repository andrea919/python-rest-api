# Stores REST API — First Version

This is the first version of a REST API built with **Flask**, featuring:
- User authentication (JWT + refresh tokens)
- Revoked token system
- Stores, items, and tags management
- Database migrations (Flask-Migrate)
- OpenAPI/Swagger documentation
- Marshmallow schemas and Flask-Smorest blueprints

The project started from a course, but I expanded it by adding features like:
- A database table for revoked tokens
- Additional validations and structure improvements

More updates will be added over time, including a simple frontend.

---

## Quick Start

```bash
git clone <your-repo-url>
cd PythonApi
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings (see Environment Setup below)
flask db upgrade
flask run

---

## Environment Setup

**Before running the application, you must set up your environment variables:**

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
2. **Edit the .env file with your configuration:**
    DATABASE_URL=sqlite:///data.db
    SECRET_KEY=your-secret-key-here
    JWT_SECRET_KEY=your-jwt-secret-key-here
    FLASK_ENV=development