# Breast_cancer_dataset으로 KNN을 학습해보자
# breat_cancer_dataset
# x : 세포의 측정값 : 30개
# y : 악성(0), 양성(1)
# 그리고 569개의 sample이 존재

# [1단계] : 데이터 불러오기 및 변수설정
# 1. Lib불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer # 유방암 데이터셋 불러오기
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler # KNN의 '표준화'와 '정규화'가 필수이다!!
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 2. 변수 설정 
data = load_breast_cancer()
x = data.data    # feature(독립변수)
y = data.target  # label(종속변수)
print(x[:2], ' ', x.shape)
# x[:2] : 첫 번째와 두 번째 샘플의 측정값을 출력한다. 각 행은 샘플 1개, 각 열은 특성 1개이다.
# x.shape = (569, 30) : 전체 샘플이 569개이고, 샘플마다 세포핵의 측정 특성이 30개 있다는 뜻이다.
print(y[:2], ' ', np.unique(y))
# y[:2] = [0 0] : 첫 번째와 두 번째 샘플의 정답이 모두 0(악성)이라는 뜻이다. x[:2]의 각 행과 순서대로 대응한다.
# np.unique(y) = [0 1] : 전체 정답에서 중복을 제거한 클래스 목록이다. 0은 악성, 1은 양성이며 개수나 확률이 아니다.

# 3. 과적합 방지 : train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# 4. 스케일링 필요(이유 : KNN은 거리기반 모델이기 때문에 크기가 영향을 미치기 때문에 스케일링(정규화/표준화)가 필요하다)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.fit_transform(x_test)

# K-NN모델에서는 k값이 중요하다. k값이 작으면 과적합, k값이 크면 과소적합이 발생한다.
# 그래서 최적의 k값을 확인하는 것이 중요하다.
train_acc = []
test_acc = []
k_range = range(3, 12, 2)
# 3~11까지 2단위씩 띄어서 표시 = 홀수만 표시

for k in k_range:
    # [2단계] : 모델 생성 및 학습
    # 1. 모델 생성
    model = KNeighborsClassifier(n_neighbors=k)
    # 2. 모델 학습
    model.fit(x_train_scaled, y_train)

    # [3단계] : 예측 및 평가
    # 1. 예측(x_train, x_test)
    y_train_pred = model.predict(x_train_scaled)
    y_test_pred = model.predict(x_test_scaled)
    # 2. 분류 정확도 평가
    train_acc.append(accuracy_score(y_train, y_train_pred))
    test_acc.append(accuracy_score(y_test, y_test_pred))

print(train_acc)
print(test_acc)

# test data의 정확도를 비교해서 k값을 선택함(... 좀 더 바람직한 방법은 GridSearchCV를 추천!)
best_idx = np.argmax(test_acc)
best_k = list(k_range)[best_idx]
best_acc = test_acc[best_idx]
print('최적의 k값 : ', best_k)
print('최고의 정확도 : ', best_acc)
# 결과 :
# 최적의 k값 :  3
# 최고의 정확도 :  0.9736842105263158

# 시각화
plt.figure()
plt.plot(k_range, train_acc, marker='o', c='b', label='train acc')
plt.plot(k_range, test_acc, marker='s', c='r', label='test acc')
plt.xlabel('k value')
plt.ylabel('accuracy')
plt.legend()
plt.grid()
plt.show()

# 그래프 해석:
# x축의 k value는 예측할 때 참고하는 가까운 이웃의 수(3, 5, 7, 9, 11)이다.
# y축의 accuracy는 정답을 맞힌 비율이다. 예를 들어 0.974는 약 97.4%의 정확도를 뜻한다.
# 파란 원(train acc)은 학습 데이터의 정확도, 빨간 사각형(test acc)은 테스트 데이터의 정확도이다.
# 이 결과에서 학습 정확도는 k에 따라 변하지만, 테스트 정확도는 모두 약 0.9737(97.37%)로 같다.
# 테스트 샘플은 114개이므로, 모든 k에서 111개를 맞히고 3개를 틀렸다는 뜻이다.
# 다만 정확도가 같아도 각 k에서 틀린 샘플까지 같다는 뜻은 아니다.
# np.argmax는 최댓값이 여러 개면 첫 번째 위치를 반환하므로 best_k가 3으로 선택된다.
# 따라서 k=3이 다른 k보다 테스트 정확도가 더 높은 것은 아니다. k 선택에는 교차검증을 활용할 수 있다.
# 두 선의 차이가 작으며, 이 그래프만으로 뚜렷한 과적합이나 과소적합을 단정하기는 어렵다.
# 참고: 위의 테스트 스케일링은 scaler.transform(x_test)를 사용해야 학습 데이터와 같은 기준이 적용된다.
# 현재처럼 테스트에 fit_transform을 쓰면 기준이 달라지므로, 이를 수정한 뒤 그래프를 다시 확인해야 한다.


# 이후 best_k값으로 모델을 생성한 후 예측하면된다

# <딥러닝> ... 나중에 더 자세히 배울 것이다.
# 활성화 함수의 종류  ->  sigmoid  /  tanh  /  ReLU  /  Leaky ReLU  /  Maxout  /  ELU  /  softmax  /  Linear
# 입력층 : 
# 은닉층 : tanh  /  ReLU  /  Leaky ReLU  /  Maxout  /  ELU
# 출력층 : linear / sigmoid / softmax
# 입력받은 값이 활성화함수를 통해 다음 노드로 이동한다.