from typing_extensions import ParamSpecArgs
from db_connect import db
from datetime import datetime

class Books(db.Model):
    __tablename__ = 'books_tb'

    _id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_name = db.Column(db.String(40), nullable=False)
    publisher = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    publication_date = db.Column(db.Datetime.date, nullable=False)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.BigInteger)
    description = db.Column(db.Text)
    link = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
