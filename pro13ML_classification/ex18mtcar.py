# Logistic Regression -> 정성적 분류 모델
# 독립변수 : 연속형
# 종속변수 : 범주형(확률값)
#  
# "wx+b를 logit변환(=오즈비(odds ratio)로 감싸기 + log변환)한 후, "sigmoid함수"를 태워주어 특정 값을 도출한다"
# = 
# wx+b(선형결합)를 로그변환한다(로그오즈(logit())으로 해석한다.)  ->  그러면 값이 -무한대 ~ +무한대의 값이 나온다. 
# 우리는 이 실수를 sigmoid함수를 씌워서 0~1사이의 값으로 만든다   ->  그때 이 값을 확률값으로 본다.

# Logistic Regression을 근거로 Neural Network에 뉴런이 사용됨을 알아야 한다!! ... 추후에 중요!!

# 승산비(오즈비), 시그모이드, 가능도(우도),

# 과정
# Logistic Regression : 오즈비에 log함수를 적용한 것으로 로짓을 대상으로 회귀분석을 한 것
# [1단계] : 독립변수에 학습된 가중치와 절편을 적용하여 z = wx + b를 계산한다.
# [2단계] : 'wx + b'를 승산비(odds ration)로 감싼다.
# [3단계] : 그리고 승산비로 감싼 값을 로그(log)변환해준다.
# [4단계] : 이 값은 확률 자체가 아니라 로그 오즈(logit)값으로 -무한대 ~ +무한대까지의 '실수' 범위르 가진다.
# [5단계] : 이후 sigmoid 함수를 적용하여 0~1사이의 '확률'을 구하고, 0.5를 기준으로 클래스를 분류한다.
# [6단계] : 그래프로 시각화를 하게 되면 sigmoid함수에 의해 여러 개의 s자 선이 나타난다. 그 중에서 어떤 s선을 사용할지 판단하기 위해서 가능성(우도)를 사용한다.
#          - ** 모델의 학습과 통계적 적합도 평가  :  가능성(우도)
#          - ** 분류 성능 평가                   :  Acccuracy, Precision, Recall, F1-score, ROC-AUC
#          가 사용된다. 
#          -> "우도를 사용한다" = "로지스틱 회귀는 최소 제곱법이 아니라 “최대 가능도 추정(MLE)”을 사용한다"

# LinearRegression은 'ols표'를 받지 못해서 오차를 알 수 없다 그래서 '예측성능평가' 시 'MSE'와 'RMSE'를 사용했다.
# LogisticRegression은 범주형 자료값을 도출하기 때문에 MLE를 사용한다.

# 확률 vs 가능도
# : 확률은 모델의 파라미터가 주어졌을 때 특정 데이터가 관측될 가능성이고,
#   가능도(우도)는 관측된 데이터를 고정한 채 어떤 파라미터가 그 데이터를 더 잘 설명하는지 나타내는 값이다.

# 이때 wx + b를 계산하기 전에 선형회귀의 추세선을 별도로 학습하는 것이 아니라 학습과정에서 분류에 적합한 가중치(W)와 절편(b)를 직접 추정한다.

# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# 실습) mtcars dataset
# 자동차 32대의 성능과 사양을 담은 데이터셋. 행 하나가 자동차 한 대, 열은 차량의 특성
# 변수(열)는 총 11개 -> mpg : 연비, cyl : 실린더 수, disp : 배기량, hp : 마력, drat : 후륜 기어비,
#                      wt : 차량 무게, qsec : ¼마일 주행 시간, vs : 엔진 형태(0=V형, 1=직렬형), 
#                      am : 변속기(0=자동, 1=수동), gear : 전진 기어 수, carb : 기화기 수
# 자동차의 종류(행)는 32대 -> 이건...너무 많다.

# 문제 정의 : “이 자동차는 마력이 얼마이고 연비가 얼마일 때, 자동일까 수동일까?”

# mtcars dataset을 사용하여 로지스틱 회귀분석을 해보자.
import statsmodels.api as sm
# 통계 분석을 가능하게 해주는 기능
mtcarsdata = sm.datasets.get_rdataset('mtcars')
print(mtcarsdata.keys())
mtcars = mtcarsdata.data
print(mtcars.head(2))
print(mtcars.info())
print()

# 연비와 마력수에 따른 변속기 분류(수동, 자동)
mtcar = mtcars.loc[:, ['mpg', 'hp', 'am']]
print(mtcar.head(3))
print(mtcar['am'].unique())
# 결과 : [1 0]

# 독립변수 : hp(마력), mpg(연비)
# 종속변수 : am(변속기)  ->  자동(0) or 수동(1)
print()
# ---------------------------------------------------------------------------------------------------------------------

# Logistic Regression 모델 제작 방법
# - logit() 
# - glm()

# ** 모델 작성 방법1 ** : logit()
import numpy as np
import statsmodels.formula.api as smf

formula = 'am ~ hp + mpg'
# 범주형(종속변수(y(변속기))) ~ 연속형(독립변수(x1(마력)) + 연속형(독립변수(x2(연비)))  -> 독립변수가 2개이기 때문
result = smf.logit(formula=formula, data=mtcar).fit()
# logit()모델 사용
print(result)
# 결과 : 
# Optimization terminated successfully.
#          Current function value: 0.300509
#          Iterations 9
# <statsmodels.discrete.discrete_model.BinaryResultsWrapper object at 0x0000027774EA9010>

print(result.summary()) # ols표와 같은 형태가 나온다.
# 결과 : 
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:                     am   No. Observations:                   32 -> :  종속변수 변동의 32%를 모델이 설명한다는 뜻
# Model:                        "Logit"   Df Residuals:                       29 -> :  분석에 사용한 관측값이 32개라는 뜻
# Method:                           MLE   Df Model:                            2
# Date:                Wed, 04 Nov 2026   Pseudo R-squ.:                  0.5551
# Time:                        10:19:40   Log-Likelihood:                -9.6163
# converged:                       True   LL-Null:                       -21.615
# Covariance Type:            nonrobust   "LLR p-value":               6.153e-06 -> 이때 p-value를 보고 판단하면 안된다. 
# ==============================================================================
#                    coef     std err         z      P>|z|    [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept(절편) -33.6052     15.077     -2.229     0.026    -63.156     -4.055
# hp(독변1)        0.0550       0.027      2.045     0.041      0.002      0.108
# mpg(독변2)       1.2596       0.567      2.220     0.026      0.147      2.372
# ==============================================================================
# 해당 모델의 평가는 Accuracy로 판단한다.
# 독립변수가 유의한 변수인지를 P>|z|를 통해 판단한다.

# LLR p-value의 역할 ... 이 p값으로 회귀계수를 보는 것이 아니라 모델의 학습과 통계적 적합도 평가에 사용되는것이다!!
# 귀무가설 : "독립변수없이 절편만 사용하는 모델이다."" 
# 대립가설 : "독립변수를 함께 사용하는 모델이다.""
# 원래 ols표에서 p-value는 "회귀계수(coef)가 0인지 아닌지"를 보았다.

pred = result.predict(mtcar[:10])
print('예측값 : ', pred.values)
# 예측값 :  [0.25004729 0.25004729 0.55803435 0.35559974 0.39709691 0.00651918 0.10844152 0.63232168 0.58498645 0.06598365]

print('예측값 : ', np.around(pred.values))
# np.around()가 0.5를 기준으로 해당 값을 나누어준다!!
# 결과 : 예측값 :  [0. 0. 1. 0. 0. 0. 0. 1. 1. 0.]
# 예측값이 0.5보다 크면 '1'로, 0.5보다 작으면 '0'으로 분류한다.


print('실제값 : ', mtcar['am'][:10].values)
# 결과 : 실제값 :  [1 1 1 0 0 0 0 0 0 0]
# 하지만 모든 예측이 적중한 것이 아니다. 그때 confusion-matrix를 사용해준다.
# 정답을 줬는데도 틀리는 이유는, 모델이 각 자동차의 정답을 그대로 저장하는 것이 아니라 전체 데이터에 맞는 하나의 규칙을 배우기 때문이다
print()

# 분류 정확도 평가
# 혼동행렬(confusion-matrix) : 인공지능이나 머신러닝의 분류모델이 예측한 결과가 실제 정답과 얼마나 맞고 틀렸는지를 4가지 경우의 수로 정리한 2x2표
# 평가 - ** 모델의 학습과 통계적 적합도 평가 : 가능성(우도)
#      - ** 분류 정확도 확인(Acccuracy(정확도), Precision(정밀도), Recall(재현도), F1-score(성능점수), ROC-AUC) ... 뒤에 이 4가지를 오차행렬표에서 구하는 방법을 구할 것이다!!
#                        - 우리는 Accuracy평가를 위해 "confusion-matrix"와 "accuracy_score()"를 사용한다

# 분류 정확도를 평가하는 데는 
# Acccuracy(정확도), Precision(정밀도), Recall(재현도), F1-score(성능점수), ROC-AUC 
# 이렇게 총 다섯가지가 있다. 이중 우리는 정확도, 정밀도, 재현도, 성능점수를 주로 본다.
# 오차행렬표(confusion-matrix)가 생성되면 그 표에서 값들을 서로 계산하여 저 4가지를 구할 수 있다.

# [분류 정확도 확인방법1 : confusion-matrix(수치에 대한 집계표(혼동 행렬))]
conf_tab = result.pred_table()
print(conf_tab)
# 결과 : 
#       [ [ 16.    3. ]
#         [  3.   10. ] ]

# 표 해석 :
#                                     <예측>
#                         Positive             Negative
#   <실제>  -   참       "TP(참 양성)"      "FP(거짓 음성)"
#           - 거짓      "FP(거짓 양성)"      "TP(참 음성)"

# ->  model이 positive(참)이라고 예측했는데 실제로 '참'인 데이터의 갯수      = TP(16개)
# ->  model이 positive(참)이라고 예측했는데 실제로는 '거짓'인 데이터의 갯수  = FP(3개)
# ->  model이 negative(거짓)이라고 예측했는데 실제로는 '참'인 데이터의 갯수  = FP(3개)
# ->  model이 negative(거짓)이라고 예측했는데 실제로 '거짓'인 데이터의 갯수  = TP(10개)

# 해석 : 모델이 26개는 맞추었지만 6개는 틀렸다.
print('분류 정확도 : ', (16 + 10) / len(mtcar))
print('분류 정확도 : ', (conf_tab[0][0] + conf_tab[1][1]) / len(mtcar))
# 결과 : 0.8125
# 해석 : 10개 중에 8.1개 정도 맞춘다.


# [분류 정확도 확인방법2 : accuracy_score()이용)]
pred2 = result.predict(mtcar)

from sklearn.metrics import accuracy_score, confusion_matrix

print('분류 정확도 : ', accuracy_score(mtcar['am'], np.around(pred2)))
# 결과 : 0.8125

# 예측 확률을 클래스(0 or 1)로 변환
pred_class = (pred2 > 0.5).astype(int)
conf_mat = confusion_matrix(mtcar['am'], pred_class)
print('confusion_matrix 혼동행렬 : \n', conf_mat)
print('분류 정확도 : ', (conf_mat[0][0] + conf_mat[1][1]) / len(mtcar))


print()
# ---------------------------------------------------------------------------------------------------------------------

# ** 모델 작성 방법2 : glm() ** : 일반화된 선형 모델로 pred_table()을 지원하지 않는다.
result2 = smf.glm(formula = formula, data=mtcar, family=sm.families.Binomial()).fit()
# 이항 분포를 사용하는 일반화 선형 모델(GLM)을 만들고, 데이터로 학습한 결과를 result2에 저장
# formula=formula  :  앞에서 정의한 식으로 종속변수와 독립변수를 지정합니다.
# data=mtcar  :  학습에 사용할 데이터입니다.
# family = sm.families.Binomial()  :  종속변수가 0 또는 1인 이항 분포를 따른다고 지정합니다. 
#                                     기본 연결 함수가 **로짓(logit)**이어서 로지스틱 회귀가 됩니다.
# .fit()  :  데이터를 이용해 회귀계수와 절편을 추정합니다.
# logit방법과의 차이는 family=sm.families.Binomial()를 사용한다.

print(result2.summary())
# 결과 : 
#                  "Generalized" Linear Model Regression Results                  
# ==============================================================================
# Dep. Variable:                     am   No. Observations:                   32
# Model:                          "GLM"   Df Residuals:                       29
# Model Family:                Binomial   Df Model:                            2
# Link Function:                  Logit   Scale:                          1.0000
# Method:                          IRLS   Log-Likelihood:                -9.6163
# Date:                Wed, 04 Nov 2026   Deviance:                       19.233
# Time:                        11:11:24   Pearson chi2:                     16.1
# No. Iterations:                     7   Pseudo R-squ. (CS):             0.5276
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          z    P>|z|(p값)   [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -33.6052     15.077     -2.229     "0.026"    -63.155      -4.055
# hp             0.0550      0.027      2.045     "0.041"      0.002       0.108
# mpg            1.2596      0.567      2.220     "0.026"      0.147       2.372
# ==============================================================================
glm_pred = result2.predict(mtcar[:10])
print('glm 예측값 : ', np.around(glm_pred.values))
print('glm 실제값 : ', mtcar['am'][:10].values)
# 결과 : 
# glm 예측값 :  [0. 0. 1. 0. 0. 0. 0. 1. 1. 0.]
# glm 실제값 :  [1  1  1  0  0  0  0  0  0  0]

# 평가 - 학습과 통계적 적합도 평가 - likelihood
#      - 분류 정확도 - confusion-matrix
#                   - accuracy-score()

glm_pred2 = result2.predict(mtcar)
print('glm 분류 정확도 : ', accuracy_score(mtcar['am'], np.around(glm_pred2)))
# 결과 : glm 분류 정확도 :  0.8125

# logit :  로지스틱 회귀 전용 모델, 이진분류에 사용된다. 연결함수는 logit에 연결된다.
# glm   :  일반화 선형모델, 이진분류/개수 데이터에서 사용된다. 연결함수는 분포에 따라 지정된다.
print()

# result.predict(newdf)   # logit()으로 학습한 모델 사용
# result2.predict(newdf)  # glm()으로 학습한 모델 사용
# result에 따라서 logit인지 glm인지 정한다.

# logit과 glm의 차이
# logit은 이진 분류용 로지스틱 회귀이고, 
# glm은 여러 종류의 회귀를 표현할 수 있는 더 넓은 틀이다.


print("새로운 값으로 예측하기 ------------------")
import pandas as pd
# 자동차의 마력(hp)과 연비(mpg)를 보고, 변속기가 자동인지 수동인지 예측하기!!를 하고 있다.

# 독립변수(연속형) : 마력, 연비
# 종속변수(범주형) : 변속기(자동or수동)

# result = smf.logit(formula=formula, data=mtcar).fit()
# result2 = smf.glm(formula = formula, data=mtcar, family=sm.families.Binomial()).fit()

# result는 logit을 사용한 것이고
# result2는 glm을 사용한 것이다.

newdf = pd.DataFrame()
newdf['mpg'] = [10, 30, 120, 130]
newdf['hp'] = [100, 110, 80, 130]
print(newdf)

new_pred = result2.predict(newdf)
# 1. 모델이 학습한 회귀계수(기울기)로 선형식 계산 -> "예측y값 = (마력계수(회귀계수1) * hp) + (연비계수(회귀계수2) * mpg) + 절편"  
#    이러면 -무한대 ~ +무한대의 값이 나온다.
# 2. 시그모이드 처리하여 확률값으로 변환
#    p = 1 / (1 + np.exp(-z))

print('예측결과 : ', np.around(new_pred.values)) # 소수점 지정 가능
print('예측결과 : ', np.rint(new_pred.values))   # 소수점 지정 불가능
# 시그모이드를 거친 확률(0~1)을 반올림해서 0 또는 1로 분류
# 결과 : 예측결과 :  [0.  1.  1.  1.]
# 해석 : 첫 번째는 변속기가 자동, 나머지 세 대는 수동으로 분류했다는 뜻



# < 머신러닝의 포용성(inclusion, tolerance) > 
# "모델 성능 100%는 좋지 않다(과적합). 이는 오히려 모델이 유연성과 포용성을 잃었다는 신호이다. 적당히 주변값을 포용하는 모델이 좋다."
# "머신러닝 모델을 평가할 때는 훈련 데이터의 100% 정확도라는 '숫자'에 집착하기보다는,
# "확실성과 다양한 변수를 얼마나 유연하게 포용할 수 있는가?"를 고려해야 한다."
#  ->  수학에서는 100%의 답을 원하지만 ML은 95%가 될 지라도 주변의 데이터(값)들을 포용하도록 하는 것이 중요하다.
# ex1) 고양이 분류 모델인 경우, 꼬리가 없는 고양이도 분류할 수 있어야 한다.
# 이는 과적합과 관련이 있다. 
# 그래서 이를 해결하기 위해 Train(학습용) / Test(검증용) 데이터를 따로 만들어서 
# 학습한 데이터(Train)과 다른 데이터(Text)를 준다. 그때 test 데이터를 잘 처리하는지 검증한다.
# 우리는 이때 포용성이 있는 모델을 만들어서 어느 정도의 유연성을 가지게 하였다.
# (회귀계수가 1이다. 모든 값에 대해서 하나의 특정값을 가리킨다) 



# < 편향과 분산 >
# 편향-분산 trade-off
# 상반관계 : '편향'과 '분산'은 일반적으로 **반비례 관계**에 있다. = 편향그래프와 분산그래프가 겹치는 접점을 찾아야 한다.
# 모델을 단순하게 만들면 편향이 커지고 분산이 작아진다. = 과소적합 위험
# 모델을 복잡하게 만들면 편향이 작아지고 분산이 커진다. = 과적합 위험
# 편향과 분산의 합(총 오차)이 최소가 되는 지점, 즉 일반화 성능이 가장 좋은 최적의 모델 복잡도를 찾는 것.

# 좋은 모델은 포용성이 있는 "일반화"된 모델이다.
# 그렇다고 너무 일반화된 것은 좋지 않다.
# 일반화와 최적화 모델 그 사이의 모델이 되는 것이 중요하다. = 포용성이 있다.


# 포용성과 편향/분산에 대해선 알고 있자!!

