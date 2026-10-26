# DataFrame의 자료를 MariaDB(=mysql)의 table(sangdata)에 저장하기

# pip install sqlalchemy 설치하기
# : DB 연결 + 관리 + 추상화를 지원한다.

import pandas as pd
from sqlalchemy import create_engine

data = {
    'code' : [10, 11, 12],
    'sang' : ['맥주', ' 사이다', '와인'],
    'su' : [20, 22, 5],
    'dan' : [5000, 3000, 70000]
}

# dic구조안에 list구조가 들어있다. != json 타입

engine = None
frame = pd.DataFrame(data)
print(frame)

try:
    # DB 연결
    engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test?charset=utf8mb4")
    # create_engine의 작성형식(고정)
    # 문제점 : 비밀번호가 노출되어 있다...그래서 .env파일을 이용하는 것이다.

    # RAM에 있는 DataFrame을 이제 DB에 저장해보자.

    # 1. 
    cnt = frame.to_sql(name='sangdata', con = engine, if_exists='append', index=False)
    # frame이라는 df를 어느 tablef로 보낼 것인지 명명하였다.
    print('저장한 행 수 : ', cnt)

    # 2. 
    # engine으로 추가한 데이터
    df = pd.read_sql("select * from sangdata", engine)
    print('저장된 자료 읽기 : ', df)

    # DataFrame으로 정해준 data를 이미 db에 넣었기에 또 실행하면 에러가 뜬다.
    
except Exception as e:
    print("오류처리 : ", e)

finally:
    if engine is not None:
        engine.dispose()
        # DB 연결 자원을 해제 시킴