# cgi-bin/hello.py : 웹 전용 파이썬이다.
import sys
sys.stdout.reconfigure(encoding = 'utf-8') # 한글깨짐 방식 - 미국인들은 쓸 필요가 없다.

ss = "파이썬 자료 출력" # 파이썬 실행문
# print(ss) # 개발자가 자신의 컴퓨터의 표준 출력장치로 값을 출력

ss2 = 123 + 200 # 파이썬의 실행문 : 파이썬의 변수의 값을 기억하고 있다.
# 클라이언트 브라우저로 파이썬 처리 값을 출력한다.

print("Content-Type:text/html; charset = utf-8")
print()

# 아래 5문은 고정이다.
print("<!DOCTYPE html>")
print("<html lang='ko'>")
print("<head>")
print("<meta charset='UTF-8'>")
print("</head>")

print("<html>")
print("<body>")
print("<<h2>파이선 문서의 자료 출력</h2>")
print(f"파이썬 변수 값1 : {ss}<br/>")
print(f"파이썬 변수 값2 : {ss2}<br/>")
print("</body>")
print("</html>")
