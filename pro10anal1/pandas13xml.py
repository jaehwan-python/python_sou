# BeautifulSoup 객체로 XML 문서 처리
# 이전에 이순신예제와 교촌치킨예제는 모두 html구조를 사용했다. 만약 xml구조일 때는 어떻게 할까?

from bs4 import BeautifulSoup

# 외부파일을 url로 가져오는 것이 아니기에 requests가 필요없다.

# 1. xml file가져오기 
with open("pandas9my.xml", mode="r", encoding="utf-8") as f:
    xmlfile = f.read()
    print(xmlfile, type(xmlfile))
    # 결과 : <class 'str'> 
# 우선 외부 파일을 일어와서 xmlfile에 저장한다.

# pip install lxml하기


# 2. 가져온 xml파일에 대해서 BeautifulSoup를 사용할 수 있게 해주기
soup = BeautifulSoup(xmlfile, "lxml")
print(type(soup))
# 결과 : <class 'bs4.BeautifulSoup'>


# 3. BeuatifulSoup를 사용할 수 있는(+xml구조가 있는) 객체에서 내가 원하는 자료 뽑아내기
itemTag = soup.find_all("item")
# item 태그를 가진 모든 값을 내놓아라.
print(itemTag)
print()

nameTag = soup.find_all("name")
print(nameTag[1])
print(nameTag[1]["id"]) # name태그로 1번째를 가진 태그의 id는?

print("---------------------")
for i in itemTag:
    nameTag = i.find_all("name")

    for j in nameTag:
        print("id : " + j["id"] + "name + " + j.string)
        tel = i.find("tel")
        print("tel : ", tel.string)

    for j in i.find_all("exam"):
        print("kor : " + j["kor"] + ", eng : " + j["eng"])
    print()

# 아까는 웹에서 데이터(html/xml)를 가져와봤고
# 이번에는 file에서 데이터(html/xml)을 가져와봤다.


print("\n\n 서울시가 제공하는 도서관 xml 문서 정보")

import urllib.request as req
import pandas as pd


# 1. url가져오기
url = "http://openapi.seoul.go.kr:8088/sample/xml/SeoulLibraryTimeInfo/1/5/"

# 2. xml 자료를 가져온 url이기에 request를 사용하여 객체로 만든다.
plainText = req.urlopen(url).read().decode()
# req.urlopen(url) : url로 보낸 응답의 요청을 받기(requests)
# .read() : 응답 본문을 바이트로 읽음
# .decode() : 바이트를 문자여로 변환한다.
# 바이트를 문자열로 바꾸었기에 디코딩 과정이다.

# response = req.urlopen(url)
# data = response.read()
# plaintext = data.decode()
# 위 과정을 풀어쓰면 이것과 같다.
print(plainText)
# 현재도 자료형의 타입이 list이다. beautifulsoup로 바꾸어주어야한다.


# 2. 가져온 url에 BeautifulSoup를 사용할 수 있게 해줌
xmlObj = BeautifulSoup(plainText, "xml")
# lxml을 하게 되면 태그명이 소문자가 된다. 
# 그러니 xml파일에서 데이터를 불러올 때는 lxml을 사용하고
# xml모듈에서 데이터를 불러올 때는 xml을 사용해라 


# 3. 불러온 데이터에 대해서 원하는 데이터 값을 추출한다.
libData = xmlObj.select("row")
# row라는 태그를 가진 모든 값을 뽑기(대신 그안의 자식태그와 텍스트도 뽑힌다.)
print(libData)


# 4. 이제 뽑은 데이터를 정렬 
rows = []
for data in libData:
    name = data.find("LBRRY_NAME").string
    addr = data.find("ADRES").string
    print("도서관 명 : ", name)
    print("주소 : ", addr)
    print()
    rows.append({'도서관명' : name, '주소' : addr })


# 5. 정렬이 된 데이터를 pandas 라이브러리를 사용하여 dataframe구조로 저장
df = pd.DataFrame(rows)
print(df)
# 결과 :             도서관명                                      주소
#           0       BIBLIOTECA                    서울특별시 강남구 도산대로 25길 15-4 1층
#           1  LH강남3단지작은도서관                     서울특별시 강남구 자곡로3길 22 
#           2  [폐관]수서동작은도서관             서울특별시 강남구 광평로 301-4 수서동주민센터 
#           3  休+밤토리SH작은도서관     서울특별시 강남구 밤고개로26길 50(율현동, 강남한신휴플러스6단지)
#           4    강남구립못골도서관                       서울특별시 강남구 자곡로 116

print("건수 : ", len(df))

print()
# html과 xml과 같은 markup 데이터 자료는 BeautifulSoup을 사용할 수 잇지만 JSON데이터 타입은 불가능하다.
