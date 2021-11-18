import pymysql
from flask import Flask
from db_connect import db
from api import board
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.register_blueprint(board)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:khm9339@127.0.0.1:3306/elice_library"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.secret_key = 'codedbyhmkim199'


db.init_app(app)
bcrypt = Bcrypt(app)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)