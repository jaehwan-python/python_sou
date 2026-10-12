# 이번엔 배열을 연산해보자.
# 기본수학함수는 배열에 요소별로 적용되고, +, -, *, / 또는 add(), subtract(), multiply(), divide()함수를 사용
# 벡터와 연산을 하므로 for문을 사용하지 않고 바로 배열에 대한 연산 가능하다.

import numpy as np


# 1. dtype변경
x = np.array([
    [1,2],
    [3,4]
    ])
# x는 (2,2)의 배열이다
print(x, ' ', x.dtype)  # 결과 : [[1 2]
#                                 [3 4]]   int64

x = np.array([
    [1,2],
    [3,4]
    ], dtype=np.float32)
print(x, ' ', x.dtype) # 결과 : [[1. 2.]
#                                [3. 4.]]   float32

x = np.array([
    [1.,2],
    [3,4]
    ])
print(x, ' ', x.dtype) # 결과 : [[1. 2.]
#                                [3. 4.]]   float64


# 2. arange()함수 : 1차원 배열 생성
y = np.arange(5, 9) 
print(y,  ' ', y.dtype)  # 결과 : [5 6 7 8]  int64  -> 1차원 배열 생성



# 3. reshpae()함수 : 기존 배열 구조변경 
y = np.arange(5, 9).reshape(2,2) # 1차원 배열인 y를 reshape하여 (2, 2)구조로 만든다 (1차원 -> 2차원)
y = y.astype(np.float32) # type변경(int64를 float32로 바꾼다)
print(y, ' ', y.dtype) # 결과 [[5. 6.]
#                             [7. 8.]]  float32

print(x.ndim, ' ', y.ndim) # 결과 : 2  2
print()



# 4. 연산
# numpy 함수(유니버셜 함수) - 위보다 연산이 빠름 : 내부적으로 벡터화하여 연산하기 때문이다.
# numpy function = universal function이다.
# 이때 x의 데이터는 np.array여야만 한다.

# 4-1. add()
print(x+y)
print(np.add(x, y)) # numpy 함수(유니버셜 함수) - 위보다 연산이 빠름

# 4-2. subtract()
print(x-y)
print(np.subtract(x, y))

# 4-3. multiply()
print(x * y)
print(np.multiply(x, y))

# 4-4. divide()
print(x/y)
print(np.divide(x, y))

# 4-5. 그 외
print(np.sqrt(x), ' ', np.exp(x), ' ', np.log(x), ' ', np.cos(x))
