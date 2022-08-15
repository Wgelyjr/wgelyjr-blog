from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc
import hashlib

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    db.create_all(app=app)
    with app.app_context():
        try:
            User.query.filter_by(name='sa').one()
        except sqlalchemy.exc.NoResultFound:
            superuser = User(name='sa', email='wgelyjr@gmail.com', password='ShenisMcGee69', role=0)
            db.session.add(superuser)
            db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.BLOB)
    role = db.Column(db.Integer)  # 0 is superuser, 1 is admin, 2 is operator, 3 is user

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        salt = 'Sally sells seashells by the seashore!'.encode(encoding='UTF-8', errors='strict')
        self.password = hashlib.md5(password.encode(encoding='UTF-8', errors='strict') + salt).digest()
        self.role = role
