# Beautifulsoup 객체 메서드 이해

from bs4 import BeautifulSoup


# 외부 웹페이지의 자료를 직접 가져오면 해당 구조를 이해하기 힘드니(데이터를 text형식으로 가져오기 때문에!) 직접 markup구조의 데이터인 html을 만들어보자.
html_page = """
<html>
    <body>
        <h1> 제목 태그 </h1>
        <p> 웹 문서 연습 </p>
        <p> 원하는 자료 읽기 </p>
    </body>
</html>
"""

print(type(html_page)) 
# 결과 : <class 'str'>
# 이건 단순히 해당 html구조를 str 타입으로만 보여줌 = 현재 '문자열' 타입이다

# 이번에는 url을 지정하여 가져오는 것이 아니기 때문에 
# 1. url지정
# 2. headers지정
# 을 안한다
# 서버에 요청을 하는 것이 아니기에 requests도 사용하지 않는다.

# 1. 해당 문자열 형태의 html_page를 가져와서 BeautifulSoup라이브러리를 사용할 수 있는 soup 객체에 저장
soup = BeautifulSoup(html_page, 'html.parser')
# 이 객체가 중요!! ㅈㄴ 중요!! ... 그래야 html을 해석할 수 있다.
# BeautifulSoup이 사용하기 위한 객체를 만들어줌
# 이 객체는 문자 형태의 markup자료구조를 해석할 수 있다.
print(type(soup))
# 결과 : <class 'bs4.BeautifulSoup'>

print()

# 예시 1
h1 = soup.html.body.h1
# body태그 내의 h1태그를 부름
print("h1 : ", h1.string)

# 예시 2
p1 = soup.html.body.p
# body태그 내의 p태그를 부름
# 지금 자료구조에서 p태그는 2개인데 최초의 p태그 hypertext만 보여준다.
print("p1 : ", p1.string)

# 예시 3
p2 = p1.next_sibling.next_sibling
# html - body - h1
#             - p
#             - p
# 이런 형태의 dom구조에서 next_sibiling과 previous_sibiling 관계를 획득한다.(DOM구조를 이용함)
# 동일한 다음의(이후) p태그의 값을 얻기 위해서는 next_sibiling을 얻는다. 
# 동일한 태그에 대해서 이전의 값을 얻기 위해서는 previous_sibiling을 쓴다.
print("p2 : ", p2.string)
# 그때 출력한 값들은 해당 태그들을 단순히 문자열로만 바라보지 않고 직접 markup구조를 해석하여 해당 hypertext의 값을 가리킨다.
# BeautifulSoup의 역할이다!!




print("\n----------------------------------------------")
html_page2 = """
<html>
    <body>
        <h1 id="title"> 제목  <b> 태그를 </b> 태그2 </h1>
        <p> 웹 문서 연습2 </p>
        <p id="my" class="our"> 원하는 자료 확인2 </p>
    </body>
</html>
"""
# 이번에는 tag에 id와 class를 주었다.

soup2 = BeautifulSoup(html_page2, 'html.parser')
# 형식 : find(tag명, attrs, recursive, string) 
# 위에서처럼(p1 = soup.html.body.p) 각 태그가 의미하는 모든 걸 입력하면 비효율적이다. 그래서 find를 사용한다.
# recursive : 자손태그

print(soup2.p, ' ', soup2.p.string)
# 이건 너무 비효율적 ... 을 계속 써주어야 한다.

# .string : 해당 태그의 hypertext값을 의미한다.

# < find() > 
print(soup2.find("p").string)
# soup2 객체에서 문자열로 적혀있는 최초(find)의 p태그의 hypertext값을 찾아라

print(soup2.find(["p", "h1"]).string)
# 이런 식으로 여러 개 태그에 대해서 hypertext값을 나타낼 수도 있다.
# : 두 태그 중 먼저 나오는 태그를 선택하여 hypertext값을 나타낸다. 
# 두 개의 tag를 모두 나타내는 것은 아니다.
# 이는 None을 반환한다. 
# -> p태그와 h1태그 중에서 먼저 있는 태그가 반환되고 거기서 hypertext가 나온다. 
#    하지만 그때 hypertext속에 또 태그가 있기에 None이 반환된다.

print(soup2.find(["p", "h1"]).get_text())
# 내가 지정한 태그의 하위태그에 있는 hypertext까지 모두 추출한다.

print(soup2.find("p", id = "my").string)
print(soup2.find(id = "title").string)
# id로 찾기
# element에 상관없이 id가 my / title인 태그의 hyptertext(.string)값을 추출한다.

print(soup2.find(class_ = "our").string)
# class로 찾기
# 속성중 class가 our인 태그를 찾아서 해당 태그의 hypertext(.string)값을 추추랗ㄴ다.


# 해당 태그를 attrs = dict형태로 찾기
print(soup2.find(attrs = {"class" : "our"}).string)
# 이런 식으로 클래스에 해당하는 태그를 찾을 수 있다.
# attrs는 태그가 가진 속성 조건을 지정한다.
# class = "our"인 태그를 attrs로 찾는다.

print(soup2.find(attrs = {"id" : "my"}).string)
# 이런 식으로 아이디에 해당하는 태그를 찾을 수도 있다.
print()




print("\n-------find_all(), findAll() 메서드 사용 -----------")
html_page3 = """
<html>
<body>
    <h1 id="title"> 제목  <b> 태그를 </b> 태그3 </h1>
    <p> 웹 문서 연습3 </p>
    <p id="my" class="our"> 원하는 자료 확인3 </p>
    <div>
        <a href = "https://www.naver.com/"> 네이버 </a>
        <a href = "https://www.daum.net/"> 다음 </a>
    </div>
</body>
</html>
"""

soup3 = BeautifulSoup(html_page3, 'html.parser')
print(soup3.find_all(['a']))
# 모든 a태그를 list형식으로 잡아들인다.
# 결과 : [<a href="https://www.naver.com/"> 네이버 </a>, <a href="https://www.daum.net/"> 다음 </a>]
print()

print(soup3.find_all(['a', 'p']))
# 모든 a태그와 p태그를 list형식으로 잡아들인다.
# 결과 : [<p> 웹 문서 연습3 </p>, <p class="our" id="my"> 원하는 자료 확인3 </p>, <a href="https://www.naver.com/"> 네이버 </a>, <a href="https://www.daum.net/"> 다음 </a>]
print()

links = soup3.find_all("a")
# print(links) = print(soup3.find_all(['a']))
# find_all은 return하는 값의 type이 복수로 list형태가 출력된다. 
# 그래서 for문으로 반복문이 가능하다!!

for i in links:
    href = i.attrs["href"]
    text = i.text 
    # i.string과 같다.
    print(href, " ", text)

print('\n 정규표현식 사용')

import re
# 문자열에서 특정 패턴을 찾는 정규표현식 모듈을 가져오는 코드 = 지금부터 정규표현식 시작~
links2 = soup3.find_all(href=re.compile(r"^htps"))
# print(links)
# 결과 : [<a href="https://www.naver.com/"> 네이버 </a>, <a href="https://www.daum.net/"> 다음 </a>]
for k in links:
    print(k.attrs["href"])

print("==============================================================================")

# 이번에는 웹사이트에서 내가 원하는 정보를 읽어보자
print("\n 벅스 사이트에서 음악 순위 읽기 .. 벅스 사이트의 url이 필요")
import requests
url = "https://music.bugs.co.kr/chart"
response = requests.get(url)
print(response.text)
# response.txt는 벅스 사이트의 makeup구조를 '문자열'구조로 보여준다!!
# 우리는 저 문자열을 해석하기 위해서 BeautifulSoup를 사용한다.
bsoup = BeautifulSoup(response.text, 'html.parser')
# markup 문자열을 해석하기 위한 BeautifulSoup객체 생성 
musics = bsoup.find_all("td", class_ = "check")
# 페이지 검사에서 해당 태그를 select an으로 보면 '음악순위'가 check라는 클래스를 가짐을 알 수 있다.

for idx, music in enumerate(musics):
# 반복할 때 순서 번호(idx)와 값(music)을 함께 꺼내 주는 파이썬 기본 함수
    print(f"{idx + 1}위 {music.input["title"]}")
    # music 객체 안에 있는 첫번째 <input>이라는 태그를 찾는다.
    # 거기서 title속성값을 가져온다.  
    # 아마 <input title="좋은 날" value="123"> 이렇게 생겼을 것이다.

    # 강사님 쉑쉑버거에서 단거 먹는거 좋아함.

