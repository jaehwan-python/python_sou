# 1회용 서버
from socket import*

# socket 객체 생성
serversock = socket(AF_INET, SOCK_STREAM) # socket(소켓의 종류를 입력, 소켓의 유형입력)
# ipv4  vs  ipv6  : 32비트와 128비트. ip주소의 개수와 크기이다.

# socket을 이용하여 특정 컴퓨터와 binding(서버의 ip와 port를 연결)해야한다.
serversock.bind(('127.0.0.1', 8888)) # 192.168.0.19라는 내 컴퓨터에서 8888번 포트를 사용할 거야
# 127.0.0.1 local host로 써줘도 된다.
# port번호 확인 : 컴퓨터 안에서 실행되는 특정 프로그램이나 서비스를 구분하기 위한 16비트의 논리적 ip주소이다.
#우리는 포트번호를 8888로 지정함.

# 방화벽 해제하는 방법
# 제어판 -> 시스템 및 보안 -> Windows Defender 방화벽 -> Windows Defendr 방화벽 설정 또는 해제 -> 개인 네트워크 설정 : 방화벽 사용 안함 클릭하면
# 내 컴퓨터의 방화벽이 꺼진다.

# client sever socket communication 검색 ... 원리 이해하기!!

# 우리는 현재 server program을 만들고 있다.
#serversock.bind(('192.168.0.19', 8888)) 

# 연결 대기상태로 전환 = listener 설정
serversock.listen(5) # 연결정보수는 최대 5개까지 허용한다.
print('서버 서비스 중')

# 클라이언트의 접속 대기
conn, addr = serversock.accept() # 수동적으로 연결을 받음 = accept()에서 클라이언트가 접속하기를 기다리고 있는 상태
print('client addr : ', addr)

# 클라이언트가 보낸 data수신
msg = conn.recv(1024).decode()
print('from client message : ', msg)

# 연결 종료
conn.close()
serversock.close()

# 현재 socket과 socket이 정보를 주고 받고 있다.









