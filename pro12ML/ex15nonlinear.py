# 지금까지 우리는 '선형회귀분석'에 대해서 학습하였고 그 때 보이는 3가지 모델로 LinearRegression, ols, Lingress가 있었다.
# 이제부터는 '비선형회귀분석'에 대해서 학습할 것이다.

# 비선형회귀분석(Non-linear Regression)
# : 직선의 회귀선을 곡선으로 바꾸어 더 정확하게 데이터 변화를 예측할 수 있다.
# 선형이라는 가정이 어긋날 때(데이터 값이 비정규성을 따를 때), 대처할 수 있는 방법으로 다항식 항을 추가하여 다항회귀모델을 작성한다.

# 선형모델을 비선형모델로 바꾼 것이다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score # 결정계수로 설명력 확보
from sklearn.model_selection import train_test_split # 과적합 문제 해결
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

x = np.array([1, 2, 3, 4, 5])
y = np.array([4, 2, 1, 3, 7])

print(np.corrcoef(x,y)[0,1])
# 상관계수의 결과 값이 행렬형태로 나타나기 때문에 그 중 0번 행, 1번 열의 값인 0.85만 꺼내겠다는 것이다.
# 결과 : 
#       [ [ 1.0,  0.85 ],
#         [ 0.85,  1.0 ] ]
# = 0.48076197382041164이 상관계수이다. = 1에 가깝기 때문에 x가 커질수록 y도 커진다.
# 하지만!! 비선형 관계를 공부할 때는 상관계수가 0에 가까워도 곡선 형태의 관계는 있을 수 있다는 점을 기억
plt.scatter(x,y)
plt.show()

# 선형회귀 모델을 사용
# 1차원을 2차원으로 올린다. 왜? -> sklearn은 2차원이 되어야 사용 가능하기 때문이다.
from sklearn.linear_model import LinearRegression
x = x[:, np.newaxis] # = 차원 확대. 1차원 -> 2차원
print(x)
# 결과 :

model = LinearRegression().fit(x,y)
y_pred = model.predict(x)
print('예측값 y : ', y_pred) 
# 추세선이 나타내고 있는 해당 x값에서의 예측값y ... 하지만 각 값의 차이가 너무 많이 난다 ㅠㅠ
print('결정계수 : ', r2_score(y, y_pred))
# 결정계수는 실제값과 예측값을 같이 적어준다!! 순서 중요!!

plt.scatter(x, y)
plt.plot(x, y_pred, c='red')
plt.show()
# 각 점에 대해서 선형직선, 선형방정식으로 만든 추세선(회귀선)을 만들어서 그어보았다.
# = 편차가 ㅈㄴ 큼

# 그래서 우리는 비선형을 사용한다.
# 결정계수가 23%로 나와도 비선형 데이터를 보고 있기에 데이터를 바꾸어야 한다.

# 비선형 모델 작성
# [방법1] : PolynomialFeatures 
from sklearn.preprocessing import PolynomialFeatures
# 다항식 특징(여러개의 변수)을 추가 가능 

poly = PolynomialFeatures(degree=2, include_bias=False)
# degree = 제곱한 값이 열의 갯수만큼 붙는다.
# include_bias = False : "상수값은 등장하지마라"

x2 = poly.fit_transform(x) # poly로 쓰기 위한 원본 데이터를 수정
print(x)
# 결과 :
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]]
# (5, 1)

print(x2)
# 결과 :
# [[ 1.  1.]
#  [ 2.  4.]
#  [ 3.  9.]
#  [ 4. 16.]
#  [ 5. 25.]]
# (5, 2)
# 옆에 제곱한 값이 생겼다.

# degree = 3일 때, x2값
# [[  1.   1.   1.]
#  [  2.   4.   8.]
#  [  3.   9.  27.]
#  [  4.  16.  64.]
#  [  5.  25. 125.]]
# (5, 3)
# 옆에 세제곱한 값이 생겼다.

model2 = LinearRegression().fit(x2, y)
# 추가된 특징(변수) 행렬값으로 모델을 생성한다.

y_pred2 = model2.predict(x2)

print('예측값 y : ', y_pred2) 
# 이번에는 y_pred가 아니라 y_pred2에 대한 예측값을 구한다.
# 결과 : [4.14285714 1.62857143 1.25714286 3.02857143 6.94285714]
print('결정계수 : ', r2_score(y, y_pred2))
# 그때 결정계수를 구해보면 0.9892183288409704이 나온다. = 굉장히 높다. 

# 이를 그림으로 확인해보자.
plt.scatter(x, y)
plt.plot(x, y_pred2, c='red')
plt.show()
# WOW ~ 이제 얼추 데이터들과 비슷한 추세로 곡선이 생겼다.
# 이때 결정계수 값은 degree값으로 정한다. 그러면 성능이 좋아진다. = 설명력이 좋아진다.

# 회귀모델 - 선형 - 단순선형회귀모델 
#                - 다중 선형회귀모델
#         - 비선형 - 다항 비선형회귀모델
# -------------------------------------------------------------------------------------------------------------

# 실습) Boston Dataset













# [방법2] : log변환 


# [방법3] : curve_fit