from flask import Flask, Blueprint, session, g, redirect, request, render_template, jsonify
from flask_bcrypt import Bcrypt
from models import *
from db_connect import db
from datetime import date
from sqlalchemy import func
import math

board = Blueprint('board', __name__)
bcrypt = Bcrypt()


@board.before_app_request
def load_logged_in_user():
    user_email = session.get('login')
    if login is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.email == user_email).first()


@board.route('/', defaults={'page': 0})
@board.route("/<int:page>")
def home(page):
    if session.get('login') is None:
        return redirect("/login")
    else:
        page_size = 8
        books = db.session.query(Books)
        last_page = math.ceil(len(books.all()) / page_size) - 1
        if page_size:
            books = books.limit(page_size)
        if page:
            books = books.offset(page*page_size).all()
        return render_template("index.html", books = books, page=page, last_page=last_page)


@board.route("/info/<int:book_id>", methods=["GET", "POST", "PATCH", "DELETE"])
def bookInfo(book_id):
    book = Books.query.filter(Books._id==book_id).first()
    method = request.method

    if method == "GET":
        # 책 정보 모두, 댓글 정보 모두
        comments = db.session.query(Comment._id, Comment.user_id, Comment.book_id, Comment.comment, Comment.star_rating, Comment.created_at, User.name).filter(Comment.book_id==book_id, Comment.user_id == User._id).order_by(Comment.created_at.desc()).all()
        print(comments)
        return render_template("info.html", book=book, comments=comments)
    
    elif method == "POST":
        # 댓글 추가 -> comment 테이블에 값 추가
        commenter = request.form['commenter']
        book_id = request.form['book_id']
        comment = request.form['comment']
        star_rating = request.form['star_rating']
        c = Comment(commenter, book_id, comment, star_rating)
        db.session.add(c)
        db.session.commit()
        ratings = db.session.query(db.func.avg(Comment.star_rating).label("rating_avg")).filter(Comment.book_id==book_id).first()
        book.rating_avg = round(ratings.rating_avg)
        db.session.commit()
        return jsonify({"result": "success"})
    
    elif method == "PATCH":
        # 댓글 수정
        comment_id = request.form['comment_id']
        comment = request.form['comment']
        star_rating = request.form['star_rating']
        comment_to_edit = Comment.query.filter(Comment._id == comment_id).first()
        comment_to_edit.comment = comment
        comment_to_edit.star_rating = star_rating
        comment_to_edit.created_at = datetime.now(timezone('Asia/Seoul'))
        db.session.commit()
        return jsonify({"result": "success"})
    
    else:
        # 댓글 삭제
        id = request.form["id"]
        Comment.query.filter(Comment._id == id).delete()
        db.session.commit()
        return jsonify({"result": "success"})


@board.route("/rent", methods=["PATCH"])
def rent():
    book_id = request.form['book_id']
    book = Books.query.filter(Books._id==book_id).first()
    if book.stock > 0:
        book.stock -= 1
        db.session.commit()

        user_id = request.form['renter']
        same_book = db.session.query(Rent).filter(Rent.book_id==book_id, Rent.user_id==user_id, Rent.return_date==None).first()
        if same_book is not None:
            return jsonify({"result": "duplicated"})
        rent = Rent(user_id, book._id)
        db.session.add(rent)
        db.session.commit()
        return jsonify({"result": "success"})
    return jsonify({"result": "disable"})


@board.route("/return", methods=["GET", "POST"])
def return_book():
    # get일 때
    # 페이지 보여주기
    # -> g.user._id에 해당하는 모든 로우를 rent_tb에서 select
    # -> 책 id를 book_tb에서 id가 같은 로우 찾아서 이미지, 책이름 불러오기
    records = db.session.query(Books.img_path, Books.book_name, Books._id, Rent.rent_date).filter(Books._id==Rent.book_id, Rent.user_id==g.user._id, Rent.return_date==None).all()
    # print(records)
    if request.method == 'GET':
        return render_template('return.html', records = records)

    # post일 때 반납 후 테이블에 반납일자 기록, book 재고 1올리기
    else:
        book_id = request.form['book_id']
        book = Books.query.filter(Books._id==book_id).first()
        rent = Rent.query.filter(
            Rent.book_id==book_id, Rent.user_id==g.user._id, Rent.return_date==None
            ).first()
        rent.return_date = datetime.now(timezone('Asia/Seoul')).date()
        book.stock += 1
        db.session.commit()
        return jsonify({"result": "success"})


@board.route("/history", methods=["GET"])
def history():
    records = db.session.query(
        Books.img_path, Books.book_name, Books._id, Books.rating_avg, Rent.rent_date, Rent.return_date).filter(Books._id==Rent.book_id, Rent.user_id==g.user._id, Rent.return_date.isnot(None)).all()
    return render_template('history.html', records = records)


@board.route("/join", methods=["GET", "POST"])
def join():
    if session.get("login") is None:
        if request.method == 'GET':
            return render_template('join.html')
        else:
            user_name = request.form['user_name']
            user_email = request.form['user_email']
            user = User.query.filter(User.email == user_email).first()
            if user is not None:
                return jsonify({"result": "duplicate"})
            user_pw = request.form['user_pw']
            pw_hash = bcrypt.generate_password_hash(user_pw).decode()

            user = User(user_name, user_email, pw_hash)
            db.session.add(user)
            db.session.commit()
            return jsonify({"result": "success"})
    else:
        return redirect("/")


@board.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('login') is None:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            user_email = request.form['user_email']
            user_pw = request.form['user_pw']
            user = User.query.filter(User.email == user_email).first()
            if user is not None:
                if bcrypt.check_password_hash(user.pw, user_pw):
                    session['login'] = user.email
                    return jsonify({"result": "success"})
                else:
                    return jsonify({"result": "fail"})
            else:
                return jsonify({"result": "fail"})
    else:
        return redirect("/")


@board.route("/logout")
def logout():
    session['login'] = None
    return redirect('/')


