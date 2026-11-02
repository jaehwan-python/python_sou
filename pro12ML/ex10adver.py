# **선형회귀모델의 선행조건**
# 1. 선형성 : 독립변수와 종속변수의 관계가 선형이어야 한다. = x,y의 평균적인 관계가 직선형태이어야 한다.
# 2. 독립성 : 독립변수 간에 상관관계가 없어야 한다. = 독립변수는 서로 독립적이어야 한다.
#             ex) 여성변수가 자매관계라면 유전적인 연관성이 높아 좋지 않다. 
#             ex) 남성변수가 형제관계라면 유전적인 연관성이 높아 좋지 않다. 
# 3. 등분산성 : 독립변수의 값에 따라 종속변수의 분산이 일정해야 한다. 
# 4. 정규성 : 잔차가 정규분포를 따라야 한다. 
# 5. 다중공선성 : 다중회귀 분석 시 두 개 이상의 독립변수 간에 강한 상관관계가 있어서는 안된다.
#                ex) 나이와 학년에 대한 신체 구조에 미치는 영향력에 대한 회귀분석을 할 때, 나이와 학년은 강한 상관관계가 있으므로 
#                    다중공선성이 발생한다. = 교집하비 너무 크므로 좋지 않다.

# ------------------------------------------------------------------------------------------

# 단순선형회귀모델의 절절성 - ols 사용
# 선형성, 정규성, 등분산성을 기본적으로 확인한다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api

advdf = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/Advertising.csv", usecols = [1, 2, 3, 4])
print(advdf.head(3), type(advdf), advdf.shape)
print(advdf.info())
print(advdf.corr())
# 결과 : 
#                       tv      radio      newspaper    sales
#        tv         1.000000   0.054809    0.056648    0.782224
#        radio      0.054809   1.000000    0.354104    0.576223
#        newspaper  0.056648   0.354104    1.000000    0.228299
#        sales      0.782224   0.576223    0.228299    1.000000

# 독립변수  :  tv
# 종속변수  :  sales
lm = smf.ols(formula = 'sales ~ tv', data=advdf).fit()
print(f'coeffient : {lm.params}, p-value : {lm.pvalues}, R-squared : {lm.rsquared}')
# coffienent : Intercept(절편)    7.032594
#              tv(기울기)         0.047537

# p-value : Intercept(절편)    1.088435e-60
#           tv(기울기)           1.467389e-42

# R-squared : 0.6124371051955132
# 상관계수(r)을 거듭제곱하면 r-squared가 된다. = 독립변수가 종속변수의 변동성을 61.2% 설명한다는 뜻

print(lm.summary())
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  sales   R-squared:                       0.612
# Model:                            OLS   Adj. R-squared:                  0.610
# Method:                 Least Squares   F-statistic:                     312.1
# Date:                Mon, 02 Nov 2026   Prob (F-statistic):           1.47e-42
# Time:                        11:39:07   Log-Likelihood:                -519.05
# No. Observations:                 200   AIC:                             1042.
# Df Residuals:                     198   BIC:                             1049.
# Df Model:                           1                                         
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      7.0326      0.458     15.360      0.000       6.130       7.935
# tv             0.0475      0.003     17.668      0.000       0.042       0.053
# ==============================================================================
# Omnibus:                        0.531   Durbin-Watson:                   1.935
# Prob(Omnibus):                  0.767   Jarque-Bera (JB):                0.669
# Skew:                          -0.089   Prob(JB):                        0.716
# Kurtosis:                       2.779   Cond. No.                         338.
# ==============================================================================

print(lm.summary().tables[1])
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      7.0326      0.458     15.360      0.000       6.130       7.935
# tv             0.0475      0.003     17.668      0.000       0.042       0.053
# ==============================================================================
# 1번째 테이블 : 회귀계수, 표준오차, t값, p값, 신뢰구간
print()

# 예측
x_new = pd.DataFrame({'tv': [10, 20, 30]})
print(x_new.values) # 예측에 참여한 x값
print('실제값 : ', advdf.sales[:3].values)
print('예측값 : ', lm.predict(x_new).values.round(1))
print('예측 결과:')
print(lm.predict(x_new))

# 경험하지 않은 tv광고비(x값)에 따른 상품 판매량 예측하기
my_new = pd.DataFrame({'tv': [50, 100, 150]})
print('예측 상품 판매량 : ', lm.predict(my_new).values)

# 시각화
plt.scatter(advdf.tv, advdf.sales)
plt.xlabel('TV광고비')
plt.ylabel('상품 판매량')   

plt.plot(advdf.tv, lm.predict(advdf), color='red', linewidth=3) 
# 회귀선

plt.show()
# ------------------------------------------------------------

print("\n 모델의 적절성 선행 조건 확인 : 1정규성, 2선형성, 3등분산성")
# 잔차(Residuals) : 실제 관측값과 모델이 예측한 값의 차이를 의미
#                 : 모델이 데이터를 얼마나 잘설명하는지를 보여주는 척도
#                  = 실제값 - 예측값
fitted = lm.predict(advdf.tv)
residual = advdf['sales'] - fitted
print("실제값 : ", advdf['sales'][:5].values)
print("예측값 : ", fitted[:5].values)
print("잔차값 : ", residual[:5].values)
print("잔차의 평균값 : ", np.mean(residual))

# 잔차에 대한 정규성, 선형성, 등분산성을 확인을 하면 모델의 적절성을 알 수 있다.
# 잔차를 보는 목적은 “이게 회귀모델인가?”를 확인하는 게 아니라, “만든 회귀모델이 데이터의 관계를 잘 설명하고 있는가?”를 확인하는 것

# 모델이 중요한 관계를 잘 설명했다면, 남은 잔차에는 일정한 규칙이 없어야 한다. 왜냐하면
# 이러한 잔차들의 패턴이 계속된다면 그 규칙을 이용해서 예측을 더 개선할 수 있다는 뜻이기 때문이다.
# 관계를 충분히 설명했다면, 같은 광고비에서 어떤 관측값은 예측보다 높고 
# 어떤 값은 낮더라도 평균적으로 어느 쪽으로 틀릴지 예상하기 어려워야한다.
# = 규칙이 없다”는 표현은 특히 잔차의 평균에 체계적인 패턴이 없어야 한다는 뜻

# 정규성  :  잔차의 분포 모양이 '정규분포'에 가까운가?	
#           ->  Q-Q plot, Shapiro 검정
# 선형성  :  예측값에 따라 잔차의 평균적 흐름에 '곡선 패턴'이 남는가?	
#           ->  잔차–예측값 그림, RESET 검정
# 등분산성  :  예측값에 따라 잔차의 '퍼지는 폭'이 일정한가?	
#           -> 잔차–예측값 그림, Breusch–Pagan 검정



# [1. 정규성 검정]
print("\n 1. 잔차의 정규성 : 잔차가 정규성을 따르는지 확인")
# 정규성 : 잔차가 정규분포를 따라야 한다. 
from scipy.stats import shapiro
import statsmodels.api as sm

# shapiro방법을 이용!!
stat, pv = shapiro(residual)
# 귀무가설: 데이터가 정규분포를 따른다.
print(f"통계량 : {stat}, p값: {pv}")
# 결과 : 
# 통계량 : 0.99053
# p값 : 0.21322
print('정규성 만족' if pv >= 0.05 else '정규성 불만족')

# Q-Q plot으로 시각화
sm.qqplot(residual, line = 's')
plt.title('Q-Q plot으로 정규성 확인')
plt.show()
# x축: 정규분포라면 나올 것으로 기대하는 분위수
# y축: 실제 잔차를 작은 값부터 정렬한 분위수
# 각 점 : 데이터들과 회귀선에 대한 잔차의 값
# 빨간 선: 정규분포와 비교하기 위한 기준선
# 파란 점들이 빨간 선에 가까울수록 잔차의 분포가 정규분포에 가깝다고 해석



# [2. 선형성 검정]
print("\n 2. 선형성 검정 : 독립변수의 변화에 종속변수도 변화하나 특정한 패턴이 있으면 안된다.")
# 선형성 : 독립변수와 종속변수의 관계가 선형이어야 한다. = x,y의 평균적인 관계가 직선형태이어야 한다.
from statsmodels.stats.diagnostic import linear_reset
reset_result = linear_reset(lm, power=2, use_f=True)
# power=2 : 독립변수를 2개 사용한다(X)
#         : 제곱항을 사용하겠다(O)
# f검정통계량을 사용할 것이다.
print('reset_result 결과 : ', reset_result.pvalue)
# 결과 : 0.05573658710952813
print('선형성 만족' if reset_result.pvalue >= 0.05 else '선형성 불만족')

# 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color':'red'})
plt.plot([fitted.min(), fitted.max()], [0,0], '--', color='yellow')
plt.show()
# 선형성 확인을 위해서 직선이 그어져야하는데 지금은 약간 삐뚤어져도 거의 직선이기에 선형성을 만족한다고 할 수 있다.
# 게다가 reset_result의 p값또한 0.05보다 크기에 선형성 만족이라고 할 수 있다.
# x축: 모델이 예측한 판매량
# y축: 잔차(= 실제 판매량 − 예측 판매량)
# 빨간 선: 잔차의 평균적인 흐름을 보여주는 LOWESS 추세선
# 노란 점선: 잔차가 0인 기준선



# [3. 등분산성 검정]
print("\n 3. 등분산성 검정 : 독립변수의 값에 관계없이 오차항의 분산이 일정한지 확인.")
# 회귀모델의 예측값이 달라져도 예측값 사이의 오차가 비슷한 정도로 흩어지는지 확인
# 등분산성 : 독립변수의 값에 따라 종속변수의 분산이 일정해야 한다. 
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residual, sm.add_constant(advdf['tv']))
bp_stat, bp_pvalue = bp_test[0], bp_test[1]
print(f"breuschpagan test 결과 : 통계량:{bp_stat}, pvalue:{bp_pvalue}")
# 통계량  :  48.037965662293594
# pvalue  :  4.180455907755742e-12
print("등분산성 만족" if bp_pvalue >= 0.05 else "등분산성 위배")
# 결과 : 등분산성 위배

# 시각화
sns.scatterplot(x=advdf['tv'], y=residual)
plt.axhline(y=0, color='red', linestyle='--')
# 잔차가 '0'인 기준선
plt.xlabel('tv광고비')
plt.ylabel('잔차')
plt.grid(alpha=0.3)
plt.show()
# x축: TV 광고비
# y축: 잔차 = 실제 판매량 − 예측 판매량
# 빨간 점선 : 잔차 0 기준선
# 광고비가 적을 때는 잔차가 비교적 좁게 모이고, 광고비가 커질수록 위아래로 넓게 퍼지는 모습이에요. 
# 따라서 등분산성을 위반하는 이분산성이 의심됩니다.
# 등분산성을 만족하려면, 광고비가 작든 크든 잔차가 퍼지는 세로 폭이 대체로 비슷해야 해요. 
# 단순히 점들이 0 위아래에 있다는 것만으로는 충분하지 않습니다.


# 이 3가지를 통해서 회귀분석의 기본 가정을 만족하는지 알 수 있다.
# 이때 정규성, 선형성, 등분산성을 만족하지 못할 경우, 
# 다음카페 - Python Analysis - 회귀분석과 관련된 정보 이해 참고
print()

# --------------------------------------------------------------------------------------------------


# 참고 : 쿡 거리(Cook's distance) : 특정 데이터가 회귀모델에 얼마나 영향을 주는지 확인
# [영향력 있는 관측치(이상치)를 탐지하는 진단 방법]
# 데이터가 적을 때, 
# 이상치가 의심스러울때, 
# 모델결과가 이상하게 나올 때, 확인한다.

from statsmodels.stats.outliers_influence import OLSInfluence
cd, _ = OLSInfluence(lm).cooks_distance
# 쿡거리, 인덱스 반환

# 쿡 거리가 가장 큰 5개 확인
print(cd.sort_values(ascending=False).head())
# 결과 : 
#    35     0.060494
#    178    0.056347
#    25     0.038873
#    175    0.037181
#    131    0.033895
print()

print(advdf.head())
print()

# 쿡 거리가 가장 큰 (이상치) 관측치 원본확인
print(advdf.iloc[[35, 178, 25, 175, 131]])
# 결과 : 
#            tv   radio   newspaper   sales
#    35   290.7     4.1         8.5    12.8
#    178  276.7     2.3        23.7    11.8
#    25   262.9     3.5        19.5    12.0
#    175  276.9    48.9        41.8    27.0
#    131  265.2     2.9        43.0    12.7
# 대부분의 tv광고비는 매우 높은데 반해,
# sales비용은 낮다. = model이 예측하기가 어렵다.

# 시각화
fig = sm.graphics.influence_plot(lm, alpha=0.05, criterion='cooks')
plt.show()
# 원의 크기가 크면 클수록 이상치일 확률이 높다.
# 그래서 원이 가장 큰 몇개의 녀석들은 빼고 간다.

# 단순선형회귀모델에서 반드시 거쳐야 할 3가지 기본 조건
# 선형성 / 정규성 / 등분산성
# 독립성과 다중공선성은 변수가 2개 이상 있어야만 한다.

