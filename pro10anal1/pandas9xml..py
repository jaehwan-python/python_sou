# pandas는 url을 이용하여 웹상의 csv 파일이나 html표 데이터(markup데이터 구조)를 DataFrame으로 읽기가 가능하다
# XML은 데이터를 태그 형태로 구조화해서 저장/전송하는 문서 형식
# 웹에서 데이터 얻기
# 파일이나 웹에서 csv / excel / xml / json 형식의 데이터를 가져와서 pandas를 이용하여 데이터를 정리하고 읽은 뒤 numpy를 이용하여 수치를 계산한다


import xml.etree.ElementTree as etree
# xml데이터를 읽고 처리하는 라이브러리 = etree로 명명함
from pathlib import Path

# xml파일 구조는 html과 유사하게 생겼다.

# xmlfile = etree.parse("pandas9my.xml") : xml 파일 읽기

xmlfile = etree.parse(Path(__file__).with_name("pandas9my.xml"))
# etree.parse() : xml파일을 읽는 역할을 한다. 
# 현재 파이썬 파일의 경로
print(xmlfile, type(xmlfile))

root = xmlfile.getroot()
# 읽어온 xml에서 최상위 요소를 가져와 root에 저장
# root는 요소객체이고 

print(root.tag)
# 읽어온 xml에서 최상위 요소의 태그를 출력
# root.tag()를 이용하여 '태그의 이름'을 문자열을 저장한다.

print(root[0].tag)
# 읽어온 xml에서 최상위 요소의 자식 태그를 출력

print(root[0][0].tag)
# 읽어온 xml에서 최상위 요소의 자식의 자식 태그를 출력
# [0]을 붙일 때 마다 첫번째 자식으로 한 단계 내려간다.
print()

myname = root.find("item").find("name").text
# root의 자식 중 첫번째 <item>요소를 찾는다.
# 그리고 그 첫번째 <item>에서 첫번째 <name>요소를 찾아서 
# 문자열로 저장한다
mytel = root.find("item").find("tel").text
print(myname + " " + mytel)

print("--------------------------------------------------------------------")

# 외부 파일(xml)파일 읽어 오기
print("\n -- 기상청 제공 XML 자료 읽기")


import requests
# request : 서버에 보내는 요청

# 1. 내가 읽고 싶은 데이터의 url가져오기
url = "https://www.kma.go.kr/XML/weather/sfc_web_map.xml"

# 2. url로 서버에 요청을 할 때 실어보낼 정보
headers = {"User-Agent" : "Mozila/5.0"}
# headers : request로 해당 웹을 열기 위해 서버에게 보내는 요청에 덧붙이는 정보

# 3. res객체를 이용하여 요청준비하기(브라우저 -> 서버)
res = requests.get(url, headers=headers)

# 4. 서버에서 받은 응답의 http 상태 코드 확인 후 오류 발생 시 예외 처리를 함 = 오류가 있는지 확인함.
res.raise_for_status() 
print(res.text, type(res.text)) # < class : str >
# 200 OK → 정상 응답이므로 다음 코드 실행
# 404 Not Found → 페이지를 찾을 수 없어 HTTPError 발생
# 500 Internal Server Error → 서버 오류로 HTTPError 발생

# 5. 최상위 태그를 반환하여 저장 ... 최상위 태그를 반환해서 저장해야 [0]...을 이용하여 하위 태그들을 선택할 수 있기 때문에 제일 처음에 태그를 선택할 때는 최상위 태그를 선택한다
root = etree.fromstring(res.text)
# etree.fromstring : 최상위 태그 선택
print(root)


# {current"} namespace 제거
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]
        # '}'를 기준으로 잘라 태그명만 따옴

# {current"} weather  ->  weather
weather = root.find('weather')
year = weather.get('year')
month = weather.get('month')
day = weather.get('day')
hour = weather.get('hour')
print(f"{year}년 {month}월 {day}일 {hour}시 현재 예보")
# 웹에 있는 정보를 가져옴

# 각 지역 순회
for local in weather.findall("local"):
    name = local.text.strip() # 지역명 (태그 안에 문자열)
    ta = local.get("ta")
    print(f"'{name}'지역의 날씨는 '{ta}'도 입니다.")
# 이는 실시간 데이터이다.

# 1019(월)
# pandas : 데이터 분석을 쉽게 해주는 lib, 데이터를 수집한 후 DataFrame이라는 구조로 만들어 pandas 함수(numpy의 유니버셜 함수)를 사용하여 이를 조작, 분석한다.
# 우리는 file i/o. 
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


