# Maria DB : jikwon, buser 테이블
# 직원번호, 직원명을 입력하여 로그인에 성공하면 해당직원, buwer정보 출력


import MySQLdb
import json


# DB 연결정보 읽기1 : json파일 읽기
# with open('DB_connect.json', mode = 'r', encoding = 'utf-8') as f:
#     config = json.load(f) 
#     # config_data라는 변수가 json파일(DB_connect.json)을 읽음 


# DB 연결정보 읽기2 : .env파일 읽기(env파일 만들어둠)
# pip install python-dotenv -> 명령쉘에 입력하기. 그래야 아래 from 문장이 활성화된다.
from dotenv import load_dotenv
import os

load_dotenv()

config = {
        'host' : os.getenv('DB_HOST'), # 127.0.0.1을 가져옴
        'user' : os.getenv('DB_USER'), 
        'password' : os.getenv('DB_PASSWORD'),
        'database' : os.getenv('DB_NAME'),
        'port' : int(os.getenv('DB_PORT')), # port번호는 int이기 때문이다. 문자열 아님!
        'charset' : os.getenv('DB_CHARSET')
        }
# 우리가 .env에 저장해둔 정보를 가져옴


def LoginFunc(): # 직원로그인 기능을 하나의 함수로 만들어둠

    conn = None

    try:
        conn = MySQLdb.connect(**config) # DB에 있는 table자료를 내 서버를 연결 시킨다. 그때 자료를 dict형으로 출력한다.
        cursor = conn.cursor() # 둘 사이의 정보를 전달, cursor = SQL문을 MariaDB에 전달하고 결과를 받아오는 객체

        jikwon_no = input("직원번호")
        jikwon_name = input("직원이름")

        if jikwon_no == "" or jikwon_name == "": # 직원번호와 직원이름이 없다면~
            print("로그인 정보를 입력하세요")
            return

        #방법1.
        '''
        sql = """
            select jikwonno as 직원번호, jikwonname as 직원명, buserloc as 근무지역, jikwonjik as 직급, jikwongen as 성별 
            from jikwon
            left outer join buser 
            on jikwon.busernum = buser.buserno
            where jikwonno = {0} and jikwonname = {1}
            """.format(jikwon_no, jikwon_name)
        # 이렇게 sql이라는 변수에 select문의 자료를 넣을 수 있다.
        ''' # ... 비권장하는 방법

        #방법2. 권장하는 방법!!
        sql = """
            select jikwonno as 직원번호, jikwonname as 직원명, busername as 부서명, buserloc as 근무지역, jikwonjik as 직급, jikwongen as 성별 
            from jikwon
            left outer join buser 
            on jikwon.busernum = buser.buserno
            where jikwonno = %s and jikwonname = %s 
            """ # format을 쓰기보다 %s를 사용하는 것을 권장
            # %s : 로그인 조건
        #sql 실행
        cursor.execute(sql, (jikwon_no, jikwon_name))

        # Login 성공 직원 정보만 출력
        data = cursor.fetchone()

        if data: 
            print("로그인 성공")
            print("직원번호 : ", data[0])
            print("직원명 : ", data[1])
            print("부서명 : ", data[2])
            print("근무지역 : ", data[3])
            print("직급 : ", data[4])
            print("성별 : ", data[5])
        else:
            print("로그인 실패 : 입력자료를 확인하세요.")


    except Exception as e:
        print('에러 : ', e)

    finally:
        if conn : 
            conn.close()

if __name__ == '__main__':
    LoginFunc()