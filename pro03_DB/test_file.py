# ----------------------연습문제1.------------------------------------------------------------
# 문1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
# 직원번호 입력 : _______
# 직원명 입력 : _______
# 직원번호 직원명 부서명 부서전화 직급 성별
#     1         홍길동 총무부 111-1111 이사 남           <== 홍길동으로 로그인한 경우


# pip install python-dotenv   설치
# env 파일로 db 연결 정보 읽기
# DB_HOST = 127.0.0.1
# DB_USER=root
# DB_PASSWORD=123
# DB_NAME=test
# DB_PORT=3306
# DB_CHARSET=utf8
import MySQLdb

from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')),     # port는 수자 처리 
    'charset':os.getenv('DB_CHARSET'),
    }

def loginfunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)  # DB 연결  # dict여서 **를 붙인다.
        cursor = conn.cursor()  # SQL 처리를 위한 객체 생성
        jikwonno = input('직원번호 입력 : ')
        jikwonname = input('직원명 입력 : ')
        if jikwonno == '' or jikwonname == '':
            print('로그인 정보를 입력하세요')
            return

        sql = """
        select 
        j.jikwonno as 직원번호, j.jikwonname as 직원명,
        b.busername as 부서명, b.busertel as 부서전화, j.jikwonjik as 직급, j.jikwongen as 성별      
        from jikwon j
        left outer join buser b on j.busernum = b.buserno
        where j.jikwonno=%s and j.jikwonname=%s
        """

        # sql 실행
        cursor.execute(sql, (jikwonno, jikwonname))  # sql 실행  # %s자리에 입력값이 들어감 

        # 로그인 성공 직원 정보 출력
        data = cursor.fetchone()


        # 로그인 성공시

        if data:
            print('로그인 성공')
            print('직원번호','직원명','부서명','부서전화','직급','성별')
            print(data[0],'      ',data[1],data[2],data[3],data[4],data[5])

        else:
            print('로그인 실패 : 다시 확인해주세요')

    except Exception as e:
        print('에러 : ', e)
    finally:
        if conn:
            conn.close()     # conn이 있으면 연결종료 



if __name__ == '__main__':
    loginfunc()


# ----------------------연습문제1-1.------------------------------------------------------------
# mariadb : jikwon, buser table

# 직원번호, 직원명을 입력하여 로그인에 성공하면 해당 직원, 부서 정보 출력

import MySQLdb
import json

from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')),     # port는 숫자 처리 
    'charset':os.getenv('DB_CHARSET'),
    }

def loginfunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)  # DB 연결  # dict여서 **를 붙인다.
        cursor = conn.cursor()  # SQL 처리를 위한 객체 생성
        jikwon_no = input('직원번호 : ')
        jikwon_name = input('직원이름 : ')
        if jikwon_no == '' or jikwon_name == '':
            print('로그인 정보를 입력하세요')
            return


        buser_sql = """
        select 
        j.jikwonno as 직원번호, j.jikwonname as 직원명,
        b.busername as 부서명, b.busertel as 부서전화, j.jikwonjik as 직급, j.jikwongen as 성명        
        from jikwon j
        left join buser b on j.busernum = b.buserno
        WHERE j.busernum = (SELECT j.busernum
	                        FROM jikwon j
	                        WHERE j.jikwonno=%s and j.jikwonname=%s)
        ORDER BY
            CASE j.jikwonjik
                WHEN '사원' THEN 1
                WHEN '대리' THEN 2
                WHEN '과장' THEN 3
                WHEN '차장' THEN 4
                WHEN '부장' THEN 5
                ELSE 6
            END ASC,
            j.jikwonname ASC;

        """
        gogek_sql = """
        SELECT g.gogekno as 고객번호, g.gogekname as 고객명, g.gogektel as 고객전화, (CASE WHEN SUBSTR(g.gogekjumin,8,1) IN ('1','2') THEN 2026 - (1900 + SUBSTR(g.gogekjumin,1,2)) + 1
                ELSE 2026 - (2000 + SUBSTR(g.gogekjumin,1,2)) + 1
            END
        ) AS 나이
        FROM jikwon j
        LEFT JOIN gogek g ON j.jikwonno = g.gogekdamsano
        WHERE j.jikwonno=%s and j.jikwonname=%s
        """


        # sql 실행
        cursor.execute(buser_sql, (jikwon_no, jikwon_name))  # sql 실행

        # 로그인 성공 직원 정보 출력
        jikwon_data = cursor.fetchall()

        if jikwon_data:
            print('로그인 성공\n')
            print('부서 명단')
            print('직원번호 직원명\t부서명\t부서전화\t직급\t성별')
            for row in jikwon_data:
                print(row[0],'\t',row[1],row[2],'\t',row[3],'\t',row[4],'\t',row[5])
            print("직원 수 : ", len(jikwon_data))
        else:
            print("로그인 실패 : 입력 자료 확인하세요")
            return

        print()
        # sql 실행
        cursor.execute(gogek_sql, (jikwon_no, jikwon_name))  # sql 실행

        # 직원이 맡은 고객 정보 출력
        gogek_data = cursor.fetchall()

        if gogek_data:
            print('관리 고객 명단')
            print('고객번호 고객명\t고객전화\t나이')
            for row in gogek_data:
                print(row[0],'\t',row[1],row[2],'\t',int(row[3]))
            print("관리 고객 수 : ", len(gogek_data))
        else:
            print("관리하는 고객이 없습니다.")
        

    except Exception as e:
        print('에러:',e)
    finally:
        if conn: 
            conn.close()  # 연결 종료  # 콘이 있다면 


if __name__ == '__main__':
    loginfunc()


# ----------------------연습문제2.------------------------------------------------------------
# 연습문제 
# 2번 문제
import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

config_data = {
    'host':os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
    'port':int(os.getenv('DB_PORT')),   # port는 숫자 처리
    'charset':os.getenv('DB_CHARSET'),
}

def genderFunc():
    conn = None
    cursor = None

    try:
        conn = MySQLdb.connect(**config_data)
        cursor = conn.cursor()
        sql = """
            SELECT jikwongen, COUNT(*), AVG(jikwonpay)
            FROM jikwon
            WHERE jikwongen IN ('남', '여')
            GROUP BY jikwongen
            ORDER BY jikwongen
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print("성별","직원수","평균급여")

        for row in data:
            print(row[0], row[1], row[2], sep="  ")

    except Exception as e:
        print('에러: ', e)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
# cursor를 닫고 conn을 닫아야한다.            

if __name__ == "__main__":
    genderFunc()


# ------------------------ 연습문제3-------------------------------------------------------------------------

# 문3) 직원별 관리 고객 수 출력 (관리 고객이 없으면 출력에서 제외)
# ​
# 직원번호 직원명 관리 고객 수
# 1 홍길동 3
# 2 한송이 1

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
    "charset": os.getenv("DB_CHARSET")
}

def LoginFunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        sql = """
        select j.jikwonno as 직원번호,
                j.jikwonname as 직원명,
                count(g.gogekno) as `관리 고객 수`
                from jikwon j inner join gogek g on j.jikwonno = g.gogekdamsano
                group by j.jikwonno, j.jikwonname
                order by j.jikwonno asc
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        print("=== 직원별 관리 고객 수 ===")
        for row in rows:
            print(f"직원번호:{row[0]}  직원명:{row[1]}  관리 고객 수:{row[2]}")

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    LoginFunc()