# cgi-bin/my.py : 웹용 파이썬 - 클라이언트에서 전송한 값 쉰 

import sys
sys.stdout.reconfigure(encoding = 'utf-8') # 순전히 한글 깨짐 방지를 위해서 사용한다.

import os
import urllib.parse

# 클라이언트가 URL뒤에 ?변수=값&변수=값 하고 주면 환경변수 QUERY_STRING에 넣어준다.
query = os.environ.get("QUERY_STRING", "")
params = urllib.parse.parse_qs(query)
# 문자열을 dictionary 형태로 변환하게 됨
# my.pay?name=tom&age=23   -->   {'name': ['홍길동'], 'age':['23']}

# 값 꺼내기  - 첫번째 값 꺼내기는 [0]
irum = params.get("name", [""])[0] # 값이 없으면 [""]을 사용한다
nai = params.get("age", [""])[0]
print(f"서버에서 출력 : {irum}님은 {nai}살")

print("Content-Type:text/html; charset = utf-8")
print('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>my(제목 수정)</title>
</head>
<body>
    <b>my 페이지</b>
    <br/>
    일반 사용자가 전송한 값 : 이름은{0}, 나이는 : {1}
    <br/>
    자료출력 : {0}, {1}
    <br/>
    <a href = "../index.html">메인으로</a>
</body>
</html>
'''.format(irum, nai))

