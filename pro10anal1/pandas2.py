# 재색인
from pandas import Series, DataFrame

# Series의 재색인
data = Series([1, 2, 3], index=(1, 4, 2))
print(data)
# index는 각 행의 이름을 의미하고 columns는 각 열의 이름을 지칭한다.

data2 = data.reindex((1, 2, 4))
data2 = data.reindex((2, 1, 4))
print(data2) # 내가 지정한 인덱스 순서대로 값을 재배치 

print('\n 재색인 할 때 값 채워 넣기')
data3 = data2.reindex([0, 1, 2, 3, 4, 5]) # 대응되는 값이 없으면 NaN
print(data3)
# 현재는 1,2,4 인덱스만 값을 가지고 있다. 나머지 방금 새로 넣어준 인덱스는 NaN으로 결측값을 가진다.
# 결과 : 
# 0    NaN
# 1    1.0
# 2    3.0
# 3    NaN
# 4    2.0
# 5    NaN

# 대응값이 없는 인덱스에 특정값으로 채우기
data3 = data2.reindex([0,1,2,3,4,5], fill_value=777)
print(data3)
# 결과 : 
# 0    777
# 1      1
# 2      3
# 3    777
# 4      2
# 5    777
# 모든 NaN이었던 데이터를 fill_value를 이용해 해당 값으로 채움

print()
# NaN 앞 값으로 NaN을 채우기
data2 = data2.sort_index()
# 현재 인덱스가 [2, 1, 4]로 정해져있어서 method를 사용 불가능하다. 사용하려면 정렬된 상태로 오름차순이 되어양하기에 sort.index()를 써주었다.
# 그럼 인덱스가 [1, 2, 4]순으로 정해진다.

data3 = data2.reindex([0, 1, 2, 3, 4, 5], method='ffill') 
# ffill을 할때는 기존 데이터가 정렬된 상태여야한다.
# ffill은 새로 생긴 위치를 앞선 인덱스의 값으로 채운다.

data3 = data2.reindex([0,1,2,3,4,5], method = 'pad')
print(data3)

data3 = data2.reindex([0,1,2,3,4,5], method = 'bfill')
print(data3)

data3 = data2.reindex([0,1,2,3,4,5], method = 'backfill')
print(data3)

# fill과 pad는 동일 : 앞선값으로 값을 채운다
# bfill과 backfill은 동일 : 뒤의 값으로 채운다.


import numpy as np
print('\n DataFrame : bool처리')
df = DataFrame(np.arange(12).reshape(4, 3), 
                index=['1월', '2월', '3월', '4월'], columns = ['강남', '강북', '서초'])
print(df)
# 결과 :     강남  강북  서초
#       1월   0     1     2
#       2월   3     4     5
#       3월   6     7     8
#       4월   9    10    11

# ndarray는 열단위로 type이 일치해야한다.

print(df['강남'])
# 해당 열 출력

print(df['강남'] > 3)
# True, False 출력

print(df[df['강남'] > 3])
# 조건이 참인 행만 출력

print(df < 3)
# 전체 자료 대상 bool값 출력

df[df < 3] = 0
# 3미만 자료는 0으로 대체

print(df)

print()

# 슬라이싱 관련 메서드
# df.loc['행(열) 이름'] : 해당 행(열)
# df.iloc['행(열) 번호'] : 위치 기준 행(열)
print(df.loc['3월'])
print(df.loc['3월, :'])
print(df.loc[:'2월'])
print(df.loc[:'2월', ['서초']]) # 2월 이하 행 '서초'열
print()

# 위치기준으로 
print(df.iloc[2]) #2행
print(df.iloc[2, :])
print()

print(df.iloc[:3]) # 3행 미만 행 모든 열
print(df.iloc[:3, 2]) #3 행 미만 행 2열
print(df.iloc[:3, 1:3]) # 3행 미만 행 1,2열
print(df.iloc[1:3, 1:3]) # 1,2행, 1,2,열

