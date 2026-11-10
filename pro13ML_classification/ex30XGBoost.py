# ensemble : 여러모델의 예측을 합쳐 성능을 높이는 방법. 종류 -> bagging / boosting
# - bagging : DecisionTree를 합친 RandomForest
# - boosting : XGBoost

# Bagging : 여러 모델을 독립적으로 학습하여 결과를 합친다. 학습데이터는 원본에서 중복을 허용하여 추출한 데이터를 각각 학습한다.
#           즉, 동일한 샘플에서 여러 번 뽑아(Bootstrap) 각 모델을 학습시켜 결과물을 집계하는 방법으로 모든 DecisionTree에 서로 다른 sampleData를 주어주는 것

# Boosting : 약한 분류기에 대해서 sample의 일부를 보완해가면서 순차적으로 학습하여 강한 분류기를 만든다.
#            앞선 모델의 부족한 부분을 다음 모델이 보완하는 방식으로 학습데이터는 동일한 데이터에서 출발한다. 
#            학습데이터에서 1번 모델이 학습을 하고 오차에 따라 가중치나 학습목표를 조정하여 다시 학습데이터를 이어서 받는다.

# 이번시간에는 Boosting에 대해서 학습한다.

# XGBoost : Boosting 알고리즘을 구현한 분류/예측모델이다.

# 실습) 유방암 데이터셋 : 종양의 측정값으로 악성인지 양성인지 분류하는 데이터 셋으로 총 569개 sample이 있다. 
# x : 예측에 사용하는 종양의 측정값 30개(반지름, 질감, 둘레, 면적 ...)
# y : 종양의 악성 여부(0과 1)

# [1단계] : 데이터 불러오기 및 변수설정
# 1-1. lib불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_breast_cancer  #  ->  유방암 데이터셋 사용
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
# pip install xgboost, lightgbm설치를 해야 xgboost를 사용할 수 있다. 
import xgboost as xgb
from lightgbm import LGBMClassifier # lightgbm은 xgboost보다 성능은 우수하나 자료가 적으면 과적합이 발생한다. 
import lightgbm as lgb

pd.set_option('display.max_columns', None)

# 1-2. 데이터 불러오기
data = load_breast_cancer()
print(data.feature_names)

# 1-3. 변수설정
# 독립변수(x)들의 종류 : ['mean radius' 'mean texture' 'mean perimeter' 'mean area' 'mean smoothness' 'mean compactness' 'mean concavity' 'mean concave points' 'mean symmetry' 'mean fractal dimension' 'radius error' 'texture error' 'perimeter error' 'area error' 'smoothness error' 'compactness error' 'concavity error' 'concave points error' 'symmetry error' 'fractal dimension error' 'worst radius' 'worst texture' 'worst perimeter' 'worst area' 'worst smoothness' 'worst compactness' 'worst concavity' 'worst concave points' 'worst symmetry' 'worst fractal dimension']
x = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target
print(x[:3], x.shape)
print(y[:3])
# 결과 : 
# (569, 30) : -> 569행 30열 짜리 데이터
# [0 0 0]   : -> 첫 3행의 데이터는 모두 양성이다.

print()
print("label분포 : ", {name:(y == i).sum() for i, name in enumerate(data.target_names)})
# 결과 : 
# label분포 :  {np.str_('malignant'): np.int64(212), np.str_('benign'): np.int64(357)}
# malignant(악성) : 212명(37%)
# benign(양성)    : 357명(63%)
# "label분포가 불균등하다!!" ... 후에 '과적합'이 발생할 수 있기에 train / test split을 해준다.
# 정답 클래스의 분포가 불균형하면 모델이 다수 클래스에 치우쳐 소수 클래스를 잘 예측하지 못할 수 있다.

# 1-4. 데이터 전처리(train/test split)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y)
# label분포가 불균등할 때 stratify=y를 써준다.
# 현재 레이블 분포가 악성 37%, 양성 63% 데이터인데 이 비율 그대로 2:8로 train : test를 나누게 되면 똑같이 y_train과 y_test데이터에서도 불균등한 정답클래스 분포를 이루게 된다. 이런 불균등한 비율을 맞추기 위해서 stratify=y를 써주었다.
# 즉, 
# train : test  = 80% : 20%  → test_size=0.2
# label데이터(y)의 비율  ->   악성 : 양성  =  37% : 63%  →  stratify=y로 각 세트 안에서 유지 : y_train도 37%:63%의 악성:양성을 이루고 y_test도 동일한 비율을 따르게 된다.
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
# 결과 : (455, 30) (114, 30) (455,) (114,)
# 즉, 전체 569개의 데이터를 train용 455개, test용 114개로 나누었다.(2:8)
# 독립변수가 30개 


# enesemble - bagging   - :  RandomForest
#           - boosting  - : XGBoost   ->  XGBClassifier
#                       - : LightGBM  ->  LGBMClassifier

# [2단계] : 모델 생성 및 학습
# 2-1. 모델1 : XGBoost
xgb_clf = xgb.XGBClassifier(
    booster='gbtree', # gbtree : tree기반(분류), 'gblinear' : 선형모델
    max_depth = 6, # 개별 DecisionTree 깊이
    n_estimator=200,
    eval_metric='logloss',
    random_state = 42
)
xgb_clf.fit(x_train, y_train)

# 2-2. 모델2 : LightGBM
lgb_clf = LGBMClassifier(
    n_estimators=200, random_state=42, verbose = -1, # 로그 숨기기
)
lgb_clf.fit(x_train, y_train)


# [3단계] : 예측 및 평가
# 두 모델에 대한 예측 평가
pred_xgb = xgb_clf.predict(x_test)
pred_lgb = lgb_clf.predict(x_test)
print(f'XGBClassifier acc : {accuracy_score(y_test, pred_xgb):.5f}')
print(f'LGBMClassifier acc : {accuracy_score(y_test, pred_lgb):.5f}')
print()


# [4단계] : feature 기여도 확인
# 독립변수들의 중요도 평가 : gain기준으로 통일
# gain : 모델이 독립변수를 기준으로 데이터를 나눴을 때 얻는 개선 정도
#        각 독립변수가 악성과 양성을 예측하는데 얼마나 도움이 됐는지를 gain을 기준으로 보는 것이다.
#        gain을 점수로 사용해서 독립변수의 중요도를 평가하는 것이다.

booster = xgb_clf.get_booster()
xgb_gain = pd.Series(booster.get_score(importance_type='gain'))
lgb_gain = pd.Series(lgb_clf.booster_.feature_importance(importance_type='gain'), 
                    index=x_train.columns # 숫자 배열을 반환하는 대신에 실제 칼럼을 반환해준다.
                    )
# 두 모델의 독립변수의 중요도를 표현하는 방법이 약간 다르다.
# 두 모델 모두 gain중요도를 기준으로 독립변수가 얼마나 영향을 미치는 지 보여준다.
print(xgb_gain)
print(lgb_gain)

# xgb_gain / xgb_gain.sum() : 각 feature의 기여도를 '비율'로 확인
# 만약 모든 중요도가 0인 경우, 0으로 나누는 오류를 방지할 수 있다. 0인 경우 1로 나누게 한다.
xgb_gain_pct = 100 * xgb_gain / (xgb_gain.sum() if xgb_gain.sum() != 0 else 1)
lgb_gain_pct = 100 * lgb_gain / (lgb_gain.sum() if lgb_gain.sum() != 0 else 1)
print(xgb_gain_pct)
print(lgb_gain_pct)
# 중요도를 비율로 나오게 된다. 이를 DataFrame으로 표현해보자.
# 사용되지 않은 feature는 0으로 채운다.
xgb_gain_pct = xgb_gain_pct.reindex(x_train.columns).fillna(0)
lgb_gain_pct = lgb_gain_pct.reindex(x_train.columns).fillna(0)

comp_df = pd.DataFrame({
    "XGBoost(gain %)" : xgb_gain_pct,
    "LightGBM(gain %)" : lgb_gain_pct
}).sort_values('XGBoost(gain %)', ascending=False)
print(comp_df.head(10))
# 이제 label데이터에 영향을 강하게 미치는 변수들 top10을 볼 수 있다.
# 결과 : 
#                          XGBoost(gain %)  LightGBM(gain %)
# worst perimeter                33.383032          2.445518
# worst concave points           29.409127         45.738001
# mean concave points            17.776577         17.430096
# worst area                      5.107299         18.552560
# mean area                       1.908297          0.772640
# mean radius                     1.749777          0.035359
# mean texture                    1.295090          1.402214
# fractal dimension error         1.259095          0.082650
# area error                      0.928325          3.061371
# radius error                    0.873514          0.402968

# 시각화
topk = 5
top = comp_df.head(topk)[::-1]
fig, axes = plt.subplots(1, 2, figsize=(8, 5))
xmax = float(np.ceil(top.max().max())) # 열별 최대값 중 최댓값: 두 모델에 공통으로 사용할 축 범위

for ax, col in zip(axes, ['XGBoost(gain %)','LightGBM(gain %)']):
    ax.barh(top.index, top[col])
    ax.set_title(f'{col.split()[0]} Feature importance')
    ax.set_xlabel('importance (%)')
    ax.set_xlim(0, xmax)

plt.tight_layout()
plt.show()
