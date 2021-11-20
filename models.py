from typing_extensions import ParamSpecArgs

from sqlalchemy.sql.schema import ForeignKey
from db_connect import db
from datetime import *

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
    img_path = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=1)

    rented = db.relationship("Rent", backref='books_tb')


class User(db.Model):
    __tablename__ = 'user_tb'
    _id = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    pw = db.Column(db.String(200), nullable=False)

    renter = db.relationship("Rent", backref='user_tb')

    def __init__(self, user_name, user_email, user_pw):
        self.name = user_name
        self.email = user_email
        self.pw = user_pw


class Rent(db.Model):
    __tablename__='rent_tb'
    _id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_tb._id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books_tb._id'), nullable=False)
    rent_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, default=date.today()+timedelta(days=14))
    # return_date = db.Column(db.Date)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
