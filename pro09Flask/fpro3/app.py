# Flask app의 Entry Point
# 라우팅, 서버 실행 담당

# JinJa2 : Flask에서 html을 동적으로 렌더링할 때 사용하는 템플릿 엔진.
# 웹 서버에서 html문을 완성한 후 클라이언트 전송.
# html안에 파이썬 변수를 넣고, 반복.조건문 등을 사용할 수 있게 해주는 도구 = CGI tool로 모두 이런 방식이다.
# Web page - browser - Server - (python) - html 
# 브라우저에서 서버에게 html을 요청하면 서버가 파이썬을 이용해서 html을 전달할 수 있다. 하지만 파이썬이 전달해줄때의 html자료의 문법이 살짝 다르다.

# 그냥 html을 넘길때는 브라우저에서 렌더링(해석)을 했지만 (기존 : 서버가 html자료를 보내면 브라우저가 해석하는 방식)
# templates(폴더)안에 html문을 전달해 줄 때는 브라우저에서 렌더링하지 않고 서버에서 실행이 되어 완전한 html이 확인되면 그때 브라우저로 보낸다. 즉 서버에서 완성시키고 완성된 html문을 보낸다. 
# 이것을 CGI라고 부른다. 브라우저에서 완성시키냐 혹은 서버에서 완성시켜서 브라우저로 보내는냐의 차이다.
# jinja2는 서버에서 완성시켜서 브라우저로 보내는 것이다.

# jinja2 template가 적용된 경우 html이 있는 폴더의 이름은 templates여야 한다.
# jinja2 template가 적용도니 경우 css, js, image자료가 있는 폴더의 이름은 static이어야만 한다.
# 두 폴더의 이름(templates, static)은 고정이다.
# 

from flask import Flask, render_template

app = Flask(__name__)

# 라우팅 요청1
@app.route("/") # 아무것도 없는 현재상태
def home():
    return render_template("home.html") # template폴더 속의 home.html을 불러온다.
# 라우팅의 특징을 url의 port번호 뒤에 입력하면 해당 특징을 가진 라우팅이 실행된다. 

# 라우팅 요청2
@app.route("/hello")
def hello():
    name = "길동이"
    addr = "서초구 서초2동 123"
    return render_template("hello.html", name = name, juso = addr) # 가져올 html이름을 댄다.

# 라우팅 요청3
@app.route("/world")
def world_image():
    return render_template("my.html")



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)