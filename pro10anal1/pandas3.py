# 연산
from pandas import Series, DataFrame
import numpy as np

s1 = Series([1,2,3], index=['a','b','c'])
s2 = Series([4,5,6,7], index=['a','b','c','d'])
print(s1)
print(s2)
print(s1 + s1) # 같은 인덱스끼리 연산, 불일치시 NaN
print(s1.add(s2)) # numpy 함수를 계승함, 불일치시 NaN
print(s1.add(s2, fill_value=0))  # + 보다 add가 유연한 연산 가능
# fill_value = 0 : NaN인 칸을 0으로 채워라

print()
print(s1.mul(s2))  # sub, div
# 마찬가지로 곱할 값이 없으면 NaN이다.
# 여기서도 마찬가지로 fill_value를 쓸 수 있따.

print('--------')
df1 = DataFrame(np.arange(9).reshape(3, 3), 
            columns=list('kbs'), index=['서울','대전','부산'])
df2 = DataFrame(np.arange(12).reshape(4, 3), 
            columns=list('kbs'), index=['서울','대전','제주','광주'])
print(df1)
# 결과 :      k  b  s
#       서울  0  1  2
#       대전  3  4  5
#       부산  6  7  8
print(df2)
# 결과 :      k   b   s
#       서울  0   1   2
#       대전  3   4   5
#       제주  6   7   8
#       광주  9  10  11
print()

print(df1 + df2)
# 결과 :       k    b     s
#       광주  NaN  NaN   NaN
#       대전  6.0  8.0  10.0
#       부산  NaN  NaN   NaN
#       서울  0.0  2.0   4.0
#       제주  NaN  NaN   NaN

print(df1.add(df2, fill_value=0))  # NaN은 0으로 채운 후 연산
# 결과 :       k     b     s
#       광주  9.0  10.0  11.0
#       대전  6.0   8.0  10.0
#       부산  6.0   7.0   8.0
#       서울  0.0   2.0   4.0
#       제주  6.0   7.0   8.0
# sub, mul, div 도 가능
print()

print('NaN(결측값) 처리 ----------------')

df = DataFrame([[1.4, np.nan], [7, -4.5], [np.nan, np.nan], [0.5, -1]], columns = ['one', 'two'])
print(df)
# 결과 :    one   two
#       0   1.4   NaN
#       1   7.0  -4.5
#       2   NaN   NaN
#       3   0.5  -1.0

print()


# DataFRame에서 Null값을 대하는 방식(True/False) : isnull(isna) vs notnull 
print(df.isnull()) # ... null값을 True로 반환
print(df.isna())   # ... null값을 True로 반환
# null값을 탐지하는 메서드(결측지 여부 확인)1
# null값을 True로 반환한다. # 둘이 같다

print(df.notnull()) # ... null값을 False로 반환
# null값을 탐지하는 메서드2
# null값을 False로 반환한다.

print()


# <행 관련>
# 현재 df 상태
#       one   two
#   0   1.4   NaN
#   1   7.0  -4.5
#   2   NaN   NaN
#   3   0.5  -1.0


print('-- 행 관련 --')

# df.dropna() : 결측값을 기준으로 행이나 열을 제거하는 함수

print(df.dropna())
# 결측치가 포함된 '행' 제거
print(df.dropna(axis=0))
# 위와 같다.

print(df.dropna(how='any')) # NaN이 하나라도 있는 '행'은 제외 = NaN이 전혀 없는 행만 출력한다.
print(df.dropna(how='all')) # 한 행의 모든 값이 NaN일 때만 해당 '행' 삭제

# <열 관련>
print('-- 열 관련 --')
print(df.dropna(axis=1))
# 결측치가 포함된 '열' 제거
print(df.dropna(subset=['one']))
# index이름이 'one'인 행에서 NaN값이 있는 열은 빼고 나머지 열 출력
print()

print(df.dropna(subset=['two']))
# index이름이 'two'인 행에서 NaN값이 있는 열은 빼고 나머지 열 출력

print()


print(df.drop(index=[0]))
# 행 기준 삭제
print(df.drop(columns = 'one'))
# 열 기준 삭제

# 여기 있는 삭제 메서드는 원본자료는 삭제되지 않는다.
print(df)


# 이렇게 db의 원시는 기억하고 있다. 하지만 원본을 삭제하고 싶으면 어떻게 할까?
# df.dropna(axis='rows', inplace=True) # 원본삭제
print(df)
print()

print('\n Nan(결측값) 관련 연산(결측값은 빼고 계산한다.) ---------------')
print(df.sum())
# 열의 합 - NaN은 연산에서 제외된다. = '열별' 합이다 (NaN은 계산X)
print(df.sum(axis=0, skipna=True))
# 위와 동일함.

print(df.sum (axis=1 ))
# 행별로 합함
# skipna=True는 기본값이다.
# mean(), min(), max(), std(), meadian(), prod()경우에도 적용된다. = 사용가능하다.(기본은 NaN 무시)
# numpy와 pandas의 함수는 기본적으로 NaN은 원래 계산을 안한다.
print()

print(df.describe())
# 요약 통계랑으로 해당 DataFrame의 모든 값들을 보여준다.
print()
# 결과 :              one       two
#           count  3.000000  2.000000
#           mean   2.966667 -2.750000
#            std    3.521837  2.474874
#            min    0.500000 -4.500000
#            25%    0.950000 -3.625000
#            50%    1.400000 -2.750000
#            75%    4.200000 -1.875000
#            max    7.000000 -1.000000

words = Series(['봄', '여름', '가을', '봄'])
print(words.describe())
# 문자열에 대해서는 더 다양한 값을 보여준다.
# 결과 : 
#       count     4
#       unique    3
#       top       봄
#       freq      2

