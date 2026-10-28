from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for

app = Flask(__name__)

# 이제는 외부에서 쿠키의 허용시간을 지정한다.
COOKIE_AGE = 60*60*24*7 # 쿠키는 7일간 살아있다


# 라우팅 정보1
@app.get("/")
def index():
    return render_template("index.html") 

# get방식으로 index.html을 브라우저에 전달한다.


# 라우팅 정보2
@app.get("/login")
def loginFunc():
    name = request.cookies.get("name")
    visits = request.cookies.get("visits")

    # 1. name의 유무 확인 = '계산'
    if name: # name이 존재하면...
        visits = int(visits or "0") + 1 # visits가 존재하면 int로 변환하고, 존재하지 않으면 0으로 초기화 후 +1
        msg = f"안녕하세요. {name}님! 방문횟수는 {visits}회 입니다."
    else: # name이 존재하지 않으면...
        visits = None
        msg = "이름을 입력하면 방문 횟수를 쿠키로 기억합니다"

    # 로그인 상태면 visits 쿠키를 증가시키고, 로그인 상태가 아니면 visits 쿠키를 초기화한다.

    resp = make_response(render_template("login.html", name = name, msg = msg, visits = visits))

    # 2. 로그인 상태(name이 존재할 때...)면 visits 쿠키 갱신 = '저장'
    if name:
        resp.set_cookie("visits", str(visits), max_age=COOKIE_AGE, httponly=True, samesite="Lax")
    else:
        resp.delete_cookie("visits")

    return resp



# 라우팅 정보3
@app.post("/login")
def logoutFunc():
    name = (request.form.get("name") or "").strip() # strip() : 앞뒤 공백제거
    resp = make_response(redirect(url_for("loginFunc"))) # get방식으로 다시 라우팅 정보2의 loginFunc를 요청한다.
    resp.set_cookie("name", name, max_age = COOKIE_AGE, samesite = "Lax")
    resp.set_cookie("visits", "0", max_age = COOKIE_AGE, samesite = "Lax")    
    return resp


# 라우팅 정보4
@app.post("/logout")
def loginFunc():
    # login(get)으로 이동
    resp = make_response(redirect(url_for("loginFunc")))

    # 쿠키 삭제
    resp.delete_cookie("name")
    resp.delete_cookie("visits")
    return resp


# get방식으로 브라우저가 입력한 특정 값을 서버가 받아서 쿠키로 저장하고, 브라우저에게 다시 전달한다. 그럼 그 전달받은 html문을 브라우저가 해석하여 출력한다.

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)