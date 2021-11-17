import pymysql
from flask import Flask
from db_connect import db

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:khm9339@127.0.0.1:3306/books_tb"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)