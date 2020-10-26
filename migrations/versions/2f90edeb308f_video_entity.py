"""video entity

Revision ID: 2f90edeb308f
Revises: 283fb4db0052
Create Date: 2020-09-03 09:29:08.202420

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '2f90edeb308f'
down_revision = '283fb4db0052'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'videos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(512), nullable=False),
        sa.Column('url', sa.String(512), nullable=False),
        sa.Column('duration', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('removed_at', sa.DateTime(timezone=True)),
        sa.Column('removed', sa.Boolean(), nullable=False, default=False),
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('videos')
