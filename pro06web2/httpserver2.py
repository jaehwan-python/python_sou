# CGIHTTPRequestHandler : SimpleHTTPRequestHandler의 확장 클래스
# HTML, CSS같은 정적 파일도 서비스하면서,
# /cgi-bin 아래의 python프로그램 같은 CGI 스크립트도 실행할 수 있게 해주는 클래스.
# get, post 모두 지원 가능
# CGI(Common Gateway Interface) : 웹서버와 외부 프로그램 사이에서 정보를 주고받는 방법이나 규약

from http.server import CGIHTTPRequestHandler, HTTPServer

port = 9999 # 이번에는 9999포트를 쓸 것이다.

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ['/cgi-bin']

def runFunc():
    serv = HTTPServer(('127.0.0.1', port), Handler)
    print('웹 서비스 진행중 ...')

    try:
        serv.serve_forever()
    except Exception as e:
        print('서버종료')
    finally:
        serv.server_close()

if __name__ == "__main__":
    runFunc()

# http://127.0.0.1:9999를 웹에 입력
