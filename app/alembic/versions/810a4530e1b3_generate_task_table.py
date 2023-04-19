"""generate task table

Revision ID: 810a4530e1b3
Revises: a2df7e9765d2
Create Date: 2023-04-19 11:19:34.611267

"""
from alembic import op
import sqlalchemy as sa

from schemas.task import TaskStatus

# revision identifiers, used by Alembic.
revision = '810a4530e1b3'
down_revision = 'a2df7e9765d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('user_id', sa.UUID, nullable=False),
        sa.Column('summary', sa.String),
        sa.Column('description', sa.String),
        sa.Column('status', sa.Enum(TaskStatus),
                  nullable=False, default=TaskStatus.NEW),
        sa.Column('priority', sa.Numeric, nullable=False, default=1)
    )
    op.create_foreign_key('fk_task_user', 'tasks',
                          'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table('tasks')
    # op.execute('DROP TYPE taskstatus;')
