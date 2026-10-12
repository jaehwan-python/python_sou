# app.py와 동일한 레벨의 db데이터를 넣어둔 파일이다.
import pymysql
import os

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_connFunc():
    return pymysql.connect(
        host=DB_HOST, 
	    port=DB_PORT, 
	    user=DB_USER, 
	    password=DB_PASSWORD,
        database=DB_NAME, charset="utf8mb4", 
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True, # True이면 commit이나 rollback을 할 필요가 없다.
    )

# DB관련정보를 db.py에 다가 적었고
# app.py에서 db.py를 불러다 쓰면 된다.


