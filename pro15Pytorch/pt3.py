# 건강보혐평가원의 심층신경망과 딥러닝 프레임워크 보기(삼성노트)

# ----------------------------------------------------------------------------------------------------------
# < 딥러닝 프레임워크 >
# [입력층]


# [은닉층]


# [출력층]

# ----------------------------------------------------------------------------------------------------------

# 비용함수란?
# 비용함수 : 모델의 예측값과 실제값의 차이(오차)를 수치화하여 모델 성능을 개선한다.
# 즉, 최적의 weight(기울기)와 b(y절편)을 찾기 위해 역전파(Backpropagation)로 계산을 한다. 그때 경사하강법을 사용한다 ... 딥러닝에서는 최소제곱법을 쓰지 않고 경사하강법을 사용한다.

# 경사하강법이란?
# 경사하강법 : 함수의 기울기를 이용해 비용함수(손실함수)가 최솟값이 되는 매개변수를 반복적으로 찾는 최적화 알고리즘 
#             머신러닝과 딥러닝 모델이 예측 오차를 줄이며 학습할 때 핵심적으로 사용
#             -> 기본원리 : 현재 위치에서 기울기(미분값)를 계산한 뒤, 함수값이 줄어드는 기울기의 반대 방향으로 일정 크기만큼 이동하는 과정을 반복

# <최소제곱법 vs 경사하강법>
# 최소제곱법(전통적인 ML모델이 사용) : 예측값과 실제값의 오차 제곱합이 최소가 되도록 모델의 파라미터를 구하는 방법
# 경사하강법(DL(DeepLearning)모델에서 사용) : 손실함수의 기울기를 계산하여 파라미터를 반복적으로 갱신하는 알고리즘

# 결국 둘 다 "평균제곱오차(MSE)"를 구한다는 최종 공통점이 존재한다.
# MSE가 작아야 예측이 정확한 모델임을 나타낸다.

print("1. 비용(cost) 구하기 - numpy + math 사용")
import math
import numpy as np
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # OpenMP 런타임 중복 우회

# a. 실제값과 모델의 예측값이 큰 경우 = w, b의 신뢰도가 낮을 때
real = np.array([10, 9, 3, 2, 11])  # 실제값
pred = np.array([11, 5, 2, 4, 11])  # 모델이 예측한 값1

cost = 0

# 실제값과 모델의 예측값의 차이(오차)
for i in range(len(real)):  # MSE(평균제곱오차)를 직접 계산
    cost += math.pow(pred[i] - real[i], 2)
    print(cost)

print('cost : ', cost / len(real))
# 결과 : cost : 17.2
# = 모델이 예측한 값과 실제값의 차이가 크다. = 성능이 좋지 않다.
print()

# b. 실제값과 모델의 예측값이 작은 경우 = w, b의 신뢰도가 높을 때
pred2 = np.array([10, 8, 3, 4, 10])  # 모델이 예측한 값2

cost = 0

# 실제값과 모델의 예측값의 차이(오차)
for i in range(len(real)):   # MSE(평균제곱오차)를 직접 계산
    cost += math.pow(pred2[i] - real[i], 2)
    print(cost)

print('cost : ', cost / len(real))
# 결과 : cost : 1.2
# = 모델이 예측한 값과 실제값의 차이가 작다. = 성능이 좋다.
# = MSE값이 작다.


# 그럼 이제부터 경사하강법에서 최적의 w, b는 어떻게 구하는지 알아보자. 
print()

print("2. 최적의 w(weight(가중치))얻기") 
import torch
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 선형회귀 모델 수식 : hypothesis = (w*x) + b
# 여기서는 w를 자동으로 학습시키는 것이 아니라 직접 변경하며 각 w에서 cost의 변화를 확인한다.
x = torch.tensor([1, 2, 3, 4, 5], dtype=torch.float32)  # = feature(독립변수)
y = torch.tensor([1, 2, 3, 4, 5], dtype=torch.float32)  # = label(종속변수)
b = 0 # bias는 편의상 '0'으로 고정
# 지도학습이다.

w_val = []
cost_val = []

# 임의의 모델 생성
for i in range(-50, 50):
    feed_w = i * 0.1  # 0.1은 learnigrate(학습율)이다.
    hypothesis = feed_w * x + b
    cost = torch.mean(torch.square(hypothesis - y))  # 비용함수(MSE)를 구한다!! = 모델성능평가

    cost_val.append(cost.item())
    w_val.append(feed_w)
    print(f'{i} : cost : {cost.item()}, weight:{feed_w}')

# w에 따른 cost변화 시각화
plt.plot(w_val, cost_val, marker='o')
plt.xlabel('w(가중치)')
plt.ylabel('cost(손실or비용)')
plt.title('가중치 w의 변화에 대한 비용함수 cost')
plt.grid()
plt.show()

# 우리 local에서 vs code로 실습을 하게 되면 matplotlib가 떴다가 사라진다.
# 그래서 34번, 35번째 줄의 import os, os.enviorn으로 실행환경을 설정해주어야한다.

# 경사하강법이란? ... model이 처음 생성될 때 w값이 랜덤으로 생성된다. 그때 weight값에 대한 cost값이 최소가 되는 지점을 접선의 기울기를 통해서 구한다. 그때 접선의 기울기가 100%로 '0'이 되는 지점을 찾아다니는 것이 아니라 적당히 95%정도 되면 그 지점을 택한다.
# weight를 늘리면 cost가 점점 줄어든다. 왼쪽이든 오른똑이든 weight값을 조금씩 주면 천천히 학습한다. 그러면서
# cost가 가장 작아지는 지점을 찾는다(중간지점으로 weight가 '1'일 때 cost가 제일 작다). 이때 학습하는 정도를 학습율(Learningrate)라고 한다.
# 느리다는 이유로 Learningrate를 너무 많이 줘버리면 cost의 minimize가 되는 지점을 못찾을 수 있다.
# 즉, Learningrate가 너무 크면 cost의 최솟값을 놓칠 수 있고
# 너무 작으면 cost값을 찾는데 시간이 오래걸린다.
# "weight값과 Learningrate를 조율하여 cost의 최소값을 찾는다!"

# 여기서 weight는 미분을 통해서 구한다. = 곡선에 접하는 접선의 기울기 값을 구해야한다. 
# 기울기 값이 음수면 w값을 오른쪽으로 이동시키고 양수면 w값을 왼쪽으로 이동한다. = 경사하강법
# 그러다 w값에 대한 기울기가 0이되는 지점이 cost가 minimize되는 지점이다. 즉, cost가 가장 작은 값은 접선의 기울기가 0이되는 지점을 구한다.

# ... 다음 시간에 이어서!
print("3. Parameter갱신방법") 
# Parameter조정방법
print()

print("4. 단순선형회귀모델로 최적weight값(cost최솟값)구하기") 
# 단순선형회귀모델(LinearRegression Model)로 실습해보자.