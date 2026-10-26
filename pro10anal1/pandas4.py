# DataFrame의 재구조화(열을 행으로, 행을 열로 바꾼다.)
import numpy as np
import pandas as pd

df = pd.DataFrame(np.arange(6).reshape(2, 3), index=['대전', '서울'], columns=['2023', '2024', '2025'])
# index로 대전과 서울의 행을 만든다
# columns로 열을 구성한다
print(df)
# 결과
#        2023  2024  2025
# 대전     0     1     2
# 서울     3     4     5

print()

# < stack, unstack을 이용한 df의 재구조화 >
df_row = df.stack()
# 열을 아래로 내려서 행의 인덱스 쪽으로 쌓기 = 구조를 바꿈
# "가로로 펼쳐진 열을 세로로 쌓기"
# 원본은 바뀌지 않는다.
print(df_row)
# 결과 :
#   대전  2023    0
#         2024    1
#         2025    2
#   서울  2023    3
#         2024    4
#         2025    5


df_col = df_row.unstack()
# 행 인덱스를 다시 열쪽으로 펼친다.
# "세로로 쌓인 인덱스르 다시 가로로 펼치기"
print(df_col)
# 결과 : 
#           2023  2024  2025
#    대전     0     1     2
#    서울     3     4     5

# 행과 열을 완전히 바꾸는 전치와는 다르다.
# 전치
# print(df.T)
# 로 표현

print('\n 범주화 -------------------------')

# 연속형을 범주형으로 바꿀 수 있다
price = [10.3, 5.5, 7.8, 3.6]
cut = [3, 7, 9, 11]
# 3~7
# 7~9
# 9~11
# 구간 기준 값을 설정한다.
# 3개의 구간이 만들어졌다.

result_cut = pd.cut(price, cut)
# price의 각 값들이 cut으로 나눈 각 구간 중 어디에 속하는지 분류해서 저장한 것이다.
# cut은 구간의 경계를 나타낸다.
# (3,7]  : 3초과 7이하
# (7, 9] : 7초과 9이하
# (9,11] : 9초과 11이하

#
# 연속형 -> 범주형  
# 구간별 그룹으로 분류
# 연속형 자료가 범주형으로 바뀌게 된다.

print(result_cut)
# 결과 : [ (9, 11], (3, 7], (7, 9], (3, 7] ]
#        Categories (3, interval[int64, right]): [(3, 7] < (7, 9] < (9, 11]]
# 가격 자체를 '계산'하는 게 아니라 각 가격을 구간이라는 범주로 바꾸는 것

# (a,b] : a초과 b이하

result_cut = pd.cut(price, bins=cut, labels=['저가', '중가', '고가'])
# price : 구간을 나눌 값들
# bins=cut : cut을 구간의 경계로 지정함
# labels = [...] : 각 구간에 이름을 붙임
# 즉, 
# (3,7]  : "저가"
# (7, 9] : "중가"
# (9,11] : "고가"

# 각 구간에 이름을 매기고 각 구간의 값들에 대해서 구간별로 쪼개어 분류를 한다.

print(result_cut)
# 결과 : ['고가', '저가', '중가', '저가']

print(pd.Series(result_cut).value_counts())
# 결과 : 저가    2
#        중가    1
#        고가    1

# value.count() : 해당 열에서 각 이름이 나온 횟수를 셈
# pd.cut() : 데이터 개수가 비슷하도록 문위수 기분 자동 분할

print('\n--------------')

datas = pd.Series(np.arange(1, 1001))
print(datas)
# 1부터 1000까지의 data가 생긴다. 그 중 내가 원하는 값을 뽑아보자
print(datas[:5])
print(datas.head()) # 갯수를 생략하면 처음의 5개값만 가져온다
# 두 개는 같다.

# head와 tail을 이용해라
print(datas.head(2))
# 처음 2개

print(datas[:-2])
# datas의 맨 끝에서 2개
print(datas.tail(2))
# 두 개는 같다.
# print(data[:5]) = print(datas.head())
# print(datas[:-2]) = print(datas.tail())

print()


# 집계함수 사용방법 : agg() or 사용자 정의함수()
# 1. agg함수
print('agg함수 : 범주의 그룹별 연산')
datas = pd.DataFrame({
    '부서' : ['개발', '개발', '영업', '영업', '인사', '개발'],
    '이름' : ['길동', '철수', '영희', '민수', '유리', '찬우'],
    '연봉' : [4500, 4200, 4000, 4500, 3500, 3900],
    '성과점수' : [90, 85, 70, 75, 88, 95]
})
# DataFrame을 구성하는 값으로 dict자료형이 오면
#  key는 열의 이름(대표), value는 그 열에 들어갈 값들이 된다
print(datas)
# 결과 :         부서   이름   연봉  성과점수
#            0   개발   길동   4500    90
#            1   개발   철수   4200    85
#            2   영업   영희   4000    70
#            3   영업   민수   4500    75
#            4   인사   유리   3500    88
#            5   개발   찬우   3900    95
print()


print(datas.groupby('부서')['연봉'].mean())
# 부서별 연봉의 평균
# 설명 : 
# datas.groupby('부서') : 같은 부서끼리 묶는다,
#['연봉'] : 묶인 데이터에서 평균을 구할 대상인 연봉의 '열'만 선택한다.
# .mean() : 각 부서안에서 연봉의 평균을 계산한다.

print(datas.groupby('부서')['이름'].count())
# 부서별 이름의 갯수(건수)

print(datas.groupby('부서')[['연봉', '성과점수']].mean())
# 부서별 연봉과 성과점수의 평균

pd.set_option('display.max_columns', None)
# 그러면 모든 자료가 전부 다 보이게 된다. 생략이 되지 않는다.
# DataFrame을 출력할 때 열이 많아도 중간 '열'들을 생략하지 않도록 설정하는 코드

print(datas.groupby('부서')['연봉'].agg(['sum', 'mean', 'count']))
# 여러 집계함수를 한 번에 처리함.

# 2. 사용장 정의 함수
# agg대신 사용자 함수를 작성
print()
data = pd.DataFrame({
    '연봉' : [4500, 4200, 4000, 4500, 3500, 3900],
    '성과점수' : [90, 85, 70, 75, 88, 95]
})

def summaryFunc(gr):
    return {
        'count' : gr.count(),
        'mean' : gr.mean(),
        'std' : gr.std(),
        'min' : gr.min()
    }
print(data.apply(summaryFunc)) 
# apply() : 함수를 실행하는 함수이다

print()

# readme.txt : 실행방법, table제작문, 소스코드
# local host 5000번을 쓰면 다른 사람들이 직접 볼 수 없기에 동영상을 찍어서 유튜브에 올리고 해당 영상의 url을 복붙한다
# ppt : 목표, 목적 및 엄무분담 사용한 핵심 주요 기능, 클래스와 table diagram, 시연영상, 소감, qna, 각자 어려움을 이겨낸 경험 한 명씩 자신의 역할을 설명한다. 주요코드

# <Merge> : DataFrame 객체 합치기!!
print("\n병합(merge) : DataFrame 객체 합치기")
df1 = pd.DataFrame({'data1' : range(7), 'key' : ['b', 'b', 'a', 'c', 'a', 'a', 'b']})
print(df1)
# 결과 : 
#    date1   key
#     0      'b'
#     1      'b'
#     2      'a'
#     3      'c'
#     4      'a'
#     5      'a'
#     6      'b'

df2 = pd.DataFrame({'key' : ['a', ' b', 'd'], 'data2' : range(3)})
print(df2)
# 결과 : 
#        key  data2
#        'a'   0
#        'b'   1
#        'd'   2

# 현재 2개의 DataFrame이 존재하고 있다.
print()


# DataFrame합치기 : merge와 concat
print('\n DataFrame의 병합 : merge와 concat!!')
# 두 DataFrame을 병합하고 싶다.

# 병합1.
print(pd.merge(df1, df2, on = 'key')) # 교집합(inner join과 비슷한 역할이다.)
# 즉, 키가 같은 녀석들과 합쳐진다.
# 두 df가 공통으로 가지고 있는 컬럼에 대해서 새 df가 만들어진다.
# 결과 : 
#           data1  key  data2
#       0      2    a      0
#       1      4    a      0
#       2      5    a      0
print()

# on = '열 이름(공통)' : 어떤 열의 값을 비교해서 연결할 지 = 두 DF에서 '이름'값이 같은 행끼리 연결
# how = 'inner' : 양 쪽에 모두 있는 값만
# how = 'left' :  왼쪽의 '행'은 모두 유지
# how = 'right' : 오른쪽의 '행'은 모두 유지
# how = 'outer' : 양쪽의 '행'을 모두 유지

# 병합2.: on='key'
print(pd.merge(df1, df2, on='key'))
print()

# 병합3. : on = 'key', how ='inner'
print(pd.merge(df1, df2, on='key', how='inner'))
print()

# 병합4.: on = 'key', how = 'outer'
print(pd.merge(df1, df2, on='key', how='outer'))
print()

# 병합5. : on = 'key', how = 'left'
print(pd.merge(df1, df2, on='key', how='left'))
print()

# 병합6. : on = 'key', how = 'right'
print(pd.merge(df1, df2, on='key', how='right'))
print()

# 병합7.
df3 = pd.DataFrame({'key2' : ['a', ' b', 'd'], 'data2' : range(3)})
print(df3)
# 결과 : 
# key2   data2
#  'a'    0
#  'b'    1   
#  'd'    2

# 공통칼람이 있을때는 on='key'를 적어줬는데 이젠 없다.
print(df1)
print(pd.merge(df1, df3, left_on='key', right_on='key2'))
# df1과 df3는 공통된 '열'이 존재하지 않는다.
# 즉, 그때는
# left_on = '왼쪽 df(df1)에서 열 이름'     : 왼쪽 df1의 'key'열을 기준으로 사용
# right_on = '오른쪽 df(df3)에서 열 이름'  : 오른쪽 df3의 'key2'열을 기준으로 사용
# 즉!!! df1['key']와 df3['key2']의 값이 같은 '행'끼리 연결된다
# 컬럼 이름으로 연결된느 것이 아니라 컬럼의 값이 같은 것끼리 연결된다. 

# 병합8. 
print('------- concat -------')
print(pd.concat([df1, df3], axis=0)) # 행단위 : 아래로 붙이기
print()
print(pd.concat([df1, df3], axis=1)) # 열단위 : 옆으로 붙이기

# merge는 공통 칼럼을 기준으로 두 df를 합친다. 
# 하지만 concat은 '상하(행단위)' 혹은 '좌우(열단위)'로 이어서 붙이는 것이다.
print()


# 피봇이란? : 한 발을 축으로 삼아 방향을 바꾸는 것
#  < 피봇연산 >
print('<피봇연산>')
data = {'city': ['강남', '강북', '강남', '강북'],
        'year' : [2000, 2001, 2002, 2002],
        'pop' : [3.3, 2.5, 3.0, 2.0]
        }
df = pd.DataFrame(data)
# 해당 데이터셋들을 DataFrame으로 만드는 과정이다. 잘기억해두자!
print(df)
# 결과 : 
#           city    year    pop
#       0   강남    2000    3.3
#       1   강북    2001    2.5
#       2   강남    2002    3.0
#       3   강북    2002    2.0


print(df['pop'].describe())
# describe() : 데이터프레임에서 해당 '열'의 주요 통계정보를 보여준다.

print('-------------')

# 피봇1.
print(df.pivot_table(index=['city']))
print(df.pivot_table(index=['city'], aggfunc='mean'))
# 위 두 코드는 서로 동일하다.
# 결과 :         pop    year
#        city
#        강남    3.15  2001.0
#        강북    2.25  2001.5

# 피봇2.
print(df.pivot_table(index=['city', 'year'], aggfunc=[len, 'sum']))

# 피봇3.
print(df.pivot_table(index=['city'], values = 'pop'))
print(df.pivot_table(index=['city'], values='pop', aggfunc='mean'))

# 피봇4.
print(df.pivot_table(index=['city'], values='pop', aggfunc=len))
# len은 따옴표를 쓰지 않는다.

# 피봇5.
print(df.pivot_table(index=['year'], values='pop', columns=['city']))

# 현재 피봇을 가지고 df를 계속 재구성하고 있다
# 구조 재구성  ->  year : 행 
#             ->  city : 열
#             ->  pop : 계산값

# 피봇6.
print(df.pivot_table(index=['year'], values='pop', columns=['city']))
print(df.pivot_table(index=['year'], values='pop', columns=['city'], margins=True))
print(df.pivot_table(index=['year'], values='pop', columns=['city'], margins=True, fill_value=0))

print()

hap = df.groupby(['city'])
print(hap)
# 이건 구조를 바꾸는 것은 아니다.
print(hap.sum)
print(df.groupby(['city']).sum())
print(df.groupby(['city']).mean())





