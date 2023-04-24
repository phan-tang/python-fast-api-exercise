"""generate user table

Revision ID: a2df7e9765d2
Revises: 94346ea83991
Create Date: 2023-04-19 11:19:29.311605

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from uuid import uuid4

from schemas import get_password_hash
from config import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision = 'a2df7e9765d2'
down_revision = '94346ea83991'
branch_labels = None
depends_on = None


def upgrade() -> None:
    table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('company_id', sa.UUID),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(255), unique=True, nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=1),
        sa.Column('is_admin', sa.Boolean, default=0),
        sa.Column('is_superadmin', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_user_company', 'users',
                          'companies', ['company_id'], ['id'])

    op.bulk_insert(table, [
        {
            "id": uuid4(),
            "email": "superadmin@email.com",
            "username": "superadmin",
            "first_name": "Superadmin",
            "last_name": "System",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "is_active": True,
            "is_admin": False,
            "is_superadmin": True,
            "created_at": datetime.utcnow(),
        }
    ])


def downgrade() -> None:
    op.drop_table('users')
