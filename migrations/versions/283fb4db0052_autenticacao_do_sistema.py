"""autenticacao do sistema

Revision ID: 283fb4db0052
Revises: 0f44243b2485
Create Date: 2020-09-02 14:26:15.171158

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '283fb4db0052'
down_revision = '0f44243b2485'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=datetime.utcnow),
        sa.Column('valid', sa.Boolean, nullable=False, default=True),
        sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        mysql_charset='utf8mb4',
    )

    op.create_table(
        'access_tokens',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=datetime.utcnow),
        sa.Column('valid', sa.Boolean, nullable=False, default=True),
        sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('refresh_token_id', sa.String(36), sa.ForeignKey('refresh_tokens.id'), nullable=False),
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('access_tokens')
    op.drop_table('refresh_tokens')
