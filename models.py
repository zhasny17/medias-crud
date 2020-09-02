from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
import hashlib

db = SQLAlchemy()
migrate = Migrate(db=db)

tables_config = {
    'mysql_charset': 'utf8mb4',
}


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __table_args__ = (
        tables_config
    )
    __tablename__ = 'users'

    @staticmethod
    def hash_password(password):
        if not password:
            return None
        return hashlib.sha256(password.encode()).hexdigest()

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True))
    removed_at = db.Column(db.DateTime(timezone=True))
    removed = db.Column(db.Boolean, nullable=False, default=False)
