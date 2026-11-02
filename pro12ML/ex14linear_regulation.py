# 과적합(Overfitting) : 머신러닝 모델이 학습 데이터에 지나치게 맞춰져 새로운 데이터에서는 성능이 떨어지는 현상
# ML모델 생성 시 굉장히 중요

# LinearRegression Overfitting : 선형회귀 모델이 훈련데이터에 너무 과하게 학습되어, 
#                                데이터에 포함된 노이즈(잡음)이나 지엽적인 특성까지 
#                                암기해 버리는 현상
# 특징 - 훈련 데이터에 대한 예측 오차는 매우 낮지만, 처음 보는 테스트 데이터나 새로운 데이터가
#        들어왔을 때 예측 성능(일반화 능력)이 크게 떨어진다.

# 선형회귀 과적합을 해결하는 방법
# 1. 특성 줄이기
# 2. 정규화 적용
# 3. 더 많은 데이터 수집하기

# 이 중에서 '정규화(Regularization) 적용하기'를 중점적으로 본다.
# 규제 : 회귀계수(파라미터)의 값이 너무 커지지 않도록 비용함수(Cost Function)에 패널티를 부과한다.
# 종류 - L1규제(Lasso 회귀) : 가중치들의 절대값 합을 최소화하며, 중요하지 않은 특성의 계수를 아예 0으로 만들어서 제거한다. 
#      - L2규제(Ridge 회귀) : 가중치들의 제곱합을 최소화하여 계수들을 0에 가깝게 작게 만든다.
#      - ElasticNet(Ridge + Lasso) : L1과 L2규제의 장점만 모아둠

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error

iris = load_iris()
print(iris.keys())
# 결과 : dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
pd.set_option('display.max_columns', None)

iris_df = pd.DataFrame(iris.data, columns = iris.feature_names)
iris_df['target'] = iris.target
iris_df['target_names'] = iris.target_names[iris.target]
print(iris_df.head(3))
#                   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)   target    target_names
#        0                5.1               3.5                1.4               0.2             0          setosa
#        1                4.9               3.0                1.4               0.2             0          setosa
#        2                4.7               3.2                1.3               0.2             0          setosa

