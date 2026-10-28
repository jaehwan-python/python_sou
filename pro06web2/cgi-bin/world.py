import sys
sys.stdout.reconfigure(encoding = 'utf-8')

v1 = "자료1"
v2 = "두번째 자료"
# 위 2개의 값을 브라우저로 출력하고 싶다.

print("Content-Type:text/html; charset = utf-8")
print('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>메인(제목 수정)</title>
</head>
<body>
    <b>world 페이지</b>
    <br/>
    자료출력 : {0}, {1}
    <br/>
    <img src = "../images/image.jpeg" />
    <br/>
    <a href = "../index.html">메인으로</a>
</body>
</html>
'''.format(v1, v2))

# hello.py에서와는 다른 방식으로 print하였다. 
# html, CSS, JavaScript, *Flask*  ->  팀프로젝트 실시