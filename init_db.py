import time
from sqlalchemy import text
from app import create_app
from db import db

app = create_app()

with app.app_context():
    max_retries = 5
    for i in range(max_retries):
        try:
            # Check if db answers
            db.session.execute(text("SELECT 1"))
            print("Database connection successful.")
            break
        except Exception as e:
            print(f"Attempt {i+1}/{max_retries}: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                print("Could not connect to the database after several attempts.")
                raise
