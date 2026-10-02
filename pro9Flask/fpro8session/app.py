from flask import Flask, render_template, request, session, redirect, url_for

# 파이썬 세션은 웹에서 사용자 정보를 서버에 저장하는 기능을 말한다(쿠키를 통해 세션 운영)
# 일정 시간 동안 동일 사용자(브라우저)와 일련의 요청을 하나의 상태로 보고 그 상태를 유지시키는 기술
# 쿠키에 비해 상대적으로 안전함

# 실습 : 사용자가 os를 선택하면 세션에 저장하고 읽기
from datetime import timedelta # timedelta : 날짜/시간을 가감해서 기간 설정하기에 효과적

app = Flask(__name__)
# flask 서버를 사용하는 객체

# Flask는 세션 사용을 위해 secret_key 설정이 필요
app.secret_key = "abcde12345" # 위조 방지용 비밀키 값
# 참고키값 자동 생성 : 터미널 창에서 > python -c "import secrets; print(secrets.token_hex(32))"
# sample : c3ad87bd89ffb954ba53205e4a14f7f288fa02e345a93413b8d34d0f6b2b7fe7
# 이렇게 참고키값을 만들 수 있다.

app.permanent_session_lifetime = timedelta(seconds=5) # 세션 만료 시간을 5초로 설정 = 5초만 유혀하다


# 라우팅 정보1
@app.get("/")
def home():
    return render_template("main.html")


# 라우팅 정보2
@app.route("/setos") # route는 get과 post 둘 다 받을 수 있다.
def setos():
    favorite_os = request.args.get("favorite_os") # 사용자가 선택한 운영체제를 받아 기억 -> 아직 안 만들었다.

    if favorite_os:
        session.permanent = True # 세션 만료 시간 설정
        session["f_os"] = favorite_os # "f_os"키 : 키로 특정값을 세션에 저장
        return redirect(url_for("showos")) # showos를 감싸고 있는 함수를 호출한다. = 클라이언트 브라우저가에서 요청한 것 처럼 생겼다
    else:
        return render_template("setos.html") 


# 라우팅 정보3
@app.route("/showos")
def showos():
    context = {}

    if "f_os" in session:
        context["f_os"] = session ["f_os"]
        context["message"] = f"당신이 선택한 문명지는 '{session['f_os']}'"
    else:
        context["f_os"] = None
        context["message"] = f"운영체제를 선택하지 않았거나 세션이 만료됨"

    return render_template("showos.html", context = context)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
    

