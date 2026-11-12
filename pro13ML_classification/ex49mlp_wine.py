# 실습) 이번에는 mlp를 wine데이터셋에서 보자. iris 데이터처럼 다항 분류를 wine 데이터셋으로 알아보자.

# wine 데이터셋 : 와인 178개의 화학 성분을 이용해 '3가지' 포도 품종을 분류하는 데이터셋이다.
# 독립변수(X, feature) : 알코올, 사과산, 색의 강도 등 와인의 특성 13개로, data.data에 저장된다.
# 종속변수(y, label)   : 각 와인의 포도 품종을 나타내는 클래스 0, 1, 2로, data.target에 저장된다.
# data = load_wine()으로 불러오면 X의 크기는 (178, 13), y의 크기는 (178,)이다.
# 총 smaple수 : 178개
# 클래스(target) 수 : 3개(각각 59개, 71개, 48개의 sample)


# [1단계] : 데이터 불러오기 및 변수설정 
# 1. 데이터 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 2. 변수설정
data = load_wine()
x = data.data   # 와인 178개의 특성 13개 → (178, 13)
y = data.target # 각 와인의 품종 0, 1, 2 → (178,)
# 특성이 13가지고 와인의 종류는 3가지이고 모든 와인의 갯수는 178개이다.
print(x[:2], ' ', x.shape)      # (178, 3)
print(y[:2], ' ', np.unique(y)) # [0  0]  [0  1  2]
# [0  0]  ->  '처음 두 행의 와인의 정답'
# [0 1 2] ->  '전체 178개 정답에서 중복을 제거'

# 3. 과적합 방지
# - train / test split o
# - KFold
# - GridSearchCV
# - L1, L2규제
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# 4. scaling 
# 입력값(x값)들을 표준화, 정규화하여 정갈하게 만든다!
# mlp는 꼭 scaling(표준화, 정규화)를 해주어야 한다!!
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test) # 학습 데이터에서 구한 평균과 표준편차를 그대로 적용한다.


# [2단계] : 모델 생성 및 학습
# 1. 모델 생성
model = MLPClassifier(
    hidden_layer_sizes=(20,10), # 은닉층이 2개이고, 첫 번째는 뉴런 20개, 두 번째는 뉴런 10개
    activation='relu',          # 은닉층의 활성화 함수(relu): 음수는 0으로 바꾸고, 양수는 그대로 전달한다.
    solver='adam',              # 손실을 줄이도록 가중치와 편향을 수정하는 최적화 알고리즘이다.
    learning_rate_init=0.001,   # 초기 학습률 : 가중치와 편향의 수정 크기에 영향을 주며, Adam이 실제 수정 크기를 조절한다.
    max_iter=1000,              # Adam 기준으로 전체 학습 데이터를 최대 1000번 반복 학습한다. 종료 조건을 만족하면 일찍 멈출 수 있다.
    random_state=42,            # 가중치 초기화와 데이터 섞기 등에 사용하는 난수 시드로, 같은 조건에서 결과를 재현하기 위한 설정이다.
    verbose=1                   # 학습 중 반복 횟수와 손실(loss)을 출력한다. False로 설정하면 출력하지 않는다.
)
#     입력층         은닉층1        은닉층2         출력층
#      13개     →     20개     →     10개     →     3개
#  와인 특성 13개                                와인 품종 3종

# 2. 모델 학습
model.fit(x_train_scaled, y_train)

# [3단계] : 모델 예측 및 평가
# 1. 모델 예측
pred = model.predict(x_test_scaled) # y_test와 비교하기 위해 테스트 데이터 36개를 예측한다.

# 2. 모델 평가(분류정확도)
print('분류 정확도 평가1(accuacy_score) : ', accuracy_score(y_test, pred))
print('분류 정확도 평가2(confusion_matrix) : ', confusion_matrix(y_test, pred))
print('분류 정확도 평가3(classification report) : ', classification_report(y_test, pred))

# confusion matrix(혼동행렬) 시각화
cm = confusion_matrix(y_test, pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('혼동행렬(confusion_matrix)')
plt.xlabel('예측값(predict)')
plt.ylabel('실제값(actual)')
plt.show()

# 이렇게 scklearn이 지원하는 지도학습이 끝났다!
