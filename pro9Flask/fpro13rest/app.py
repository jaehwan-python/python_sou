from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for, jsonify

app = Flask(__name__)


# 라우팅 정보1
@app.get("/")
def index():
    return render_template("index.html")


# 라우팅 정보2
@app.get("/api/friend")
def api_friendFunc():
    name = request.args.get("name", "").strip()
    age_str = request.args.get("age", "").strip()
    # get방식으로 요청받은 정보를 request.get에 임시 저장 후 name, age객체에 저장

    # 입력 검증1. name
    if not name:
        return jsonify({"ok" : False, "error" : "name is required"}), 400
        # dict형태의 파일을 json형태로 바꾸어준다.
        # "400" = bad request를 의미한다. = 잘못된 요청이다. = 서버의 문제가 아닌 클라이언트의 요청이 문제이다.  

    # 입력 검증2. age_str
    if not age_str.isdigit():
        return jsonify({"ok" : False, "error" : "age is required"}), 400

    age = int(age_str)
    age_group = f"{(age//10)*10}대" 
    # 23 -> 20대

    # 만약 name과 age가 입력되었을 때 수행 
    return jsonify({
        "ok":True, 
        "name":name,
        "age":age,
        "age_group":age_group,
        "message":f"{name}님은 {age}살이고 {age_group}입니다."
    })



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)