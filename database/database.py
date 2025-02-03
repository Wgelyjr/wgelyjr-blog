import hashlib
from flask_sqlalchemy import SQLAlchemy
from config import Config
db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    db.create_all()
    if User.query.count() == 0:

            # Create the admin user
            admin_user = User(
                name="admin",
                email="admin@admin.admin",
                password=hashlib.md5("admin".encode(encoding='UTF-8', errors='strict') + Config.SECRET_KEY.encode()).digest()
            )
            db.session.add(admin_user)
            db.session.commit()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.BLOB)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
