# Perceptron : sklearn이 제공하는 단층신경망(뉴런과 노드가 존재)
# 이항분류(y=wx+b)(sigmoid함수) 가능 = Regression보다 Classification을 해본다.
# 활성화 함수는 기본적으로 계단함수(step function)를 사용한다. = 이항분류가 기본이다.

# 활성화 함수의 종류  ->  sigmoid  /  tanh  /  ReLU  /  Leaky ReLU  /  Maxout  /  ELU  /  softmax  /  Linear
# 입력층 : 
# 은닉층 : tanh  /  ReLU  /  Leaky ReLU  /  Maxout  /  ELU
# 출력층 : linear(하나로 나갈 때) / sigmoid(2개 노드로 출력층을 나갈 때) / softmax(3개 이상의 노드로 출력층을 나갈 때)
# 병렬 연산을 해야하기 때문에 GPU가 중요함
# 다음카페 - ML - https://alexlenail.me/NN-SVG/index.html - perceptron구조 확인해보기

# 실습1) 논리회로 분류
import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

feature = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # 2차원
print(feature)
# label = np.array([0,0,0,1])     # and : 두 조건이 모두 참이어야  참
# label = np.array([0,1,1,1])     #  or : 두 조건 중 하나라도 참이면 참
# label = np.array([0, 1, 1, 0])  # XOR : 두 입력이 서로 다를 때만 1이 되는 논리 연산

# AND는 두 입력이 모두 '1'일 때만 '1', OR는 입력 중 하나라도 '1'이면 1'이다.
# feature 순서가 [0,0], [0,1], [1,0], [1,1]이므로
# AND의 label은 [0,0,0,1], OR의 label은 [0,1,1,1]이다.
label = np.array([0, 1, 1, 0])

# 헌데 단층 퍼셉트론은 xor을 완전히 분류할 수 없다. 왜냐하면 내가 찍은 점을 좌표에 찍었을 때, 
# 하나의 직선으로 클래스 0과 1을 나눌 수 없기 때문이다. 
# 그래서 은닉층이 있는 다층 신경망을 사용해야 한다.

ml = Perceptron(max_iter=100).fit(feature, label)
# max_iter = 학습횟수.
# 1회 학습은 epoch : 전체 학습 데이터를 한 번 모두 학습하는 것을 뜻함.
pred = ml.predict(feature)
print('pred : ', pred)
print('acc : ', accuracy_score(label, pred))

#Perceptron은 딥러닝의 경사하강법과는 달리 틀린 것만 고치는 알고리즘
# 흐름 : 예측 -> 맞았는지 확인 -> 틀리면 Weight를 갱신, 맞으면 통과 -> 이 과정 반복
# 선형회귀식 사용(LogisticRegresion에서 힌트 얻음) : 선형 결합으로 결정 경계 계산
#  - input에 대한 가중치 합 계산 후 실제값과 예측값 비교(Loss function)
#  - 기본 퍼셉트론 학습 규칙으로 직접 가중치(W) 갱신하기를 max_iter만큼 반복함

# 학습 원리
# 1. 입력값과 가중치의 선형 결합 계산 (z = wx + b)
# 2. 활성화 함수(계단 함수)를 사용하여 선형결합의 결과를 0 또는 1로 변환
#    계산 결과를 이용해 클래스 예측
# 3. 실제값과 예측값 비교
# 4. 틀리게 예측한 경우 가중치(W)와 편향(b)을 갱신
# 5. 전체 학습 데이터를 반복하면서 분류 오류를 줄임
print()

# ----------------------------------------------------------------------
# 실습2) 일반 자료 분류
x = np.array([
    [2,3],
    [3,3],
    [1,1],
    [5,2],
    [6,1]
])
y = np.array([1, 1, 1, -1, -1])

model2 = Perceptron(max_iter=100, eta0 = 0.1, random_state=42) # eta0 : 학습율(학습량)을 의미한다.
# eta0는 적당히 주는 것이 중요하다.
# 너무 크면 성큼성큼 학습하기에 중간에 데이터를 놓칠 수 있고
# 너무 작으면 학습시간이 너무 오래 걸린다.

model2.fit(x, y)
pred2 = model2.predict(x)
print('예측값 : ', pred2)
print('실제값 : ', y)
print('정확도 : ', accuracy_score(y, pred2))

# Parameter확인
print('가중치(w, weight) : ', model2.coef_)   # 회귀계수(기울기)의 값
print('편향(b, bias) : ', model2.intercept_) # 회귀계수(절편)의 값
# x는 2개의 열을 가지고 있음 = 2개의 독립변수를 가짐
# 결과 : 
# ->  가중치(w, weight) :  [[-0.4  0.8]]
# ->  편향(b, bias)     :  [0.4]
# "예측y값 = (-0.4*x1) + (0.8*x2) + 0.4"

# 결정경계(w1*x1 + w2*x2 + b)의 시각화
import matplotlib.pyplot as plt
plt.scatter(x[:,0], x[:,1], c=y, cmap='bwr')
weight = model2.coef_[0]
bias = model2.intercept_[0]
x_vals = np.linspace(0, 7, 100)
y_vals = -(weight[0] * x_vals + bias) / weight[1]
plt.plot(x_vals, y_vals)
plt.title('sklearn Perception')
plt.xlabel('x1')
plt.ylabel('x2')
plt.show()

# MLP를 이용하여 익숙해져야 한다!! = 다층 퍼셉트론