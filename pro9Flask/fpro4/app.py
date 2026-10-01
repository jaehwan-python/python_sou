from flask import Flask, render_template

app = Flask(__name__)

# 라우팅 정보
@app.route("/")
def index():
    return render_template("index.html")

# 1. condition
@app.route("/condition")
def condition():
    score = 85
    return render_template("condition.html", score = score)

# 2. loop
@app.route("/loop")
def loop():
    users = ["김재환", "유선규", "허준호"]
    return render_template("loop.html", users = users)

# 3. filter
@app.route("/filter")
def filter():
    message = "hello flask jinja2"
    price = 12345 # 이번에는 2개의 변수를 들고 간다
    return render_template("filter.html", message=message, price = price)

# template_filter : Jinja2에는 기본적으로 천단위 콤마가 없다. 그래서 직접 구현하거나 format을 사용한다.
@app.template_filter("format") 
def format_number(value):
    return format(value, ",") # = 넘겨받은 숫자 세자리 마다 , 출력한다


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000);