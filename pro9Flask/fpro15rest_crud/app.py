
from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for, jsonify
import pymysql
from db import get_connFunc

app = Flask(__name__)

"""
상품 CRUD라면 보통 이렇게 restful이 구성
GET      /api/sangdata     전체 상품 조회 
GET      /api/sangdata/1   1번 상품 조회
POST     /api/sangdata     상품 추가
PUT      /api/sangdata/1   1번 상품 수정
DELETE   /api/sangdata/1   1번 상품 삭제
"""   

# 라우팅 정보1
@app.get("/")
def index():
    return render_template("index.html")


# 라우팅 정보2 : 전체 상품 자료 읽기(crud_Read)
# app.py를 이용해 get방식으로 요청한 것을 app.py에서 app.get을 통해 get방식으로 받음을 알 수 있다.
@app.get("/api/sangdata")
def list_sangdata():
    sql = "select code, sang, su, dan from sangdata order by code asc"
    
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    return jsonify({"ok" : True, "datas" : rows})


# 라우팅 정보3 : 상품 자료 추가(crud_create)
@app.post("/api/sangdata")
def create_sangdata():
    data = request.get_json()
    # print("data : ", data)
    code = data["code"]
    sang = data["sang"]
    su = int(data["su"]) # 수량이 연산에 참여하지 않는다면 int는 굳이 필요없다.
    dan = int(data["dan"])

    isql = "insert into sangdata(code, sang, su, dan) values(%s,%s,%s,%s)"

    # db와 flask서버의 연결객체
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(isql, (code,sang,su,dan))
            # isql에 code, sang, su, dan이 차례대로 %s로 들어가서 sql문을 구성한다.
    return jsonify({"ok" : True})

# 요청명이 같더라도 get방식으로 오는 지 혹은 다른 방식으로 오는지에 따라서 수행하는 경로가 다르다!!


# 라우팅 정보4 : 상품 자료 수정하기(crud_update)
@app.put("/api/sangdata/<int:code>")
def update_sangdata(code):
    data = request.get_json()
    
    sang = data["sang"]
    su = data["su"]
    dan = data["dan"]
    usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"

    with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(usql, (sang,su,dan, code))
                # sang, su, dan의 순서가 맞아야 차례대로 %s로 들어간다.
    return jsonify({"ok" : True})


# 라우팅 정보5 : 상품 자료 삭제하기(crud_delete)_이번에는 예외처리(try ~ except ~ finally)도 넣어서 알아보자.
@app.delete("/api/sangdata/<int:code>")
def delete_sangdata(code):
    try:
        dsql = "delete from sangdata where code = %s"
        with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(dsql, (code,)) # code는 튜플자료이기 때문!!
                # sang, su, dan의 순서가 맞아야 차례대로 %s로 들어간다.
                if cur.rowcount == 0:
                    return jsonify({"ok": False, "msg" : "해당자료없음"})
            
        return jsonify({"ok" : True, "msg" : "삭제완료"})

    except Exception as err:
        return jsonify({"ok":False, "msg":str(err)})
    

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
