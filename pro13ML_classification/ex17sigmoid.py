# Regression   ->   classification   ->   clustering 
# 지난 시간까지 '선형회귀분석'과 '비선형회귀분석'을 배웠다.
# Regression(회귀)는 정량적이라서 우리가 회귀선으로 값을 예측할 수 있었지만
# 이번에 배울 classification은 정성적인 값으로 우리가 회귀선을 통해서 값을 분류할 것이다.

# classification의 종류에는
# - Logistic Regression 
# - Decision Tree
# - Random Forest
# - SVM
# - K-MM
# 이 존재한다. 우리는 이 중 Logistic Regression을 중점적으로 배운다. 
# 왜냐하면 Logistic Regression  ->  ANN  ->  MLP  ->  Deep Learning  ->  생성형 Model(LLM)
# 이 되어서 중요하기 때문이다. 그리고 유일하게 Logistic Regression언 Classification 중에서 y = wx + b를 이용하여
# 추세선을 그려 데이터를 분류한다.

# y = wx + b
# 이 추세선에서 기울기(w)는 입력데이터 갯수만큼 생긴다.

# Linear Regression은 독립변수 : 연속형, 종속변수 : 연속형이었다.
# Logistic Regression은 독립변수 : 연속형, 종속변수 : 범주형(확률값)이다. 
# 그래서 wx+b를 logit변환하여 sigmoid를 태워주어 특정 값을 도출한다.

# 그래서 우리는 Logistic Regression의 방법에 대해서 학습한다.
# 그 알고리즘을 파악한다.

# 승산비(오즈비), 시그모이드, 가능도(우도),

# 과정
# Logistic Regression : 오즈비에 log함수를 적용한 것으로 로짓을 대상으로 회귀분석을 한 것
# [1단계] : 독립변수에 학습된 가중치와 절편을 적용하여 z = wx + b를 계산한다.
# [2단계] : 'wx + b'를 승산비(odds ration)로 감싼다.
# [3단계] : 그리고 승산비로 감싼 값을 로그(log)변환해준다.
# [4단계] : 이 값은 확률 자체가 아니라 로그 오즈(logit)값으로 -무한대 ~ +무한대까지의 '실수' 범위르 가진다.
# [5단계] : 이후 sigmoid 함수를 적용하여 0~1사이의 '확률'을 구하고, 0.5를 기준으로 클래스를 분류한다.
# [6단계] : 그래프로 시각화를 하게 되면 sigmoid함수에 의해 여러 개의 s자 선이 나타난다. 그 중에서 어떤 s선을 사용할지 판단하기 위해서 가능성(우도)를 사용한다.
#          모델의 학습과 통계적 적합도 평가 : 가능성(우도)
#          분류 성능 평가 : Acccuracy, Precision, Recall, F1-score, ROC-AUC
#          가 사용된다. 
#          -> "우도를 사용한다" = "로지스틱 회귀는 최소 제곱법이 아니라 “최대 가능도 추정(MLE)”을 사용한다"
# 확률 vs 가능도
# : 확률은 모델의 파라미터가 주어졌을 때 특정 데이터가 관측될 가능성이고,
#   가능도(우도)는 관측된 데이터를 고정한 채 어떤 파라미터가 그 데이터를 더 잘 설명하는지 나타내는 값이다.

# 이때 wx + b를 계산하기 전에 선형회귀의 추세선을 별도로 학습하는 것이 아니라 학습과정에서 분류에 적합한 가중치(W)와 절편(b)를 직접 추정한다.

# sigmoid function 적용 연습
# LogisticRegression 모델은 wx+b를 logit 변환한 값에 sigmoid function처리한 값을 사용한다.

# Linear Regression에서는 독립변수도 연속형 종속변수도 연속형이라서 wx+b를 수치값으로 받았다(정성적)
# 하지만 Logistic Regression은 독립변수는 연속형, 종속변수는 범주형이다.(정량적) 그래서 수치값이 아닌 확률값을 받게 된다.
# wx+b를 연속형으로 반환한다. 하지만 우리는 정량적으로 반환해야한다.
# 그래서 승산비(odds ration)로 감싸서 로그를 씌운다. 그러면 -무한대에서 +무한대의 범위를 가진다. = 로짓변환
# 그다음 sigmoid함수를 통과시킨다. 그러면 0~1사이의 실수값이 된다. 0.5를 기준으로 크면 1, 작으면 0으로 값을 내놓았다.

# log(p / 1 - p) = wx + b라고 정의된다.
# 그러므로 z = wx + b   ->   sigmoid(z)   ->   p(0 ~ 1) : 이항분류

# sigmoid function 수식에 의해 변환된 값 확인
import math

def MySigmoidFunc(num):    # 이때 num은 logit변환을 한 값이라고 가정!...sigmoid부터 진행하면 된다.
    return 1 / (1 + math.exp(-num))

print(MySigmoidFunc(3))
print(MySigmoidFunc(1.5))
print(MySigmoidFunc(-5.0))
print(MySigmoidFunc(-10))
# 결과 : 
# 0.9525741268224334
# 0.8175744761936437
# 0.0066928509242848554
# 4.5397868702434395e-05


import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

print("\n로짓(logit)변환이 되었다고 가정한 값으로 sigmoid함수를 통과한 후의 결과를 시각화")
x = np.linspace(-10, 10, 50)
# 입력자료(독립변수) : 연속형

# 선형결합(이미 logit된 값)
w = 1.5
b = -2
z = w*x + b
# 모델이 1차 방정식을 만들었다.

def OurSigmoidFunc(z):    # 이때 num은 logit변환을 한 값이라고 가정!...sigmoid부터 진행하면 된다.
    return 1 / (1 + np.exp(-z))

p = OurSigmoidFunc(z)
# 모델이 z값을 주었다. .. 해당 z에는 logit이 되어있다.
print("p : ", p)
# 0~1사이의 값(확률)이 출력됨.
# 출력자료(종속변수) : 범주형
# 결과 : 
#   [4.13993755e-08 7.63639448e-08 1.40858451e-07 2.59822907e-07
#    4.79260816e-07 8.84028624e-07 1.63064936e-06 3.00783886e-06
#    5.54814808e-06 1.02338864e-05 1.88769322e-05 3.48192229e-05
#    6.42245224e-05 1.18460049e-04 2.18485712e-04 4.02937317e-04
#    7.42992282e-04 1.36964005e-03 2.52347464e-03 4.64482037e-03
#    8.53420671e-03 1.56292700e-02 2.84536579e-02 5.12530324e-02
#    9.06171702e-02 1.55266585e-01 2.53197177e-01 3.84761164e-01
#    5.35653671e-01 6.80289391e-01 7.96951173e-01 8.78637645e-01
#    9.30334354e-01 9.60987588e-01 9.78465443e-01 9.88209160e-01
#    9.93573106e-01 9.96505489e-01 9.98102476e-01 9.98970396e-01
#    9.99441555e-01 9.99697171e-01 9.99835804e-01 9.99910977e-01
#    9.99951736e-01 9.99973834e-01 9.99985814e-01 9.99992309e-01
#    9.99995831e-01 9.99997740e-01]

# 시각화
plt.figure(figsize=(8,5))
plt.scatter(x, p, label='sigmoid(z)', color = 'blue')
# plot은 직선
# scatter는 점선
plt.axhline(0.5, color = 'red', linestyle = '--')
plt.title('z = wx + b  -->  sigmoid  -->  확률(이항분류)')
plt.xlabel('x(입력값)')
plt.ylabel('y(확률값)')
plt.grid(True)
plt.legend()
plt.show()
# 0.5보다 큰 실수 값은 1로 분류하고 0.5보다 작은 값들은 0으로 분류한다.
# 이 과정이 logistic Regression의 알고리즘이다.
