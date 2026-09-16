# 서버 서비스는 계속 유지
import socket
import sys

# host = '192.168.00.19' or 'localhost' or '127.0.0.1'
host = '' # 사용 가능한 주소 모두 가능
port = 7788
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversock.bind((host, port))
    serversock.listen(5)
    print('서버(무한 루핑) 서비스 중')

    while True:
        conn, addr = serversock.accept()
        print('client info : ', addr[0], '', addr[1])
        print(conn.recv(1024).decode()) # 수신 메시지 출력
        conn.send(('from server : ', str(addr[1]) + '행운을 빌게').encode)

except Exception as e:
    print('err : ', e)
    sys.exit
finally:
    conn.close()
    serversock.close()

# 문자열을 보내서 문자열을 받음. 이번에는 HTML을 보냄.
# 클라이언트의 요청을 받아 http https를 통해서 html문서, css, java와 같은 웹 콘텐츠를 제공하는 하드웨어 및 소프트웨어 시스템이다.
# web서버의 특징 정리