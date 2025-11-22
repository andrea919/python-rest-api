from __future__ import with_statement

import logging
from logging.config import fileConfig
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import your app and db
from app import create_app
from db import db

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

app = create_app()

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=db.metadata,
        literal_binds=True,
        compare_type=True,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    with app.app_context():
        # Get the database URL from app config
        configuration = config.get_section(config.config_ini_section)
        configuration['sqlalchemy.url'] = app.config['SQLALCHEMY_DATABASE_URI']
        
        connectable = engine_from_config(
            configuration,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=db.metadata,
                compare_type=True,
                render_as_batch=True
            )

            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()