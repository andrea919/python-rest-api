import time
import os
from app import create_app
from db import db

app = create_app()

with app.app_context():
    max_retries = 5
    for i in range(max_retries):
        try:
            db.session.execute("SELECT 1")
            print("Database connection successful, tables may already exist.")
            break
        except Exception as e:
            print(f"Attempt {i+1}/{max_retries}: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else: 
                # In case it can't connect after 5 tries
                try:
                    db.create_all()
                    print("Database tables created successfully!")
                except Exception as create_error:
                    print(f"Could not create tables: {create_error}")