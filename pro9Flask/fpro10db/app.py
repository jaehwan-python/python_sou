from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for, flash

# flash : 에러 표시
# pip install pymysql설치!
import pymysql
import os
from flask import get_flashed_messages # 저장해 둔 메세지르 꺼내는 함수
# ex) flash("에러~") -> 메세지를 세션에 잠시 저장(RAM)한다. 그리고 나서 get_flashed_messages()하면 메세지 읽기 가능하다.

app = Flask(__name__)
app.secret_key = "abcd1234" # 쿠키 서명용 비밀키

# MariaDB 연결정보
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")
# 보통은 .env파일로 만들어서 사용한다(.env파일은 github에 안올라가기 때문 - 그래서 그냥 직접 적어줌)

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4", # 전 세계 문자(한글 포함) + 이모지까지 처리 가능

        cursorclass=pymysql.cursors.DictCursor,
        autocommit = False 
    )
    # DictCursor : select 결과를 'dict type' 형태로 접근 가능하게 해준다.
    # 예: {'code':1, 'sange':'mouse' ...} -> row['code'], row['sang']가능. 원래는 row[0], row[1] 이런식이다.


# 라우팅 정보1
@app.get("/")
def index():
    return redirect(url_for("show_list"))
# url창에서 /show를 입력하면 show_list가 실행된다.
# 만약 /show/의 이름을 /korea/, /era/등등 다른 이름으로 바꾸게 되면 url이름은 바뀌어도 실행되는 함수는 그대로다. 
# 함수와 매핑되어 있는 라우팅 요청명이 바뀌지만 해당 함수가 바뀌지 않는다. = url_for의 원리 
# = url이 함수(show_list)를 실행하고 그 함수를 매핑하고 있는 라우팅명이 url에 표기 된다.

# 라우팅 정보1 없이 브라우저를 실행하면 Not Found가 뜨지만 /show/요청을 쓰면 함수가 실행된다


# 라우팅 정보2
@app.get("/show/")
def show_list():

    # DB연결
    conn = get_conn()
    try:
        # conn연결을 위한 cur객체 생성
        with conn.cursor() as cur:
            cur.execute("select code, sang, su, dan from sangdata order by code asc")
            rows = cur.fetchall()
        
        # 새로 넣은 flask 라이브러리 "flash"에 의해서...
        messages = list(get_flashed_messages())
        return render_template("list.html", rows=rows, messages=messages)
        
    except Exception as e:
        # return f"에러 발생: {e}"
        print(e)

    finally:
        conn.close()


# 라우팅 정보3
@app.get("/add/")
def add_form():
    messages = list(get_flashed_messages())
    return render_template("form_add.html", messages=messages) # 추가 form 호출


# 라우팅 정보3-1 (추가 처리)
@app.post("/add/") 
def add_save():
    sang = (request.form.get("sang") or "").strip()
    su_raw = (request.form.get("su") or "").strip()
    dan_raw = (request.form.get("dan") or "").strip()

    # 서버에서도 클라이언트가 전달한 입력자료 검사
    if not sang or not su_raw.isdigit() or not dan_raw.isdigit():
        flash("sang은 필수, su, dan은 숫자만 허용")
        return redirect(url_for("add_form"))

    su = int(su_raw) # 연산없이 추가할 경우라면 숫자화하지 않아도 된다.
    dan = int(dan_raw)

    # 새상품 추가 처리
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # code는 자동증가를 위해 프로그램으로 작성된다.
            cur.execute("select max(code) as max_code from sangdata")
            row = cur.fetchone()
            max_code = row["max_code"] if row else None # fetchone으로 가장 큰 값을 골라서 row에 넣었다. 만약 sangdata의 5번 (가장큰값)은 max_code가 되고 아예 데이터가 없으면 none을 반환한다.
            next_code = (max_code + 1) if max_code is not None else 1 # 위에서 골랐던 max_code가 존재하고 none값이 아니라면 max_code에 1을 더해서 next_code로 저장한다. (최초의 상품인 경우 1이라는 값을 준다)

            # 본격적인 상품 추가
            cur.execute("insert into sangdata(code, sang, su, dan) values (%s, %s, %s, %s)", (next_code, sang, su, dan)) # code에 next_code를 넣는다.
            conn.commit()

            # 새상품 추가 후 목록 보기
            return redirect(url_for("show_list")) 
        
    except Exception as e:
        conn.rollback()
        flash(f"저장 실패 : {e}")
        return redirect(url_for("add_form"))

    finally:
        conn.close()


# 라우팅 정보4
@app.get("/edit/<int:code>/") # <!-- 요청방법1 : <td><a href = "/edit/1/"> 수정 </a></td> 위 방식과 동일-->때문에 <int:code>를 써준다.
def edit_form(code:int): # edit_form 호출
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("select * from sangdata where code=%s", (code,)) # code는 tuple자료이기에 ()꼭 해주기!
            row = cur.fetchone() 
            # 5번쩨 이후의 자료(row)가 있는지 확인
        
        # 5번째 이후의 자료가 없으면 ...
        if not row:
            flash("해당 자료가 없어요")
            return redirect(url_for("show_list"))

        # 5번째 이후의 자료가 있으면!!
        messages = list(get_flashed_messages())
        return render_template("form_edit.html", row=row, messages=messages)
        # 그 때 5번째 이후의 row가 있으면 그 row를 들고 edit.html로 이동한다.
    
    finally:
        conn.close()
# 우리는 utl-for로 edit을 호출했는데 정작 [관리]에 커서를 올리면 /edit/1의 형태(왼쪽 아래에)로 뜬다. 왜 그럴까?
# list.html에서 edit함수요청을 보내고 app.py에서 라우팅 정보4에서 받은 함수가 실행되는 라우팅 내용이 /edit/<int:code>/ 이거다라는 걸 나타내기 때문이다.


# 라우팅 정보4-1(수정처리)
@app.post("/edit/<int:code>/") 
def edit_save(code:int): # 수정처리
    sang = (request.form.get("sang") or "").strip()
    su_raw = (request.form.get("su") or "").strip()
    dan_raw = (request.form.get("dan") or "").strip()
    
    # 서버에서도 클라이언트가 전달한 입력자료 검사
    if not sang or not su_raw.isdigit() or not dan_raw.isdigit():
        flash("sang은 필수, su, dan은 숫자만 허용")
        return redirect(url_for("edit_form", code=code))

    su = int(su_raw) # 연산없이 추가할 경우라면 숫자화하지 않아도 된다.
    dan = int(dan_raw)

    # 수정하기
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("update sangdata set sang=%s, su=%s, dan=%s where code=%s", (sang, su, dan, code)) # code는 tuple자료이기에 ()꼭 해주기!
        conn.commit() # 성공하면...
        return redirect(url_for("show_list")) 

    except Exception as e:
        conn.rollback() # 실패하면...
        flash(f"수정 실패 : {e}")
        return redirect(url_for("edit_form", code=code))
    
    finally:
        conn.close()


# 라우팅 정보5
@app.post("/delete_row/<int:code>/") 
def delete_row(code:int):
    conn = get_conn()
    
    try:
        with conn.cursor() as cur:
            # 삭제하기
            cur.execute("delete from sangdata where code=%s", (code, ))
            # 실제 DB에는 반영x
        conn.commit()
            # 실제 DB에 반영o
        return redirect(url_for("show_list")) # 삭제 후 목록 보기
    
    except Exception as e:
            conn.rollback() 
            flash(f"삭제 실패 : {e}")
            return redirect(url_for("show_list"))
        
    finally:
        conn.close()




if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
