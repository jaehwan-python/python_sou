# css 선택자 사용
from bs4 import BeautifulSoup

html_page = """
<html>
    <body>
        <div id = "hello">
            <a href= "https://www.naver.com/"> 네이버 </a>

            <span>
                <a href= "https://www.daum.net/"> 다음 </a>
            </span>

            <ul class = "world">
                <li> 안녕 </li>
                <li> 반가워 </li>
            </ul>
        </div>

        <div id = "hi" class = "good">
            두번째 div에요!
        </div>
    </body>
</html>
"""

# 지금은 외부 서버에 url을 통해 요청을 하는 것이 아니기에 1,2,번과정은 생략한다. 불러올 데이터에 대해서 곧바로 BeautifulSoup를 사용할 수 있는 객체로 선언한다. 
soup = BeautifulSoup(html_page, "html.parser")
# 이제 soup안에 해당 html_page가 있다고 생각해라

# css 선택자로 tag찾기

print("1. select_one()")
# select_one() :  CSS 선택자 조건에 맞는 '첫 번째' 태그 '하나'를 찾는 메서드

# 1. 
# aa = soup.select_one("div")
# body영역내에 있는 div태그 중 첫번째 div를 보여줘.

# 2. 
# aa = soup.select_one("div#hello")
# div태그 중 "id"가 "hello"인 태그가 나온다.(# : 아이디)

# 3.
# aa = soup.select_one("div.good")
# "class"가 "good"이라면 두번째 div가 나온다.(. : 클래스)

# 4.
aa = soup.select_one("div#hello > a")
# "id"가 "hello"인 div의 직계자식 중 a태그를 고르고 그 중 첫번째 a 태그 요소를 검색
print(aa, aa.string)
# 실제 반환값은 모두 1개이다.
# .string = 해당 tag의 hypertext값을 반환해라


print("\n 2. select()")

# 1. 
bb = soup.select("div")
# 반환값이 복수이다. = 리스트형 자료로 나온다.

# 2.
bb = soup.select("div#hello > ul.world")
# 아이디가 hello인 div 태그에서 '직계'의 클래스가 world인 ul 태그
# 직계(>)

# 3.
bb = soup.select("div#hello ul.world")
# 아이디가 hello인 div 태그에서 '자손'의 클래스가 world인 ul 태그
# 자손( )

# 4. 
bb = soup.select("div#hello ul.world > li")
# 아이디가 hello인 div태그의 '자손' 중에서 / 클래스가 world인 ul태그의 '자식' 중에서 / li태그를 가지는 것

print("bb : \n ", bb)
for i in bb:
    print(i, " ", i.text)
    # bb로 뽑은 각 태그에서 hypertext값을 빼낸다.



# < 예제1 > : 위키백과 - '이순신'
print("예제1 : 위키백과에서 이순신으로 검색된 자료 읽기")
import requests

# 1. url로 가져오기
url = "https://ko.wikipedia.org/wiki/이순신"

# 2. 서버로 요청을 할때 보낼 정보 넣기
headers = {"User-Agent":"Mozilla/5.0"}
# 웹 서버에 요청을 보내는 프로그램의 정보를 전달하려고 작성한다.

# 3. 서버로 보낸 요청을 받아올 객체 생성 ... 해당 객체는 url의 html의 구조 정보(텍스트)를 가지고 있다.
wiki = requests.get(url, headers=headers)
print(wiki.text[:300]) 
# 500자 정도의 markup태그의 text를 가져와라 = 문자열 type
# 가져온 html문 구조가 문자열 구조라서 아무 의미도 없다.

# 4. 가져온 정보가 저장된 객체에 대해서 BeautifulSoup를 사용하여 보다 쉽고 빠르게 태그를 이용하여 정보를 빼냄
soup = BeautifulSoup(wiki.text, "html.parser")

# 5. BeautifulSoup를 사용할 수 있는 객체에 대해서 원하는 Tag를 뽑아낸다.
result = soup.select("p#mwIA")
print(result)
# 이렇게 문자열인 html구조를 해석할 수 잇게 되었다.
# id가 mwIA인 p태그의 내용을 전부 다 보여줘. 
# 그때 해당 자료들은 복수형자료로 반환된다 = list형자료이다
print()


# 6. 가져온 결과(tag)에 대해서 내가 필요한 태그만 놔두고 나머지는 제거하여 남은 tag의 hypertext만 출력 
# 하지만 결과값으로 p#mwIA의 hypertext 뒤에 쓸데없는 부가적인 태그가 많이 존재한다.
for s in result:
    for sup in s.find_all("sup"):
        sup.decompose()
        # 태그 삭제
    print(s.get_text(strip=True, separator= " "))
    # 이렇게 하면 해당 문자열만 출력하고 문자열 앞뒤에 있는 쓸데없는 태그들은 출력되지 않는다.
    # strip=True : 공백과 줄바꿈을 제외시킨다 그때 태그는 제외하고 텍스트만 추출한 것이다.
    # separator = " " : 안전빵으로 적어주기

# 이렇게 위키백과의 한 자료를 읽어올 수 있다. = 웹에서 자료불러오기
print()


# < 예제 2 > : 교촌치킨의 각 치킨 가격들의 평균, 분산, 표준편차 구하기
print("\n\n 예제2 : 교촌 치킨 사이트에서 메뉴와 가격자료를 읽고 평균과 평균대비 다른 치킨들의 가격들이 골고루 분포되어 있는지 확인해보자")
import pandas as pd

# 1단계 
import pandas as pd
url = "https://www.kyochon.com/menu/chicken.asp"
headers = {"User-Agent":"Mozilla/5.0"}
kyochon = requests.get(url=url, headers=headers)
print()
# print(kyochon.text)
# 해당 url의 html자료를 읽음 .. 문자열로

# 2단계 
soup2 = BeautifulSoup(kyochon.text, "html.parser")

# 3단계
# 메뉴명 얻기
names = soup2.select("dl.txt > dt")
# print(names)
# 클래스가 txt인 dl의 태그에서 자식 태그 중 dt태그를 출력하라

# 4단계
# 가격 찾기
prices = [int(tag.text.strip().replace(",",""))
            for tag in soup2.select("p.money strong")]
#           클래스가 money인 p태그의 자손 태그 중 strong태그를 가진 녀석들을 모두 골라라. 
print(prices)
print()

# 5단계
# dataFrame 형태로 표현하기
df = pd.DataFrame({"상품명" : names, "가격" : prices})
# 위에서 얻은 값을 dataframe으로 만들어줌
print(df.head(3))
# 결과 :
#                 상품명         가격
#      0    [간장윙박스20PCS]    23000
#      1    [레드윙박스20PCS]    23000
#      2  [마라레드윙박스20PCS]  23000
print()

# 6단계
# 가격의 평균, 표준편차 구하기
print(f"가격 평균 : {df["가격"].mean():.2f}")
# 결과 : 20422.08

print(f"가격 표준편차 : {df["가격"].std():.2f}")
# 결과 : 5074.23

print()

# 7단계
# 변동계수(cv, 표준편차를 산술평균으로 나눈 값) : 상대적인 변동성을 파악하기 위해 사용된다.
cv = df["가격"].std() / df["가격"].mean() * 100
print(f"가격 변동 계수(cv) : {cv:.2f}%")
# 결과 : 24.85% 
# "가격 변동 계수(상대적인 산포 정도)가 24.84%이므로 각 치킨의 가격들이 평균과 대비하여 가격 대가 적당히 퍼져있는 편이다"


