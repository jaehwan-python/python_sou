# 1019(월)
# pandas : 데이터 분석을 쉽게 해주는 lib, 데이터를 수집한 후 DataFrame이라는 구조로 만들어 pandas 함수(numpy의 유니버셜 함수)를 사용하여 이를 조작, 분석한다.
# 우리는 file i/o를 하고 있다.
# 우리는 기상청 web에서 데이터(url)를 가져와봤다.

# 우리는 네이버에서 데이터를 가져올 수 있다.
# 네이버에서 검사를 누르고 select an..을 누르면 해당 버튼들의 정볼르 알 수 있다.
# 대부분의 프로그램은 html데이터구조로 되어 있다.

# beautifulsoup : html, xml구조로 구성되어 있는 웹문서를 읽어들일때 사용되는 강력한 라이브러리이다.
# beautifulsoup를 이용하여 위부 웹문서(html / xml)를 request로 불러온다. 그때 불러온 자료는 str구조가 된다.
# html.parser
# lxml
# xml
# 이 3가지 라이브러리의 차이 장단점 알아두기
# 카페 : 'BeautifulSoup 사용방법 및 웹 문서 스크랩핑'

# BeautifulSoup 객체를 이용한 문서(html, xml)처리 : markup만 처리한다.
import requests
# url로 요청한 정보를 받아오기 위한 객체생성
from bs4 import BeautifulSoup
# BeautifulSoup를 사용하여 해당 웹문서(html / xml)구조를 수월하게 가져옴
# 이전에는 최상위 태그를 지정하여 가져온 후에 그 다음 root[0]하여 그 하부 태그를 계속 지정하여 번거로웠다.
# 하지만 BeautifulSoup을 사용하면 한번에 tag를 지정할 수 있다.


# < 외부 웹에서 html구조의 데이터를 읽어오기 >

# 1. url지정
baseurl = "https://www.naver.com/"

# 2. 정보요청을 할 때 실어갈 데이터 지정
headers = {"User-Agent" : "Mozilla/5.0"}
# 웹서버에 요청을 보낼 때 함께 전달할 정보를 dictionary로 만든것

# 3. request를 이용하여 서버에 요청을 보낼때 html/xml값을 받아올 객체 source 지정
source = requests.get(baseurl, headers=headers)
# 내가 지정한 baseurl로 heeadrers정보를 가지고 요청을 보내라. 
# 네이버 서버에서 받은 응답 객체를 저장하였다

print(source, type(source))
# 결과 : <Response [200]> <class 'requests.models.Response'>

print(source.status_code)
# 결과 : 200

# print(source.text, type(source.text))
# 결과 : 긴 markup구조의 데이터를 받아와서 str로 나타냄 = 그냥 html모양을 나타내는 문자열
# print(source.content)

# 지금처럼 하면 naver url의 markup이 문자열로만 받기 때문에 아무 의미가 없다.
# 즉 이 문자열을 객체로 받아야 해당 객체가 기능을 한다. ... beautifulsoup를 이용한다!

# 4. 받아온 데이터 정보에서 실제 데이터(source.text) 꺼내기
conv_data = BeautifulSoup(source.text, 'html.parser')
# 아까는 받은 naver의 markup을 문자열로 읽었는데 이제는 해당 문자열을 읽어서 html로 해석하였다.
# print(conv_data, type(conv_data))
# <class 'bs4.BeautifulSoup'>

# 이후 soup.find와 같은 메서드(BeautifulSoup의 메서드)로 문자열 형태의 html태그에서 원하는 태그를 찾을 수 있다. 

# 5. 가져온 데이터 정보에 대해서 내가 원하는 tag 값 뽑아내기
for atag in conv_data.find_all("a"):
# html로 해석한 데이터 중에서 "a" tag만 뽑아냄.
    href = atag.get("href") # a태그
    title = atag.get_text(strip = True) # hypertext
    if title:
        print(href)
        print(title)
        print("-----------------------------------")
# naver html에서 atag가 가지고 있는 href와 title을 보여줌 

# 스크랩핑 : 특정 웹페이지 안에서 필요한 데이터를 골라서 추출하는 과정
# 크롤링 : 특정 웹페이지를 찾아다니며 데이터를 수집하는 과정

