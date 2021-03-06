from sqlalchemy.sql.schema import ForeignKey
from db_connect import db
from datetime import datetime, date, timedelta
from pytz import timezone

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
    stock = db.Column(db.Integer, default=2)
    rating_avg = db.Column(db.Integer, default=0)

    rented = db.relationship("Rent", backref='books_tb')
    commented = db.relationship("Comment", backref='books_tb')

    def __init__(self, book_name, publisher, author, publication_date, pages, isbn, description, link, img_path):
        self.book_name = book_name
        self.publisher = publisher
        self.author = author
        self.publication_date = publication_date
        self.pages = pages
        self.isbn = isbn
        self.description = description
        self.link = link
        self.img_path = img_path


class User(db.Model):
    __tablename__ = 'user_tb'
    _id = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    pw = db.Column(db.String(200), nullable=False)

    renter = db.relationship("Rent", backref='user_tb')
    commenter = db.relationship("Comment", backref='user_tb')

    def __init__(self, user_name, user_email, user_pw):
        self.name = user_name
        self.email = user_email
        self.pw = user_pw


class Rent(db.Model):
    __tablename__='rent_tb'
    _id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_tb._id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books_tb._id'), nullable=False)
    rent_date = db.Column(db.Date, default=datetime.now(timezone('Asia/Seoul')).date)
    due_date = db.Column(db.Date, default=datetime.now(timezone('Asia/Seoul')).date()+timedelta(days=14))
    return_date = db.Column(db.Date)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id


class Comment(db.Model):
    __tablename__='comment_tb'
    # 1. ????????? 2. ???id 3. ?????? 4. ?????? 5. ?????????
    _id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_tb._id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books_tb._id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Seoul')))

    def __init__(self, user_id, book_id, comment, star_rating):
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        self.star_rating = star_rating

