# Linear Regression은 선형회귀로 정량적인 '예측'을 하였고(Regression)
# Logistic Regressions 로지스틱 회귀분류로 정성적인 '분류'를 쓴다.(Classification)
# Decision Tree는 분류의 일종으로 이제 정성적 분류와 정량적 예측 모두 할 수 있는 모델이다.

# DecisionTree(의사결정나무) 분류 모델
# 데이터 균일도에 따른 규칙기반의 결정트리
# 트리는 데이터를 직각(수직과 수평)기준으로 나누면서 영역을 만든다.
# LinarRegression에서 Random Forest로 넘어가기 위한 중간 다리 역할을 Decision Tree가 해준다.

# Decision Tree : 데이터에 있는 규칙이나 패턴을 if_then 형태의 나무구조로 나타내어 분류나 회귀를 수행하는 지도학습모델

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn. tree import DecisionTreeClassifier, plot_tree

x, y = make_classification(n_samples=100, n_features=2, n_redundant = 0, n_informative=2, random_state=42)
# n_informative : 분류에 더 적합한 독립변수 2개 생성
print(x[:3])
print(y[:3])

# Decision Tree는 크게 2가지 계수를 가진다.
# GINI Impurity
# Entropy Impurity

# 지니 불순도(GINI)를 기준으로, 최대 깊이 3으로 제한하는 분류모델을 생성
# GINI Impurity는 하나의 노드에 서로 다른 클래스가 얼마나 섞여 있는지를 나타낸다.
# ex) class 0 (100%)  class 1 (0%) : 완전순서
#     class 0 (50%)   class 1(50%) : 불순도 가장 높음
model = DecisionTreeClassifier(criterion='gini', max_depth=3) # tree 최대 길이
# 깊이가 너무 크면 학습 데이터에 과적합될 수 있고, 너무 작으면 과소적합될 수 있다.

model.fit(x,y)
print('Train Accuracy : ', model.score(x, y))
# 결과 ; 1.0


# 시각화
plt.figure(figsize = (10, 6))
plot_tree(model, feature_names=['x1', 'x2'], class_names = ['0','1'], filled=True) 
plt.show()
# 지니 불순도를 기준으로 분류함
# 분할기준 : GINI
# 내부적으로 알고리즘을 통해 어떤계수를 어떻게 사용하여 분류할지 알아서 처리해준다.

# 결정 경계 시각화
xx, yy = np.meshgrid(   # x축, y축 값을 조합해서 좌표격자를 생성
    np.linspace(x[:,0].min(), x[:,0].max(), 100),  # x1범위를 100개의 구간으로 나누었다.
    np.linspace(x[:,1].min(), x[:,1].max(), 100),
)

# 모든 좌표에 대해서 예측값을 계산
z = model.predict(np.c_[xx.ravel(), yy.ravel()])
z = z.reshape(xx.shape) # 예측결과를 원래 grid로 변환
print(z)

plt.contour(xx, yy, z, alpha=0.3) # 영역을 색으로 채워 결정경계를 표현
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.title("Decision Tree Model's Boundary")
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()

# Logistic Regression과 달리 계단형으로 구분지어서 분류하고 있다.