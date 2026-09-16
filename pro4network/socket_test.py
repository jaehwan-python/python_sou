# 네트워크 : 두 대 이상의 컴퓨터나 장치를 서로 연결하여 데이터를 주고 받을 수 있다.

# 네트워킹(행위) : 두 대 이상의 컴퓨터를 연결하여 네트워크를 만들고, 연결하고, 통신하게 하는 모든 활동 
#                 = PC와 서버연결, TCP/IP 통신(컴퓨터와 컴퓨터 사이에서 데이터를 주고받을 때의 약속), socket통신(socket이라는 프로그램을 이용하여 통신을 한다), 인터넷 연결...
# ex) http : html, css, json, javaScript, XML등의 data를 주고받을 수 있도록 하는 통신규약
# python의 Web Lib를 이용하면 Web을 만들 수 있지만 가장 많이 쓰는 것은 Flask와 FastAPI이고 우리는 Flask를 쓸 것이다. 전문적으로 Web을 만들기 위해서는 Django를 사용한다.

# socket : 소켓(socket)은 프로세스가 네트워크 세계로 데이터를 내보내거나 혹은 그 세계로부터 데이터를 받기 위한 실제적인 창구 역할을 한다.
# 그러므로 프로세스가 데이터를 보내거나 받기 위해서는 반드시 소켓(socket)을 열어서 소켓(socket)에 데이터를 써보내거나 소켓(socket)으로부터 데이터를 읽어들여야 한다.
# 프로그램과 프로그램이 네트워크를 통해 데이터를 주고받기 위해 사용하는 연결 지점 + socket이란 TCP/IP의 프로그래머 인터페이스이다.
# 통신 기기간 대화가 가능하도록 하는 통신방식으로 클라이언트/서버 모델에 기초한다.
# 프로그램 상에서는 소켓(socket)을 이용하여 데이터를 주고받을 수 있도록 통신한다. -> 클라이언트/서버 모델에 기초한다.
# TCP는 통신상태를 확인하고 양호하면 통신을 한다. 그래서 느리다.

# https://daum.net:80/index.html -> 분석해서 역할을 해석해보기
# :80/index.html
# TCP : 연결을 맺고 신뢰성 있게 데이터를 전달하는 연결지향 프로토콜
#     : 클라이언트 프로그램(socket)  ->  네트워크  ->  서버 프로그램(socket) 
#     ex) 인터넷
# UDP : 연결없이 빠르게 데이터를 전달하는 비연결지향 프로토콜

# -------------------------------------------------------------------------------------------------------------------------------------------------
# 이번시간에는 인터넷에서 데이터를 가져온다.

# "지금까지는 전문가들이 만들어 둔 server를 이용했다면 이번에는 인터넷 server를 직접 구축해볼 것이다."

# 인터넷상에서 데이터를 주고받으려면 무조건 socket이라는 것이 있다. 그렇게 데이터를 주고받으면 인터넷 server를 구축하고 마지막에는 Flask lib를 이용하여 
# 인터넷 서버를 구축하는 것이다.
# 첫번째 프로젝트 : 인터넷 서버를 만들어서 인터넷 서비스를 만드는 것 = Web Project

# socket 통신 확인
import socket

# 서비스 이름과 프로토콜 이름을 사용해 서비스 기본 port 확인
print(socket.getservbyname('http', 'tcp')) # 80
print(socket.getservbyname('https', 'tcp')) # 443 ... 해당 서비스명과 프로토콜을 사용하여 port번호를 확인할 수 있다.
# getservbyname : socket(import socket)이 지원하는 메서드

print(socket.getservbyname('http', 'tcp'))   # -> 80 : WWW
print(socket.getservbyname('https', 'tcp'))  # -> 443
print(socket.getservbyname('ftp', 'tcp'))    # -> 21 : 파일 전송
print(socket.getservbyname('ssh', 'tcp'))    # -> 22 : 원격 컴퓨터 접속
print(socket.getservbyname('smtp', 'tcp'))   # -> 25 : 메일 송수신
print(socket.getservbyname('pop3', 'tcp'))   # -> 110 : 이메일 서버 서비스 
print()

# 특정 Web서버의 ip주소 확인
print(socket.getaddrinfo('www.naver.com',80, proto = socket.SOL_TCP))
# [(<AddressFamily.AF_INET: 2>, 0, 6, '', ('223.130.192.248', 80))] 
#          주소체계,       소켓타입(0), 프로토콜 번호(6), 실제접속주소  
# 전세계에 naver 서버가 구축되어 있다. 그 주소가 223.120.192.248이다. 각 지역에 있는 naver web server를 구축해두었다.
# 우리는 서울에 있는 naver web server로 연결이 된다. 만약 서울의 server가 죽으면 가까운 지역의 server가 나에게 service를 해준다.
# web server는 한 대만 존재하지 않고 각 기업별로 많다.
# Web server는 방화벽을 잘 설치하여 pw와 username을 보안상으로 잘 구축해두어야한다.

