# < 기술 통계 관련 연습문제 >


print( '1번 : array 관련 문제')
# 1번 : array 관련 문제
# 정규분포를 따르는 난수를 이용하여 5행 4열 구조의 다차원 배열 객체를 생성하고, 각 행 단위로 합계, 최댓값을 구하시오.

# < 출력 결과 예시>
# 1행 합계   : 0.8621332497162859
# 1행 최댓값 : 0.3422690004932227

# 2행 합계   : -1.5039264306910727
# 2행 최댓값 : 0.44626169669315

# 3행 합계   : 2.2852559938172514
# 3행 최댓값 : 1.5507574553572447

import numpy as np
np.random.seed(42)
data = np.random.randn(5, 4)
print(data)

i = 1
for row in data:
    print(f'{i}행 합계 : ', np.sum(row))
    print(f'{i}행 최댓값 : ', np.max(row))
    i += 1
print()
for a in data.sum(axis=1):
    print(a)
    # 오직 행 합계만 따로 출력할 수 있다.


print( '2번 : indexing 관련 문제')
# 2번 : indexing 관련 문제
# 2번-1. 6행 6열의 다차원 zero 행렬 객체를 생성한 후 / 다음과 같이 indexing 하시오.

#   조건1> 36개의 셀에 1~36까지 정수 채우기
#   조건2> 2번째 행 전체 원소 출력하기 
#              출력 결과 : [ 7.   8.   9.  10.  11.  12.]
#   조건3> 5번째 열 전체 원소 출력하기
#              출력결과 : [ 5. 11. 17. 23. 29. 35.]
#   조건4> 15~29 까지 아래 처럼 출력하기
#              출력결과 :  [[15.  16.  17.]
#                          [21.  22.  23]
#                          [27.  28.  29.]]

zarr = np.zeros((6, 6))
print(zarr)
# (6,6)형태의 모든 값이 0인 배열을 만들어라

cnt = 0
for i in range(6):
    for j in range(6):
        cnt += 1
        zarr[i, j] = cnt

print(zarr)

print(zarr[1, :])
print(zarr[:, 4])
print(zarr[2:5, 2:5])

# 2번-2  :  6행 4열의 다차원 zero 행렬 객체를 생성한 후 아래와 같이 처리하시오.

#     조건1> 20~100 사이의 난수 정수를 6개 발생시켜 각 행의 시작열에 난수 정수를 저장하고, 두 번째 열부터는 1씩 증가시켜 원소 저장하기
#     조건2> 첫 번째 행에 1000, 마지막 행에 6000으로 요소값 수정하기

# <<출력 예시>>
# 1. zero 다차원 배열 객체
#  [[ 0.  0.  0.  0.]
#        ...
#   [ 0.  0.  0.  0.]]

# 2. 난수 정수 발생
# random.randint(s, e, n)


# 3. zero 다차원 배열에 난수 정수 초기화 결과. 두 번째 열부터는 1씩 증가시켜 원소 저장하기
# [[  90.   91.   92.   93.]
#  [  40.   41.   42.   43.]
#  [ 100.  101.  102.  103.]
#  [  22.   23.   24.   25.]
#  [  52.   53.   54.   55.]
#  [  71.   72.   73.   74.]]

# 4. 첫 번째 행에 1000, 마지막 행에 6000으로 수정
#  [[ 1000.  1000.  1000.  1000.]
#   [   40.    41.    42.    43.]
#   [  100.   101.   102.   103.]
#   [   22.    23.    24.    25.]
#   [   52.    53.    54.    55.]
#   [ 6000.  6000.  6000.  6000.]]

zarr2 = np.zeros((6, 4))
print(zarr2)

ran = np.random.randint(20, 100, 6)
print(ran)
# 결과 : [81 81 66 81 70 74]

ran = list(ran)
for row in range(len(zarr2)):
    num = ran.pop(0)
    for col in range(len(zarr2[0])):
        zarr2[row, col] = num
        num += 1

print(zarr2)
zarr2[0][:] = 1000
zarr2[-1][:] = 6000
print(zarr2)
# 결과 : [[1000. 1000. 1000. 1000.]
#         [  81.   82.   83.   84.]
#         [  66.   67.   68.   69.]
#         [  81.   82.   83.   84.]
#         [  70.   71.   72.   73.]
#         [6000. 6000. 6000. 6000.]]


# 3) step3 : unifunc 관련문제

#  표준정규분포를 따르는 난수를 이용하여 4행 5열 구조의 다차원 배열을 생성한 후
#  아래와 같이 넘파이 내장함수(유니버설 함수)를 이용하여 기술통계량을 구하시오.
#  배열 요소의 누적합을 출력하시오.

# <<출력 예시>>

# ~ 4행 5열 다차원 배열 ~

# [[ 0.56886895  2.27871787 -0.20665035 -1.67593523 -0.54286047]

#            ...

# [ 0.05807754  0.63466469 -0.90317403  0.11848534  1.26334224]]

arr3 = np.random.randn(4, 5) # 4행 5열짜리 데이터를 난수생성을 통해서 만들었다.
print(arr3)

print('------------- 기술 통계량 -----------')

print('평균 : ', np.mean(arr3)) # = arr3.mean() 이렇게 적어주어도 된다.
print('합계 : ', np.sum(arr3))
print('표준편차 : ', np.std(arr3))
print('분산 : ', np.var(arr3))
print('최댓값 : ', np.max(arr3))
print('최솟값 : ', np.min(arr3))

print('1사분위수 : ', np.percentile(arr3, 25))
print('2사분위수 : ', np.percentile(arr3, 50))
print('3사분위수 : ', np.percentile(arr3, 75))
# 전체 데이터를 작은 값부터 큰 값까지 순서대로 나열한 뒤 , 이를 4등분하는 지점에 있는 값

print('누적합 : ', np.cumsum(arr3))

print()



# < numpy 문제 추가 ~ >
# Q1) 브로드캐스팅과 조건 연산(전치)
# 다음 두 배열이 있을 때,

a = np.array([[1], [2], [3]])
b = np.array([10, 20, 30])

# 두 배열을 브로드캐스팅하여 곱한 결과를 출력하시오.
# 그 결과에서 값이 30 이상인 요소만 골라 출력하시오.

result = a * b
print('result : ', result)
print(result[result >= 30])

print()


# Q2) 다차원 배열 슬라이싱 및 재배열
# - 3×4 크기의 배열을 만들고 (reshape 사용),  
# - 2번째 행 전체 출력
# - 1번째 열 전체 출력
# - 배열을 (4, 3) 형태로 reshape
# - reshape한 배열을 flatten() 함수를 사용하여 1차원 배열로 만들기
arr = np.arange(1, 13).reshape(3,4)
print(arr)
print(arr[1])
print(arr[:,0])
resh = arr.reshape(4, 3)
print(resh)
# 차원 떨어트리기(2차원 -> 1차원) : flatten(), ravel()함수 : 한 차원씩 떨어트린다.
# flatten() : 복사본을 만들어서 동작하기 때문에 원본에 영향이 가지 않는다. 메모리 낭비가 있다
# ravel() : 원본을 그대로 바꾸기 때문에 메모리 측면에서 효율적이다.
flat = resh.flatten() 
# flat = resh.ravel()을 사용해도 동일한 결과값이 나온다.
print(flat)

print()


# Q3) 1부터 100까지의 수로 구성된 배열에서 3의 배수이면서 5의 배수가 아닌 값만 추출하시오.
# 그런 값들을 모두 제곱한 배열을 만들고 출력하시오.
arr = np.arange(1, 101, 1)
imsi = (arr % 3 == 0) & (arr % 5 != 0)
print(imsi)

filtered = arr[imsi]
print(filtered)
# bool값을 숫자로 출력하게 된다.

squ = filtered **2
print(squ)

print()


# Q4) 다음과 같은 배열이 있다고 할 때,
# arr = np.array([15, 22, 8, 19, 31, 4])
# 값이 10 이상이면 'High', 그렇지 않으면 'Low'라는 문자열 배열로 변환하시오.
# 값이 20 이상인 요소만 -1로 바꾼 새로운 배열을 만들어 출력하시오. (원본은 유지)
# 힌트: np.where(), np.copy()
arr = np.array([15, 22, 8, 19, 31, 4])

# where()함수를 사용한 경우
labels = np.where(arr >= 10, 'High', 'Low')
print(labels)

# copy()함수를 사용한 겨우
new_arr = np.copy(arr)
new_arr[new_arr >= 20] = -1
print(new_arr)


print()


# Q5) 정규분포(평균 50, 표준편차 10)를 따르는 난수 1000개를 만들고, 상위 5% 값만 출력하세요.
# 힌트 :  np.random.normal(), np.percentile()
data = np.random.normal(loc=50, scale=10, size=1000)
# 평균 : loc -> 50에 근접한다
# 표준편차 : scale -> 10이라는 표준편차를 가진다.
print(data)

threshold = np.percentile(data, 95)
top5 = data[data > threshold]
print('top5 : ', top5)
