# < DB에서 데이터 가져오기 >

# 우리가 직접 만든 DB("coffeedb")에 만들어둔 데이터(survey테이블)를 가져와보자

import os 
import pymysql

# 연결할 DB를 설정
def get_conn():
    return pymysql.connect(
        host = os.getenv("DB_HOST", "127.0.0.1"),
        port = int(os.getenv("DB_PORT", "3306")),
        user = os.getenv("DB_USER", "root"),
        password = os.getenv("DB_PASSWORD", "123"),
        database = os.getenv("DB_NAME", "coffeedb"),
        charset = "utf8mb4", 
        cursorclass = pymysql.cursors.DictCursor,
        autocommit = True
    )

# DB에 연결 및 필요한 값 넣어주기
def insert_survey(gender:str, age:int, co_survey:str):
    sql = "insert into survey(gender, age, co_survey) values(%s, %s, %s)"
    conn = get_conn()

    # DB는 필요할때만 연결하고 사용하지 않을때는 끊어주어야 하기때문에 try문 사용!
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (gender, age, co_survey))
            # 위에서 만든 sql문을 집어넣음
    finally:
        conn.close()
        # DB 연결을 끊음

# 다시 DB연결
def fetchall_survey():
    sql = "select rnum, gender, age, co_survey from survey order by rnum asc"
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
            # 해당 결과를 가져온다.
    finally: 
        conn.close()
    