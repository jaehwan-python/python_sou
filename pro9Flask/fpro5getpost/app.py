from flask import Flask, render_template, request 
app = Flask(__name__)

# 라우팅 정보
@app.route("/")
def index():
    return render_template("index.html")

# get방식
@app.route("/get_form")
def get_form():
    return render_template("get_form.html")

@app.route("/get_result")
def get_result():
    name = request.args.get("username") # get방식의 username 요청자료 받기(args) # get방식일 때는 args로 자료를 받는다. 
    age = request.args.get("age") # get방식으로 age 요청자료 받기 -> '23'문자 타입으로만 받기
    age = age + "살"
    return render_template("get_result.html", name = name, age = age)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)