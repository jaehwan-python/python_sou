from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for, jsonify

from db import get_connFunc
# 이 부분을 통해서 app.py라는 기둥 py에서 db요청 자료를 받아올 수 있다.

"""
<RESTFul>
상품 CRUD라면 보통 이렇게 restful이 구성
GET      /api/sangdata     전체 상품 조회 
GET      /api/sangdata/1   1번 상품 조회
POST     /api/sangdata     상품 추가
PUT      /api/sangdata/1   1번 상품 수정
DELETE   /api/sangdata/1   1번 상품 삭제
"""   

app = Flask(__name__)
# 나중에 뒷 수업에서도 모든 과정을 Flask로 할 것이기 때문에 잘 정리해두기!


# 라우팅 정보1
@app.get("/")
def index():
    return render_template("index.html")


# 라우팅 정보2 : 전체 직원 조회
@app.get("/acorn/jikwon")
def jikwon_list():
    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay,
        year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum=buser.buserno
        order by jikwonno
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({"ok":True, "data":rows})
# "ok":True, "data":rows 이 문자열을 클라이언트에서 JavaScript가 받는다.


# 라우팅 정보3 : 직원 1명 조회
@app.get("/acorn/jikwon/<int:no>") # 요청명에 데이터가 따라 들어온다.
def jikwon_one(no):
    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay,
        year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum=buser.buserno
        where jikwonno=%s
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no,)) 
            # 불러온 no자료가 튜플자료이기 때문에 (no, )형태로 썼다.
            row = cur.fetchone()

    return jsonify({"ok":True, "data":row})


# 라우팅 정보4 : 부서 전체 조회
@app.get("/api/buser")
def buser_list():
    sql = """
        select * from buser order by buserno
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rowss = cur.fetchall()

    return jsonify({"ok":True, "data":rowss})


# 라우팅 정보5 : 특정 부서 조회
@app.get("/api/buser/<int:no>") # 요청명에 데이터가 따라 들어온다.
def buser_one(no):
    sql = """
        select jikwonno, jikwonname, jikwonjik, jikwonpay, year(jikwonibsail) as ibsayear 
        from jikwon
        where busernum = %s
        """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no,)) 
            # 불러온 no자료가 튜플자료이기 때문에 (no, )형태로 썼다.
            rowsss = cur.fetchall()

    return jsonify({"ok":True, "data":rowsss})


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
