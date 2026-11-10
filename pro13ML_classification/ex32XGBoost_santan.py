# 실습) 산탄데르 은행 관련 데이터로 고객만족 여부를 분류한다.
# label(class, y)명은 target이다.
# 0 : 만족
# 1 : 불만족


# [1단계] : 데이터 불러오기 및 변수설정
# 1-1. lib불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score

from xgboost import XGBClassifier
from xgboost import plot_importance

# 1-2. 데이터 불러오기
df = pd.read_csv('train_bank.csv', encoding = 'latin-1')
print(df.head(2))
# 결과 : 
#   "ID"  var3  var15  imp_ent_var16_ult1 ...  saldo_medio_var44_ult1  saldo_medio_var44_ult3     var38  "TARGET"
# 0   1     2     23                 0.0  ...                     0.0                     0.0  39205.17       0
# 1   3     2     34                 0.0  ...                     0.0                     0.0  49278.03       0
print(df.shape)
print(df.info())
# 결과 :
# [2 rows x 371 columns]
# (76020, 371)
# 79020행, 371열 짜리 대용량 데이터이다.

# 1-3. 전체 데이터에서 '만족(1)'과 '불만족(0)'의 비율 = label데이터의 비율 확인
print(df['TARGET'].value_counts())
unsatisfied_cnt = df[df["TARGET"]== 1].TARGET.count() # total열의 1인 행의 수
total_cnt = df['TARGET'].count() # total열의 모든 행의 수
# 데이터의 맨 마지막 열("TARGET")에 '0'과 '1'로 만족과 불만족이 구분되어 있다.
print(f"불만족의 비율은 {unsatisfied_cnt / total_cnt}")
# 결과 : 불만족의 비율은 0.0395685345961589 = 약 4%정도
pd.set_option('display.max_columns', None) # 해당 데이터의 열의 일부가 생략되어 있을 때 전부 보고 싶으면 이 코드를 써준다.
print(df.describe())
# 모든 열에 대한 통계량 정보가 나온다.
print(df['var3'].describe())
# 결과 : 
#              TARGET  
# count    76020.000000  
# mean         0.039569  
# std          0.194945  
# min          0.000000  
# 25%          0.000000  
# 50%          0.000000  
# 75%          0.000000  
# max          1.000000  
# count    76020.000000
# mean     -1523.199277
# std      39033.462364
# min   "-999999.000000" -> 이상치이다. 그래서 이를 현재 중앙값으로 대체해준다.
# 25%          2.000000
# 50%          2.000000
# 75%          2.000000
# max        238.000000
df['var3'] = df['var3'].replace(-999999, 2)
# 중앙값으로 대체 해줌
print(df['var3'].describe())
df.drop('ID', axis=1, inplace=True) 
# ID는 식별자이므로 제거
print(df.describe())
# ID 열은 제거하였고 var3열에서는 이상치 값을 제거해주었다.
# 남은 행과 열을 보자.
print(df.shape)

# 1-4. 변수설정 
x_features = df.iloc[:, :-1] # 마지막 열("TARGET") 빼고 모든 열에 대한 모든 행
y_label = df.iloc[:, -1] # 마지막 열("TARGET")의 모든 행

# 1-5. 과적합방지-train / test split()
x_train, x_test, y_train, y_test = train_test_split(
    x_features, y_label, test_size=0.3, random_state=42, stratify=y_label
) 
# "train : test" 데이터의 비율을 "7 : 3"으로 설정하였고, 현재 label분포가 균등하지 않은데 이러한 불균등이
# train과 test데이터에도 똑같이 나타나도록 함.
print(x_train.shape, x_test.shape)
train_cnt = y_train.count()
test_cnt = y_test.count()
print('train용 데이터 label값 분포 비율 : ', y_train.value_counts() / train_cnt)
print('test용 데이터 label값 분포 비율 : ', y_test.value_counts() / test_cnt)
# train용 데이터에 대해서 label값의 분포(0과1의 비율)가  0 -> 0.9604241  :  1 -> 0.039576 이다.
# test용 데이터에 대해서 label값의 분포(0과1의 비율)가   0 ->  0.960449  :  1 -> 0.039551 이다.
# label클래스 불균형이 심하다.(96% : 4%) ... -> roc_auc_score()가 효과적이다.

# train/test split의 stratify=y와 roc_auc_score는 모두 label클래스의 불균형을 해결해주는 것이 아니라 
# 각각의 비율을 유지하면서 성능을 평가하도록 하는 기능이다!!
print()


# [2단계] : 모델 생성 및 학습
xgb_clf = XGBClassifier(n_estimators = 100, random_state = 12, eval_metric = 'auc')
xgb_clf.fit(x_train, y_train, eval_set=[(x_test, y_test)], verbose=True)
# eval_set은 학습진행 중 사용되는 성능평가용 매개변수이다. train과 동시에 test를 진행한다 
# 학습은 x_train, y_train으로 하고 학습도중 검증은 x_test, y_test로 성능 확인이 가능하다. 
# [0]     validation_0-auc:0.82589
# [1]     validation_0-auc:0.83577
# [2]     validation_0-auc:0.83721
# [3]     validation_0-auc:0.83787
# ...
# [97]    validation_0-auc:0.82860
# [98]    validation_0-auc:0.82826
# [99]    validation_0-auc:0.82811
# validation_0  :  eval_set에 넣은 첫 번째 평가 데이터
# auc 수치 : 실제 1인 데이터에 실제 0인 데이터보다 높은 예측 점수를 주는 것
# ex) auc = 0.83 : 불만족 고객과 만족 고객을 한 명씩 뽑아 비교했을 때 약 83%의 경우에 불만족 고객에게 더 높은 불만족할 확률을 주었다는 뜻
#                  얼마나 잘 맞추었냐를 판단


# [3단계] : 예측 및 평가
# 분류 성능 평가 -> roc_auc / accuracy / recall / precision 중 roc_auc와 accuracy를 보자.

# 분류성능평가 방법1. roc_auc
xgb_roc_score = roc_auc_score(y_test, xgb_clf.predict_proba(x_test)[:, 1])
# predict_proba(x_test)  :  고객별로 두 클래스(0과1)의 예측 확률을 반환
print(f"분류 정확도 평가1(xgb_roc_score) : {xgb_roc_score:.5f}")
# 결과 : xgb_roc_score : 0.82811

# ** ROC와 AUC 정리 **
# 모델은 고객의 불만족(1) 확률을 예측하고, 기준값(ex) 0.5) 이상이면 '불만족'으로 분류한다.
# 예) 기준값이 0.5이면 불만족 확률이 0.5 이상인 고객을 불만족(1)으로 판단한다.
# 기준값을 높이면 실제 불만족 고객을 놓치기 쉽고,
# 기준값을 낮추면 불만족 고객을 더 많이 찾지만 만족 고객도 불만족으로 잘못 판단하기 쉽다.
#
# 1. ROC(Receiver Operating Characteristic) 곡선
# 여러 기준값에 따른 FPR과 TPR을 연결한 그래프이다.
# - 가로축 FPR: 실제 만족(0) 고객 중 불만족(1)으로 잘못 판단한 비율
# - 세로축 TPR: 실제 불만족(1) 고객 중 불만족(1)으로 올바르게 찾은 비율(재현율)
# 왼쪽 위에 가까울수록 오분류는 적고 실제 불만족 고객은 많이 찾는 좋은 모델이다.
#
# 2. AUC(Area Under the ROC Curve)
# ROC 곡선 아래의 면적으로, 여러 기준값에 걸친 모델의 "구별 능력"을 "숫자"로 요약한다.
# - AUC = 1.0: 만족과 불만족을 완벽하게 구별한다.
# - AUC = 0.5: 무작위 수준의 구별 능력이다.
# AUC가 약 0.828이면 무작위로 뽑은 '불만족고객'과 '만족고객' 한 쌍에서,
# 불만족 고객에게 더 높은 불만족 확률을 주는 비율이 약 82.8%라는 뜻이다.
# (두 고객의 예측 확률이 같으면 0.5회 정답으로 계산한다.)
# 전체 고객의 82.8%를 맞혔다는 정확도(accuracy)와는 다른 지표이다.
#
# 3. 위 코드의 의미
# predict_proba(x_test)  :  각 고객의 [만족(0) 확률, 불만족(1) 확률]을 반환한다.
# [:, 1]  :  모든 고객의 불만족(1) 확률만 선택한다.
# roc_auc_score(y_test, ...)  :  실제 정답과 불만족 예측 확률로 ROC AUC를 계산한다.

# 성능평가 방법2. accuracy_score
pred = xgb_clf.predict(x_test)
print('예측값 : ', pred[:5])
print('실제값 : ', y_test[:5].values)
print('분류 정확도 평가2(accuracy_score) : ', accuracy_score(y_test, pred))
# 결과 : 분류 정확도 평가(accuracy_score) :  0.9599228273261422
# roc_auc : 만족과 불만족을 얼마나 잘 구분하는가?
# accuracy : 전체 고객 중 얼마나 맞혔는가?
# recall : 실제 불만족 고객을 얼마나 찾아냈는가?
# precision : 불만족이라고 예측한 고객 중 실제 불만족한 비율은?
# 불만족 고객을 놓치지 않는 것이 중요하다면 recall도 살펴보는 것을 권장한다. 
print()
print("-----------------------------------------------------------------------------")

# GridSearchCV로 최적의 파라미터 찾기
# Overfitting방지
# 1. trian/test split
# 2. Kfold
# 3. GridSearchCV

# 이번에는 XGBoost에서 GridSearchCV를 사용해서 Overfitting을 방지해보자.
print('\n GridSearchCV로 최적의 파라미터 찾기')
xgb_clf2 = XGBClassifier(n_estimators = 10)
# max_depth : tree깊이, 
# min_child_weight : 관측치, 가중치합 최소, 
# colsample_bytree : 피처 비율
params = {
    'max_depth' : [5, 7],
    'min_child_weight': [1, 3], 
    'colsample_bytree' : [0.5, 0.75]
}
# GridSearchCV가 사용하는 params는 굉장히 많다.
gridcv = GridSearchCV(xgb_clf2, param_grid=params)
gridcv.fit(x_train, y_train, eval_set=[(x_test, y_test)], verbose = False)
print('gridcv 최적 파라미터 : ', gridcv.best_params_)
# 결과 : gridcv 최적 파라미터 :  {'colsample_bytree': 0.5, 'max_depth': 5, 'min_child_weight': 1}

# GridSearchCV를 사용해서 최적의 파라미터를 선정하는 이유 : 
# 파라미터에 따라 모델의 복잡도가 달라지고, 복잡도가 과적합에 영향을 주기 때문이다.
# 예를 들어 max_depth는 트리의 최대 깊이이다. 너무 깊으면 학습 데이터의 세세한 특징과 잡음까지 외워서 과적합될 수 있고 
# 너무 얕으면 중요한 패턴도 배우지 못해서 과소적합될 수 있다.
# 따라서 새로운 데이터에서도 잘 예측하는 깊이를 찾도록 하는 파라미터를 정하는 모델을 만들기 위해서
# 파라미터를 최적으로 찾아주는 GridSearchCV를 사용한다.
# GridSearchCV로 최적의 파라미터를 찾고 해당 최적의 파라미터를 model에 넣어서 사용한다.
print()

# 모델 생성 및 학습
best_clf = XGBClassifier(n_estimators = 10, random_state = 12, colsample_bytree = 0.75, max_depth = 5, min_child_weight = 1)
best_clf.fit(x_train, y_train)

# 모델 예측 및 분류 정확도 평가
# 분류 정확도 평가 방법1 : roc_auc
xgb_roc_score2 = roc_auc_score(y_test, best_clf.predict_proba(x_test)[:, 1])
print(f'분류 정확도 평가1(xgb_roc_score2) : {xgb_roc_score2:.5f}')
# 결과 : 분류 정확도 평가1(xgb_roc_score2) : 0.84206

# 분류 정확도 평가 방법2 : accuracy_score
pred2 = best_clf.predict(x_test)
print('예측값 : ', pred2[:5])
print('실제값 : ', y_test[:5].values)
print('분류 정확도 평가2(accuracy_score) : ', accuracy_score(y_test, pred2))
# 분류 정확도 평가(accuracy_score) :  0.9602297640971674

# label분포가 균등하면 accuracy_score만 확인해도 되지만.
# label분포가 불균등할 때 분류정확도를 확인할 때 roc_auc_score를 함께 출력해서 확인한다.  

# accuracy_score ->  "전체 고객 중 얼마나 맞혔나?"
# roc_auc_score  ->  "불만족 고객에게 더 높은 불만족 점수를 주었나?"
# recall         ->  "실제 불만족 고객을 얼마나 찾아냈나?"
# precision      ->  "불만족이라고 예측한 고객이 얼마나 실제로 불만족인가?"

# label분포가 불균등일수록 분류 정확도가 accuracy_score하나만으로 판단하기 힘들다!! 