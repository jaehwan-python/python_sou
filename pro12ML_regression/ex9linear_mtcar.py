# 선형회귀분석 ex8linear_iris.py로 연습을 했으면 이번에느 ex9linear_mtcar.py로 연습을 해보자.

# ----------------------------------------------

# [1단계] : 데이터 준비
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api

mtcars = statsmodels.api.datasets.get_rdataset('mtcars').data
print(mtcars.head(3), type(mtcars))
# mtcars 데이터셋은 자동차의 연비와 관련된 데이터셋이다. 
# 1974년 Motor Trend 잡지에서 발췌한 데이터로, 
# 32대의 자동차에 대한
# 1. 연비(mpg), 
# 2. 실린더 수(cyl), 
# 3. 배기량(disp), 
# 4. 마력(hp),  
# 5. 무게(wt) 등의 정보를 담고 있다.
# 결과 : 
#                 mpg  cyl   disp   hp  drat     wt   qsec  vs  am  gear  carb
# rownames                                                                    
# Mazda RX4      21.0    6  160.0  110  3.90  2.620  16.46   0   1     4     4
# Mazda RX4 Wag  21.0    6  160.0  110  3.90  2.875  17.02   0   1     4     4
# Datsun 710     22.8    4  108.0   93  3.85  2.320  18.61   1   1     4     1 <class 'pandas.DataFrame'>

print(mtcars.columns)
# 컬럼의 종류 : mpg, cyl, disp, hp, drat, wt, qsec, vs, am, gear, carb

print(mtcars.info())
# 데이터 셋 정보

# 변수 설정
# 독립변수(x) : 마력수(hp)
# 종속변수(y) : 연비(mpg)
print(np.corrcoef(mtcars.hp, mtcars.mpg)[0,1])
# 결과 : -0.7761683718261298 
# 해석 : 상관계수가 -0.77로 음의 상관관계가 강하다. 독립변수가 종속변수를 잘 설명하고 있다. = 회귀모델을 만들기에 적합하다.

# 시각화
plt.scatter(mtcars.hp, mtcars.mpg)
plt.xlabel('마력수(hp)')
plt.ylabel('연비(mpg)')
plt.title('마력수와 연비의 관계')
plt.show()
# 우햐항이 뚜렷하게 보인다.
# 이제부터 우리는 이 산점도 위에서 "잔차 제곱의 합이 최소"가 되는 추세선을 그리는 작업을 할 것이다. 
# = 최소제곱법(OLS)으로 회귀모델을 만들 것이다.

# [2단계] : 단순 선형회귀분석
result = smf.ols(formula = 'mpg ~ hp', data=mtcars).fit()
print(result.summary())
# smf.ols(...)   :          최소제곱법(OLS)을 사용하는 선형회귀 모델을 만든다. 실제 연비와 예측 연비의 차이를 제곱한 합이 최소가 되도록 직선을 구한다.
# formula = 'mpg ~ hp'  :   mpg가 예측할 값(종속변수), hp가 설명에 사용할 값(독립변수)이라는 뜻
# data = mtcars   :         mtcars 데이터에서 두 변수를 가져온다.
# .fit()   :                데이터로 모델을 학습하여 절편과 기울기를 구한다.
# result =   :              학습 결과를 저장한다.

# 결과 : 
#                             OLS Regression Results                            
# ========================================================================================
# Dep. Variable:                    mpg       R-squared:                       0.602 : 독립변수가 종속변수의 변동성을 60.2% 설명한다는 뜻
# Model:                            OLS       Adj. R-squared:                  0.589
# Method:                 Least Squares       F-statistic:                     45.46
# Date:                Mon, 02 Nov 2026       Prob (F-statistic):           1.79e-07
# Time:                        09:56:38       Log-Likelihood:                -87.619
# No. Observations:                  32       AIC:                             179.2
# Df Residuals:                      30       BIC:                             182.2
# Df Model:                           1                                         
# Covariance Type:            nonrobust                                         
# ========================================================================================
#                  coef             std err          t       P>|t|      [0.025      0.975]
# ----------------------------------------------------------------------------------------
# Intercept     30.0989(y절편)       1.634       18.421      0.000      26.762      33.436
# hp            -0.0682(기울기)      0.010       -6.742      0.000      -0.089      -0.048
# =========================================================================================
# Omnibus:                        3.692       Durbin-Watson:                   1.134
# Prob(Omnibus):                  0.158       Jarque-Bera (JB):                2.984
# Skew:                           0.747       Prob(JB):                        0.225
# Kurtosis:                       2.935       Cond. No.                         386.
# ==========================================================================================


# [3단계] : 선형회귀방정식
# 음의 상관관계가 있으므로 hp가 증가하면 mpg는 감소한다.
# mpg(y값) = -0.0682 * hp(x값) + 30.0989 ... (+ err)


# [4단계] : 값을 넣어보자.
print('마력수 110에 대한 연비 예측 : ', result.predict({'hp':[110]}))
print('마력수 150에 대한 연비 예측 : ', result.predict({'hp':[150]}))
print(result.predict(pd.DataFrame({'hp':[110, 150]})))  
# 결과 :
# 마력수 110에 대한 연비 예측 :  22.5189
# 마력수 150에 대한 연비 예측 :  19.7779

# 기울기와 절편만 구하기
yhat = result.params['hp']
# 기울기
bias = result.params['Intercept']
# 절편

# 회귀식 구하기
print(f"회귀식 : mpg = {yhat:.4f} * hp + {bias:.4f}")
print(f"회귀식 : mpg = {result.params['hp']:.4f} * hp + {result.params['Intercept']:.4f}")
# 결과 :   
# 회귀식 : mpg = -0.0682 * hp + 30.0989
# 회귀식 : mpg = -0.0682 * hp + 30.0989
# 해석 : 두 변수의 관계를 나타내는 직선의 방정식이 완성되었다. 이제 우리는 이 회귀식을 이용하여 마력수에 따른 연비를 예측할 수 있다.
#        마력이 1증가할 때 연비는 0.0682 감소한다. 마력이 10 증가하면 연비는 0.682 감소한다. 마력이 100 증가하면 연비는 6.82 감소한다.

# 이제 우리가 그린 그림(산점도)에 회귀선을 그려보자.
# 1. x축은 마력수(hp), y축은 연비(mpg)이다.
plt.scatter(mtcars.hp, mtcars.mpg)

# 2. 회귀선 그리기
plt.plot(mtcars.hp, result.predict(mtcars), color='red', linewidth=2)

# 3. x축과 y축에 라벨을 붙이고 제목을 붙인다.
plt.xlabel('마력수(Horsepower)')
plt.ylabel('연비(Miles per Gallon)')
plt.title('Scatter Plot of MPG vs HP')
plt.legend()

# 4. 그래프 보여주기
plt.show()

# 결정계수
print('결정계수(R2) : ', result.rsquared)
# 마력(hp=x축)으로 연비(mpg=y축)의 변동을 설명할 수 있는 비율은 약 60.24%이다. 
# 나머지 40%는 다른 변수들에 의해 설명된다.

print('새로운 마력수에 대해서 예측된 연비 주장')
new_data = pd.DataFrame({'hp':[110, 150, 200, 250]})
new_pred = result.predict(new_data)
print(pd.DataFrame({'마력수(hp)' : new_data['hp'], '예측연비(mpg)' : new_pred.round(2)}))
# 결과 :
#    마력수(hp)  예측연비(mpg)          
# 0       110          22.52
# 1       150          19.78
# 2       200          16.46
# 3       250          13.14
# 해석 : 


# --------------------------------------------------------------------------------------
# 다중선형회귀 : x가 2개 이상인 경우
print("\n 다중선형회귀 : x가 2개 이상인 경우")
# 변수 설정
# 독립변수(x) : 마력수(hp), 차량무게(wt)
# 종속변수(y) : 연비(mpg)

result2 = smf.ols(formula = 'mpg ~ hp + wt', data=mtcars).fit()
# 이번에는 독립변수가 2개이다. 그래서 formula = 'mpg ~ hp + wt'로 설정한다.
print(result2.summary())
# 결과 : 
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                    mpg   R-squared:                       0.827
# Model:                            OLS   Adj. R-squared:                  0.815
# Method:                 Least Squares   F-statistic:                     69.21
# Date:                Mon, 02 Nov 2026   Prob (F-statistic):           9.11e-12
# Time:                        10:46:37   Log-Likelihood:                -74.326
# No. Observations:                  32   AIC:                             154.7
# Df Residuals:                      29   BIC:                             159.0
# Df Model:                           2                                         
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept     37.2273      1.599     23.285      0.000      33.957      40.497
# hp            -0.0318      0.009     -3.519      0.001      -0.050      -0.013
# wt            -3.8778      0.633     -6.129      0.000      -5.172      -2.584
# ==============================================================================

print('회귀계수 : \n', result2.params)

# yhat = w1 * hp + w2 * wt + bias
print(f"회귀식 : mpg(y값) = {result2.params['hp']:.4f} * hp(x1값) + {result2.params['wt']:.4f} * wt(x2값) + {result2.params['Intercept']:.4f}")  

y_pred2 = result2.predict(mtcars)
print('실제값 : ', mtcars.mpg[:5].values.round(2))
print('예측값 : ', y_pred2[:5].round(2))

print('새로운 마력수에 대해서 예측된 연비 주장')
new_data2 = pd.DataFrame({'hp':[110, 150, 200, 250], 'wt':[2.5, 3.0, 3.5, 4.0]})
new_pred2 = result2.predict(new_data2)

print(pd.DataFrame({'마력수(hp)' : new_data2['hp'], 
                    '차량무게(wt)' : new_data2['wt'], 
                    '예측연비(mpg)' : new_pred2.round(2)}))
# 결과 : 
#          마력수(hp)   차량무게(wt)  예측연비(mpg)
#    0        110          2.5          24.04
#    1        150          3.0          20.83
#    2        200          3.5          17.30
#    3        250          4.0          13.77

# 결정계수 확인하기
print('결정계수(R2) : ', result2.rsquared)
# 결과 : 결정계수(R2) :  0.815
# 해석 : 독립변수 2개(hp, wt)로 종속변수(mpg)의 변동을 설명할 수 있는 비율은 약 81.5%이다.

# 시각화
plt.figure(figsize=(8,6))
plt.scatter(mtcars.mpg, y_pred2)

# 실제값과 예측값이 일치하는 기준선
min_val = min(mtcars.mpg.min(), y_pred2.min())
max_val = max(mtcars.mpg.max(), y_pred2.max())

plt.plot([min_val, max_val], [min_val, max_val], color='red', linewidth=2)
# plt.plot : 같은 위치의 실제값과 예측값을 연결하는 직선을 그린다. = 기준선
# 실제값과 예측값이 일치하면 직선 위에 점이 찍힌다. 직선에서 멀리 떨어진 점은 실제값과 예측값의 차이가 크다는 뜻
# 시작점 : (min_val, min_val)
# 끝점   : (max_val, max_val)

plt.xlabel('실제 연비(mpg)')       
plt.ylabel('예측 연비(mpg)')
plt.title('다중선형회귀 : 실제값 vs 예측값')

plt.legend()
plt.show()      

# **선형회귀모델의 선행조건**
# 1. 선형성 : 독립변수와 종속변수의 관계가 선형이어야 한다.
# 2. 독립성 : 독립변수 간에 상관관계가 없어야 한다. (다중공선성 문제)
# 3. 등분산성 : 독립변수의 값에 따라 종속변수의 분산이 일정해야 한다.
# 4. 정규성 : 잔차가 정규분포를 따라야 한다.
# 5. 다중공선성 : 다중회귀 분석 시 두 개 이상의 독립변수 간에 강한 상관관계가 있어서는 안된다.

# 모델의 절절성