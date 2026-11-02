# Sales 변수에 영향을 주는 변수들을 선택하여 선형회귀분석을 실시한다.
# 변수 선택은 모델.summary() 함수를 활용하여 타당한 변수만 임의적으로 선택한다.
# 회귀분석모형의 적절성을 위한 조건도 체크하시오.
# 완성된 모델로 Sales를 예측.

# 다중 선형 모델의 적절성 선행 조건 실습 -ols사용
# 선형성, 정규성, 등분산성, 독립성, 다중공선성 검정을 기본적으로 사용한다. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

import statsmodels.formula.api as smf
import statsmodels.api

# 1. 정규성, 독립성 검정을 위한 lib
from scipy.stats import shapiro 
import statsmodels.api as sm

# 2. 선형성 검정을 위한 lib
from statsmodels.stats.diagnostic import linear_reset

# 3. 등분산성 검정을 위한 lib
from statsmodels.stats.diagnostic import het_breuschpagan

# 4. 다중공선성 검정을 위한 lib
from statsmodels.stats.outliers_influence import variance_inflation_factor 


df = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/Carseats.csv")
print(df.head(3), df.shape)
print(df.info())
df = df.drop([df.columns[6], df.columns[9], df.columns[10]], axis = 1)
print(df.corr())
#                 Sales  CompPrice    Income  Advertising  Population     Price       Age  Education
# Sales        1.000000   0.064079  0.151951     0.269507    0.050471 -0.444951 -0.231815  -0.051955
# CompPrice    0.064079   1.000000 -0.080653    -0.024199   -0.094707  0.584848 -0.100239   0.025197
# Income       0.151951  -0.080653  1.000000     0.058995   -0.007877 -0.056698 -0.004670  -0.056855
# Advertising  0.269507  -0.024199  0.058995     1.000000    0.265652  0.044537 -0.004557  -0.033594
# Population   0.050471  -0.094707 -0.007877     0.265652    1.000000 -0.012144 -0.042663  -0.106378
# Price       -0.444951   0.584848 -0.056698     0.044537   -0.012144  1.000000 -0.102177   0.011747
# Age         -0.231815  -0.100239 -0.004670    -0.004557   -0.042663 -0.102177  1.000000   0.006488
# Education   -0.051955   0.025197 -0.056855    -0.033594   -0.106378  0.011747  0.006488   1.000000
# 숫자형 변수들 사이의 상관계수를 계산해서 출력함.
# ->  1에 가까움   :  한 변수가 커질수록 다른 변수도 커지는 경향
# ->  −1에 가까움  :  한 변수가 커질수록 다른 변수는 작아지는 경향
# ->  0에 가까움   :  직선적인 관계가 약함

lm = smf.ols(formula = 'Sales ~ Income+Advertising+Price+Age', data = df).fit()
print(lm.summary())
# 결과 : 
#                              OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Sales   R-squared:                       0.371
# Model:                            OLS   Adj. R-squared:                  0.364
# Method:                 Least Squares   F-statistic:                     58.21
# Date:                Mon, 02 Nov 2026   Prob (F-statistic):           1.33e-38
# Time:                        14:52:29   Log-Likelihood:                -889.67
# No. Observations:                 400   AIC:                             1789.
# Df Residuals:                     395   BIC:                             1809.
# Df Model:                           4                                         
# Covariance Type:            nonrobust                                         
# ===============================================================================
#                   coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------
# Intercept      15.1829      0.777     19.542      0.000      13.656      16.710
# Income          0.0108      0.004      2.664      0.008       0.003       0.019
# Advertising     0.1203      0.017      7.078      0.000       0.087       0.154
# Price          -0.0573      0.005    -11.932      0.000      -0.067      -0.048
# Age            -0.0486      0.007     -6.956      0.000      -0.062      -0.035
# ==============================================================================
# Omnibus:                        3.285   Durbin-Watson:                   1.931
# Prob(Omnibus):                  0.194   Jarque-Bera (JB):                3.336
# Skew:                           0.218   Prob(JB):                        0.189
# Kurtosis:                       2.903   Cond. No.                     1.01e+03
# ==============================================================================

# p값(P>|t|)이 값이 모두 '0.05'보다 작기 때문에 Income부터 Age까지 사용되는 변수들 모두 sales에 영향을 미친다고 말할 수 있다.
# 4개의 독립변수의 p값이 모두 0.05보다 작다
# = 유의한 변수들이다.

# 현재 Skew(왜도)가 0.218이다.
# 왜도는 
#    '0' : 좌우 대칭
# '양수' : 오른쪽으로 꼬리가 길다.
# '음수' : 왼쪽으로 꼬리가 길다. 
# 0.218이면 대체로 대칭적이라고 할 수 있다. 

# 현재 Kurtosis(첨도)가 2.903이다.
# 첨도는
# '3이상' : 정규분포보다 극단값이 나타나는 성향이 크다
#     '3' : 정규분포의 첨도와 동일
# '3이하' : 정규분포보다 극단값이 나타나는 성향이 작음
# = 3에 가까울수록 정규분포와 닮아서 더 좋아진다.

# Prob (F-statistic):           1.33e-38
# f검정의 p값 : “독립변수들을 사용한 모델이, Sales의 평균값만으로 예측하는 모델보다 설명력이 있는가?”**를 확인
# 귀무가설: 절편을 제외한 모든 회귀계수가 0이다.
# 대립가설: 적어도 하나의 회귀계수는 0이 아니다.
# 1.33e-38 = 1.33 × 10⁻³⁸

print(f"수정된 결정계수는 {lm.rsquared_adj:.4f}이므로 양호하다.")

print('\n 선형회귀 모델의 적절성 조건 체크 후 모델 사용')
print(df.columns)
# Index(['Sales', 'CompPrice', 
#       'Income', 
#       'Advertising', 'Population', 
#       'Price', 
#       'Age', 'Education'],dtype='str')
# Sales, Income, Advertising, Price, Age는 0, 2, 3, 5, 6번째 '열'이다.
print()
# -------------------------------------------------------------------------------------------------------------------------------------
# 조건을 확인해보자.

# 잔차항 구하기
df_lm = df.iloc[:, [0, 2, 3, 5, 6]]
# 해당 순서에 해당하는 열들을 가져옴.

print(df_lm.head(2))
fitted = lm.predict(df_lm)
# 학습을 통해 예측값을 얻었음

residual = df_lm["Sales"] - fitted
# 잔차를 얻었음
# 종속변수 Salse에 대해서 독립변수 Income, Advertising, Price, Age값이 대입된다.
# "잔차 = 실제값 - 예측값"이므로
# df_lm["Sales"]는 실제값이고
# fitted는 예측값이다.

# lm = smf.ols(formula = 'Sales ~ Income+Advertising+Price+Age', data = df).fit() 위에서 lm을 이것으로 정의함.
# predict(df_lm)을 호출하면 다음처럼 처리한다..
# Income, Advertising, Price, Age → 예측에 사용
# Sales                           → 예측에 사용하지 않음
# Sales가 첫 번째 열이어서 제외되는 게 아니라, 예측 대상인 종속변수이기 때문에 
# 사용하지 않는 거예요. Sales 열의 위치를 바꿔도 동일합니다

print('잔차(Residual)는 : ', residual)
print('잔차 평균 : ', np.mean(residual))
# -------------------------------------------------------------------------------------------------------------------------------------

# [1. 정규성 확인]
# from scipy.stats import shapiro 
# import statsmodels.api as sm
stat, pv = shapiro(residual)
print(f"통계량 : {stat:.5f}, p값 : {pv:.5f}")
print(f'정규성 만족' if pv >= 0.05 else '정규성 위배')

# 시각화 : Q-Q plot
sm.qqplot(residual, line='s')
plt.title('1. 정규성 확인 : Q-Q plot')
plt.show()



# [2. 선형성 확인]
# from statsmodels.stats.diagnostic import linear_reset
reset_result = linear_reset(lm, power=2, use_f = True)
print(f"reset_result : {reset_result.pvalue:.5f}")
print('선형성 만족' if reset_result.pvalue >= 0.05 else ' 선형성 위배')

# 시각화 : regplot
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color' : 'red'})
plt.plot([fitted.min(), fitted.max()], [0, 0], '--', color='grey')
plt.xlabel('예측 판매량(Sales)')
plt.ylabel('잔차(실제값 - 예측값)')
plt.title('2. 선형성 확인 : 예측값과 잔차')
plt.show()



# [3. 등분산성 확인]
# from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residual, sm.add_constant(df_lm["Sales"]))
bp_stat, bp_pvalue = bp_test[0], bp_test[1]
print(f"p-value : {bp_pvalue}")
print("등분산성 만족" if bp_pvalue >= 0.05 else "등분산성 위배!!")
# 결과 :
# p-value : 0.016415470734788235
# 등분산성 위배!!

# 시각화 : 예측값에 따른 잔차의 퍼짐 확인
plt.figure(figsize=(8, 6))
sns.scatterplot(x=fitted, y=residual)
plt.axhline(0, color='red', linestyle='--', label='잔차 0 기준선')
plt.xlabel('예측 판매량(Sales)')
plt.ylabel('잔차(실제값 - 예측값)')
plt.title('3. 등분산성 확인 : 예측값과 잔차')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
# 예측값과 관계없이 잔차의 세로 퍼짐이 비슷하면 등분산성에 부합한다.
# 깔때기처럼 퍼짐이 넓어지거나 좁아지면 이분산성을 의심한다.



# [4. 독립성 확인] 
# 독립성 검정 : 독립변수들 간에 값이 서로 관련되지 않아야 한다.(종속변수 연관X)
# 잔차가 자기상관(인접 관측치의 오차가 관련됨)이 있는지 확인한다.
# Durbin-Watson : 잔차의 자기상관(autocorrelation) 검증 지표
# model.summary()로 확인이 가능하다.
# 값의 범위는 "0 ~ 4"이고 '2'이면 정상이다.
# 2 > 값 : 음의 자기상관을 가짐
# 2 = 값 : 정상
# 2 < 값 : 양의 자기상관을 가짐
# 해석 : "독립변수인 Income + Advertising + Price + Age 간에 서로 관련이 없다.""
import statsmodels.api as sm
print('Durbin-Watson : ', sm.stats.stattools.durbin_watson(residual))
# 결과 :
# Durbin-Watson :  1.9314981270829592
# model.summary() 전체 표에서 Durbin-Watson을 찾아도 되지만
# 이렇게 저 한 줄 코드로(194번 줄) 곧바로 찾을 수 있다.

# 시각화 : plot
plt.plot(np.arange(len(residual)), residual, marker='o', linestyle='-')
plt.axhline(0, color='red', linestyle = '--')
plt.xlabel('관측순서')
plt.ylabel('잔차')
plt.title('4. 독립성 확인 : 잔차 순서 그래프')
plt.grid(alpha = 0.3)
plt.show()
# 잔차가 0을 중심으로 불규칙하게 음직이므로 독립성에 부합한다.



# [5. 다중공선성 확인]
# 다중공선성 검정 : 독립변수들 간에 강한 상관관계가 있어서는 안된다.
# VIF(variance_inflation_factor, 분산 인플레이션 요인, 분산 팽창 지수)

from statsmodels.stats.outliers_influence import variance_inflation_factor 
df_ind = df[['Income', 'Advertising', 'Price', 'Age']] # 독립변수

vifdf = pd.DataFrame()
vifdf['변수'] = df_ind.columns
vifdf['vif_value'] = [variance_inflation_factor(df_ind.values, i) \
                        for i in range(df_ind.shape[1])]
# vifdf라는 df에 변수, vif_value라는 컬럼을 추가해주었다.

print(vifdf)
# 10을 초과하지 않으면 다중공선성에 문제가 없다. = 독립변수간의 상관관계가 없다.
# 결과 :
#               변수     vif_value
#    0        Income     5.971040
#    1   Advertising     1.993726
#    2         Price     9.979281
#    3           Age     8.267760

# 시각화
sns.barplot(x='변수', y='vif_value', data=vifdf)
plt.axhline(10, color='red', linestyle = '--')
plt.title('5. 다중공선성 검정')
plt.ylabel('vif')
plt.show()
# Price 독립변수는 다른 독립변수들과 애매하게 영향을 미치지 않는다...약간 의심해보자...
print()
# -------------------------------------------------------------------------------------------------------------------------------------



# 유의한 모델이므로 완성된 모델 저장 후 읽어 모델 재사용이 가능해야한다.

# joblib으로 모델 저장 및 불러오기
import joblib
from pathlib import Path

# 실행 위치와 관계없이 이 파이썬 파일과 같은 폴더에 저장한다.
model_path = Path(__file__).resolve().parent / 'carseats.joblib'
# carseats.joblib라는 파일명으로 저장
# C:\works\projects\pro12ML\carseats.joblib 이 경로에다가.

joblib.dump(lm, model_path) 
# 학습한 모델을 파일에 저장

mymodel = joblib.load(model_path) 
# 저장한 모델을 다시 불러오기
# 다시 학습하는 것이 아니라 이미 학습된 절편과 계수 등을 불러오는 것

print(mymodel.summary())
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Sales   R-squared:                       0.371
# Model:                            OLS   Adj. R-squared:                  0.364
# Method:                 Least Squares   F-statistic:                     58.21
# Date:                Mon, 02 Nov 2026   Prob (F-statistic):           1.33e-38
# Time:                        16:20:55   Log-Likelihood:                -889.67
# No. Observations:                 400   AIC:                             1789.
# Df Residuals:                     395   BIC:                             1809.
# Df Model:                           4                                         
# Covariance Type:            nonrobust                                         
# ===============================================================================
#                   coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------
# Intercept      15.1829      0.777     19.542      0.000      13.656      16.710
# Income          0.0108      0.004      2.664      0.008       0.003       0.019
# Advertising     0.1203      0.017      7.078      0.000       0.087       0.154
# Price          -0.0573      0.005    -11.932      0.000      -0.067      -0.048
# Age            -0.0486      0.007     -6.956      0.000      -0.062      -0.035
# ==============================================================================
# Omnibus:                        3.285   Durbin-Watson:                   1.931
# Prob(Omnibus):                  0.194   Jarque-Bera (JB):                3.336
# Skew:                           0.218   Prob(JB):                        0.189
# Kurtosis:                       2.903   Cond. No.                     1.01e+03
# ==============================================================================


# 결과 검증
print("새로운 값으로 예측")
new_df = pd.DataFrame({'Income':[35, 62], 'Advertising':[6, 3], 'Price':[105, 88], 'Age':[32, 55]})
# 새로운 데이터로 준비
# 첫 번째 사례의 네 변수 → 첫 번째 Sales 예측
# 두 번째 사례의 네 변수 → 두 번째 Sales 예측

new_pred = mymodel.predict(new_df)
# 학습된 모델에 입력값을 넣어 예측값을 계산
print('Sales 예측 결과 : ', new_pred.values)
# 결과 : [8.71289759 8.49715914]