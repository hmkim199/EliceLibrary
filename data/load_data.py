import csv
from datetime import date, datetime
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()
mysql_pw = os.environ.get("MYSQL_PASSWORD")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=mysql_pw,
  database="elice_library"
)

mycursor = mydb.cursor()
beforeSQL = "DELETE FROM books_tb;"
mycursor.execute(beforeSQL)
mydb.commit()
sql = "INSERT INTO books_tb (book_name, publisher, author, publication_date, pages, isbn, description, link, img_path) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

with open('library.csv', 'r', encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)

    for row in reader:
        publication_date = datetime.strptime(
						row['publication_date'], '%Y-%m-%d').date()
        img_path = f"/book_img/{row['id']}"
        try:
            open(f'../static/{img_path}.png')
            img_path += '.png'
        except:
            img_path += '.jpg'
        
        val = (row['book_name'], row['publisher'], row['author'], publication_date, int(row['pages']), int(row['isbn']), row['description'], row['link'], img_path)
        mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")