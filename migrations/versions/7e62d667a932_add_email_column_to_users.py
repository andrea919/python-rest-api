"""Add email column to users

Revision ID: 7e62d667a932
Revises: 973b4a285c70
Create Date: 2025-12-02 11:20:19.162661
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e62d667a932"
down_revision = "973b4a285c70"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("email", sa.String(), nullable=True),
    )

    op.create_unique_constraint(
        "uq_users_email",  
        "users",           
        ["email"],         
    )

    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(),
        nullable=False,
    )


def downgrade():
    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique",
    )
    op.drop_column("users", "email")
