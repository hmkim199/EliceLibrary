from typing_extensions import ParamSpecArgs
from db_connect import db
from datetime import date

class Books(db.Model):
    __tablename__ = 'books_tb'

    _id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_name = db.Column(db.String(40), nullable=False)
    publisher = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.BigInteger)
    description = db.Column(db.Text)
    link = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=1)


class User(db.Model):
    __tablename__ = 'user_tb'
    _id = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    pw = db.Column(db.String(200), nullable=False)

    def __init__(self, user_name, user_email, user_pw):
        self.name = user_name
        self.email = user_email
        self.pw = user_pw