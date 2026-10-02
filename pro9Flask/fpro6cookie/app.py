from flask import Flask, render_template, render_template_string
from flask import Flask, request, make_response, redirect, url_for
# redirect : 브라우저르 다른 url로 이동시키는(302) 리다이렉트 응답 생성
# url_for : 라우팅 함수의 url을 안전하게 생성하는 함수
# render_template_string : 문자열로 된 html을 렌더링(반환))하는 함수 = 문자열로 작성한 jinja템플릿을 렌더링하여 html로 변환하는 함수


app = Flask(__name__)

# 간단 html : text로 작성
HOME_HTML = """
    <h2> Flask Cookie Text </h2>
    
    <form action="/set_cookie" method="post">
        쿠키값 : <input type = "text" name = "name" placeholder = "예:hong">
    <button type = "submit"> 쿠키저장 </button>
    </form>

    <p>
        <a href = "/read_cookie"> 쿠키읽기 </a> |
        <a href = "/delete_cookie"> 쿠키삭제 </a>
    </p>
    """ 
    #text로 작성한 형태의 html이다.

# 각 브라우저의 쿠키의 위치는 검색하면 나온다. 크롬은 개발자도구 -> application -> storage -> cookies에 들어가면 확인 가능하다. 자신의 정보를 담아두어야 하기 때문이다. 
# naver에 들어가서 검사 -> application -> storage -> cookies에 들어가면 naver의 쿠키를 확인할 수 있다. = 서버가 클라이언트(브라우저)에게 정보를 저장해둠. 


# 라우팅 정보
'''
@app.route("/")
def index():
    return render_template_string(HOME_HTML)
'''

# 라우트라고 쓰면 범용적이고 해당 정보 취득 방식을 아래처럼 적어줘도 된다(get, post)
# 1. get방식
@app.get("/")
def home():
    return render_template_string(HOME_HTML)

# 2. post방식
@app.post("/set_cookie")
def set_cookie():

    # 1. 쿠키저장
    irum = request.form.get("name", "anonymous") # form으로 받은 name값을 가져온다.


    # 2. 응답객체 생성
    # 클라이언트에 쿠키를 심으려면 응답 객체가 필요하다
    # 먼저 "read_cookie" url로 redirect하는 응답 객체를 생성한다."
    # 그 응답에 따라 쿠키를 추가한 뒤 브라우저에 돌려준다.
    
    # res = make_response(redirect("/read_cookie")) 
    # 프로그램 상에서 클라이언트가 redirect되는 것처럼 보이지만 실제로는 브라우저가 redirect되는 것이다. --- 중요!!

    resp = make_response(redirect(url_for("read_cookie"))) # url_for() : 라우팅 함수의 url을 안전하게 생성하는 함수
    # url_for() : 라우팅 함수의 url을 안전하게 생성하는 함수
    # 위 요청과 동일하다. = 아래 a태그를 클릭하면 브라우저가 /read_cookie로 이동하는 것과 동일하다.
    # url_for("함수명")

    # res = make_response(redirect("/read_cookie"))   ->    @app.get("/read_cookie") : @app.get("/read_cookie")에서 라우팅이름이 바뀌면 안된다. url_for("read_cookie")는 라우팅이름이 바뀌어도 똑같이 수행된다.
    # res = make_response(redirect(url_for("read_cookie")))   ->   def read_cookie() : @app.get("/read_cookie")의 /read_cookie의 이름이 바뀌어도 항상 똑같이 아래 url_for가 수행된다.

    # 원래라면 브라우저의 url에서 데이터를 요청해야하지만 rediret를 사용하면 브라우저의 url에서 데이터를 수행하지 않고 서버가 브라우저에게 


    # 3. 쿠키 이름 지정 = # 쿠키를 심는다.
    resp.set_cookie(
        key = "name", # 쿠키 이름
        value = irum, # 사용자가 전송한 값을 쿠키에 저장
        max_age = 60*5, # 쿠키의 유효기간을 5분으로 설정(일반적으로 1년)
        httponly = True, # 자바스크립트에서 쿠키를 읽지 못하도록 설정(보안)
        samesite = "Lax" # 크로스 사이트 요청 위조(CSRF) 공격 방지 -> web 브라우저는 공격 노출에 쉽다.
    )

    return resp 
    # 쿠키가 포함된 응답을 브라우저로 반환 
    # 클라이언트 컴퓨터(하드디스크)에 저장된다.
    # 브라우저는 쿠키를 저장하고, redirect 요청에 따라 read_cookie로 다시 요청한다.



# a. 쿠키 읽기
@app.get("/read_cookie")
def read_cookie():
    # 브라우저가 요청에 실어 보낸 모든 쿠키 중에서 내 서버가 만든 쿠키(name)을 꺼낸다
    # 만약 없으면 None을 반환한다.
    
    name = request.cookies.get("name") # 브라우저가 요청에 실어 보낸 모든 쿠키 중에서 내 서버가 만든 쿠키(name)을 꺼낸다. 만약 없으면 None을 반환한다.

    return f"""
        <h3> 쿠키 읽기 </h3>
        <p> value 쿠키 값 : {name}값 </p>
"""

# b. 쿠키 삭제
@app.get("/delete_cookie")
def delete_cookie(): # 쿠키 삭제 후 홈(/)으로 이동하기 위해 redirect 응답을 만듦

    resp = make_response(redirect(url_for("home")))
    resp.delete_cookie("name")
    return resp


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)