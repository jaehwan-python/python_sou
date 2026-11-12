# Classification의 마지막 알고리즘 : 최근접 이웃 = K-Nearest Neighbors
# KNN알고리즘 : 우리가 예측하려고 하는 임의의 데이터와 거리가 가장 가까운 k개의 데이터를 찾아 다수결에 의해 데이터를 예측하는 방법
# 두 집단에 대해서 해당 값(*)이 어디 class에 속하는지 동심원을 그려서 찾는다.
# 해당 값(*)을 기준으로 동심원을 그리고 그 동심원 안에 클래스의 데이터가 몇 개 들어있는지 다수결로 따진다.
# 만약 동심원 안에 여러 클래스의 값이 동일한 갯수로 들어있다면 "해당 값(*)과 클래스의 값(점) 사이의 거리"를 구한다.

# 두 점 사이의 거리
# - 맨해튼 거리(L1)
# - 유클리디안 거리(L2) ... 주로 사용한다. 

# 이러한 KNN 알고리즘은 데이터 전처리 시 표준화, 정규화 과정이 필수적이다!!

# --------------------------------------------------------------------

# [1단계] : 데이터 불러오기 및 변수설정
# 1. Lib 불러오기
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 2. 데이터 불러오기...처음이니까 직접 데이터를 만들어서 연습해보자 
# 독립변수(train)
train = [
    [5, 3, 2],
    [1, 3, 5],
    [4, 5, 6]
]
# 종속변수(label)
label = [0, 1, 1]

# (5, 3) → label 0
# (1, 3) → label 1
# (4, 5) → label 1
# 여기서 label은 각 데이터가 속한 클래스(종류)이다. 그래프에서는 색깔로 구분한 것

# 시각화
train = np.array(train)
plt.scatter(train[:, 0], train[:, 1], c=label, s=100, cmap='coolwarm')
# 모든 행의 첫 번째 값(5, 1, 4), 모든 행의 두 번째 값(3, 3, 5), c=label(0, 1, 1)에 따라 색 지정
plt.xlabel('특성1')
plt.ylabel('특성2')
plt.show()


# [2단계] : 모델 생성 및 학습  # 가까운 이웃 3개를 참조, 가까운 이웃일수록 더 높은 가중치를 부여
# 1. 모델 생성 
kmodel = KNeighborsClassifier(n_neighbors=3, weights='distance')

# 2. 모델 학습
kmodel.fit(train, label)


# [3단계] : 모델 예측 및 평가
# 1. 모델 예측
pred = kmodel.predict(train)
print('pred : ', pred)
# 결과 : pred :  [0 1 1]

# 2. 모델 평가(분류정확도평가)
print(f"test acc : {kmodel.score(train, label)}")
# 결과 :  test acc : 1.0

# 3. 새로운 데이터로 예측
new_data = [[1, 2, 9],
            [6, 2, 1]]
new_pred = kmodel.predict(new_data)
print('새로운 데이터에 대한 예측값 : ', new_pred)


# 클라우드, physicalAI, github, notion, 네트워크 공부해보기 
# NVIDA의 아이작 심 써보기

# 다음은 Breast_cancer_dataset으로 KNN을 학습해보자
# breat_cancer_dataset
# x : 세포의 측정값 : 30개
# y : 악성(0), 양성(1)
# 그리고 569개의 sample이 존재