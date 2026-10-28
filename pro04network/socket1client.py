# client
from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('127.0.0.1', 8888))
clientsock.send("안녕 서버".encode())

clientsock.close()

# server 실행중 -> client 실행함 -> server가 메시지 수신 후 종료