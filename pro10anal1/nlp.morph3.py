# 이번에는 외부 웹(donga.com)에서 가져온 데이터(긴 글)에서 특정 단어 관련 문서를 검색한 후 명사만 추출하여 해당 명사의 갯수를 워드클라우드로 시각화 해보자.
# 워드 클라우드 그리기를 위해서는
# pip install simplejson pytagcloud ... 설치 실패 ㅅㅂ

# ... 
# 그래서 구글드라이브에 강사님이 만들어 두신 pygame.zip을 다운로드하여 압축풀고 나서 해당 파일들을 우리 가상환경의 라이브러리에 '직접' 넣어준다. 
# 해당경로를 아래와 같다.
# C:\Users\user\anaconda3\envs\myproject\Lib\site-packages 여기에
# 넣어주고 나면 이제 우리 vs code에서 import pygame을 하면 곧바로 사용할 수 있다.
import pygame

from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request
from konlpy.tag import Okt
from collections import Counter
# 단어 수를 세는 라이브러리

import pytagcloud 
# 처음에 노란 줄이 뜬다. 그러면
# 터미널 창에 pip install simplejson pytagcloud 를 입력하면 이제 설치가 된다. 
# C:\Users\user\anaconda3\envs\myproject\Lib\site-packages에 pytagcloud폴더가 생겼다.
# site-package에 있는 걸 불러왔다.
import matplotlib.pyplot as plt
import koreanize_matplotlib
# 한글깨짐 방지
import matplotlib.image as mpimg
import webbrowser
import pandas as pd
import numpy as np


searchWord = input("검색어 : ")
print(quote(searchWord)) 
# 인코딩을 위해 quote를 써주었다.
# 검색어는 "가을"로 해라.


target_url = "https://www.donga.com/news/search?query=" + quote(searchWord)
# 이 url로 해당 페이지로 갔다. = 검색창에 "가을"을 입력했을 때 나오는 화면

source_code = urllib.request.urlopen(target_url)
# print(source_code)


soup = BeautifulSoup(source_code, 'lxml', from_encoding='utf-8')
# 우리가 가져온 url이 xml파일일 수도 있으니 
# pip install lxml을 터미널 창에 입력한다.
# soup = BeautifulSoup(source_code, 'html-parser', from_encoding='utf-8')
print(soup)


# 스크래핑 : 웹페이지에서 제목, 본문, 가격 등 필요한 데이터를 추출하는 작업
# 크롤링 : 웹페이지의 링크를 따라 여러 페이지를 돌아다니며 정보를 수집하는 과정


msg = ""

for title in soup.find_all("h4", class_="tit"):
    title_link = title.find("a")
    # print(title_link)
    # 이건 스크래핑이 아니라 크롤링이다.

    article_url = title_link["href"]
    # print(article_url)
    # 해당 url이 가리키고 있는 모든 url을 출력한다.
    # 결과 :
    #       https://sports.donga.com/news/article/all/20261022/134888956/1
    #       https://sports.donga.com/news/article/all/20261022/134888881/1
    #       https://sports.donga.com/news/article/all/20261022/134888871/1
    #       https://www.donga.com/news/Society/article/all/20261022/134888448/1
    #       https://sports.donga.com/news/article/all/20261022/134888295/1
    #       https://sports.donga.com/news/article/all/20261022/134887419/1
    #       https://www.donga.com/news/Society/article/all/20261022/134888049/1
    #       https://sports.donga.com/news/article/all/20261022/134887289/1
    #       https://sports.donga.com/news/article/all/20261022/134886507/1
    #       https://sports.donga.com/news/article/all/20261022/134886489/1
    #       https://www.donga.com/news/Series/70030000000285

    # 이제 각각의 뉴스 기사의 url에 들어가서 긴 글을 가져와서 나올 것이다.

    try:
        source_article = urllib.request.urlopen(article_url)
        # '가을'이라고 검색했을 때 나오는 여러 기사들의 각각의 기사들의 해당 url로 들어감
        
        soup2 = BeautifulSoup(source_article, 'lxml')
        # print(soup2)
        # 내가 들어간 기사를 BeautifulSoup로 받아서 html파일로 가져온다.

        contents = soup2.select("div.article_txt")
        # print(contents)
        # 기사에 내가 원하는 내용을 태그로 찝음 = url이 가리키는 모든 기사들의 동일한 태그가 가리키고 있는 부분을 잡아두고 내가 가져오라고 하면 가져온다.

        for imsi in contents:
            item = str(imsi.find_all(string=True))
            msg += item
        # contents의 내용을 imsi가 받아서 imsi는 모든 문자열을 받는다. 크롤링에 의해 여러 페이지에서 데이터를 받아왔기에 현재 이 코드는 모든 페이지의 해당 태그들에 해당하는 내용의 문자열을 가져왔다.
        # 이제 그 기사의 태그들에서 string만 가져온다.


    except Exception as e:
        pass

    finally:
        print(msg)
    # 내가 들어가 url에서 article_get이라는 태그를 클래스로 가지는 부분의 문자열만 출력하였다.
    # 이제 그 문자열에서 명사만 뽑아보자.

    # 형태소 분석 후 명사만 출력
    okt = Okt()
    nouns = okt.nouns(msg)
    # 해당 문자열 자료(msg)에서 명사만 뽑아라.

    result = []
    for n in nouns:
        if len(n) > 1:
            result.append(n)
# print(result[:20])
# 두 글자 이상만 뽑아내서 저장했다.

count = Counter(result)
# print(count)
# 뽑은 각 단어들이 몇번씩 나왔는지 표시해준다.

tag = count.most_common(50)
print(tag)
# 가장 자주 나오는 명사 중 50개만 보여줘
# 결과 : [('가을', 21), ('전현무', 17), ('청년', 14), ('리즈', 14), ('참여', 12), ('기자', 12), ('감성', 11), ('스포츠동아', 11), ('여행', 11), ('문화', 10), ('이번', 10), ('이벤트', 10), ('비콘', 10), ('부산', 9), ('아웃도어', 9), ('빈티', 9), ('라운드', 9), ('카카오', 9), ('공간', 8), ('전시', 8), ('상품', 8), ('신세계', 8), ('브랜드', 8), ('고객', 8), ('제공', 7), ('시민', 7), ('이용', 7), ('현장', 7), ('도심', 7), ('일상', 6), ('행사', 6), ('사진', 6), ('예술가', 6), ('직접', 6), ('김태현', 6), ('무단', 6), ('배포', 6), ('학습', 6), ('금지', 6), ('구매', 6), ('센텀시티', 6), ('팝업', 6), ('활용', 6), ('인증', 6), ('경품', 6), ('골목', 6), ('상권', 6), ('관광', 6), ('식이', 6), ('여행지', 6)]


# 이제 워드클라우드(WordCloud)를 사용해보자.
taglist = pytagcloud.make_tags(tag, maxsize=100)
# pytagcloud.make_tags : 단어별 빈도 데이터를 워드클라우드에 사용할 태그 목록으로 변환하는 함수
# print(taglist)
# 결과 : [{'color': (139, 29, 94), 'size': 129, 'tag': '가을'}, {'color': (188, 191, 204), 'size': 110, 'tag': '전현무'}, {'color': (64, 184, 158), 'size': 94, 'tag': '청년'}, {'color': (119, 177, 211), 'size': 94, 'tag': '리즈'}, {'color': (127, 163, 37), 'size': 84, 'tag': '참여'}, {'color': (47, 47, 48), 'size': 84, 'tag': '기자'}, {'color': (138, 123, 29), 'size': 78, 'tag': '감성'}, {'color': (126, 184, 42), 'size': 78, 'tag': '스포츠동아'}, {'color': (35, 143, 41), 'size': 78, 'tag': '여행'}, {'color': (44, 109, 125), 'size': 73, 'tag': '문화'}, {'color': (147, 64, 134), 'size': 73, 'tag': '이번'}, {'color': (56, 17, 10), 'size': 73, 'tag': '이벤트'}, {'color': (204, 91, 29), 'size': 73, 'tag': '비콘'}, {'color': (164, 87, 26), 'size': 67, 'tag': '부산'}, {'color': (170, 30, 153), 'size': 67, 'tag': '아웃도어'}, {'color': (44, 101, 153), 'size': 67, 'tag': '빈티'}, {'color': (10, 107, 163), 'size': 67, 'tag': '라운드'}, {'color': (213, 155, 117), 'size': 67, 'tag': '카카오'}, {'color': (64, 59, 187), 'size': 61, 'tag': '공간'}, {'color': (151, 12, 56), 'size': 61, 'tag': '전시'}, {'color': (182, 94, 185), 'size': 61, 'tag': '상품'}, {'color': (18, 196, 216), 'size': 61, 'tag': '신세계'}, {'color': (149, 81, 100), 'size': 61, 'tag': '브랜드'}, {'color': (186, 196, 219), 'size': 61, 'tag': '고객'}, {'color': (12, 157, 168), 'size': 55, 'tag': '제공'}, {'color': (157, 40, 162), 'size': 55, 'tag': '시민'}, {'color': (202, 132, 109), 'size': 55, 'tag': '이용'}, {'color': (216, 162, 31), 'size': 55, 'tag': '현장'}, {'color': (51, 102, 127), 'size': 55, 'tag': '도심'}, {'color': (76, 11, 175), 'size': 49, 'tag': '일상'}, {'color': (134, 120, 126), 'size': 49, 'tag': '행사'}, {'color': (167, 61, 148), 'size': 49, 'tag': '사진'}, {'color': (72, 209, 210), 'size': 49, 'tag': '예술가'}, {'color': (184, 37, 28), 'size': 49, 'tag': '직접'}, {'color': (217, 209, 215), 'size': 49, 'tag': '김태현'}, {'color': (120, 29, 84), 'size': 49, 'tag': '무단'}, {'color': (69, 200, 115), 'size': 49, 'tag': '배포'}, {'color': (75, 79, 170), 'size': 49, 'tag': '학습'}, {'color': (107, 200, 175), 'size': 49, 'tag': '금지'}, {'color': (186, 31, 10), 'size': 49, 'tag': '구매'}, {'color':(53, 197, 134), 'size': 49, 'tag': '센텀시티'}, {'color': (62, 210, 33), 'size': 49, 'tag': '팝업'}, {'color': (209, 90, 218), 'size': 49, 'tag': '활용'}, {'color': (154, 150, 90), 'size': 49, 'tag': '인증'}, {'color': (159, 109, 162), 'size': 49, 'tag': '경품'}, {'color':(83, 69, 25), 'size': 49, 'tag': '골목'}, {'color': (144, 13, 25), 'size': 49, 'tag': '상권'}, {'color': (188, 169, 119), 'size': 49, 'tag': '관광'}, {'color': (21, 119, 159), 'size': 49, 'tag': '식이'}, {'color': (100, 10, 133), 'size': 49, 'tag': '여행지'}]
# 위와 같은 형태로 나온다.
print(len(taglist))
# 결과 : 50
# tag자체가 50개 데이터만 반환하기 때문.

pytagcloud.create_tag_image(taglist, "nlp_word.png", 
                            size=(1000, 600), background = (0, 0, 0), fontname = "korean", rectangular = False)
# taglist를 이미지로 만들어서 nlp_word.png로 파일에 저장하였다.
# nlp_word.png가 생겼다.
# 한글 파일이 깨진다...

# C:\Windows\Fonts 여기서 맑은고딕(malgum.ttf파일3개)을 복사하여
# C:\Users\user\anaconda3\envs\myproject\Lib\site-packages\pytagcloud\fonts 이 경로에 복사한 내용을 넣어준다.

# C:\Users\user\anaconda3\envs\myproject\Lib\site-packages\pytagcloud\fonts 여기서 fonts.json의
# name : "korean"으로, "ttf" : "malgun.ttf"으로 수정한다. 

img = mpimg.imread("nlp_word.png")
plt.imshow(img)
plt.show()
# 받은 명사들을 모두 그림에다가 표현함 = matplotlib를 이용했음

webbrowser.open("nlp_word.png")

print("\n\n---------------------")

df = pd.DataFrame(count.items(), columns = ["단어", "빈도수"])
print(df.head())
# 이제 받은 명사들과 그 갯수에 대한 계산을 DataFrame으로 만들었다.

if not df.empty:
    print("\n 빈도수 기준 내림차순 정렬 ----")
    df = df.sort_values(by='빈도수', ascending=False)
    df = df.reset_index(drop=True)
    print(df.head())

    # 1. Pandas 사용해보기
    print("\n 1. Pandas 기초 통계 : \n", df["빈도수"].describe())

    # 2. Numpy 사용해보기
    print("\n 2. Numpy 기초 통계 : \n")
    freq = df["빈도수"].to_numpy()
    print("전체 단어 출현 횟수 : ", np.sum(freq))
    print("평균 빈도수 : ", np.mean(freq))
    print("표준 편차 : ", np.std(freq))

    # 3. Matplotlib 사용해보기
    print("\n 3. Matplotlib 기초 시각화 : \n")
    top10 = df.head(10).sort_values(by='빈도수')
    plt.figure(figsize=(10, 6))
    plt.barh(top10['단어'], top10['빈도수'])
    plt.xlabel("단어")
    plt.ylabel("빈도수")
    plt.show()

    df.to_csv("nlp_freq.csv", index = False, encoding='utf-8')

else:
    print("분석할 단어가 없어요")