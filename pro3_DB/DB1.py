# SQLite : 핸드폰 안에 있는 개인용 DBMS이다
# 파이썬에 기본 내장되어 있어 따로 설치할 필요가 없다. = 경량 DBMS
# 서버가 필요없다 = 임베디드 DBMS -> 시스템 내에서 별도의 자원을 사용할 필요가 없다.

import sqlite3

print(sqlite3.sqlite_version) # 우리가 쓸 sqllite3의 버전 확인
print()

'''
conn = sqlite3.connect('exam.db') # exam.db라는 파일(.py)을 생성하고 연결함. = 메모리에 저장이 된다. = 영속성
conn = sqlite3.connect(':memory:') # 이렇게 적어주면 RAM에서만 작업한다. 그래서 휘발성이 있다. = 휘발성
'''

# 우리는 ":memory:"를 사용한다.
conn = sqlite3.connect(':memory:') # connect : DB와 연결을 함

try: 
    cur = conn.cursor(); # cursor : DB에 SQL문을 전달하고 결과를 받아오는 객체 ... 그 객체의 이름 = cur
#                          cursor : SQL문 실행을 담당한다.
#   table 생성
    cur.execute("create table if not exists friends(name text, phone text, addr text)") # friends라는 table을 만들고 컬럼 생성(name, phone, addr)

#   자료 입력
    cur.execute("insert into friends values('홍길동', '010-1111-1111', '서초 1동')") # 표에 들어갈 자료를 넣는다.
    cur.execute("insert into friends values(?, ?, ?)", ('이기자', '111-2222', '서초 2동')) # ?를 사용하면 SQL Injection을 방지할 수 있다.

    inputdatas = ('신기해', '111-1234', '서초 3동')
    cur.execute("insert into friends values(?, ?, ?)", inputdatas) 

    inputdatas2 = ('신기한', '111-3333', '역삼 1동'), ('신기루', '111-4444', '역삼 2동') # 이런식으로 여러명을 써줄 수도 있다. 
#                                                                                         ... tuple형태의 자료형을 해줌.
    cur.executemany("insert into friends values(?, ?, ?)", inputdatas2)
#   executemany : 여러개의 자료를 넣을 때 사용한다. (tuple형태로 넣어야 한다.)

    conn.commit() # commit : table에 있는 자료를 저장하는 것
#   수정된 자료를 다시 DB에 저장한다. (commit을 해주지 않으면 자료가 저장되지 않는다.)

#   자료보기
    cur.execute("select * from friends")
#   1. 한 개의 행만 읽기
    print(cur.fetchone()) # fetchone : 한 줄만 가져온다. = 한 행(Record)만 읽기 ... fetchone은 하나의 행을 tuple형태로 가져온다.
    print(cur.fetchone()) # 다음 행의 자료를 가져온다.
#   record pointer가 있는 지점의 자료만 읽는다.    
#   record pointer는 수많은 행 중에서 현재 읽고 있는 행의 위치를 가리킨다.
#   record pointer는 초기에 모든 행 위에 존재하고 위에서부터 차례대로 한 행씩만 읽어 내려간다.

#   2. 모든 행 읽기
    print(cur.fetchall()) # fetchall : 모든 행을 가져온다. = 모든 행(Record)을 읽기 ... fetchall은 모든 행을 list 안에 tuple형태로 가져온다.
#   record pointer가 자료를 지정할 수 없을 때까지 읽는다.
    print()

#   3. 한 행씩 읽기 
    cur.execute("select * from friends") # 모든 행을 가져와라. 하지만 가급적 컬럼명을 직접 써주는 방법을 권장한다. (select name, phone, addr from friends)
    for r in cur:
#       print(r) # 한 행씩 읽는다. = 한 행(Record)씩 읽기 ... for문을 사용하면 fetchone과 같은 효과를 낸다.
        print(r[0] + '님의 전화는', r[1], r[2]) # tuple형태로 가져오기 때문에 인덱스로 접근해야 한다. ... 계산이 가능해진다.
#       fetchall은 자료를 모두 가져오는 것만 가능하다. 하지만 for문을 사용하면 한 행씩 가져오면서 계산도 가능하다!!
#   안드로이드 : java script
#   아이폰 : swift를 사용한다. (java script와 swift는 문법이 다르다())

#   Maria DB, Oracle, MySQL은 서버형 DBMS이다. = 서버가 필요하다. = ip주소가 필요하다 = 그리고 그 서버를 연결해주는 클라이언트/서버 구조
#   SQLite는 서버형 DBMS가 아니다. = 서버가 필요없다. = 임베디드 DBMS = 내 서버에 내장형으로 되어있다. 외부에 있는 SQLite에는 접근할 수 없다.   



except Exception as e:
    print('err : ', e)
    conn.rollback() # commit하여 저장된 자료를 취소하고 이전 상태로 되돌린다. (rollback을 해주지 않으면 자료가 저장되지 않는다.)
finally: # error에 상관없이 무조건 수행하는 문장
    conn.close()

#네트워크 작업시에는 항상 예외처리를 해줘야 한다.



