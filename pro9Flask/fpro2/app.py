from flask import Flask, request, make_response

# request : 현재 들어온 http 요청 정보(파라미터, 폼, 헤더, 쿠키)를 담는 객체(브라우저 -> 서버)
# make_response : 응답(response) 객체를 직접 만들어 반환할 때 사용하는 함수(서버 -> 브라우저)

app = Flask(__name__)

# 라우팅 정보
@app.route("/")
def home():
    return "<h2> 홈페이지 </h2> <p> /login으로 이동해 보세요 </p>"

@app.route("/login", methods = ["GET","POST"]) # -> 이제 브라우저가 post방식으로도 요청을 할 수도 있다.
def login():
    if request.method == "GET": # get요청이면
        return  """ 
            <h2> 로그인 페이지 </h2>
            <form action = "/login" method = "post"> <!--get방식으로 입력받은 정보(username)를 다시 /login으로 보내는데 post방식으로 보내겠다. 그럼 아래에 있는 post에 대한 request.method 조건문이 실행된다 -->
                사용자명 : 
                <input type = "text" name = "username" placeholder = "사용자 이름을 입력해용">
                <button type = "submit"> 로그인 </button>
            </form>

            <p> POST 요청 시 username 값을 서버가 받아서 처리한다. </p>
        """    
    elif request.method == "POST": # post요청이면
        user = request.form.get("username", "").strip()
        # username에 적은 이름을 꺼내서(get) user에 저장한다.

        if not user: # user가 없으면 이부분 실행
            return "사용자 이름을 입력하세요 <br>"   "<a href = '/login'> 로그인 화면으로 돌아가기 </a>"

        # 정상 입력 시 -> 로그인 성공 메시지 출력
        message = f"""
            <h2> 로그인 성공!! </h2>
            <p> 안녕하세욥 {user} 회원님. 준비된 서비스마음껏 활용하세요~ </p>
            <a href = '/login'> 메인화면으로 이동 </a>
        """

        return make_response(message, 200)  # 서버가 클라이언트에게 주는 파일은 정상이다~ 임을 명시
                                            # 전송메세지, Http상태코드를 보냄
    
    else:
        return make_response("잘못된 요청", 405)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)


# 파이썬이 따로 만들어진 html자료를 브라우저로 넘긴다. 
# 폴더이름이 templates라고 정해진 폴더에 html을 만든다. 
# = 파이썬으로 html을 불러서 브라우저에 전달한다. ...jinja2