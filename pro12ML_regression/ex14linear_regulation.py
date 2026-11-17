# 과적합(Overfitting) : 머신러닝 모델이 학습 데이터에 지나치게 맞춰져 새로운 데이터에서는 성능이 떨어지는 현상
# ML모델 생성 시 굉장히 중요

# LinearRegression Overfitting : 선형회귀 모델이 훈련데이터에 너무 과하게 학습되어, 
#                                데이터에 포함된 노이즈(잡음)이나 지엽적인 특성까지 
#                                암기해 버리는 현상
# 특징 - 훈련 데이터에 대한 예측 오차는 매우 낮지만, 처음 보는 테스트 데이터나 새로운 데이터가
#        들어왔을 때 예측 성능(일반화 능력)이 크게 떨어진다.

# 선형회귀 과적합을 해결하는 방법
# 1. 특성 줄이기
# 2. 정규화 적용 ㅇ
# 3. trian / test split ㅇ
# 4. 더 많은 데이터 수집하기

# 이 중에서 '정규화(Regularization) 적용하기'를 중점적으로 본다.
# 규제 : 회귀계수(파라미터)의 값이 너무 커지지 않도록 비용함수(Cost Function)에 패널티를 부과한다.
# 종류 - L1규제(Lasso 회귀) : 가중치들의 절대값 합을 최소화하며, 중요하지 않은 특성의 계수를 아예 0으로 만들어서 제거한다. 
#      - L2규제(Ridge 회귀) : 가중치들의 제곱합을 최소화하여 계수들을 0에 가깝게 작게 만든다.
#      - ElasticNet(Ridge + Lasso) : L1과 L2규제의 장점만 모아둠

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

iris = load_iris()
print(iris.keys())
# 결과 : dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
pd.set_option('display.max_columns', None)
# iris 데이터 준비

iris_df = pd.DataFrame(iris.data, columns = iris.feature_names)
iris_df['target'] = iris.target
iris_df['target_names'] = iris.target_names[iris.target]
print(iris_df.head(3))
#                   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)   target    target_names
#             0           5.1               3.5                1.4               0.2             0          setosa
#             1           4.9               3.0                1.4               0.2             0          setosa
#             2           4.7               3.2                1.3               0.2             0          setosa

# 지도학습 : 독립변수가 종속변수에 영향을 준다. 얼마만큼 어떻게 영향을 주는지 모델을 만드는 3가지 방식
# 방법 1 : fit_model = LinearRegression().fit(x, y)
# 방법 2 : model2 = smf.ols(formula='y~x', data=df).fit()
# 방법 3 : model = stats.linregress(x, y))
# 으로 확인할 수 있다.

# 독립변수가 연속형, 종속변수도 연속형인 회귀분석에서 정량적인 분석을 사용한다. = 문제지와 답지를 주고 모델이 학습하게 함.
# 이후 모두 다 만들어진 모델을 평가를 해야한다. 
# 평가방법 - ols표의 설명력
#         - predict()
#         - MSE/RMSE
# ** MSE(평균제곱오차) : 모델 내부 비교, 계산이 편리. 하지만 단위가 제곱된 값이다.
#    RMSE(route mse) : MSE를 제곱근한 값으로 제곱이 풀린다. = 원래 단위값을 사용한다.
# 하지만 평가 과정에서 선형회귀모델이 너무 과하게 학습되어 데이터에 포함된 노이즈나 특성까지 암기해버려 본래 예측에는 오히려 약해지는 경우,
# 그때 우리는 선형회귀모델의 과적합. LinearRegression Overfitting이라고 부른다.

# Train / Test Split : 해당 모델이 기존데이터 말고 나머지 데이터에 대해서 잘작동하는지 확인하기 위해 전체 데이터를 나누는 과정

# 모든 모델에서 Overfitting이 발생할 수 있지만, 우리는 선형회귀에 대해서 배우고 있으니 선형회귀에서 Overfitting을 해결하는 4가지 방법을 보자.
# - 1. 변수(feature)를 줄이기
# - 2. 정규화(Regularization) 적용하기 -> L1, L2규제, ElasticNet ... 이 정규화는 선형회귀모델만 검사가 가능하다.
# - 3. Train/Test split
# - 4. 더 많은 데이터 수집하기

print(iris_df.shape)
# 결과 : (150, 6)


# Train(학습) / Test(검증) 데이터로 분리
train_set, test_set = train_test_split(iris_df, test_size = 0.3, random_state=12, shuffle=True)
# 7 ㄷ 3으로 쪼갬
# 그전에 값들을 모두 섞어서 하나로 섞는다.
# print(train_set.shape, test_set.shape)
# print(train_set.head(3))
# print(test_set.head(3))

# 변수 설정
print(train_set.iloc[:, [2]]) # = 독립변수(x) : petal length(cm)
# 모든 행의 2열 : (105, 6)
print(train_set.iloc[:, [3]]) # = 종속변수(y) : petal width(cm)
# 모든 행의 3열 : (45, 6)
# 105와 6을 학습용 데이터로 사용하고
# 46와 6을 테스트용 데이터로 사용했다.

# 회귀분석 방법1 : LinearRegression
# 1-1. 학습은 train dataset 사용
model_linear = LinearRegression().fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])
print('slope : ', model_linear.coef_)
print('bias : ', model_linear.intercept_)

# 1-2. 모델 검증은 test dataset 사용
pred = model_linear.predict(test_set.iloc[:, [2]])
print("예측값 : ", np.round(pred[:5].flatten(), 1))
print("실제값 : ", test_set.iloc[:, [3]][:5].values.flatten())
# 학습데이터와 검증데이터를 이렇게 나누어서 진행한다.

# 결과 : 
# 예측값 :  [0.2  1.7  0.2  1.3  2.1]
# 실제값 :  [0.3  1.9  0.2  1.3  2.3]

# 설치한 모델의 설명력을 알아보기 위해서 결정계수를 알아보자!!
print(f'r2_score(결정계수) : {r2_score(test_set.iloc[:,[3]], pred)}')
# '실제값' : test_set.iloc[:,[3]]
# '예측값' : pred
# 순서를 바꾸어서 적으면 안된다.
# 결과 : 0.9383321928068769
# 이 때 결과는 결정계수고 결정계수는 상관계수의 제곱이다.
# 즉 현재 이 모델은 독립변수에 의한 종속변수의 값을 잘 설명하고 있다.

# 시각화
plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]], color = 'red')
plt.plot(np.array(test_set.iloc[:, [2]]), model_linear.predict(test_set.iloc[:, [2]]))
plt.show()

print('\nRidge -----------')
# 회귀분석 방법1 - Ridge: alpha값을 조정(가중치 제곱합을 최소화)하여 과대/과소적합을 피한다. 다중공선성 문제 처리에 효과적.
from sklearn.linear_model import Ridge
model_ridge = Ridge(alpha=10).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_ridge.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]]))  # 0.91880
print(model_ridge.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))    # 0.94101
pred_ridge = model_ridge.predict(test_set.iloc[:, [2]])
print('ridge predict : ', pred_ridge[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_ridge)))  # 0.9410

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='blue')
plt.plot(np.array(test_set.iloc[:, [2]]), model_ridge.predict(test_set.iloc[:, [2]]))
plt.show()

print('\nLasso -----------')
# 회귀분석 방법2 - Lasso: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
from sklearn.linear_model import Lasso
model_lasso = Lasso(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_lasso.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
print(model_lasso.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
pred_lasso = model_lasso.predict(test_set.iloc[:, [2]])
print('lasso predict : ', pred_lasso[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_lasso)))

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='green')
plt.plot(np.array(test_set.iloc[:, [2]]), model_lasso.predict(test_set.iloc[:, [2]]))
plt.show()

# 회귀분석 방법3 - Elastic Net 회귀모형 : Ridge + Lasso의 형태로 가중치 절대값의 합(L1)과 제곱합(L2)을 동시에 제약 조건으로 가지는 모형
print('\nElasticNet -----------')
# 회귀분석 방법 - ElasticNet: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
from sklearn.linear_model import ElasticNet
model_elastic = ElasticNet(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_elastic.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
print(model_elastic.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
pred_elastic = model_elastic.predict(test_set.iloc[:, [2]])
print('ElasticNet predict : ', pred_elastic[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_elastic)))

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='cyan')
plt.plot(np.array(test_set.iloc[:, [2]]), model_elastic.predict(test_set.iloc[:, [2]]))
plt.show()