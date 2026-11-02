# 단순 선형회귀를 하는 것.... - iris dataset사용
# 상관관계가 약한 경우와 강한 경우로 회귀모델을 각기 생성한 후 비교
# 다음 카페 - 데이터 분석 - 42번 보면서 공부하기

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

iris  = sns.load_dataset('iris')
print(iris.head(3), type(iris))
print(iris.iloc[:, 0:4].corr())
# 결과 : 
#                     sepal_length  sepal_width   petal_length  petal_width
#    sepal_length       1.000000     -0.117570      0.871754      0.817941
#    sepal_width       -0.117570      1.000000     -0.428440     -0.366126
#    petal_length       0.871754     -0.428440      1.000000      0.962865
#    petal_width        0.817941     -0.366126      0.962865      1.000000

# 상관관계가 약한 회귀모델과 상관관계가 강한 회귀모델을 비교해보자


print("\n 연습1 : 상관관계가 약한 변수를 사용 : - 0.117570")
result1 = smf.ols(formula = 'sepal_length ~ sepal_width', data=iris).fit()
print(result1.summary())
print('R squared : ', result1.rsquared)
# 결과 : 0.0138226 
# 해석 : 해석력이 1퍼센트다 = 잘해석하지 못한다.
print('p-value : ', result1.pvalues.iloc[1])
# 결과 : 0.1518982 > 0.05 : 이 모델은 유의하지 못한다.

# 시각화
plt.scatter(iris.sepal_width, iris.sepal_length)
plt.plot(iris.sepal_width, result1.predict(), color = 'r')
plt.show()
# ----------------------------------------------------------------------------

print("\n 연습2 : 상관관계가 강한 변수를 사용 : 0.871754")
result2 = smf.ols(formula = 'sepal_length ~ petal_length', data=iris).fit()
print(result2.summary())
print('R squared : ', result2.rsquared)
# 결과 : 0.7599546457725151
# 해석 : 해석력이 76퍼센트다 = 잘해석한다. = 독립변수가 종속변수를 잘 설명하고 있다
print('p-value : ', result2.pvalues.iloc[1])
# 결과 : 1.038667419449791e-47 < 0.05 : 이 모델은 유의하다.

# 시각화
plt.scatter(iris.petal_length, iris.sepal_length)
plt.plot(iris.petal_length, result2.predict(), color = 'b')
plt.show()

# 음이든 양이든 상관관계가 -1이나 1에 가까워야 한다. 0에 가까우면 좋지 않다.
# 최소 0.3은 이상이되어야 한다. = 그래야 스피어만 상관계수에 의해서 두 변수간의 상관관계를 잘설명한다.

print("\n 모델 예측값 확인")
# 모델 실제값과 예측값 비교1
print("실제값 : ", iris.sepal_length[:10].values.round(1))
print("예측값 : ", result1.predict()[:10].round(1))
# 실제값 :  [5.1  4.9  4.7  4.6  5.0  5.4  4.6  5.0  4.4  4.9]
# 예측값 :  [5.7  5.9  5.8  5.8  5.7  5.7  5.8  5.8  5.9  5.8]
# 실제값과 예측값의 차이가 많이 난다.
print()

# 모델 실제값과 예측값 비교2
print("실제값 : ", iris.sepal_length[:10].values.round(1))
print("예측값 : ", result2.predict()[:10].round(1))
# 실제값 :  [5.1  4.9  4.7  4.6  5.0  5.4  4.6  5.0  4.4  4.9]
# 예측값 :  [4.9  4.9  4.8  4.9  4.9  5.0  4.9  4.9  4.9  4.9]
# 실제값과 예측값의 차이가 거의 나지 않는다.


print("\n 새로운 petal_length로 sepal_length를 예측")
# 예측값 구해보기
new_data = pd.DataFrame({'petal_length': [1.1, 0.5, 6.0]}) # 임의의 petal_length : 1.1, 0.5, 6.0 넣어줌
y_pred = result2.predict(new_data)
print("예측된 꽃받침의 길이 : ", y_pred.values.round(5))
# 결과 :
# 예측된 꽃받침의 길이 :  [4.75642 4.51106 6.76014]

# ---- 여기까지는 독립변수 1개 : 단순 선형 회귀..


# 이제부터는 다중 선형 회귀
print("\n 독립변수가 복수인 경우 - 다중선형회귀")

# 방법1
# result3 = smf.ols(formula='sepal_length ~ petal_lenth + petal_width', data=iris).fit()
# 이런식으로 독립변수(x)가 2개 이상인 경우가 대부분이다.
# 이때는 구조방정식을 사용한다.
# 하지만 우리는 다중선형회귀는 보지 않는다!! 다행이다.

# 방법2
column_select = "+".join(iris.columns.difference(['sepal_length', 'sepal_width', 'species']))
# 3개의 열을 뺀 나머지는 '+'로 묶으라는 뜻
print(column_select)
# 결과 : petal_length + petal_width
result3 = smf.ols(formula='sepal_length ~ ' + column_select, data = iris).fit()
print(result3.summary())
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:           sepal_length   R-squared:                       0.766
# Model:                            OLS   Adj. R-squared:                  0.763 # 독립변수가 2개 이상이므로 조정된 계수를 본다. 모델을 기준으로 평가
# Method:                 Least Squares   F-statistic:                     241.0
# Date:                Fri, 30 Oct 2026   Prob (F-statistic):           4.00e-47
# Time:                        17:15:53   Log-Likelihood:                -75.023
# No. Observations:                 150   AIC:                             156.0
# Df Residuals:                     147   BIC:                             165.1
# Df Model:                           2                                         
# Covariance Type:            nonrobust                                         
# ================================================================================
#                    coef    std err          t      P>|t|      [0.025      0.975]
# --------------------------------------------------------------------------------
# Intercept        4.1906      0.097     43.181      0.000       3.999       4.382
# petal_length     0.5418      0.069      7.820      0.000       0.405       0.679
# petal_width     -0.3196      0.160     -1.992      0.048      -0.637      -0.002
#                                                    2개의 독립변수를 썼는데 모두 0.05보다 작기때문에 유의미한 변수로 사용할 수 있다.
#                                                    만약 0.05보다 크면 유의하지 않기 때문에 변수로 사용하지 않는다.
#                                                    각 변수를 기준으로 비교
# ==============================================================================
# Omnibus:                        0.383   Durbin-Watson:                   1.826
# Prob(Omnibus):                  0.826   Jarque-Bera (JB):                0.540
# Skew:                           0.060   Prob(JB):                        0.763
# Kurtosis:                       2.732   Cond. No.                         25.3
# ==============================================================================