import pymysql
from flask import Flask
from flask_bcrypt import Bcrypt
from db_connect import db
from api import board
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.register_blueprint(board)

load_dotenv()

mysql_pw = os.environ.get("MYSQL_PASSWORD")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:"+mysql_pw+"@localhost:3306/elice_library"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.secret_key = os.environ.get("APP_SECRET_KEY")


db.init_app(app)
bcrypt = Bcrypt(app)


if __name__ == '__main__':
    # local에서는 port 5000 debug True로 하기
    # 배포시에 port 80 debug False로!
    app.run('0.0.0.0', 80, debug=False)