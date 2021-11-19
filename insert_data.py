# 이미지 파일 경로만 추가적으로 삽입하는 코드.
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="khm9339",
  database="elice_library"
)

mycursor = mydb.cursor()

sql = "UPDATE books_tb SET img_url=%s WHERE _id=%s"
path = "book_img/"
data_cnt = 32
for i in range(1, data_cnt+1):
    new_path = path + str(i)
    try:
        real_path = "C:/Users/hmkim/Desktop/3-1-hyeminKim/static/" + new_path
        open(f'{real_path}.png')
        new_path += '.png'
    except:
        new_path += '.jpg'
    val = (new_path, i)
    mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")