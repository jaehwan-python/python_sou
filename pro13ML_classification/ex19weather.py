# LogisticRegression : 날씨예보(비가 올지 안올지)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/weather.csv")
print(data.head(2), data.shape)
# 결과 : 
#          Date  MinTemp  MaxTemp  Rainfall  Sunshine  WindSpeed  Humidity  Pressure  Cloud  Temp RainToday RainTomorrow
# 0  2016-11-01      8.0     24.3       0.0       6.3         20        29    1015.0      7  23.6        No          Yes
# 1  2016-11-02     14.0     26.9       3.6       9.7         17        36    1008.4      3  25.7       Yes          Yes 
# (366, 12)
# 366행, 12열의 값
# ... RainTomorrow는 Yes라는 str값이다.
# 우린 이를 숫자로 바꾸어 주어야 한다.

print(data.info())
#  Column   Non-Null          Count        Dtype  
#   ---      ------      --------------   -----  
#    0        Date        366 non-null      str    
#    1      MinTemp       366 non-null    float64
#    2      MaxTemp       366 non-null    float64
#    3      Rainfall      366 non-null    float64
#    4      Sunshine      363 non-null    float64
#    5      WindSpeed     366 non-null     int64  
#    6      Humidity      366 non-null     int64  
#    7      Pressure      366 non-null    float64
#    8       Cloud        366 non-null     int64  
#    9        Temp        366 non-null    float64
#   10      RainToday     366 non-null      str    
#   11     RainTomorrow   366 non-null      str
# 1 ~ 9행까지 독립변수로 쓴다.
# 11행은 종속변수가 된다.
# 나머지 0, 10행은 뺀다. -> 필요없기 때문

df = pd.DataFrame()
df = data.drop(['Date', 'RainToday'], axis = 1)
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes' : 1, 'No' : 0})
# Sunshine 등 분석에 사용하는 열에 결측값이 있는 행을 제외한 뒤 학습/검증 데이터를 나눈다.
df = df.dropna().copy()
print(df.head(2), df.shape)
print(df['RainTomorrow'].unique())
# 결과 :
#    MinTemp  MaxTemp  Rainfall  Sunshine  WindSpeed  Humidity  Pressure  Cloud  Temp  RainTomorrow
# 0      8.0     24.3       0.0       6.3         20        29    1015.0      7  23.6             1
# 1     14.0     26.9       3.6       9.7         17        36    1008.4      3  25.7             1 (366, 10)

# 독립변수 : 나머지열 - 연속형
# 종속변수 : Rainbow - 범주형

print('\n' "학습용 : train dataset, 검증용 : test dataset")
# 학습한 데이터로 검증까지하면 당연한 정답이 나오기 때문에 과적합 문제가 생긴다. 그래서 train_test_split을 통해서 모델의 성능을 검증한다. = 과적합 방지 목적

train, test = train_test_split(df, test_size = 0.43, random_state = 42)
# seed를 random_state = 42로 고정을 했기에 강사님이랑 동일한 값이 나온다.
# ->  train데이터 : 전체 데이터의 약 57%, 모델 학습용
# ->  test데이터  : 전체 데이터의 약 43%, 성능 검증용
print(train.shape, test.shape)
print(train.head(3))
print(test.head(3))

# 모델 생성 - logit()모델
col_select = "+".join(train.columns.difference(['RainTomorrow']))
print(col_select)
my_formula = 'RainTomorrow ~ ' + col_select
model = smf.logit(formula = my_formula, data=train).fit()
# .fit()으로 모델을 생성하여 앞서 주었던 데이터(trian과 test 데이저 중 data = train을 사용)를 학습하여 그 결과로 회귀계수와 절편을 생성

print(model.summary())   # 각 변수별 p-value  >  0.05인 경우 제거후 고민한다.
# 결과 : 
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:           RainTomorrow   No. Observations:                  206
# Model:                          Logit   Df Residuals:                      196
# Method:                           MLE   Df Model:                            9
# Date:                Wed, 04 Nov 2026   Pseudo R-squ.:                  0.4589
# Time:                        15:04:41   Log-Likelihood:                -52.477
# converged:                       True   LL-Null:                       -96.986
# Covariance Type:            nonrobust   LLR p-value:                 2.562e-15
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    281.4473     66.675      4.221      0.000     150.766     412.128
# Cloud          0.0158      0.138      0.115      0.908      -0.254       0.286
# Humidity       0.0501      0.032      1.543      0.123      -0.014       0.114
# MaxTemp       -0.3909      0.348     -1.123      0.262      -1.073       0.291
# MinTemp       -0.0613      0.087     -0.702      0.483      -0.233       0.110
# Pressure      -0.2803      0.065     -4.323      0.000      -0.407      -0.153
# Rainfall      -0.1096      0.088     -1.249      0.212      -0.282       0.062
# Sunshine      -0.4026      0.149     -2.695      0.007      -0.695      -0.110
# Temp           0.5603      0.355      1.578      0.114      -0.135       1.256
# WindSpeed     -0.0212      0.039     -0.545      0.586      -0.098       0.055
# ==============================================================================
# Intercept    281.447250
# Cloud          0.015845
# Humidity       0.050073
# MaxTemp       -0.390876
# MinTemp       -0.061339
# Pressure      -0.280264
# Rainfall      -0.109617
# Sunshine      -0.402560
# Temp           0.560347
# WindSpeed     -0.021242
# 모든 독립변수에 대해서 회귀계수(기울기)를 만나보았다

print(model.params)
# 학습된 모델(logit)의 회귀계수를 보여준다.
print()

print("예측값 : ", np.rint(model.predict(test)[:5].values))
print("실제값 : ", test['RainTomorrow'][:5].values)


# 분류 정확도
# < Train데이터만 가지고 분류 정확도 확인 > ... pred_table()
# pred_table() : 기본적으로 모델 학습에 사용한 train 데이터만 대상으로 혼동행렬을 생성하기 때문에 
#                train에 대한 정확도만 구하고 test에 대한 정확도는 구하지 못한다.
pred_mat = model.pred_table()
print(pred_mat)

print("분류 정확도(Accuracy) : ", (pred_mat[0][0] + pred_mat[1][1]) / len(train))
# train데이터만 가지고 평가함


# < Test데이터를 가지고 분류 정확도 확인 > = conf_mat
from sklearn.metrics import accuracy_score, confusion_matrix
pred = model.predict(test)
# accuracy_score는 confusion_matrix 둘 다 test 데이터를 가지고 혼동행렬을 만든다.

conf_mat = confusion_matrix(test['RainTomorrow'], np.rint(pred))
# test['RainTomorrow'] : 실제값
# np.rint(pred) : 예측값
print(conf_mat)

print('분류 정확도(Accuracy) : ', (conf_mat[0][0] + conf_mat[1][1]) / len(test))
print('분류 정확도(Accuracy) : ', accuracy_score(test['RainTomorrow'], np.rint(pred)))
print('분류 정확도(Accuracy) : ', accuracy_score(test['RainTomorrow'], (pred >= 0.5).astype(int)))
# np.rint와 np.around그리고 (pred >= 0.5).astype(int)는 아래 코드와 동일하다.
# accuracy_score는 test데이터만 가지고 평가하기 때문이다!!

# train과 test의 분류 정확도는 거의 비슷하게 나와야 한다!! = 정상적인 모델
# train데이터로는 분류 정확도가 잘 나왔는데 test데이터로 해보니 분류정확도가 잘 안나온다면(차이가 '10'이상 난다면)
# 과적합 문제가 있는 것이다.

# model.pred_table()  : 모델 학습에 사용한 "train용 데이터"의 혼동행렬을 생성한다.
# confusion_matrix(실제값, 예측값)  : 전달받은 값으로 혼동행렬을 생성한다.
# accuracy_score(실제값, 예측값)  : 전달받은 값으로 정확도를 바로 계산한다.

# 이때 model.pred_table()과 confusion_matrix(실,예)의 차이는
# 평가할 데이터를 어디서 가져오는지가 다르다는 점이다.
# model.pred_table()       ->  모델에 저장된 학습 데이터로 혼동행렬 생성
# confusion_matrix(실,예)  ->  네가 전달한 데이터로 혼동행렬을 생성
# 또 pred_table() 자체는 혼동행렬만 만든다. 
# 정확도는 그 행렬로 맞춘 개수 / 전체 개수를 따로 계산하는 것

# 혼동행렬을 만드는 model.pred_table()과 confusion_matrix()는 값의 차이나는 이유가 
# pred_table은 컴퓨터가 기존 데이터를 train과 test로 무작위로 나누는 방식을 선택하여 train값에 대한 결과를 나타내고 
# confusion_matrix는 내가 직접 입력한 값에 대한 결과가 혼동행렬로 나오는거야. 
# 그래서 model이 성능이 좋으면 model.pred_table()로 예측한 결과와 confusion_matrix()로 나온 결과가 비슷하여 
# 과적합이 일어나지 않는다. 하지만 두 방식의 혼동행렬(분류 정확도)의 차이가 크면 
# 과적합이 일어났다는 뜻이다.

# train_test_split()은 기존 데이터를 학습용 train과 검증용 test로 나눈다.
# model.pred_table()은 학습에 사용한 train의 실제값과 예측값으로 혼동행렬을 만든다.
# 현재 confusion_matrix()에는 test의 실제값과 예측값을 전달하여 혼동행렬을 만든다.
# confusion_matrix()는 전달하는 값에 따라 train과 test 모두 평가할 수 있다. : 내가 직접 실제값과 예측값을 입력하면 되기 때문

# train과 test의 데이터 개수가 다르므로 혼동행렬의 개수보다 정확도를 비교한다.
# train 정확도는 높은데 test 정확도가 크게 낮다면 과적합을 의심할 수 있다.
# 두 정확도가 비슷하더라도 둘 다 낮으면 성능이 좋은 모델이라고 할 수 없다.