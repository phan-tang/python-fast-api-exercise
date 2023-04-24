"""generate company table

Revision ID: 94346ea83991
Revises: 
Create Date: 2023-04-19 11:19:19.443355

"""
from alembic import op
import sqlalchemy as sa

from schemas import CompanyMode

# revision identifiers, used by Alembic.
revision = '94346ea83991'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode),
                  nullable=False, default=CompanyMode.ACTIVE),
        sa.Column('rating', sa.Numeric),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('companies')
    op.execute('DROP TYPE companymode;')
