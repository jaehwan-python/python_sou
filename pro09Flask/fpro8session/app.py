from flask import Flask, render_template, request, session, redirect, url_for

# 파이썬 세션은 웹에서 사용자 정보를 서버에 저장하는 기능을 말한다(쿠키를 통해 세션 운영)
# 일반적인 세션은 서버 RAM에 데이터를 저장하고 세션 id만 브라우저에 넘겨준다.
# 그러나 Flask서버는 세션 데이터 자체를 서명도니 쿠키 형태로 브라우저에 전달한다.
# 일정 시간 동안 동일 사용자(브라우저)와 일련의 요청을 하나의 상태로 보고 그 상태를 유지시키는 기술
# 쿠키에 비해 상대적으로 안전함

# 실습 : 사용자가 os를 선택하면 세션에 저장하고 읽기
from datetime import timedelta 
# timedelta : 날짜/시간을 가감해서 기간 설정하기에 효과적
# 시간 간격을 나타낸다
# 이후 아래에서 timedelta(seconds = 5)를 통해 5초동안 서버(세션)을 유지해라는 것을 알 수있다

app = Flask(__name__)
# flask 서버를 사용하는 객체

# Flask는 세션 사용을 위해 secret_key 설정이 필요
app.secret_key = "abcde12345" # 위조 방지용 비밀키 값
# secret_key는 이 쿠키가 위조/변조되었는지 확인하기 위한 서명키이다.
# 참고키값 자동 생성 : 터미널 창에서 > python -c "import secrets; print(secrets.token_hex(32))"
# sample : c3ad87bd89ffb954ba53205e4a14f7f288fa02e345a93413b8d34d0f6b2b7fe7
# 이 값이 변조 여부를 확인할 수 있는 서명용 키가 된다.
# 만약 브라우저에서 사용자가 이를 조작하여 쿠키의 값을 바꾸게 되면 세션은 정상세션으로 인정하지 않게된다.
# 따라서 사용자가 자신의 세션 쿠키 내용을 디코딩해서 내용자체를 볼 가능성이 있다. 하지만 그렇게 봐서 수정하게 되면 서명 키가 수정되어 세션이 정상작동하지 않게 된다.
# 이렇게 참고키값을 만들 수 있다.


app.permanent_session_lifetime = timedelta(seconds=5) # 세션 만료 시간을 5초로 설정 = 5초만 유혀하다
# 영구 세션으로 설정된 세션의 유효기간을 5초로 정함

# 라우팅 정보1
@app.get("/")
def home():
    return render_template("main.html")


# 라우팅 정보2
@app.route("/setos") # route는 기본적으로 get방식을 받는다.
def setos():
    favorite_os = request.args.get("favorite_os") # 사용자가 선택한 운영체제를 받아 기억 -> 아직 안 만들었다.
    # 브라우저가 get요청으로 보낸 데이터("favorite_os")를 request에 임시저장하고 favorites_os에 저장한다.
    # 예를 들어 setos?favorite_os=Windows라고 입력하게 되면 Windows라는 값을 flask서버의 request가 받아서 favorite_os에 저장한다.
    
    if favorite_os:
    # 사용자가 favorites_os를 windows / macos / linux 중 하나로 선택하였다.
        session.permanent = True 
        # 세션 만료 시간 설정 : 앞에서 5초로 정했기에 여기서도 5초로 정해진다.
        session["f_os"] = favorite_os 
        # "f_os"키 : 키로 특정값을 세션에 저장
        # 세션 내용을 직렬화하고 서명해서 세션 쿠키를 생성한다.
        # 이전에는 우리가 resp.set_cookie()로 직접 서버에서 쿠키를 생성하였지다.
        # 하지만 session["f_os"] = favorites_os를 통해 flask가 세션 데이터준비 + secret_key로 서명 + 세션 쿠키 생성 + response에 set_cookie추가 + 브라우저에 전달
        # 이 역할을 모두하게 된다. 
        return redirect(url_for("showos")) 
        # showos를 감싸고 있는 함수를 호출한다. = 클라이언트 브라우저가에서 요청한 것 처럼 생겼다
        # return을 통해서 redirect가 브라우저로 넘어가고 넘어간 redirect값에 의해서 다시 showos를 호출한다
        # return redirect(url_for("showos"))할 때 위에서 session["f_os"]=favorite_os해주었으니까 
        # 브라우저로 쿠키가 같이 넘어가게 된다.
        # # 이때 브라우저에서 내가 보낸 favories_os쿠키도 같이 넘어오게 된다.
    else:
        return render_template("setos.html") 
    # 만약 내가 클릭을 안했다면 favorite_os로 돌아가서 다시 선택해라.


# 라우팅 정보3
@app.route("/showos")
def showos():
    context = {}
    # 빈 dictionary 생성 : 나중에 html에 전달할 데이터를 담는 통

    if "f_os" in session:
    # 현재 session 안에 f_os로 windows가 담겨있다
        context["f_os"] = session ["f_os"]
        # session["f_os"]값인 Windows를 context["f_os"]에 담는다
        # 결과적으로 context = {"f_os" : "Windows"}
        context["message"] = f"당신이 선택한 문명지는 '{session['f_os']}'"
        # 결과 :
        # {"f_os": "Windows",
        #  "message": "당신이 선택한 운영체제는 'Windows'"
        # } 이렇게 context의 dict형태의 자료가 만들어진다.
    
    # 만약 시간(5초)가 지나 세션이 더 이상 유효하지 않게 되면
    else:
        context["f_os"] = None
        context["message"] = f"운영체제를 선택하지 않았거나 세션이 만료됨"
        # 결과 :
        # {"f_os": None,
        #  "message": "운영체제를 선택하지 않았거나 세션이 만료됨"
        # } 이런 context 데이터 형태를 출력함.

    return render_template("showos.html", context = context)
    # 위에서 입력한 context값을 들고 showos.html로 가 html을 수정하여 수정한 html을 브라우저로 보내라


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
    

