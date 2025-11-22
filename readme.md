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

## ▶️ Quick Start

```bash
pip install -r requirements.txt
flask db upgrade
flask run
