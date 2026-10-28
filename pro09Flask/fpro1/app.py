# pip install flask를 터미널 창에 입력한다
# 이제 live server이용하지 않는다.

# pip install waitress # 실무형 서버

# 지금 받는 모든 자료는 브라우저로 간다. 즉 브라우저가 해석할 수 있는 자료로 html tag를 적어도 된다

# 1. 개발용 서버 

from flask import Flask 
# Web Server(Was Application Server) 생성에 필요하다. 현재 http 서버가 아니라 was 서버이다.
# 현재 WAS 서버 : py 프로그램 코드를 실행해서 요청을 처리하는 서버
# 지금까지는 vs code에서 지원하는 live server를 사용하였지만 이제부터는 flask 프레임워크를 사용하여 flask서버를 사용할 것이다. 그래서
# 이제 부터는 open with liveserver를 누르지 않아도 된다.

# Flask 기본 Web 서버는 실무용이 아니라 개발/학습(실습)용이다. = Light Weight Server
# 실무형 서버 : gunicorn, waitress, Nginx ...

# 2. 실무형 서버
from waitress import serve # 실무형 서버 제작


app = Flask(__name__) # flask 객체를 생성. 현재 모듈의 이름을 생성자에 전달

# 라우팅이란?
# 브라우저가 어떤 url 주소로 요청했을 때, Flask가 어떤 python 함수를 실행할지 연결해주는 것


# 라우팅1
@app.route("/") 
# flask가 지원함
# url 매핑이 이루어지고 있다. = 라우팅
# 클라이언트 요청이 '/'일 때 아래 함수 수행
def abc(): # client 요청을 처리(수정하고자하는 정보 전달)하는 핸들러 함수 
    return "<h2> 안녕하세요 </h2> 반가워요"; # client 브라우저에 반환(전달)
# 우리는 라우팅이 된 함수를 뷰함수라고 부른다.

# 라우팅2
@app.route("/about")
def about():
    return "플라스크에 대하여..."


# 라우팅3
@app.route("/user/<name>") # url에 변수의 값이 있는 경우
def user(name):
    return f"네 친구 {name}"

if __name__ == '__main__':
    # app.run() # flask가 지원하는 함수로 실습용 기본 서버로 서비스를 실행함

# 여기까지 적으면 해당 주소의 서버가 터미널 창에 생긴다.
# Running on http://127.0.0.1:5000 이 주소를 복사해서 브라우저에서 실행하면 된다.
# 그때 WAS서버가 생긴다.
# 나가고 싶으면 컨트롤 C를 눌러라

# 127.0.0.1 - - [23/Sep/2026 10:04:41] "GET / HTTP/1.1" 200 -
# 127.0.0.1 - - [23/Sep/2026 10:04:41] "GET /favicon.ico HTTP/1.1" 404
# get방식으로 요청을 하였다. 200 : 통신상태 양호
# favicon 그림은 내가 원하는 대로 꾸민다.

    # 1. 개발(실습)용 서버 생성
    # app.run(debug = False, host = '0.0.0.0', port = 5000) # 위와 동일
    # app.run(debug = True, host = '0.0.0.0', port = 5000) # 수정이 가능한 상태가 된다. 우린 개발을 할 것이기 때문에 debug를 true로 시작한다.

    # 2. 실무형 서버 생성
    print("웹 서버 서비스 중(실무용)")
    serve(app=app, host = '0.0.0.0', port = 8000) # 실무형 서버 생성

# 서버에 동시에 갑자기 여러명이 들어올 때 폭주할 때 server가 안죽게 이용하려면 Nginx를 사용한다

# 우리는 현재 pip install flask와 pip install waitress를 통해서 2개 종류(개발용, 실무용)의 server를 만들 수 있게 되었다

# 브라우저로 가서 url창에 http://127.0.0.1:8000/about 쓰면 라우팅2를 수행하고
# http://127.0.0.1:8000/user/한국인 이라고 쓰면 라우팅 3을 수행한다.
# http://127.0.0.1:8000뒤에 라우팅 정보를 적어주면 내가 적은 요청정보를 서버로부터 받아와서 브라우저가 해석할 수 있다. 이때 서버의 정보가 파이썬이기에 우리는 flask를 사용한다.


