# Decision Tree이용 - 다항분류(softmax함수 사용) - iris dataset으로 실습 ... 이항분류가 기본이지만 다항분류도 해보자
# iris데이터는 0,1,2로 다항 함수 처리의 예시로 사용하기 좋다.
# 2개(이항분류)로 분류 할때는      ->  "sigmoid"
# 3개 이상(다항분류)을 분류할 때는 ->  "softmax"
# 를 사용한다.

# softmax함수 : 인공지능의 다중 클래스 분류(Multi-claa-Classification)문제에서 출력층에 주로 사용된다.
#              인공신경망에서 확률값을 얻기 위해 마지막 층에 사용되는 함수.
#              확률값이 가장 높은 녀석을 찾는다.

# [1단계] : 데이터 불러오기 및 변수 설정
# 1. Lib불러오기
import numpy as np
import pandas as pd

# Regression에 사용되는 Lib(범용)
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, MinMaxScaler # 표준화와 정규화
# 표준화와 정규화
# : 표준화 : 데이터들의 평균을 '0', 표준편차를 '1'로 만드는 방식
# : 정규화 : '0~1'사이의 수치값으로 바꾸는 방식

# Classification에 사용되는 Lib(범용)
from sklearn.linear_model import LogisticRegression
# LogisticRegression : 이항분류 뿐 아니라 다항분류(다중클래스)를 지원하고 있다.

iris = datasets.load_iris()
print(iris.keys())
# 결과 : 
# dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])

print("iris.target : ", iris.target)
# 결과 : 
# [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2
#  2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
#  2 2]

print(iris.data[:3])
# 결과 :
# [[5.1 3.5 1.4 0.2]
#  [4.9 3.  1.4 0.2]
#  [4.7 3.2 1.3 0.2]]

print(np.corrcoef(iris.data[:2], iris.data[:3])[0, 1])
# 결과 : 0.977

# 2. 변수 설정
x = iris.data[:, [2, 3]]  # 꽃잎 length, width
y = iris.target # 꽃 종류 : 0, 1, 2
print(x.shape, y.shape)
# (150, 2) (150,)
print(x[:3], y[:3], set(map(int, y)))
# {0, 1, 2}

# 3. 과적합 문제 방지 : train / test split()
print('\n train / test split (7:3)')
# train / test split : 이미 확보한 데이터 전체를 무작위로 나눠서 train용과 test용으로 구분하는 것. 새로운 데이터를 만들어내는 건 아니다.
# 모델이 처음 보는 데이터도 잘 예측하는지 확인하려고
# 모델은 800개로만 학습하고, 남겨둔 200개로 평가
# 모델이 학습할 때 보지 않은 데이터
# 이미 전체 1,000개로 학습했다면, 그중 200개를 나중에 test로 골라도 제대로 된 평가가 안 돼. 모델이 이미 봤기 때문이다. 이 경우에는 데이터를 먼저 나눈 뒤 모델을 새로 학습하거나, 별도로 수집한 새 데이터로 평가해야 한다.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=0)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
print(x_train[:3], x_test[:3], y_train[:3], y_test[:3])
# model.fit(x_train, y_train) : 학습용 데이터로 학습
# model.score(x_test, y_test) : 학습할때 보지 않은 평가용 데이터로 추후에 평가 시 사용
# 결과 :
# x_train[:3] = 
# [[3.5 1. ]
#  [5.5 1.8]
#  [5.7 2.5]] 

# x_test[:3] = 
# [[5.1 2.4]
#  [4.  1. ]
#  [1.4 0.2]] 

# y_train[:3] = 
# [1 2 2] 

# y_test[:3] = 
# [2 1 0]
print()

# Scaling - 데이터 크기 표준화/정규화 
# : 최적화 과정에서 안정성, 수렴속도 향상, 과적합/과소적합 방지 등의 효과가 있다. = 변수들의 값 크기를 일정한 기준으로 맞춰 최적화의 안정성과 수렴 속도를 높인다.


# <Overfitting 해결방법>
# 1. train / test split
# 2. k fold 
# 3. GridSearchCV
# 4. L1, L2규제

'''
# 표준화 :
print("표준화")
sc = StandardScaler()
sc.fit(x_train)
sc.fit(x_test)
# 주의 : feature(독립변수(x))만 스케일링한다.
# 스케일링 기준은 train으로만 구하고, 같은 기준을 test에 적용해야 한다.

x_train = sc.transform(x_train)
x_test = sc.transform(x_test)
print(x_train[:3])
print(x_test[:3])

# 스케일링 원복 : 원래 데이터로 돌아간다.
origin_x_train = sc.inverse_transform(x_train)
print("원복한 초기 데이터 : ", origin_x_train[:3])
print()
'''


# [2단계] : 모델 생성 및 학습
from sklearn.tree import DecisionTreeClassifier
# 1. 모델 생성
model = DecisionTreeClassifier(criterion = 'entropy', max_depth = 5, random_state =0 )
print(model)

# 2. 모델 학습-train용 데이터
model.fit(x_train, y_train)
# train으로 학습하는 것

# [3단계] : 예측 및 평가
# 1. 모델 예측
# 분류(Classification)결과를 예측
y_pred = model.predict(x_test) # x_test로 예측
print('예측값 : ', y_pred)
print("실제값 : ", y_test)

# 2. 모델 성능 확인
print(f"총 갯수 : {len(y_test)}, 오류수 : {(y_test != y_pred).sum()}")
# 총 갯수 : 45개
# 오류 : 1개
print(f"분류 정확도 : {accuracy_score(y_test, y_pred)}") # 0.97777
conf_mat = confusion_matrix(y_test, y_pred)
print("혼동행렬 : \n", conf_mat)
# 결과 : 
#       [ [16  0  0]
#         [ 0 17  1]
#         [ 0  0 11] ]
# print("분류 정확도 : ", (conf_mat[0][0] + conf_mat[1][1]) / len(y_test))
# 현재 3개라서 저 수식으로는 구할 수 없다.
# 그래서
print("분류정확도 : \n", np.trace(conf_mat) / np.sum(conf_mat)) # 이렇게 적어준다.
# 결과 :  0.9777777777777777

print(f"train score : {model.score(x_train, y_train)}") # 0.9714285
print(f"test score : {model.score(x_test, y_test)}")    # 0.97777
# train score와 test score의 차이가 크면 과적합을 의심해보아야 한다.
# --------------------------------------------------------------------------------------------------------------------------

# 모델이 학습이 끝난 후 검증이 끝난 모델을 저장한 후 읽기
import joblib

# 1. 모델 저장
joblib.dump(model, 'ex20model.sav') # 혹은 .sav대신 .model을 대신 쓸 수 있다.
# 이제 동일한 수준의 경로에 ex20model.sav로 방금 만든 model을 저장하였다.

# 2. 모델 읽어오기
read_model = joblib.load('ex20model.sav')
print(read_model)
# 결과 : LogisticRegression(C=1, random_state=0)
# 모델을 생성하여 불러왔다.

print("새 값으로 예측하기 ---------------")
new_data = np.array([[5.5, 2.2]])

# 주의 : 만약 앞서 표준화를 시켜서 적용했다면 출력값도 표준화된 형태로 나타난다. 
#        그래서 다시 원래 데이터와 동일한 형태를 원한다면 다시 원복을 시켜주어야 한다.
# 만약 이전에 표준화를 하여서 다시 원복을 해야한다면..
'''
sc = StandardScaler()
sc.fit(new_data)
new_data = sc.transform(new_data) 
'''
# 이 과정을 해주어서 다시 데이터를 원래대로 만들어주면 된다. 하지만 우리는 표준화를 하지 않았기 때문에 원복을 할 필요도 없다.
new_pred = read_model.predict(new_data)
print("예측결과의 확률값(sigmoid) : ", read_model.predict_proba(new_data))
print("확률값의 가장 큰 인덱스 번호 : ", new_pred)

# 결과 : 
# 예측결과의 확률값(sigmoid) : [[2.53496435e-05  5.43511967e-02   9.45623454e-01]]  ->  분류할 붓꽃 품종이 3개라서 확률도 3개가 나온다. 
# setosa일 확률: 약 0.0025%
# versicolor일 확률: 약 5.44%
# virginica일 확률: 약 94.56%
# 꽃 3개를 예측한 게 아니라, 꽃 1개가 세 품종 각각에 속할 확률을 구한 것

# 예측결과 :  [2]  ... 예측결과의 확률값 중 가장 큰 값이 몇번째있는가?
# 하지만 setosa,  virgnia, virgnica 이 품종 중 virginica로 예측했다는 뜻은 아니다.
# 확률:  [0.000025, 0.05435, 0.94562]
# 인덱스:    0         1        2
# # softmax는 결과값을 확률값으로 반환한다.


# 시각화  ->  iris데이터로 예제를 들 때 이 시각화는 자주 사용한다!!
import matplotlib.pyplot as plt

import koreanize_matplotlib
from matplotlib.colors import ListedColormap

def plot_decision_regionFunc(X, y, classifier, test_idx=None, resolution=0.02, title=''):
    markers = ('s', 'x', 'o', '^', 'v')      # 마커 표시 모양 5개 정의
    colors = ('r', 'b', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    #print('cmap : ', cmap.colors[0], cmap.colors[1], cmap.colors[2])

    # decision surface 그리기
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    xx, yy = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    # xx, yy를 ravel()를 이용해 1차원 배열로 만든 후 전치행렬로 변환하여 퍼셉트론 분류기의 
    # predict()의 인자로 입력하여 계산된 예측값을 Z로 둔다.
    Z = classifier.predict(np.array([xx.ravel(), yy.ravel()]).T)
    Z = Z.reshape(xx.shape)   # Z를 reshape()을 이용해 원래 배열 모양으로 복원한다.

    # X를 xx, yy가 축인 그래프 상에 cmap을 이용해 등고선을 그림
    plt.contourf(xx, yy, Z, alpha=0.5, cmap=cmap)   
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    X_test = X[test_idx, :]
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], color=cmap(idx), marker=markers[idx], label=cl)

    if test_idx:
        X_test = X[test_idx, :]
        plt.scatter(X_test[:, 0], X_test[:, 1], c=[], linewidth=1, marker='o', s=80, label='testset')

    plt.xlabel('꽃잎 길이')
    plt.ylabel('꽃잎 너비')
    plt.legend(loc=2)
    plt.title(title)
    plt.show()

x_combined_std = np.vstack((x_train, x_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regionFunc(X=x_combined_std, y=y_combined, classifier=read_model, test_idx=range(105, 150), title='scikit-learn제공') 


# Logistic Regression : 오즈비에 log함수를 적용한 것으로 로짓을 대상으로 회귀분석을 한 것
# [1단계] : 독립변수에 학습된 가중치와 절편을 적용하여 z = wx + b를 계산한다.
# [2단계] : 'wx + b'를 승산비(odds ration)로 감싼다.
# [3단계] : 그리고 승산비로 감싼 값을 로그(log)변환해준다.
# [4단계] : 이 값은 확률 자체가 아니라 로그 오즈(logit)값으로 -무한대 ~ +무한대까지의 '실수' 범위르 가진다.
# [5단계] : 이후 sigmoid 함수를 적용하여 0~1사이의 '확률'을 구하고, 0.5를 기준으로 클래스를 분류한다.
# [6단계] : 그래프로 시각화를 하게 되면 sigmoid함수에 의해 여러 개의 s자 선이 나타난다. 그 중에서 어떤 s선을 사용할지 판단하기 위해서 가능성(우도)를 사용한다.
#           - 모델의 학습과 통계적 적합도 평가 : 가능성(우도)
#           - 분류 성능 평가 : Acccuracy, Precision, Recall, F1-score, ROC-AUC
# 이제부터 분류성능 평가에 대해서 얘기해보자.

# 분류 성능 평가에는 ... 분류성능평가지도
# - 정확도(Accuracy) : 전체 데이터에서 모델이 옳게 판단한 비율 
#                    -> 수식 :  (TP + TN) / (TP + FN + FP + TN)
# - 정밀도(Precision) : 양성 가운데 맞춘 양성의 수 
#                    -> 수식: TP / (TP + FP)
# - 특이도(Specificity) : 음성 가운데 맞춘 음성의 수 
#                    -> 수식: TN / (TN + FP)
# - 민감도(Sensitivity=Recall) : 실제양성을 양성으로, 음성을, 음성으로 판단한 비율 
#                    -> 수식: TP / (TP + FN)
# - 성능점수(F1 Score) : 정밀도와 민감도의 조화 평균
#                    -> 수식: 2 * 정밀도 * 민감도 / (정밀도 + 민감도)
# 이들은 모두 오차 행렬에 기반해서 만들어진다.

# 오차행렬 표 해석 :
#                                     <예측>
#                         Positive             Negative
#   <실제>  -   참       "TP(참 양성)"      "FP(거짓 음성)"
#           - 거짓      "FP(거짓 양성)"      "TP(참 음성)"
# 정밀도와 민감도는 trade-off 관계이다.

# ROC커브 y축의 1.0에 가까이 가면 더 가까이 갈수록 더 좋은 모델이다. = 죽 면적이 넓어야 좋은 모델이다.
# 

# 분류 성능 평가를 할때 오차행렬을 통해서 분류 정확도만 보는게 아니라 저 5가지 중 precision과 Recall까지 분석한다.
# 그리고 나서 ROC커브를 생성한다.