# ex9linear_mtcar.py와 다르게 이번에는 LinearRegression을 사용한다.
# 마찬가지로 mtcars dataset으로 모델 생성 후 모델 평가 점수 출력

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression    # summary() 지원안함. 'ols' vs 'LinearRegression'
import statsmodels.api
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error

mtcars = statsmodels.api.datasets.get_rdataset('mtcars').data
print(mtcars.head(3))
print('상관계수 : \n', mtcars.corr(method='pearson'))
print()

# hp(마력)가 mpg(연비)에 영향을 주는 인과관계가 있다고 가정하고 모델을 생성
x = mtcars[['hp']].values
print(x[:5])
# 결과 : [[110]
#         [110]
#         [ 93]
#         [110]
#         [175]]
# 입력은 2차원이고..

y = mtcars['mpg'].values
print(y[:5])
# 결과 : [21.  21.  22.8 21.4 18.7]
# 출력은 1차원이다!!

# 선형회귀 시작!
lmodel = LinearRegression().fit(X=x, y=y)
print('slope : ', lmodel.coef_)
print('intercdpt : ', lmodel.intercept_)

plt.scatter(x,y)
plt.plot(x, lmodel.coef_ * x + lmodel.intercept_, c='r')
plt.show()

# mpg 예측
pred = lmodel.predict(x)
print("예측값 : ", np.round(pred[:5], 1))
print("실제값 : ", y[:5])
# 결과 : 
# 예측값 :  [22.6 22.6 23.8 22.6 18.2]
# 실제값 :  [21.  21.  22.8 21.4 18.7]

# 모델 성능은 알 수 없다. summary()표가 없기 때문!!
# 그래서 모델 성능 지표를 만들어주어야 한다.
# MSE(평균제곱오차) : 모델 내부 비교, 계산이 편리. 하지만 단위가 제곱된 값이다.
# RMSE(route mse) : MSE를 제곱근한 값으로 제곱이 풀린다. = 원래 단위값을 사용한다.

print("MSE : ", mean_squared_error(y, pred))
print("RMSE : ", np.sqrt(mean_squared_error(y, pred)))
print('r2_score(결정계수, 설명력) : ', r2_score(y, pred))
# r2_score(y, pred) : 실제값과 예측값
# 결과 : r2_score(결정계수, 설명력) :  0.602437341423934
# = 모델 설명력이 60.2%이다.
# 모델 설명 시 r2_score 하나만 보고 모델을 판단해서는 안된다. 왜냐하면 이상치에 민감하고 변수가 많으면 설명력이 좋아지기 때문이다.
# 모델 평가는 r2_score이고, RMSE 등과 함께 적어준다.

# 모델 저장 및 읽기는 이전 실습과 동일
print('새로운 hp로 mpg 예측')
new_hp = [[100], [110], [120]]
new_pred = lmodel.predict(new_hp)
print('예측 결과 : ', np.round(new_pred.ravel(),2)) 
# print('예측 결과 : ', np.round(new_pred.flatten(),2)) # 위와 동일
# 결과 : 예측 결과 :  [23.28 22.59 21.91]

# linearRegresion과 ols의 차이
# 둘 다 기본적으로 최소제곱법(OLS)으로 선형회귀모델을 학습
