#!/bin/sh

# Run database initialization
python init_db.py

# Run migrations
flask db upgrade

# Start the app
exec gunicorn --bind 0.0.0.0:80 "app:create_app()"