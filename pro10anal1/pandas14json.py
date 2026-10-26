# JSON 자료를 처리 : XML과 HTML을 사용하는 것에 비해 경량임으로 빠른 처리가 가능하다. 배열 개념만 있으면 된다.
# BeautifulSoup을 지원 하지 않는다.

# json파일의 특징
# 1. 파이썬의 딕셔너리와 비슷하지만, JSON에서는 **true, false, null**을 
#    쓰고 파이썬에서는 **True, False, None**을 씁니다.
# 2. 배열 형태로 표현한 json데이터는 출력하면 *바깥은 list, 안의 각 항목은 dict**가 됩니다.

import json
dict = {"name" : "tom", 
        "age" : 23, 
        "score" : [90, 88, 80]}

print(dict, type(dict))
print("\njson 인코딩 : dict 자료를 str 자료형으로")
# 인코딩 : 문자열을 바이트로 바꾸는 것
# 디코딩 : 바이트를 문자열로 바꾸는 것 - 파일 저장이나 네트워크 전송을 할 때 사용

str_val = json.dumps(dict)
str_val = json.dumps(dict, indent = 4)
print(str_val, type(str_val)) #  < class : str >


# **json 자료에서의 인코딩과 디코딩**

# json.dumps({"name": "홍길동"})    # JSON 인코딩  :         dict        →   JSON 문자열(str)
# json.loads('{"name": "홍길동"}')  # JSON 디코딩  :  JSON 문자열(str)   →         dict

# 나  ->  서버
# : 내 문자열을 내가 인코딩하여 바이트로 전송을 하면 서버가 이 바이트를 받고  디코딩하여 문자열로 처리한다. 
# 서버  ->  나
# 서버가 가진 문자열을 서버가 인코딩하여 바이트로 전송을 하면 내가 디코딩하여 값을 볼 수 있다.

# json / xml / html모두 데이터를 요청을 하고 받는 requests객체에 대해서 인코딩과 디코딩과정을 거친다
# json : json.loads(text)
# xml : etree.fromstring(text)
# html : BeautifulSoup(Text, html.parser) 

# str_val = json.dumps(dict)을 통해서 해당 dict객체를 보내면 서버가 문자열로 받을 수 있게 인코딩 해주었다.

# print(str_val["name"]) # dict 명령을 할 수 없다. string만 가능 ... TyperError
print(str_val[0:20])
# 내가 보낸 요청을 받아올때 0번째부터 19번째까지만 출력해
# 문자열 관련 함수만 처리가능하다.

print("\n\n 디코딩 : str  ->  dict로 변환")
json_val= json.loads(str_val)
print(json_val, type(str_val))
print(json_val["name"]) 
# dict관련 명령어 처리기능
print()

for k in json_val.keys():
    print(k)

for v in json_val.values():
    print(v)

print("--------------------------------------")
print("\n\n 서울시가 제공하는 도서관 xml 문서 정보")

# 1단계
import urllib.request as req
import pandas as pd
url = "http://openapi.seoul.go.kr:8088/sample/json/SeoulLibraryTimeInfo/1/5/"
plainText = req.urlopen(url).read().decode()
# print(plainText)
# 여기서 json데이터 타입은 BeatifuleSoup를 사용할 수 없다.
# response = req.urlopen(url)   # ① 서버로 요청을 보내고 응답 받기 .. 그때 응답은 서버가 인코딩을 하여 보내기 때문에 바이트형식으로 온다.
# data = response.read()        # ② 응답 본문을 바이트(bytes)로 읽기 .. 서버가 보낸 바이트 응답을 읽는다.
# plainText = data.decode()     # ③ 바이트를 문자열(str)로 변환한다. .. 그리고 그 바이트 응답을 문자열로 바꾼다.
# 결국 plainText는 문자열을 가진다.

# 2단계
# str로 읽은 파일을 json파일(dict형태)로 바꾸었다.
jsonData = json.loads(plainText) 
# 해당 받은 문자열로 받은 데이터(문자열)를 dict로 받기 위해 디코딩을 해줌

# json타입으로 디코딩
print(jsonData["SeoulLibraryTimeInfo"]["row"][1]["LBRRY_NAME"])
# 결과 : LH강남3단지 작은도서관
#  jsonData = { "SeoulLibraryTimeInfo" : { "row": [{"LBRRY_NAME": "첫 번째 도서관"},
#                                                  {"LBRRY_NAME": "LH강남3단지 작은도서관"}]
#                                        }
#             }
# print(jsonData["SeoulLibraryTimeInfo"].get("row"))

print()
# dict의 get()사용 
libData = jsonData.get("SeoulLibraryTimeInfo").get("row")
# print(libData)
name = libData[0].get("LBRRY_NAME")
print(name) 
# 결과 : BIBLIOTECA

print()

# .get()은 ()안에 키의 이름이 들어가고 그 키의 값을 뻬온다.
datas = []
for ele in libData:
    name = ele.get("LBRRY_NAME")
    tel = ele.get("TEL_NO")
    addr = ele.get("ADRES")
    print(name, " ", tel, " ", addr)
    datas.append([name, tel, addr])

df = pd.DataFrame(datas, columns=["도서관명", "전화", "주소"])
print(df)
# 결과 : 
#               도서관명            전화                                      주소
#   0          BIBLIOTECA                                  서울특별시 강남구 도산대로 25길 15-4 1층
#   1    LH강남3단지작은도서관   02-459-8700                     서울특별시 강남구 자곡로3길 22 
#   2    [폐관]수서동작은도서관  02-3423-8584            서울특별시 강남구 광평로 301-4 수서동주민센터 
#   3    休+밤토리SH작은도서관   02-2226-7942     서울특별시 강남구 밤고개로26길 50(율현동, 강남한신휴플러스6단지)
#   4     강남구립못골도서관     02-459-5522                       서울특별시 강남구 자곡로 116