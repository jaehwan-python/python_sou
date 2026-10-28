import sys
sys.stdout.reconfigure(encoding = 'utf-8') # 순전히 한글 깨짐 방지를 위해서 사용한다.

import os
import urllib.parse


# get / post 요청 구분
method = os.environ.get("REQUEST_METHOD", "GET")

if method == "POST": # POST일 때
    length = int(os.environ.get("CONTENT_LENGTH", 0))
    body = sys.stdin.read(length)
else: # GET일 때 
    body = os.environ.get("QUERY_STRING", "")


params = urllib.parse.parse_qs(body)

irum = params.get("name", [""])[0]
junhwa = params.get("phone", [""])[0]
gen = params.get("gen", [""])[0]

print("Content-Type:text/html; charset = utf-8")
print('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>friend</title>
</head>
<body>
    <b> **친구정보** </b>
    <br/>
    일반 사용자가 전송한 값 : 이름은{0}, 전화는 : {1}, 성별은 {2}
    <br/>
    <a href = "../index.html">메인으로</a>
</body>
</html>
'''.format(irum, junhwa, gen))
# 넘어가는 데이터가 get과 달리 보이지 않아 보안에 뛰어나다 = post방식
# 반면 get은 모든 정보가 다 보인다.