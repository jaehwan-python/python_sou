'''
원격 DataBase와 연동 프로그래밍 ... 이번에는 SQLite를 사용하지 않고 원격 DB인 maria DB를 사용한다.
Maria DB : 
준비1) 연결용 Driver File(모듈) 필요
준비2) ip 주소(네트워크에서 컴퓨터나 장치를 구분 규약)가 필요하다. (ip 주소를 알아야 DB에 접근할 수 있다.)


*
Maria DB : 서버형 DBMS이다. = 서버가 필요하다. = ip주소가 필요하다 = 그리고 그 서버를 연결해주는 클라이언트/서버 구조
SQLite : 서버형 DBMS가 아니다. = 서버가 필요없다. = 임베디드 DBMS = 내 서버에 내장형으로 되어있다. 외부에 있는 SQLite에는 접근할 수 없다.


Driver File : DB에 접근할 수 있도록 도와주는 파일이다. (DB에 접근할 수 있도록 도와주는 프로그램)
을 설치해야한다
pip install mysqlclient ... 명령쉘에 입력 ... 그러면 lib - package에 설치가 된다.

'''


import MySQLdb # MySQLdb : Maria DB에 접근할 수 있도록 도와주는 모듈이다. (Driver File)

# DB 연결 담당을 하는 객체를 생성한다. (DB에 접근할 수 있도록 도와주는 객체)


# 연결 방법(매핑)1. 직접 연결정보를 적어주는 방법(conn으로 연결정보 저장)
'''
conn = MySQLdb.connect(host = '127.0.0.1' #  192.168.0.19인 내 ip를 써줘도 된다. local host
                    , user = 'root'
                    , password = '123'
                    , database = 'test'
                    , port = 3306)  # port : DB가 사용하는 포트번호를 써준다. (기본값은 3306이다.) Maria DB / MySQL 서버가 기본적으로 사용하는 포트번호
                                    # 포트는 외부에서 접근할 수 있도록 열어줘야 한다. (방화벽에서 포트번호를 열어줘야 한다.) 
                                    # 이렇게 적으면 우리가 만든 test라는 DB에 접근할 수 있다. (DB에 접근할 수 있도록 도와주는 객체)
'''
# 따로 maria DB command prompt에서 실행할 필요 없다. = 연결정보를 미리 적어줌

# SQLite는 원격DBMS가 아니기 때문에 ip주소를 적어서 연동할 필요가 없다.
# 하지만 Maria DB는 원격DBMS이기 때문에 ip주소를 적어서 연동해야 한다. (ip주소를 알아야 DB에 접근할 수 있다.)

# ip주소 - port번호가 하위로 존재한다. (ip주소 - port번호 - DB이름 - table이름 - column이름)


# 연결 방법(매핑)2. dict 형태로 적어주는 방법(dict형태)
# dict 형태로 적어줄 수도 있다.
'''
config_data = {'host' : '127.0.0.1'
                , 'user' : 'root'
                , 'password' : '123'
                , 'database' : 'test'
                , 'port' : 3306
                , 'charset' : 'utf8'} # 'charset' : 'utf8' : 한글을 사용하기 위해서 적어준다. (한글이 깨지지 않도록)
'''
                # 연결 정보만 따로 빼낼 수도 있다.
# ... 이렇게 적어두면 누구나 다 사용할 수 있다. (보안상 위험하다.) ... 그래서 dict 형태로 적어서 json 파일로 만들어서 사용하면 된다. (보안상 안전하다.) 
# ... json 파일은 암호화가 가능하다. (보안상 안전하다.)
'''
{'host' : '127.0.0.1'
, 'user' : 'root'
, 'password' : '123'
, 'database' : 'test'
, 'port' : 3306
, 'charset' : 'utf8'}
'''
# 이 부분만 별도의 파일로 만들어라. ... DB_connnect.json에 따로 저장 


# 연결 방법(매핑)4. json 파일(외부의 json파일을 만들어 거기에 연결정보르 저장한 후 불러오는 방법)
# 별도 저장된 json 파일 읽기(json은 큰따옴표를 쓴다!)

import json
with open('DB_connect.json', mode = 'r', encoding = 'utf-8') as f:
    config_data = json.load(f) # config_data라는 변수가 json파일(DB_connect.json)을 읽음


def myFunc():
    try:
        # 연결 방법2, 3
        conn = MySQLdb.connect(**config_data) # **config_data : dict 형태로 적어준 연결 정보를 unpacking 해준다. (연결 정보만 따로 빼낼 수도 있다.)
        # conn.autocommit(True) # 자동 커밋 : 내가 직접 설정을 해야하지만 파이썬에서는 수동커밋이 더 편하다.
        # conn.autocommit(False) # 수동 커밋 : 기본값 -> 그래서 내가 직접 커밋과 rollback을 해줘야한다.

        cursor = conn.cursor() # cursor() : DB에 SQL문을 전달하고 결과를 받아오는 객체 ... 그 객체의 이름 = cursor

        
        # < 자료 추가 > ... 5, 6번데이터 추가
        '''
        isql = "insert into sangdata(code, sang, su, dan) values(5, '마스크', 5, '3000')" # 이미 추가했기에 한번더 실행을 누르면 중복으로 error가 뜬다.
        # cursor.execute(isql)
        # conn.commit()

        isql = "insert into sangdata values(%s, %s, %s, %s)"

        ins_data = (6, '커피', 10, 5000) # 문자와 날짜는 무조건''를 해야한다. 또 저 자료형은 tuple이기 때문에 ()를 빼도 좋다.
        # ins_data = 6, '커피', 10, 5000   # 이렇게 적어줘도 좋다.
        cursor.execute(isql, ins_data)
        conn.commit() # 원격 DB에 저장이 된다.
        '''

        # < 자료 수정 >
        '''
        usql = "update sangdata set sang = %s, su = %s, dan = %s where code = %s" # 이 순서는 바뀌면 안된다.
        up_data = '물티슈', 3, 1000, 5  #   = ()'물티슈', 3, 1000, 5)
        cursor.execute(usql, up_data)
        conn.commit()
        # 5번 데이터를 수정하였다.(마스크 -> 물티수)
        '''
        '''
        usql = "update sangdata set sang = %s, su = %s, dan = %s where code = %s" # 이 순서는 바뀌면 안된다.
        up_data = '콜라', 11, 3000, 6  #   = ()'물티슈', 3, 1000, 5)
#       insert, update, delete는 성공하면 성공갯수를 반환하고 실패하면 0을 반환한다.
        cou = cursor.execute(usql, up_data)
        print('수정 갯수 : ', cou)
        conn.commit()
        '''

#       < 자료 삭제 >
        code = '6'; # ... 추후에 우리는 web program에서 data를 받아올 것이다. input()함수이용
        # dsql = "delete from sangdata where code = " + code # : 이런 식으로 문자열끼리 더하면 해킹에 위험하다(주의)..SQL injection에 걸릴 수 있다.
        # print(dsql)
        # 참고 : **Secure Coding 가이드라인에 맞게 프로그래밍 해야한다!!**
        # SQL injection : 사용자의 입력값을 검증하지 않는 웹 어플리케이션의 허점을 악용해 악의적인 SQL쿼리문을 실행하고 DB를 조작하는 해킹 기법이다.
        # 저 가이드라인에 맞춰서 프로그래밍 해야한다.
        
        # 추천 방법1. 권장..!
        dsql = "delete from sangdata where code = %s" 
        cou = cursor.execute(dsql, (code,))

        # 추천 방법2.
#       dsql = "delete from sangdata where code = '{0}'".format(code)
#       cursor.execute(dsql, (code,)) # 이렇게 쓰면 수정값만 확인 가능
#       cou = cursor.execute(dsql, (code,)) # cou를 붙이면 삭제 후 반환값까지 알 수 있다.
        if cou != 0:
            print('삭제 성공')
        else:
            print('삭제 실패')
        conn.commit()
        

        # < 자료 읽기 >
#       sql = "select * from sangdata" # sangdata라는 table에 있는 모든 자료를 가져와라.
        sql = "select code, sang, su, dan from sangdata" # 이게 원칙이다.

        # 방법1.
        cursor.execute(sql)
        for data in cursor.fetchall():
#           print(data)
            print("%s %s %s %s"%data) # tuple형태로 가져오기 때문에 인덱스로 접근해야 한다. ... 계산이 가능해진다.
        print()

        # 방법2.
        cursor.execute(sql)
        for data in cursor:
            print(data[0], data[1], data[2], data[3]) # tuple형태로 가져오기 때문에 인덱스로 접근!
        print()

        # 방법3.
        cursor.execute(sql)
        for code, sang, su, dan in cursor:
            print(code, sang, su, dan) 
        print()

        # 방법4.
        cursor.execute(sql)
        for a, b, 수량, 단가 in cursor:
            print(a, b, 수량, 단가*1000) # 별명을 지어줄수도 있고 컬럼에 대하여 걔산도 가능하다


    except Exception as e:
        print('err : ', e)
        conn.rollback()


    finally:
        conn.close()

# DB2_Maria.py가 메인 모듈임을 알림. 가독성을 위해 적어줌
if __name__ == '__main__':
    myFunc()