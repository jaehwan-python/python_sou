
from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for, jsonify
import pymysql
app = Flask(__name__)

# 라우팅 정보1
@app.route("/")
def index():
    return render_template("main.html")

# main.html에서...
# 라우팅 정보2 : legacy를 눌렀을 때
@app.route("/legacy")
def legacy_f():
    pass 
# legacy방법 생략

# 라우팅 정보3 : async를 눌렀을 때
@app.route("/async")
def async_f():
    pass
# async방법 생략

# 라우팅 정보4 : **fetch**를 눌렀을 때
@app.route("/fetch")
def fetch_f():
    return render_template("show3.html")

# 라우팅 정보4-1. DB의 sangdata로 부터 데이터불러오기
@app.get ("/api/sangdata")
def sangdata():
    conn = pymysql.connect(
        host="localhost",
        user = "root",
        password = "123",
        database = "test",
        charset = "utf8mb4"
    )

    cur = conn.cursor()
    cur.execute("select code, sang, su, dan from sangdata")

    # 컬럼명 얻기
    columns = [col[0] for col in cur.description]
    rows = cur.fetchall()
    result = [dict(zip(columns, row)) for row in rows]
    print(result) 

    cur.close()
    conn.close()

    return jsonify(result)
    # jsonify : Flask에서 파이썬 데이터를 JSON 응답으로 만들어서 브라우저에게 보내주는 함수

# 터미널 창에서 값이 뜨게 된다(웹페이지에서 뜨는 것X) :  
# [{'code': 1, 'sang': '장갑', 'su': 3, 'dan': 10000}, {'code': 2, 'sang': '벙어리장갑', 'su': 2, 'dan': 12000}, {'code': 3, 'sang': '가죽장갑', 'su': 10, 'dan': 50000}, {'code': 4, 'sang': '가죽점퍼', 'su': 5, 'dan': 650000}, {'code': 5, 'sang': '물티슈', 'su': 3, 'dan': 1000}, {'code': 6, 'sang': '빼빼로', 'su': 5, 'dan': 1200}]

# 라우팅 정보5 : **axios**를 눌렀을 때
@app.route("/axios")
def axios_f():
    return render_template("show4.html")



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
