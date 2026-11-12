# MLP란 여러 개의 퍼셉트론 뉴런을 여러 층으로 쌓은 다층 신경망 구조이다
# 입력층과 출력층 사이에 하나 이상의 은닉층을 가지고 있는 신경망이다.
# 인접한 두 층의 뉴런 간에는 완전 연결  ->  fully connected된다.

# 인공신경망 구조 - FCNN - : 완전연결신경망
#                       - 한 층의 모든 뉴런이 다음 층의 모든 뉴런과 연결
#                - LeNet - : 초기의 대표적인 합성곱 신경망
#                        - 손글씨 숫자 같은 이미지 인식에 사용
#                - AlexNet - : LeNet보다 깊고 규모가 큰 CNN
#                          - 2012년 이미지 분류대회에서 뛰어난 성과를 내며 딥러닝 확산에 기여

# 실습1) 논리회로 분류
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# feature와 label 구분
feature = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # 2차원
print(feature)
# label = np.array([0,0,0,1])     # and : 두 조건이 모두 참이어야  참
# label = np.array([0,1,1,1])     #  or : 두 조건 중 하나라도 참이면 참
# label = np.array([0, 1, 1, 0])  # XOR : 두 입력이 서로 다를 때만 1이 되는 논리 연산

# AND : 두 입력이 모두 '1'일 때만 '1'
# OR : 입력 중 하나라도 '1'이면 1'이다.
# feature 순서가 [0,0], [0,1], [1,0], [1,1]이므로 
# 'AND'의 label은 [0,0,0,1]
# 'OR'의 label은 [0,1,1,1]이다.
label = np.array([0, 1, 1, 0]) # xor해결함

# MLP(Multi Layer Perceptron) : 입력층과 출력층 사이에 은닉층이 있는 인공신경망
# 입력층 : 특성입력
# 은닉층 : 패턴학습 -> 입력값에 가중치와 편향을 적용하고, 활성화 함수를 거쳐 패턴을 학습
# 출력층 : 예측결과
# max_iter의 추천 횟수 : 500 ~ 1000
model = MLPClassifier(max_iter=500, # 모델을 학습하는 최대 반복 횟수 = epoch
                    hidden_layer_sizes=10, # 은닉층 10개
                    solver='adam', # 가중치와 편향을 조정하는 최적화 방법 = cost(loss, 손실)최소화 방식 
                    learning_rate_init=0.01,
                    verbose=1
                    ).fit(feature, label)
print(model)
# 결과 : 
# Iteration 1, loss = 0.80704575
# Iteration 2, loss = 0.79198773
# Iteration 3, loss = 0.77869287
# Iteration 4, loss = 0.76603475
# ...
# Iteration 497, loss = 0.02664414
# Iteration 498, loss = 0.02654106
# Iteration 499, loss = 0.02644238
# Iteration 500, loss = 0.02634108
# loss(: 실제값과 예측값의 차이)가 점점 줄어드는 모습을 보인다.

print(model)
print("입력층 node 갯수 : ", model.n_features_in_)      # 입력층  : 2개
print("은닉층 node 갯수 : ", model.hidden_layer_sizes)  # 은닉층  : 10개
print("출력층 node 갯수 : ", model.n_outputs_)          # 출력층  : 1개
print("전체 층 수 : ", model.n_layers_)                 # 전체 층 : 3개

# 층과 층 사이의 가중치 확인
for i, weightt in enumerate(model.intercepts_):
    print(f"가중치 {i} : {weightt.shape}")

for i, biass in enumerate(model.intercepts_):
    print(f"편향 {i} : {biass.shape}")

pred = model.predict(feature)
print('pred : ', pred)
print('acc : ', accuracy_score(label, pred))

# 우리는 현재 지도학습을 보고있다. LogisticRegression이 아닌 MLPClassifier를 사용하는 지도 학습으로 이 또한 feature와 label을 받아 학습한다.
# feature = [[0, 0], [0, 1], [1, 0], [1, 1]]
# label   = [0,       1,      1,      0]
# 우리는 이 문제(feature)와 정답(label)을 보고 xor규칙이다고 부르지만, 모델은 and / or / xor중 무엇인지 구별하는 것이 아니다.
# model은 어떤 값(feature)을 넣으면 이런 값(label)이 나오도록 가중치와 편향을 계속 조정해 나간다.

print('\n--------------------------------------------')
# 실습2) 일반 자료로 분류
from sklearn.datasets import make_moons
# 비선형 분류 및 군집화를 위한 초승달 모야 데이터셋 생성 함수
from sklearn.model_selection import train_test_split

x, y = make_moons(n_samples=300, noise=0.2, random_state=42)
print(x[:2]) # 2차원 : 
print(y[:2]) # 1차원 : 

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model2 = MLPClassifier(hidden_layer_sizes=(10, 10), 
                        solver='adam',
                        max_iter=1000, 
                        random_state=42, 
                        activation='relu')
# node가 100개짜리인 layer 하나를 만들지 
# node가 10개인 layer10개를 만들지 model이 정한다.

# 활성화 함수(activation) : 뉴런이 계산한 값을 어떤 값으로 바꿔 다음 층에 전달할지 정하는 함수
# [입력 → 가중합 z = w₁x₁ + w₂x₂ + b → 활성화 함수 f(z) → 다음 층]
# 활성화 함수 종류 - step function / sigmoid fuction / softmax function / Tanh function / ReLU function / Leaky ReLU function / linear function
# 이 중 출력층에서 쓰이는 활성화 함수 -> 출력층이 1개 : linear function
#                                   -> 출력층이 2개 : sigmoid function
#                                   -> 출력층이 3개 이상 : softmax function

# 손실 최소화 : 예측이 정답에 가까워지도록 가중치(weight)와 편향(bias)을 조정하는 과정
# [입력 → 예측 → 손실 함수로 오차 계산 → 역전파로 기울기 계산 → 최적화 알고리즘으로 가중치와 편향 수정]
# 손실 함수(loss function) : 예측이 얼마나 틀렸는지 수치로 계산하는 함수
# 손실 함수 종류 - 교차 엔트로피 : 분류에 사용하며, 정답 클래스에 부여한 확률이 높을수록 손실이 작다.
#               - 평균제곱오차(MSE) : 회귀에 사용하며, 실제값과 예측값 차이의 제곱을 평균한다.
# 최적화 알고리즘(solver) : 계산한 손실을 줄이는 방향으로 가중치와 편향을 수정하는 방법
# 최적화 방법 종류 - SGD : 일부 학습 데이터로 구한 기울기를 이용해 가중치와 편향을 조금씩 수정한다.
#                  - Adam : 이전 기울기 정보를 활용하여 가중치별 수정 크기를 조절한다.
#                  - L-BFGS : 손실 곡면의 굽은 정도를 근사하여 수정 방향과 크기를 정한다.
# solver='adam' : 손실 함수의 이름이 아니라, 손실을 최소화하기 위해 사용하는 최적화 방법이다.
# learning_rate_init : Adam이나 SGD의 초기 학습률로, 가중치와 편향을 수정하는 크기에 영향을 준다.

# 학습률 : 손실을 줄이기 위해 가중치와 편향을 한 번에 얼마나 수정할지 정하는 값
# 새 가중치 = 기존 가중치 − 학습률 × 손실의 기울기
# 너무 크면   :  손실이 최소인 지점을 지나쳐 흔들리거나 학습이 불안정해질 수 있다.
# 너무 작으면 :  조금씩 이동하므로 학습이 오래 걸릴 수 있다.

model.fit(x_train, y_train)
pred = model.predict(x_test)
print('acc : ', accuracy_score(y_test, pred))
