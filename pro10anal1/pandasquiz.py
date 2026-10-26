print("--------------- sk하이닉스 상위10위 증권사 df로 표현하기 ------------------------")

from bs4 import BeautifulSoup
import pandas as pd
import requests


# 1단계 : url로 내가 가져오고 싶은 데이터가 있는 웹 지칭하기
url = "https://stock.naver.com/market/stock/kr/stocklist/priceTop"


# 2단계 : 웹으로 요청을 보낼 때 필요한 정보
headers = {"User-Agent":"Mozilla/5.0"}


# 3단계 : 웹으로 데이터를 보내고 응답을 받아올 때 디코딩함
pay = requests.get(url, headers=headers)
# print(pay.text)
# 불러온 자료 전체에서 html을 문자열로만 읽음 = 디코딩하였기 때문


# 4단계 : 문자열 자료(pay.text)를 해석하기 위해서 BeautifulSoup객체를 사용함
soup3 = BeautifulSoup(pay.text, "html.parser")


# 5단계 : 내가 원하는 hypertext가 있는 tag를 자손관계로 가져옴.
tags = soup3.select("div.stock-name-container span.SingleLineText_text__HI_cb")[:10]
# 클래스가 stock-name-container인 div태그의 자손 중에서 클래스가 SingleLineText_text__HI_cb인 span태그 중 상위 10개

print("찾은 태그 수:", len(tags))
# 결과 : 0
# **개발자 도구에서는 종목이 뜨지만 해당 페이지의 원문에서는 보이지 않는 경우
#   requests가 '원문'을 읽기 때문에 request객체가 해당태그를 찾지 못하게 되는 것이다.
#   requests는 서버가 처음 보내준 html을 받는데 개발자 도구의 태그 요소는 js가 실행한 뒤의 구조가 뜨기 때문이다.

# 셀레니움 사용하기


# 6단계
names = [tag.get_text(strip=True) for tag in tags]


# 7단계
data = ({
    "순위": range(1, len(names) + 1),
    "종목명": names
})
# 1번째 부터 11-1번째까지


# 8단계 : df구조로 출력
print()
df = pd.DataFrame(data)
print(df.to_string(index=False))

# df.to_string : DataFrame을 출력용 문자열로 변환
# index=False : 기본 인덱스를 표현하지 않음
