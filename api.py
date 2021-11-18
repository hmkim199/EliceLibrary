from flask import Flask, Blueprint, session, g, redirect, request, render_template, jsonify
from flask_bcrypt import Bcrypt
from models import Books, User
from db_connect import db

board = Blueprint('board', __name__)
bcrypt = Bcrypt()


@board.before_app_request
def load_logged_in_user():
    user_email = session.get('login')
    if login is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.email == user_email).first()


@board.route("/")
def home():
    if session.get('login') is None:
        return redirect("/login")
    else:
        return redirect("/main")


@board.route("/join", methods=["GET", "POST"])
def join():
    if session.get("login") is None:
        if request.method == 'GET':
            return render_template('join.html')
        else:
            user_name = request.form['user_name']
            user_email = request.form['user_email']
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


