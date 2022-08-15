import datetime
from database.database import db


class Posts(db.Model):
    __tablename__ = "blog.posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String)
    body = db.Column(db.String)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    def __init__(self, author, title, body):
        now = datetime.datetime.now()
        self.author = author
        self.title = title
        self.body = body
        self.date = now.strftime('%m%d%Y')
        self.time = now.strftime('%X')


class Comments(db.Model):
    __tablename__ = "blog.comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    author = db.Column(db.Integer)
    body = db.Column(db.String)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    def __init__(self, post_id, author, body):
        now = datetime.datetime.now()
        self.post_id = post_id  # the id of the post that the comment is applied to
        self.author = author
        self.body = body
        self.date = now.strftime('%m%d%Y')
        self.time = now.strftime('%X')
