# client
from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('192.168.0.19', 7788))
clientsock.send("안녕 반가워".encode())
print('수신자료:', clientsock.recv(1024).decode())

clientsock.close()

# server 실행중 -> client 실행함 -> server가 메시지 수신 후 종료
# 서버는 무한이다
# client 일회용
# 그래서 client prompt에서 계속 수행하면 서버는 걔속 동작을 받는다