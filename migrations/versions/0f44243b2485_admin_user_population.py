"""admin user population

Revision ID: 0f44243b2485
Revises: 
Create Date: 2020-09-02 12:34:17.540951

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
import uuid


# revision identifiers, used by Alembic.
revision = '0f44243b2485'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    users_table = op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(150), unique=True, nullable=False),
        sa.Column('username', sa.String(150), nullable=False),
        sa.Column('password', sa.String(150), nullable=False),
        sa.Column('admin', sa.Boolean, nullable=False, default=False),
        sa.Column('active', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('removed_at', sa.DateTime(timezone=True)),
        sa.Column('removed', sa.Boolean(), nullable=False, default=False),
        mysql_charset='utf8mb4',
    )

    op.bulk_insert(
        users_table,
        [
            {
                'id': str(uuid.uuid4()),
                'name': 'Lucas',
                'username': 'lucas',
                # qpalzm
                'password': '1c358e3d51968ace657b0f01d5eea55b7930ff3f45f75f1f9858ed1b8f9d0f83',
                'admin': True,
                'active': True,
                'created_at': datetime.utcnow(),
                'updated_at': None,
                'removed_at': None,
                'removed': False,
            }
        ]
    )



def downgrade():
    op.drop_table('users')
