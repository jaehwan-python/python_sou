# 단순선형회귀 : ols를 이용한 결과 이해
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression # 첫번째 방법(LinearRegression)
import statsmodels.formula.api as smf             # 두번째 방법(ols)
from scipy import stats                           # 세번째 방법(Linegress)


# 음료 : 친밀도, 적절성, 만족도 데이터 이용
df = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/drinking_water.csv")
print(df.head(3))
print(df.corr()) # 상관계수 : 공분산(cov)을 표준화한것
# 결과 : 
#               친밀도       적절성       만족도
#    친밀도    1.000000     0.499209     0.467145
#    적절성    0.499209     1.000000    "0.766853"
#    만족도    0.467145     0.766853     1.000000

# 음료 적절성과 만족도는 양의 상관관계가 매우 강하다.
# 음료 적절성이 만족도에 영향을 준다 = 적절성과 만족도는 변수간의 원인과 결과의 관계(인과관계)가 있는지 파악해야한다

# 귀무가설 : 적절성과 만족도는 인과관계가 없다
# 대립가설 : 적절성과 만족도는 인과관계가 있다.
# 원래 회귀분석은 귀무가설과 대립가설을 세우지 않지만 인과관계에 대해서 가설을 세워볼 수 있다.

model = smf.ols(formula = '만족도 ~ 적절성', data=df).fit()
print(model.summary())
# 결과 :
#                               OLS Regression Results                            
# ==================================================================================
# Dep. Variable:                 만족도       R-squared:                       0.588
# Model:                            OLS       Adj. R-squared:                  0.586
# Method:                 Least Squares       F-statistic:                     374.0
# Date:                Fri, 30 Oct 2026       Prob (F-statistic):           2.24e-52
# Time:                        12:51:33       Log-Likelihood:                -207.44
# No. Observations:                 264       AIC:                             418.9
# Df Residuals:                     262       BIC:                             426.0
# Df Model:                           1                                         
# Covariance Type:            nonrobust                                         
# ==================================================================================
#                  coef     std err        t       P>|t|      [0.025      0.975]
# ----------------------------------------------------------------------------------
# Intercept      0.7789      0.124      6.273      0.000       0.534       1.023
# 적절성         0.7393      0.038     19.340      0.000       0.664       0.815
# ==================================================================================
# Omnibus:                       11.674      Durbin-Watson:                   2.185
# Prob(Omnibus):                  0.003      Jarque-Bera (JB):               16.003
# Skew:                          -0.328      Prob(JB):                     0.000335
# Kurtosis:                       4.012      Cond. No.                         13.4
# ==================================================================================

# 표에서 주요값 뽑아내기
print('parameters : ', model.params)
print('R-squared : ', model.rsquared) # : 1에 가까우면 좋지만 너무가까우면 기형모델이다.
# 결과 : 
# Intercept  :  0.778858 (bias)
# 적절성     :  0.739276 (weight)

print('p-value : ', model.pvalues)
# 결과 :
#       Intercept    1.454388e-09
#          적절성    2.235345e-52

print('예측값 : ', model.predict()[:5])
print('실제값 : ', df.만족도[:5].values)
# 결과 : 
# 예측값 :  [3.73596305 2.99668687 3.73596305 2.25741069 2.25741069]
# 실제값 :  [3          2          4          2          2         ]

plt.scatter(df.적절성, df.만족도)
slope, intercept = np.polyfit(df.적절성, df.만족도, 1)
plt.plot(df.적절성, slope * df.적절성 + intercept, c = 'b')
plt.show()
# 잔차 제곱의 합이 최소가 되는 추세선을 그었다.

print("\n 실제값과 예측값 비교")
result_df = pd.DataFrame({  '실제값' : df['만족도'], 
                            '예측값' : model.predict(), 
                            '잔차' : model.resid})
print(result_df.head(10).round(3))
# 결과 : 
#        실제값    예측값      잔차
#    0     3       3.736     -0.736
#    1     2       2.997     -0.997
#    2     4       3.736      0.264
#    3     2       2.257     -0.257
#    4     2       2.257     -0.257
#    5     3       2.997      0.003
#    6     4       3.736      0.264
#    7     2       2.257     -0.257
#    8     3       2.257      0.743
#    9     3       2.257      0.743

# 회귀모델 평가지표의 종류
# 1. 결정계수 : 독립변수가 종속변수의 분산을 얼마나 잘 설명하는지 = 설명력
# 2. 실제값과 예측값간의 예측오차(MAE, MSE, RMSE)
# 3. p-value


# Model 오차로 평가
print(f"RSS : {model.ssr:.4f}")                          # 잔차제곱합(Residual Sum of Squares) 
print(f"MSE : {np.mean(model.resid**2):.4f}")            # 평균제곱오차(Mean Squared Error) 
print(f"RMSE : {np.sqrt(np.mean(model.resid**2)):.4f}")  # 평균제곱근오차(Root Mean Squared Error) 
# RSS : 74.4092
# MSE : 0.2819
# RMSE : 0.5309
# 기준은 딱히 없지만 모든 오차는 작을수록 좋다.

# ① RSS — "잔차제곱합(Residual Sum of Squares)" :  sum((실제값 - 예측값) ** 2)
# 계산 예시  : RSS = 25 + 100 + 25 = 150 
# 설명: 실제값과 예측값의 차이를 각각 제곱한 다음 모두 더한 값.
#   - 오차를 제곱하므로 음수와 양수가 서로 상쇄되지 않습니다.
#   - 값이 작을수록 예측값이 실제값에 가깝습니다.
#   - 데이터 개수가 많아질수록 커질 수 있어, 서로 다른 크기의 데이터셋을 직접 비교하기에는 불편합니다.

# ② MSE — "평균제곱오차(Mean Squared Error)"  :  MSE=RSS / n
# 계산 예시 : MSE = 150 / 3 = 50 
# 설명: RSS를 데이터 개수로 나눈 값, 즉 잔차제곱의 평균.
#   - RSS와 달리 데이터 개수를 고려합니다.
#   - 값이 작을수록 좋습니다.
#   - 다만 오차를 제곱했기 때문에 원래 점수 단위가 아니라 점² 단위입니다.

# ③ RMSE — "평균제곱근오차(Root Mean Squared Error)"  : RMSE = sqrt(MSE) 
# 계산 예시 : RMSE = sqrt(50) = 7.07 (약) 
# 설명: MSE에 제곱근을 적용하여 오차를 원래 데이터와 같은 단위로 표현한 값입니다.
#   - 위 예제에서는 RMSE가 약 7.07점입니다.
#   - 실제 점수를 예측할 때 오차가 어느 정도 규모인지 이해하기 쉽습니다.
#   - 값이 작을수록 모델의 예측이 실제값에 가깝습니다.
# 단, RMSE가 7.07점이라고 해서 모든 예측이 정확히 7.07점씩 틀린다는 의미는 아닙니다.

# RSS는 오차를 제곱해서 전부 더한 값, MSE는 그것을 평균낸 값, RMSE는 다시 원래 단위로 바꾼 값.
# 세가지 지표 모두 작을수록 예측오차가 작지만, 실제 모델의 오차 규모를 이해하기에는 RMSE가 가장 직관적이다.
# LingerRegression과 OLS는 RSS가 최소가 되는 회귀직선을 구한다.
# 그리고 완성된 모엘이 얼마나 정확하게 예측하는지는 MSE, RMSE등의 지표로 평가한다.

# 생성된 모델로 새로운 x값에 대한 예측결과를 출력하면 된다.
# 독립변수(연속형) + 종속변수(연속형) -> "정량적분석"
new_data = pd.DataFrame({'적절성': [3.123, 4.123, 5.123]})
new_pred = model.predict(new_data)
print(pd.DataFrame({'적절성' : new_data['적절성'], '예측만족도' : new_pred}).round(3))
# 결과 : 
#             적절성    예측만족도
#        0    3.123       3.088
#        1    4.123       3.827
#        2    5.123       4.566

# 선형회귀모델 제작 시, 가장 먼저
# 상관계수를 확인해야 한다