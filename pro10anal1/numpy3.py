# 배열에 행, 열 추가 ...

import numpy as np

aa = np.eye(3)
# 주대각이 1인 (3,3)인 행렬 생성
print(aa)
# 결과 : [[1. 0. 0.]
#         [0. 1. 0.]
#         [0. 0. 1.]]

bb = np.c_[aa, aa[2]]
# aa의 2열과 동일한 열을 aa에 추가한다.
# : aa[2]행을 가져와서 aa에 '열'방향으로 붙인다. = bb
print("bb = \n" , bb)
# 결과 :  [[1. 0. 0. 0.]
#          [0. 1. 0. 0.]
#          [0. 0. 1. 1.]] # 열이 추가되었다

cc = np.r_[aa, [aa[2]]]
# aa의 2행과 동일한 행을 cc에 추가한다.
# : aa에서 aa[2]행을 가져와서 aa에 '행'방향으로 붙인다 = cc 
print('cc = \n', cc)
# 결과 :  [[1. 0. 0.]
#          [0. 1. 0.]
#          [0. 0. 1.]
#          [0. 0. 1.]] # 행이 추가되었다.
# .c_를 써주면 열을 붙이는 것이고
# .r_과 [aa[]]를 써주면 행을 붙이는 것이다.

print('-------------------------------')
print('\n append, insert, delete 함수를 써보자구')
a = np.array([1, 2, 3])
print(a)
# 결과 : [1 2 3]

# append : 추가
b = np.append(a, [4, 5])
# 결과 : [1 2 3 4 5]
b = np.append(a, [4, 5], axis = 0)
# axis = 0이면 '행' 기준
# axis = 1이면 '열' 기준
# 결과 : [1 2 3 4 5]
# b = np.append(a,[4,5], axis =1) ... error
# a가 1차원 배열이라 axis=1인 열이 존재하지 않기 때문이다.
print(b)
# 결과 : [1 2 3 4 5]

# insert : 삽입
c = np.insert(a, 0, [6, 7])
# a에서 0번째 위치에 데이터 삽입 = index로 넣을 수 잇따.
# append는 단순히 맨 뒤에 데이터 값을 넣었다면 insert는 내가 원하는 index 위치에 데이터값을 넣을 수 잇다.
print(c)
# 결과 : [6 7 1 2 3]

# delete : 삭제
d = np.delete(a, 1) 
# a배열에서 1번째 index를 가진 자료 삭제하여 새로운 배열을 반환한다.
print(d)
# 결과 : [1 3]

print()

aa = np.arange(1, 10).reshape(3, 3)
print(aa)
# 결과 : [[1 2 3]
#         [4 5 6]
#         [7 8 9]]

print(np.insert(aa, 1, 99))
# 결과 : [ 1 99  2  3  4  5  6  7  8  9]
# 차원이 축소되었다. 2차원이 1차원으로 떨어짐
# axis를 적지 않았기 때문에..axis를 안적으면 차원이 떨어진다!!
# 우리가 배우는 배열은 항상 2차원이기에 axis=0,1을 적지않으면 1차원으로 떨어진다.

print(np.insert(aa, 1, 99, axis = 0))
# '행' 기준으로(차원이 안떨어짐 = 차원유지)
# 결과 : [[ 1  2  3]
#         [99 99 99]
#         [ 4  5  6]
#         [ 7  8  9]]

print(np.insert(aa, 1, 99, axis = 1))
# '열' 기준으로(차원이 안떨어짐 = 차원유지)
# 결과 : [[ 1 99  2  3]
#         [ 4 99  5  6]
#         [ 7 99  8  9]]

# 차원을 유지하고 싶으면 axis를 꼭 써주어야 한다.
# **axis를 사용하지 않으면 np는 배열을 우선 한 줄로 다 펼쳐서 연산한다**
print()


# 조건 연산 : where(조건, 참, 거짓)
print("조건 연산")

x = np.array([1,2,3])
y = np.array([4,5,6])
conditionData = np.array([True, False, True])
result = np.where(conditionData, x, y)
# 조건이 True면 x에서, False이면 y에서 같은 위치의 값을 골라 result에 저장한다.
# np.where(조건, 참일 때 값, 거짓일 때 값)
#             x = [ 1,     2,     3] : 참일 때의 값을 선택하는 부분
#             y = [ 4,     5,     6] : 거짓일 때의 값을 선택하는 부분
# conditiondata = [True, False, True]
print(result)  
# 결과 :           [ 1      5     3 ]

print()

print(x)
aa = np.where(x >= 2)
print(aa)  
# 해당 where의 조건을 만족하는 값이 있는 데이터의 인덱스를 보여준다.
# 현재 '2', '3'이라는 값이 해당 조건을 만족한다. 여기서 2, 3은 1번째, 2번째 인덱스를 가진다
# 결과 : (array([1, 2]),)  
# array([1, 2]) : 조건을 만족하는 데이터값들의 인덱스
# (..., ) : 인덱스를 표현한 배열을 담은 튜플. 마지막 쉽표 = 원소가 하나인 튜플임을 나타낸다 = 튜플 속 배열이 하나다. 
print(a[aa]) 
# 결과 : [2 3]

print()
kbs = np.concatenate([x, y])  # 배열 결합
print(kbs) 
# + 는 해당 값들끼리 더하는 것이고
# concatenate를 사용하면 두 배열을 더하여 1차원으로 만든다.
# 결과 : [1 2 3 4 5 6]

mbc, sbs = np.split(kbs, 2)
# split은 배열을 같은 크기의 여러 배영로 나누어라
# np.split(나눌 배열, 나눌 개수, axis = 0) : 행 기준으로 해당 배열을 해당 갯수로 나누어라
print('mbc : ', mbc)
print('sbs : ', sbs)
# 결과 : [1 2 3]
# 결과 : [4 5 6]

print()
a = np.arange(1, 17).reshape(4, 4)
print(a)
# 결과 : [[ 1  2  3  4]
#         [ 5  6  7  8]
#         [ 9 10 11 12]
#         [13 14 15 16]]


# 배열을 나누는 방향이 정해져 있는 함수 (np.hsplit  vs  np.vsplit)
# 1. 행분할 : np.hsplit
x1, x2 = np.hsplit(a, 2)
# 열을 나누어서 좌우로 분할(axis=1)
print(x1)
# 결과 : [[ 1  2]
#         [ 5  6]
#         [ 9 10]
#         [13 14]]
print(x2)
# 결과 : [[ 3  4]
#         [ 7  8]
#         [11 12]
#         [15 16]]

print()

# 2. 열분할 : np.vsplit
y1, y2 = np.vsplit(a, 2)
# 행을 나누어서 위아래로 분할(axis = 0)
print(y1)
# 결과 : [[1 2 3 4]
#         [5 6 7 8]]
print(y2)
# 결과 : [[ 9 10 11 12]
#         [13 14 15 16]]

print('----------------')
# 표본 추출(Sampling)은 전체 데이터인 모집단(Population)에서 일부 데이터를 뽑아 조사/분석하는 것
# 단순 무작위 추출 : 전체에서 랜덤으로 추출
# ->  복원 추출 : 뽑은 데이터를 다시 넣고 또 뽑음 - 중복 허용
# ->  비복원 추출 : 중복이 없다.

li = np.array([1, 2, 3, 4, 5, 6, 7])

# 1. 단순 무작위 추출
sample1 = np.random.choice(li, size=3, replace = False)  # 단순무작위 추출(비복원 추출)
print(sample1)
# 결과 : [4 6 7]

sample2 = np.random.choice(li, size=3, replace = True)   # 단순무작위 추출(복원 추출) = 중복 허용
print(sample2)
# 결과 : [2 3 5]

print()

# 2. 복원 추출
for _ in range(5):
# _ : 반복되는 변수는 사용하지 않겠다.
    print(li[np.random.randint(0, len(li) - 1)], end = ' ')
    # 무작위의 정수 인덱스

# 3. 비복원 추출
import random
print(random.sample(li.tolist(), 5))
# random.sample은 list type을 원함

# 이렇게 기초 numpy는 끝~