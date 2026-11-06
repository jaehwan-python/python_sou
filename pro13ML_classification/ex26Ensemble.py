# 앙상블  학습 : 여러 개의 분류기를 생성하고, 그 예측을 결합함으로써 더 정확한 예측결과를 얻음
# 강력한 하나의 모델 보다는 약한 모델 여러 개를 조합하여 더 정확한 예측결과를 도출
import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold # 불균형한 데이터가 있을때 StratifiedKFold를 사용한다.
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline 

from sklearn.ensemble import VotingClassifier # 3개의 모델을 서로 연결시켜준다 = 일체형을 관리 시킴

# 사용할 Classification Model -> 3가지
from sklearn.linear_model import LogisticRegression  # 로지스틱 회귀 모델
from sklearn.tree import DecisionTreeClassifier      # 결정나무 회귀 모델
from sklearn.neighbors import KNeighborsClassifier   # K-NN 모델

from sklearn.metrics import accuracy_score
from collections import Counter


cancer = load_breast_cancer()
print(cancer.keys())
# 결과 : 
# dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])

x, y = cancer.data, cancer.target
# x = cancer.data    # 입력: 종양의 측정값 30개
# y = cancer.target  # 정답: 0(악성), 1(양성)
print(x[:2])
print(y[:2])
# 결과(x의 0번째 행_cancer.data의 측정값 30개) : 
# [[1.799e+01 1.038e+01 1.228e+02 1.001e+03 1.184e-01 2.776e-01 3.001e-01 1.471e-01 2.419e-01 7.871e-02 1.095e+00 9.053e-01 8.589e+00 1.534e+02 6.399e-03 4.904e-02 5.373e-02 1.587e-02 3.003e-02 6.193e-03 2.538e+01 1.733e+01 1.846e+02 2.019e+03 1.622e-01 6.656e-01 7.119e-01 2.654e-01 4.601e-01 1.189e-01]

# 결과(x의 1번째 행_cancer.data의 측정값 30개) : 
#  [2.057e+01 1.777e+01 1.329e+02 1.326e+03 8.474e-02 7.864e-02 8.690e-02 7.017e-02 1.812e-01 5.667e-02 5.435e-01 7.339e-01 3.398e+00 7.408e+01 5.225e-03 1.308e-02 1.860e-02 1.340e-02 1.389e-02 3.532e-03 2.499e+01 2.341e+01 1.588e+02 1.956e+03 1.238e-01 1.866e-01 2.416e-01 1.860e-01 2.750e-01 8.902e-02]]
# 결과의 형태
#  [ [첫 번째 샘플의 측정값 30개]
#    [두 번째 샘플의 측정값 30개] ]

# 결과(y) :
# [0,1]
# 0: 악성(malignant)
# 1: 양성(benign)

print(np.unique(y))
print(cancer.target_names)
print('악성 종양 수 : ', np.sum(y==0))
print('양성 종양 수 : ', np.sum(y==1))
# 악성 종양 수 :  212
# 양성 종양 수 :  357

# 0과 1의 비율
counter = Counter(y)
total = sum(counter.values())
for cls, cnt in counter.items():
    print(f"class {cls} : {cnt}개 ({cnt / total :.2f})")
# class 0 : 212개 (0.37)
# class 1 : 357개 (0.63)
print()

# train / test split
# train -> x,y값
# test -> x,y값
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y)
# stratify=y : trian, testy 비율 유지(불균형한 데이터 모델 평가 시 왜곡 방지)

y_li = y.tolist()
ytr_li = y_train.tolist()
yte_li = y_test.tolist()
print('전체 분포 : ', Counter(y_li))
print('train 분포 : ', Counter(ytr_li))
print('test 분포 : ', Counter(yte_li))
# 전체 분포 :  Counter({1: 357, 0: 212})
# train 분포 :  Counter({1: 285, 0: 170})
# test 분포 :  Counter({1: 72, 0: 42})
print()


# 개별모델 작성
# make_pipeline : 전처리와 모델을 일체형 객체로 처리
# make_pipeline을 할때 표준화와 정규화도 해야만한다.

# 모델1 : Logistic Regression
logi = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, solver='lbfgs', random_state=42))

# 모델2 : Decision Tree ... tree계열 model은 스케일이 달라도 분할 로직에는 영향을 미치지 않는다. = 표준화/정규화가 필요없다.
tree = DecisionTreeClassifier(max_depth=5, random_state=12)
# 그래서 make_pipeline을 안해도 되기 때문에 표준화도 안해도 된다

# 모델3 : KNN 
knn= make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))

# 이제부터 이 3가지 모델을 하나로 합치자 = 앙상블 모델
votingModel = VotingClassifier(estimators = [('LR', logi), ('KNN', knn), ('DT', tree)], voting ='soft')
# estimator : “어떤 모델들의 예측을 모아 최종 판단할 것인가”를 지정하는 역할
# voting에는 hard와 soft가 있는데 우리는 soft를 사용한다.
# 세 모델이 각각 예측한 결과를 모아서 최종 결과를 정하는 것이 Voting(투표) 예측
# soft voting : 각 모델이 계산한 클래스별 확률을 평균내고, 평균 확률이 높은 클래스를 선택
# hard voting : 각 모델이 예측한 정답 번호를 다수결로 결정

# 개별 모델의 성능을 확인해보자. : 세 모델이 각각 유방암 데이터의 악성·양성을 예측했을 때, 실제 정답과 일치한 비율(정확도)
named_models = [('LR', logi), ('KNN', knn), ('DT', tree)]
for name, clf in named_models:
    clf.fit(x_train, y_train)
    pred = clf.predict(x_test)
    print(f'{name}정확도 : {accuracy_score(y_test, pred):.4f}')
# LR정확도 : 0.9912
# KNN정확도 : 0.9737
# DT정확도 : 0.8772

# 세 모델을 하나로 합침 : votingModel의 성능
votingModel.fit(x_train, y_train)
vpred = votingModel.predict(x_test)
print(f'votingModel 분류 정확도 : {accuracy_score(y_test, vpred):.4f}')
print()

# 선택적 작업 : breast_cancer 데이터가 다소 불균형을 이루므로 StratifiedKFold를 사용할 수 있다.
# "불균형" : 0과1의 비율이 한쪽으로 치우처져있음
cvfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)
cv_score = cross_val_score(votingModel, x, y, cv=cvfold, scoring='accuracy')
print(f' 보팅 5겹 cv 정확도의 평균 : {cv_score.mean():.4f} (표준편차 : +- {cv_score.std():.4f})')
# 결과 : 
# 보팅 5겹 cv 정확도의 평균 : 0.9701 (표준편차 : +- 0.0181)
print()

# ...어제한거 복습 - 모델 성능 지표
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
print('\n votingModel 상세 평가')
print(classification_report(y_test, vpred))
print('confusion_metrix : \n : ', confusion_matrix(y_test, vpred))
print('roc_auc_score : \n : ', roc_auc_score(y_test, votingModel.predict_proba(x_test)[:,1]))
# votingModel 상세 평가

# 분류 표 : 
#               precision    recall  f1-score   support
#            0       0.95      0.95      0.95        42
#            1       0.97      0.97      0.97        72
#     accuracy                           0.96       114
#    macro avg       0.96      0.96      0.96       114
# weighted avg       0.96      0.96      0.96       114

# confusion_metrix : 
#                    [ [40    2]
#                      [ 2   70] ]
# roc_auc_score : 
#                  0.994047619047619

# 랜덤포레스트는 '의사결정나무모델'을 500개 이상 연결하여 앙상블을 만든 것이다. 그때 의사결정나무모델은 sample data을 모두 다 다르게 받는다. = bagging  ->  random-forest
# 그때 앙상블의 기법(voting / bagging / boosting) 중 하나인 '배깅(bagging)'을 쓴다.
# https://bkshin.tistory.com/entry/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D-11-%EC%95%99%EC%83%81%EB%B8%94-%ED%95%99%EC%8A%B5-Ensemble-Learning-%EB%B0%B0%EA%B9%85Bagging%EA%B3%BC-%EB%B6%80%EC%8A%A4%ED%8C%85Boosting
# 위 url 배깅과 부스팅에 대한 설명 있음

# boosting : 하나의 샘플 데이터를 모든 모델이 공유받아서 Decision Tree를 받는다. 한번 처리한 후 모두가 공유하는 sample data를 조금씩 수정한다. = boosting  ->  xgboost 
# 부스팅이 성능은 좋지만 과적합에 걸릴 확률이 높아서 거의 bagging을 많이 쓴다.
# = Random Forest를 사용한다.