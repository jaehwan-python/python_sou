# Overfitting(과적합) 방지 수단
# 1. train / test split : 일반화 성능 향상
# 2. K-Fold : 안정적인 모델 평가가 가능
# 3. Grid-Search-CV : 최적의 하이퍼파라미터 검색 가능

# iris dataset을 이용할 것이다.

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
print(iris.keys())

# 과적합 예방 : train / test split
train_data = iris.data
train_label = iris.target
print(train_data[:3])
print(train_label[:3])
# train_data : 학습용 입력값 — 꽃받침 길이·너비, 꽃잎 길이·너비                       = 독립변수
# train_label : 학습용 정답 — 각 꽃의 품종 (0: setosa, 1: versicolor, 2: virginica)  = 종속변수

# 분류(Classification) 모델 생성
df_clf = DecisionTreeClassifier()
df_clf.fit(train_data, train_label)
pred = df_clf.predict(train_data)
# 학습용 데이터로 검증

print('예측값 : ', pred)
print("실제값 : ", train_label)
print("분류 정확도 : ", accuracy_score(train_label, pred))
# 결과 : 분류 정확도 :  1.0 = 100%
# 과적합이 의심된다!!

print("\n -----------------------------------------------------------------")


# [과적합 방지 방법1] : train / test split 
# : 학습데이터와 검증데이터로 나누는 방법이다. 하지만 이는 데이터가 적은 경우 유용하지 않다.
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=12
)

# 학습용 - train data로 학습!
df_clf.fit(x_train, y_train)

# 검증용 - test data로 검증!
pred2 = df_clf.predict(x_test)

print('예측값(split) : ', pred2)
print("실제값(split) : ", y_test)
print("분류 정확도(split) : ", accuracy_score(y_test, pred2))
# 결과 : 분류 정확도(split) :  0.9777777777777777  =  97%
# 어느정도 과적합이 해결되었다!!
# "최적화된 모델보다 일반화된 모델이 더 좋은 모델이다!"
print("\n -----------------------------------------------------------------")


# [과적합 방지 방법2] : K-Fold 교차 검증(K-Fold cross validation)
# : 머신러닝 모델의 일반화 성능을 객관적으로 평가하기 위해 데이터를 K개의 부분집합(Fold)으로 나누어 학습과 검증을 반복하는 방법
# Original data를 5단계로 나눈다. 
# 그리고 앞에서 첫 4개는 train용으로 쓰고 나머지 1개의 data는 test용을 사용한다. 그리고 나머지 데이터들도 똑같이 test용으로 한번씩 사용한다.

# 1단계 :    [           Original Set            ]
# 2단계 :    [ < Training >              Testing ]
# 3단계 :    [ < Training  Validation >  Testing ]
# Validation : 2단계의 Training 데이터를 다시 어느정도의 비율로 나누어서 
# Training과 Validation으로 나누고 이때 Validation은 학습과 동시에 검증한다.
# **어느정도의 비율**  ->  
# train용 데이터 : test용 데이터의 비율
# 4:1  ->  3:2  ->  2:3  ->  1:4 ... 이런식으로 반복하여 모델을 학습시킨다.

# 교차 검증(Cross Validation) : 데이터를 나누는 구성을 바꿔 가며 여러 번 학습하고 평가하는 방법
# 데이터를 한 번만 나누면, 우연히 쉬운 꽃들이 평가용으로 뽑혀 정확도가 높게 나올 수도 있다. 
# 교차 검증은 여러 번 평가해서 이런 우연의 영향을 줄인다.
# 파일에서 사용하는 5-Fold 교차 검증은 붓꽃 150송이를 30송이씩 5개 묶음으로 나눈다.

from sklearn.model_selection import KFold
import numpy as np

features = iris.data # 독립변수 지정
# [ [5.1 3.5 1.4 0.2]
#   [4.9 3.  1.4 0.2]
#   [4.7 3.2 1.3 0.2] ]

label = iris.target  # 종속변수 지정
# [0 0 0]

# 붓꽃의 일종인 setosa, versicolor, virginica이 3개의 꽃 품종에 대해서 
# 이 3개 꽃에 대한 측정값을 iris.data에 표현하고 
# 저 3가지 품종에 대해서 
# 번호 0,1,2를 매겨 표현한게 iris.target이다.
# 그때 분리된 두 numpy배열 데이터인 iris.data와 iris.target에서
# iris.data의 꽃에 대한 특징(측정값)을 독립변수(x)로 지정하여 features로 변수를 주고
# iris.target에서는 꽃의 품종 3가지(setosa, versicolor, virginica)를 출력값으로 준다.


# 모델 생성
df_clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=12)
kfold = KFold(n_splits=5)  # k:5회 접기
cv_acc = []  # 각 1회마다 정확도를 저장할 리스트
print('iris shape : ', features.shape)
# KFold 학습, 시 전체 150행이 학습데이터(4/5, 120개), 검증데이터(1/5, 30)로 분할된다.
# 그리고 이 과정이 반복된다.
print()

n_iter = 0
for train_index, test_index in kfold.split(features): # 각 구간별로 자른다
    # print('n_iter(반복수) : ', n_iter)
    # print('train_index : ', train_index)
    # print('test_index : ', test_index)
    n_iter += 1

    print()
    xtrain, xtest = features[train_index], features[test_index]
    ytrain, ytest = label[train_index], label[test_index]

    # 학습 및 예측
    df_clf.fit(xtrain, ytrain)   # train용 데이터로 학습
    pred = df_clf.predict(xtest) # 모델 생성을 위한 학습 도중 예측 - 검증 목적
    n_iter += 1

    # 반복할 때 마다 정확도 출력
    acc = np.round(accuracy_score(ytest, pred), 5)
    train_size = xtrain.shape[0]
    test_size = xtest.shape[0]
    print(f"반복수 : {n_iter}, 교차검증 정확도 : {acc}, 학습데이터의 크기 : {train_size}, 검증크기 : {test_size}, 검증 데이터의 인덱스 : {test_index}")

    cv_acc.append(acc)
    # 정확도 acc를 cv_acc(비어 있는 list)에 넣어줌
    # cv_acc : 교차검증(Cross Validation)의 정확도(accuracy)

print('cs_acc : ', np.array(cv_acc).astype(float)) 
print('평균 검증 정확도 : ', np.mean(cv_acc))
# 결과 : 
# 반복수:2, 교차검증 정확도 : 1.0, 학습데이터의 크기 : 120, 검증크기 : 30, 
#        검증(test) 데이터의 인덱스 : [ 0  1  2  3  4  56  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29]

# 반복수:4, 교차검증 정확도 : 0.96667, 학습데이터의 크기 : 120, 검증크기 : 30, 
#        검증(test) 데이터의 인덱스 : [30 31 32 33 3435 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59]

# 반복수:6, 교차검증 정확도 : 0.83333, 학습데이터의 크기 : 120, 검증크기 : 30, 
#        검증(test) 데이터의 인덱스 : [60 61 62 63 6465 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89]

# 반복수:8, 교차검증 정확도 : 0.93333, 학습데이터의 크기 : 120, 검증크기 : 30, 
#        검증(test) 데이터의 인덱스 : [ 90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119]

# 반복수:10, 교차검증 정확도 : 0.73333, 학습데이터의 크기 : 120, 검증크기 : 30, 
#        검증(test) 데이터의 인덱스 : [120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149]

# 이렇게 train용 데이터를 일정 비율(5개 단위)로 무작위로 뽑아서 검증(test)을 함께 진행한다. 그때 검증 용 데이터의 크기는 30이다. 그리고 나머지 120개는 학습용으로 쓰인다.

# ** train용으로 학습하면서 test로 검증을 동시에 한다!! **

# 결과 :
# cs_acc :  [1.      0.96667 0.83333 0.93333 0.73333]
# 평균 검증 정확도 :  0.8933320000000002 


print("\n 과적합 방지 목적 처리 2-1 : 교차 검증 단순화 '함수' 사용")
# cross_val_score를 이용해서 교차 검증(Cross Validation)을 간단히 수행
from sklearn.model_selection import cross_val_score
data = iris.data
label = iris.target

score = cross_val_score(df_clf, data, label, scoring='accuracy', cv=5)
print('교차 검증별 정확도 : ', np.round(score, 3))
print('평균 검증 정확도 : ', np.round(np.mean(score)))
print("\n -----------------------------------------------------------------")


# [과적합 방지 방법3] : Grid-Search-CV
# 과적합 방지 간접 방법
# 최적의 parameter 찾기(내부적으로 KFold를 사용해 과적합을 줄이는데 도움을 준다)

from sklearn.model_selection import GridSearchCV
# class DecisionTreeClassifier(
#  *,
#  criterion: Literal['gini', 'entropy', 'log_loss'] = "gini",
#  splitter: Literal['best', 'random'] = "best",
#  max_depth: Int | None = None,
#  min_samples_split: float = 2,
#  min_samples_leaf: float = 1,
#  min_weight_fraction_leaf: Float = 0,
#  max_features: float | Literal['auto', 'sqrt', 'log2'] | None = None,
#  random_state: Int | RandomState | None = None,
#  max_leaf_nodes: Int | None = None,
#  min_impurity_decrease: Float = 0,
#  class_weight: Mapping | str | Sequence[Mapping] | None = None,
#  ccp_alpha: float = 0
# )
# 편의상 일부 parameter만 사용. 원래는 위와 같이 길게 적어주어야 한다.
# max_depth : 노드의 최대 깊이
# min_sample_split : 노드 분할을 위한 최소한의 샘플수 (과적합 제어와 관련)

# parameter가 너무 많다. 그래서 우리는 GridSearchCV의 도움을 받는다.

parameters = {'max_depth' : [1, 2, 3], 'min_samples_split' : [2, 3]}
grid_tree = GridSearchCV(estimator=df_clf, param_grid=parameters, cv=3, refit=True)
# 원래라면 DecisionTree의 내부 parameter를 우리가 직접 일일이 지정해주어야 하지만
# GridSearchCV lib를 사용하면 내부적으로 복수 개의 모형을 생성하여, 이를 실행시켜
# 최적의 parameter를 알아서 찾아준다.
grid_tree.fit(x_train, y_train)

import pandas as pd
pd.set_option('display.max_columns', None)
# 모든 열이 나오게 보여줌
scores_df = pd.DataFrame(grid_tree.cv_results_)
# 결과를 DataFrame에 저장을 한다.
print(scores_df)

print('GridSearchCV 최적 parameter : ', grid_tree.best_params_)
print('GridSearchCV 최적 정확도 : ', grid_tree.best_score_)
# 결과 :
# GridSearchCV 최적 parameter :  {'max_depth': 3, 'min_samples_split': 2}
# GridSearchCV 최적 정확도 :  0.9238095238095237
# 추천된 parameter를 저걸({'max_depth': 3, 'min_samples_split': 2})로 가져서 DecisionTree 모델을 사용하면 92%정확도(최적화됨)를 가진 model이 생성된다

# 위에서 GridSearchCV로 추천받은 parameters로 model 생성(직접입력하여생성 or best_estimator)
bestModel = grid_tree.best_estimator_
print(bestModel)
best_pred = bestModel.predict(x_test) 
print('예측결과 : ', best_pred)
print('정확도 : ', accuracy_score(y_test, best_pred))


# 기타 과적합방지 방법 : 불필요한 변수제거, 정규화(L1, L2), 학습데이터 증가, 조기종료 ...
# 우리는 이 중 3가지에 대해서 배워 보았다.



# Regression  ->  Classification  ->  Clustering
# We are on Classification.
# On here, there are many types of Classification. One of them is Logistic Regression. 
# sort : Logistic Regression, Decision Tree, Random Forest, SVC, K-NN
# The last lesson, we have to studied about Decision Tree. There are two types of it. Gini Impurity and Entropy Impurity

# We have to study about Overfitting problem.
# To solve it, we would use to 
# 1. train / test split
# 2. K-Fold
# 3. Grid-Search-CV
