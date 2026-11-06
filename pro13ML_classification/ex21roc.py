# ROC(Receiver Operating Characteristic) Curve는 모든 분류 
# 임계값에서 분류 모델의 성능을 보여주는 그래프로 
# x축이 fpr(1-특이도) : 실제 음성을 양성으로 잘못 예측한 비율
# y축이 tpr(민감도)   : 실제 양성을 양성으로 찾아낸 비율
# 인 그래프이다.
# 즉 '민감도'와 '특이도'의 관계를 표현한 그래프이다.
# ROC Curve는 AUC(Area Under Curve : 그래프 아래의 면적)를 이용해서 .. : 면적이 클수록 양성과 음성을 구분하는 능력이 좋다는 뜻 
# 모델의 성능을 평가한다. AUC가 클수록 정확히 분류함을 뜻한다. 
# fpr(1-특이도 : 위양성률)이 변할 때 tpr(민감도)이 어떻게 변하는지 알려 주는 곡선이다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, random_state=123)
# n_redundant : 독립변수 중 다른 독립변수의 선형 조합으로 나타내는 성분 수
# 데이터 100개를 생성하고, 각 데이터의 입력 특성(독립변수)를 2개로 설정하였다. 그리고 다른 특성의 선형조합으로 만든 중복 특성은 0개로 서로 독립변수간 영향을 미치지 않는다는 뜻이다.
print(x[:3], x.shape)
print(y[:3], y.shape)
# 임의로 생성한 독립변수(2개) : 
# [[-0.01032243 -0.80566819]    ->  [1]
#  [-1.10293659  2.21661117]    ->  [0]
#  [-1.90795358 -0.20839902]]   ->  [0]
#  (100, 2)
# 그 독립변수에 의한 종속변수값 : 
# [1 0 0] (100,)
plt.scatter(x[:, 0], x[:,1])
plt.show()


# 로지스틱 회귀 모델 생성
model = LogisticRegression().fit(x,y)
# 모델을 만들고 내가 설정한 x,y를 학습하게 한다.
y_hat = model.predict(x)
# y_hat : 예측값
# 그리고 나서 학습한 model에 x(임의의 100개의 값)를 넣어서 종속변수 값인 0혹은 1을 y_hat에 저장한다.
print('y_hat(예측값) : ', y_hat[:10])
print('real(실제값) : ', y[:10])
# 결과 : 
# y_hat(예측값)  :  [0  0  0  1  1  1  0  0  0  1]
# real(실제값)   :  [1  0  0  1  0  1  0  1  0  1]
# 예측값(y_hat)과 실제 정답(y)을 각각 처음 10개씩 출력해서 비교한다.


# ROC커브를 위한 '판별 경계선 설정용 결정함수'로 데이터 얻기
f_value = model.decision_function(x)
# decision_function(x) : 입력 데이터를 보고 “0 쪽인지, 1 쪽인지” 판단하기 위한 점수를 계산하는 함수
# 역할 : 각 데이터에 대해 클래스(종속변수 값) '1' 쪽으로 얼마나 기울어 있는지 나타내는 점수를 구한다
# 점수가 '음수'면 클래스 0으로 예측
# 점수가 '양수'면 클래스 1로 예측
# '0'이 기본 판정 경계
# 결정함수에 의해 수식이 생김
# "결정점수 = w₁ × 첫 번째 특성 + w₂ × 두 번째 특성 + b"
# 해석 : 결정점수 값을 '0' 혹은 '1'을 기준으로 최종 의미를 0에 가깝냐 1에가깝냐라는 결론을 도출한다.

print('f_value : ', f_value[:10])
# f_value(결정점수) : 결정함수에 대한 결정 점수(y값)

df = pd.DataFrame(np.vstack([f_value, y_hat, y]).T, columns = ['f', 'y_hat', 'y'])
print(df.head())
# 결과 : 
#          f       y_hat(예측값)     y(실제값)
# 0   -0.285798         0.0             1.0
# 1   -0.940896         0.0             0.0
# 2   -4.232468         0.0             0.0
# 3    2.804258                      1.0
# 4    0.061371         1.0             0.0
# 이제 예측값과 실제값을 보여주는 df가 만들어졌고 decision_function에 의한 f(f_value)도 생성되었다.


# 모델 성능 파악
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y, y_hat))
# 결과 : 
# [[44  4]
#  [8  44]]
# 결과값을 혼동행렬로 df로 표현을 하였다.
# 전체 100개 중 대각선의 44 + 44 = 88개를 맞혔고, 나머지 4 + 8 = 12개를 틀렸다.

accuracy = (44 + 44) / 100    # 정확도 = TP + TN / 전체수
precision = 44 / (44 + 8)     # 정밀도 = TP / (TP + FP) 
recall = 44 / (44 + 4)        # 재현도 = TP / (TP + FN)
specificity =  44 / (8 + 44)  # 특이도 = TN / FP + TN 
fallout = 8 / (8 + 44)        # 위양성률(fpr) = FP / (FP + TN)
print('accuracy(정확도)는... : ', accuracy)
print('precision(정밀도)는... : ', precision)
print('recall(재현도)는... : ', recall)
print('specificity(특이도)는... : ', specificity)
print('위양성률(fallout)는... : ', fallout) # = print('위양성률(fallout)는... : ', 1 - specificity)
# 결과 :
# accuracy(정확도)는...    :  0.88
# precision(정밀도)는...   :  0.8461538461538461
# recall(재현도)는...      :  0.9166666666666666
# specificity(특이도)는... :  0.8461538461538461
# 위양성률(fallout)는...   :  0.15384615384615385
print()

from sklearn import metrics
accuracy_score = metrics.accuracy_score(y,y_hat)
print('accuracy(정확도) : ', accuracy_score)
# 결과 : 
# accuracy(정확도) :  0.88

# 분류성능평가
cl_rep = metrics.classification_report(y, y_hat)
print('**분류모델 성능 평가 보고서** : \n', cl_rep)
#                            precision   recall   f1-score   support

#            0             "0.85"      "0.92"     0.88        48
#            1              0.92        0.85      0.88        52

#     accuracy                                    0.88       100
#    macro avg(평균)        0.88       0.88       0.88       100
# weighted avg(가중평균)     0.88       0.88      0.88       100

# Precision : 예측한 것 중 맞힌 비율 (예측의 정확성)
# Recall    : 실제 정답 중 찾아낸 비율 (정답 탐지 능력)
# F1-score  : Precision과 Recall의 조화평균
# Support   : 실제 클래스별 데이터 개수
# Accuracy  : 전체 데이터 중 올바르게 분류한 비율
# Macro avg : 클래스별 성능의 단순평균
# Weighted avg : 클래스별 데이터 개수를 고려한 가중평균

# 표(Classification Report) 해석 ->  
# precision :  모델이 0으로 예측한 것 중 85%가 실제로 0이다.
# recall : 실제 0인 값, 48개 중 92%를 제대로 찾았다.


# ROC커브 그리기(AUC보기)
fpr, tpr, thresholds = metrics.roc_curve(y, model.decision_function(x))
# thresholds : 분류 결정 임계값(결정수값)

plt.plot(fpr, tpr, 'o-', label='LogisticRegression')
plt.plot([0,1], [0,1], 'k--', label='landom classifier line(AUC:0.5)')
plt.plot([fallout], [recall], 'ro', ms=6) # 위양성률, 재현율 출력
plt.xlabel('fpr(위양성률 = fallout)')
plt.ylabel('tpr(재현율 = recall)')
plt.title('ROC Curve')
plt.legend()
plt.show()

print('AUC(Area Under the Curve) : ROC커브의 밑면적으로 1에 근사할 수록 좋은 모델이다')
print('AUC : ', metrics.auc(fpr,tpr))
# AUC :  0.9547275641025641