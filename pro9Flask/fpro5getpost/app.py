from flask import Flask, render_template, request 
app = Flask(__name__)

# 라우팅 정보
@app.route("/")
def index():
    return render_template("index.html")

# 1. get방식
@app.route("/get_form")
def get_form():
    return render_template("get_form.html")

@app.route("/get_result")
def get_result():
    name = request.args.get("username") # get방식의 username 요청자료 받기(args) # get방식일 때는 args로 자료를 받는다. 
    age = request.args.get("age") # get방식으로 age 요청자료 받기 -> '23'문자 타입으로만 받기
    age = age + "살"
    return render_template("get_result.html", name = name, age = age)


# 2. post방식
@app.route("/post_form")
def post_form():
    return render_template("post_form.html")    

@app.route("/post_result", methods = ["POST"]) # post방식을 사용하려면 methods를 써서 지칭해주어야한다.
def post_result():
    name = request.form.get("username") # get방식과 달리 post방식은 form으로 자료를 받는다.
    email = request.form.get("email") 
    # name은 username을 받고 email을 email을 받아서 post_result.html에 넘겨준다.
    return render_template("post_result.html", name = name, email = email) # post_result.html을 재사용한다. post방식은 age가 없으므로 age는 빼고 email을 넣는다.

# get -> args
# post -> form
#을 사용한다.


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)