# web server : html서비스가 가능한 서버
# 클라이언트(웹 브라우저)의 요청을 받아 http https를 통해 HTML, 이미지, CSS, JavaScript 같은 정적 웹 콘텐츠를 제공하는 하드웨어 및 소프트웨어 시스템

# 단순한 HTTPServer 구축 - 기본적인 socket 연결

from http.server import SimpleHTTPRequestHandler, HTTPServer

port = 7777 #우리가 쓸 수 있는 port번호도 제한적이다 찾아보기

# get요청에 대해 문서를 읽어 client로 전송하는 역할을 한다.
handler = SimpleHTTPRequestHandler

# HTTPServer 객체 생성
serv = HTTPServer(('127.0.0.1', port), handler)
print('웹 서비스 시작!')

# 하염없이 기다리게 하여 무한 루프에 빠트려야 한다.
serv.serve_forever() # 웹서비스가 무한루프에 빠짐 ... 여기까지하고 
# 파워쉘에서 python httpserver1.py를 입력하면 웹 서비스 시작!하면서 대기상태
# 그리고 웹에서 실행해 본다.

# -- 이렇게 server를 하나 만들었다. 
# http://192.168.0.19:7777을 입력하면 web생성됨
# http://192.168.0.19:7777/abc.html을 입력하면 내가 만들어 둔 각각의 html자료가 생성된다. 이름은 '웹'

# 다음이나 네이버는 80을 안써도 된다. 이미 다른 서버가 80을 쓰고 있기 때문이다.
# http://192.168.0.19:7777/abc.html -> 이거를 '브라우저'가 해석을해서 보여주는 역할을한다. 즉 브라우저는  HTML, 이미지, CSS, JavaScript 같은 정적 웹 
#                                      콘텐츠를 해석하여 보여준다.
# 브라우저는 기본적으로 소켓을 내장하고 있다. 내가 만든 웹도 소켓을 가지고 있다. 소켓과 소켓이 통신을 하여 코드를 해석한다. 
# 이렇게 서버가 클라이언트에게 요청하는 방식은 모두 get방식이다. 
#  