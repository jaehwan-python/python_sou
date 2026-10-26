# numpy다음 pandas를 배우는 이유
# : numpy에서 배열에 기초적인 연산을 배웠으면 pandas에서는 이름이나 위치로 행열을 선택하여 조건에 맞는 데이터를 조회가능하다
#   또한, 지금까지 배운 배열과 연산을 바탕으로 pandas를 이용해 파일을 읽고 / 데이터를 정리하고 / 필요한 통계를 구하는 과정을 배운다.

# 고수준의 자료구조(Series, DataFrame)와 빠르고 쉬운 데이터 분석용 함수 제공(벡터로 구성이 되어 있다.)
# 통합된 시계열 연산, 축약연산, 누락 데이터 처리, SQL, 시각화 ... 등을 제공
# 데이터 랭글링(Data Wrangling), 데이터 먼징(Data Munging)을 효율적으로 처리 가능

# "데이터 랭글링/먼징" : 분석이나 머신러닝에 활용하기 위해 가공되지 않은 원시 데이터(Raw_Data)를 정리/변환/구조화하는 작업
#                       = 모델이 학습하기 좋은 형태로 만드는 과정 
#                       = 착한데이터를 만들기
#                       = 데이터를 분석하기 좋게 만드는 과정

# "데이터 랭글링" : 데이터를 준비하는 전체 과정. 지저분하거나 형식이 맞지 않는 원시 데이터를 원하는 형태나 포맷으로 스크립트 등을 통해 변환 및 수정하는 구체적 작업
#           ex) 파일읽기, 표 병합, 구조변경, 정제 
# "데이터 먼징" : 지저분한 값을 정리하고 변환하느 작업
#          ex) 결측값 처리, 중복값 제거, 자료형 통일

# CSV 읽기 → 여러 표 합치기 → 중복·결측값 처리 → 분석용 표 만들기
# └──────────────── 랭글링 전체 과정 ────────────────┘
#                            └─ 먼징에 해당하는 작업 ─┘

# numpy의 1차원 배열
# = pandas의 sereis

# numpy의 2차원 이상의 배열(행렬)
# DataFrame

# 즉, pandas에서는 벡터 -> series(1차원 = 각 행) -> DataFrame(2차원)
# 구조이다.


# py분석1.pdf의 pandas읽어보기
# 표 형태의 데이터의 자료구조로 여러개의 칼럼을 가진다.
# 그 때 각 행을 series라고 하고 series에는 색인을 가지게 된다.
# series는 'list', 'tuple', 'dict' type만 series 형태의 객체로 바꿀 수 있지만 set은 불가능하다.
# 말했다! 'set'은 Series 자료가 될 수 없다고!!
# '파이썬 머신러닝 가이드' 읽어보기

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# 1. Series : 일련의 객체를 담을 수 있는 1차원 배열과 같은 자료구조로 색인(index)을 가진다(자료구조에 대해서는 추후에 학습예정)
obj = pd.Series([3, 7, -5, 4])
# 이번에는 numpy의 단순 행렬이 아니라 pandas의 Series이다
# obj를 출력하면 4행1열 구조처럼 보이지만 실제로는 원소가 4개인 1차원 배열이다.
# 그때 인덱스가 같이 나오게 된다.
# 왼쪽은 인덱스 값 오른쪽은 실제 원소값이다.
# ... 여기서 4행 1열인 2차원 표를 만드려먼 DataFrame을 사용한다.
# obj = pd.Series((3, 7, -5, 4)) 이렇게 tuple형태는 가능하다(나아가 dict도 가능!) 하지만 set은 안된다.
print(obj, type(obj))
# 결과 : 0    3
#        1    7
#        2   -5
#        3    4
#      인덱스 : 값
#        dtype: int64 <class 'pandas.Series'>
# 만약 obj의 series 안에 데이터 type이 다른 데이터가 있으면 object가 뜨게 된다.
# pd.Series안에는 모두 동일한 type의 데이터가 있어야 type이 pandas.Series로 뜬다.
# 만약 pd.Series안에 하나라도 type이 다른 데이터가 있으면 pandas.Object로 뜬다.
# obj = pd.Series([3, 7, -5, 4, '일'])
# # 결과 : < class 'pandas.Object' >

print()


# 2. pandas의 색인
obj2 = pd.Series([3, 7, -5, 4], index = ['a', 'b', 'c' ,'d'])
print(obj2)
# 이와 같이 인덱스를 내가 직접 줄 수 있다.
# 결과 : 'a'   3
#        'b'   7
#        'c'  -5
#        'd'   4

# padas vs numpy vs python함수
print("3. padas vs numpy vs python함수")
print(obj2.sum(), ' ', np.sum(obj2), ' ', sum(obj2))
#  numpy의 pandas함수 / numpy 함수   /    python 함수
print(obj2.std()) 
# std() : 표준편차 : 각 원소들이 평균에서 얼마나 퍼져있는지 나타낸다.
# 결과 : 5.123475382979799

# pandas의 함수는 numpy기반이다. 그러기에 python함수와 달리 universal function으로 구분되고 속도가 빠르다.


# 4. 색인 or 값 출력
print(obj2.index)
# 색인만 출력
print(obj2.values)
# 값만 출력


# 5. 인덱싱과 슬라이싱
print(obj2['a'])
# a라는 인덱스의 값인 '3'이 출력되었다.
print(obj2[['a']])
# a라는 인덱스와 그 '행'까지 출력된다.

print(obj2[['a', 'b']])
# 지정한 인덱스와 그 값만 선택
# 결과 : a  3  
#        b  7
print(obj2['a' : 'c'])
# a부터 c까지 범위를 의미

# print(obj2[2])
# KeyError : 인덱스 순서로 문자열을 사용중이라서 error가 뜬다.
# 지금 각 값들의 인덱스는 모두 'a' 'b' 'c'로 문자열이다.
# 이름표(인덱스)가 2인 원소를 찾는데 지금 인덱스가 2인 원소는 없다.
# 인덱스가 'b'인 원소로 찾아야 함.

# loc vs iloc
# 객체(series / dataframe type).iloc[행의 위치(정수번째), 열의 위치(정수번째)] : 행과 열의 정수번째 인덱스로 저장하고 열의 위치는 마지막을 포함하지 않는다. 
# 객체(series / dataframe type).loc[행의 이름, 열의 이름] : 행과 열의 이름으로 표현하여 벡터값을 가리킨다. 그때 열은 마지막 값도 포함한다
# 그럴 때 iloc를 쓰자.
print(obj2.iloc[2])
# iloc[위치번호] : series의 2번째 위치에 있는 값을 꺼내라.
print(obj2.loc['c'])
# 이번에는 인덱스 이름으로 값을 찾는다.
# loc['인덱스이름'] : 해당 이름을 가지고 있는 series를 다시 찾는다.

print(obj2[1:3])
# print(obj2[[2, 1]])
print(obj2.iloc[[2, 1]])
print(obj2.iloc[[1, 2]])
# 위치 기반 2번, 1번 순서대로 출력

print('a' in obj2)
# 인덱스 'a'여부를 확인 
# 결과 : True
print('k' in obj2)
# 결과 : False


# 6. 파이썬 dict자료를 Series 객체로 생성
print('\n파이썬 dict자료를 Series객체로 생성')

names = {'mouse' : 5000, 'keyboard' : 35000, 'monitor' : 5000}
print(names)

obj3 = Series(names)
# dict자료를 pandas에서 사용하기 위해 Series형태로 바꿈(형변환 : dict -> Series)
print(obj3, type(obj3))
# 결과 : mouse        5000
#        keyboard    35000
#        monitor      5000
#                          dtype: int64 <class 'pandas.Series'>

print('\n해당이름으로 index 설정')
obj3.index = ['마우스', '키보드', '모니터']
print(obj3, type(obj3))
# 결과 : 마우스     5000
#        키보드    35000
#        모니터     5000
#                       dtype: int64 <class 'pandas.Series'>

print('\n해당이름으로 name 설정')
obj3.name = '상품가격'
print(obj3)
# 해당 Series(obj3)의 이름을 '상품가격'이라고 붙임

print("-" * 50)

print("\n DataFrame : vector -> Seires -> DataFrame")
# 0차원 : 스칼라
# 1차원 : 벡터(Series)
# 2차원 : 행렬(DataFrame)
# 3차원 : 텐서
# DataFrame : 
# 표 모양(2차원 형태자료)의 자료구조로 여러 개의 칼럼을 가진다.(series가 모인 형태) 
# ** Seires는 1차원 형태의 자료형이다.
# 각 칼럼은 서로 다른 종류의 값을 기억할 수 있다.
# 같은 길이의 리스트에 담긴 dict type의 데이터를 이용해 data Frame을 객체 생성.

# obj3 : 
#            '상품가격'
#  결과 : 마우스     5000
#         키보드    35000
#         모니터     5000

df = pd.DataFrame(obj3)
print(df, type(df))

print()

data = {
    'irum' : ['홍길동', '한국인', '신기해', '공기밥', '한가해'], # list 타입
    'juso' : ('역삼동', '신당동', '역삼동', '역삼동', '신사동'), # tuple 타입
    'nai' : [23, 25, 33, 30, 35]                               # list 타입
}

# <DataFrame>
frame = pd.DataFrame(data)
# 이제부터 난 해당 값들의 집합(list, tuple, list)를 dataframe으로 볼거다. 그리고 그 dataframe은 frame이라는 객체를 참조한다.
# dict -> DataFrame
print(frame)
# 결과 :     irum    juso   nai
#        0  홍길동  역삼동   23
#        1  한국인  신당동   25
#        2  신기해  역삼동   33
#        3  공기밥  역삼동   30
#        4  한가해  신사동   35 
#                               <class 'pandas.DataFrame'>

print()

# < Series >
print(frame['irum'], type(frame['irum']))
# print(frame.irum, type(frame.irum))
# 이렇게 써도 된다. = 인덱스 값으로 값을 부름
# 결과 : 0    홍길동
#        1    한국인
#        2    신기해
#        3    공기밥
#        4    한가해
#                   <class 'pandas.Series'>

# 벡터 = 하나의 값 - '홍길동'
# 벡터(1차원) = Series(1차원)  ->  DataFrame(2차원)

print(DataFrame(data=data, columns=['juso', 'irum', 'nai']))
# data라는 값을 dataframe을 만들기 위한 data로 가지면서 해당 dataframe의 열(columns)은 사용할 열과 표시 순서이다.
# 이는 지정한 열 순서로 새 DataFrame을 만드는 것이다.
# 이 코드는 열 순서를 바꾼다.
# 결과 :      juso    irum   nai
#         0  역삼동  홍길동   23
#         1  신당동  한국인   25
#         2  역삼동  신기해   33
#         3  역삼동  공기밥   30
#         4  신사동  한가해   35

print()

print("--------------------------------------------------------------")

# 중요!! 
#  columns = [...] : 열에 이름 매기기
#  index = [...]   : 행에 이름 매기기

# Nan(결측치)란? : 값이 없거나 또는 값을 알 수 없는 Missing Value
frame2 = pd.DataFrame(data, columns=['irum', 'nai', 'juso', 'tel'])
print(frame2)
# tel은 값이 없지만 자리만 확보하였다. tel은 Nan이라는 데이터로 Series를 채운다.

# 물론 NaN에 인덱스 값도 부여할 수 있다.
frame2 = pd.DataFrame(data, columns=['irum', 'nai', 'juso', 'tel'], index=['a', 'b', 'c', 'd', 'e'])
print(frame2)

# NaN에 인덱스를 부여할 수 있다는 것은 값을 추가할 수도 있다는 것이다.
# 초기에 열을 생성할 때는 값을 주지 않았기에 NaN(결측값)으로 표현했지만 이제는 값을 넣어서 결측값이 아니다.
frame2['tel'] = '111-1111'
print(frame2)

val = pd.Series(['222-2222', '333-3333', '444-4444'], index=['b', 'c', 'e'])
# 한번에 열을 지정하여 값을 한번에 추가하였다.
print(val)

print()
frame2['tel'] = val
# tel이라는 index를
# 기존 자료 덮어쓰기
print(frame2)
# 결과 :     irum   nai   juso     tel
#        a  홍길동   23  역삼동       NaN
#        b  한국인   25  신당동  222-2222
#        c  신기해   33  역삼동  333-3333
#        d  공기밥   30  역삼동       NaN
#        e  한가해   35  신사동  444-4444


# 전치하기
# 전치 : 행과 열을 바꾸는 것
# 해당 dataframe에 .T를 붙여주면 행과 열이 바뀐다.
print()
print(frame.T) 
# 결과 :         0    1    2    3    4
# irum  홍길동  한국인  신기해  공기밥  한가해
# juso  역삼동  신당동  역삼동  역삼동  신사동
# nai    23   25   33   30   35
print()

# ndarray를 가지고 데이터 값만 뽑기 ... -> 이 부분 중요!!
# numpy -> ndarray(0차원 ~ 다차원)
# pandas -> dataframe(항상 2차원) + 행열 이름이 존재
# 즉, 같은 데이터를 이름표가 있는 표로 다루면 DataFrame, 배열로 다루면 ndarray이다.
print(frame2.values, type(frame2.values))
# 결과 : [['홍길동' 23 '역삼동' nan]
#         ['한국인' 25 '신당동' '222-2222']
#         ['신기해' 33 '역삼동' '333-3333']
#         ['공기밥' 30 '역삼동' nan]
#         ['한가해' 35 '신사동' '444-4444']]   <class 'numpy.ndarray'>
# 지금은 이름이 없는, 오로지 값으로만 빼낸 형태이기에 class가 numpy.ndarray로 뜬다.

print(frame2.values[0,1])
# 0행1열의 값
# 결과 : 23

print(frame2.values[0:2])
# ndarray가 나온다.
# 결과 : [['홍길동' 23 '역삼동' nan]
#         ['한국인' 25 '신당동' '222-2222']]
# ** 23이 아니다!! ...  ',' 가 없잖아! = 0행부터 1행까지
print()


# <삭제>
# 1. 'd'행 삭제
# 새로운 dataframe을 생성하고 그 복사본에다가 작업을 하는 것이기에 frame2에는 적용이 되지 않는다.
frame3 = frame2.drop('d', axis=0)
print(frame3)
# frame2는 그대로다.
# 결과 :     irum   nai   juso        tel
#        a  홍길동   23  역삼동       NaN
#        b  한국인   25  신당동  222-2222
#        c  신기해   33  역삼동  333-3333
#        e  한가해   35  신사동  444-4444
# 행을 삭제할 것이기 때문에 axis=0을 꼭 적어주어야 한다.

# 2. 'tel'열 삭제
frame4 = frame2.drop('tel', axis=1)
print(frame4)
# 결과 :    irum    nai  juso
#       a  홍길동   23  역삼동
#       b  한국인   25  신당동
#       c  신기해   33  역삼동
#       d  공기밥   30  역삼동
#       e  한가해   35  신사동
# 열을 삭제할 것이기 때문에 axis=1을 꼭 적어주어야 한다.

print()

print('-------------')
print(frame2)
# 원본은 그대로 살아있다.
# 결과 :     irum   nai   juso        tel
#        a  홍길동   23  역삼동       NaN
#        b  한국인   25  신당동  222-2222
#        c  신기해   33  역삼동  333-3333
#        d  공기밥   30  역삼동       NaN
#        e  한가해   35  신사동  444-4444

# 1. 행 단위 정렬(역방향)
print(frame2.sort_index(axis=0, ascending=False))

# 2. 열 단위 정렬(정방향)
print(frame2.sort_index(axis=1, ascending=True))

print()

# 순위 매김
print(frame2.rank(axis=0))
# 결과 :    irum  nai  juso  tel
#        a   5.0  1.0   4.0  NaN
#        b   4.0  2.0   1.0  1.0
#        c   2.0  4.0   4.0  2.0
#        d   1.0  3.0   4.0  NaN
#        e   3.0  5.0   2.0  3.0

print('10월 14일')

counts = frame2['juso'].value_counts()
# 주소열을 선택하여 
# .value_counts() : 동일한 주소가 몇번씩 나오는 지 알려줘.
print(counts)
# 결과 : 
#        juso
#       역삼동    3
#       신당동    1
#       신사동    1

# 문자열 자르기
data = {
    'juso' : ['서초구 서초2동', '강남구 역삼동', '강남구 대치동'],
    'inwon' : [23, 25, 15]
}
fr = pd.DataFrame(data)
# dict형 데이터를 dataframe으로 만들기 위해서는 pd.DataFrame(dict, tuple, list)함수를 써준다.
print(fr)
# 결과 :             juso        inwon
#           0   서초구 서초2동     23
#           1   강남구 역삼동      25
#           2   강남구 대치동      15

result1 = Series(x.split()[0] for x in fr.juso)
result2 = Series(x.split()[1] for x in fr.juso)
# split()은 문자열을 공백 기준으로 쪼개라라는 뜻이다. 
# 그때 [0]은 쪼갠 문자열의 0번째 값 ... 서초구   강남구  강남구 
# 그때 [1]은 쪼갠 문자열의 1번째 값 ... 서초2동  역삼동  대치동
print(result1)
# 결과 :  0    서초구
#         1    강남구
#         2    강남구
print(result2)
# 결과 : 0    서초2동 
#        1    역삼동
#        2    대치동

print(result1.value_counts())
# 결과 : 강남구    2
#        서초구    1