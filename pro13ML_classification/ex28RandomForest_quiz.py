# 예제1) RandomForest

# 중요도, 교차검증까지 해보기

# input variables (based on physicochemical tests):
#  1 - fixed acidity                      = 독립변수들
#  2 - volatile acidity
#  3 - citric acid
#  4 - residual sugar
#  5 - chlorides
#  6 - free sulfur dioxide
#  7 - total sulfur dioxide
#  8 - density
#  9 - pH
#  10 - sulphates
#  11 - alcohol

#  Output variable (based on sensory data):
#  12 - quality (score between 0 and 10)  = 종속변수
# --------------------------------------------------------------------------------------
# [1단계] 라이브러리 불러오기
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# [2단계] 데이터 불러오기 및 결측값 확인
# Kaggle 페이지는 CSV 자체가 아니므로 UCI에서 제공하는 원본 CSV를 사용한다.
# 이 파일은 쉼표가 아니라 세미콜론(;)으로 열을 구분한다.
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
df = pd.read_csv(url, sep=';')
print(df.head(2))
df.info()
print(df.shape)
print('열별 결측값 개수:\n', df.isnull().sum())
# 사용할 측정값이나 정답이 비어 있는 행을 제거한다.
df = df.dropna().copy()

# [3단계] 독립변수(feature)와 종속변수(label) 지정
# quality를 제외한 11개 측정값으로 와인의 품질 점수를 예측한다.
# 점수를 연속값으로 예측하는 회귀가 아니라, 점수별 범주를 구분하는 다중 분류이다.
df_x = df.drop(columns='quality')
df_y = df['quality']
print('품질 점수별 개수:\n', df_y.value_counts().sort_index())
# 모든 입력이 수치형이고 나무 모델이므로 LabelEncoder나 표준화는 필요 없다.

# [4단계] 학습용 데이터와 테스트용 데이터 분리
# stratify로 품질 점수별 비율을 가능한 한 유지한다.
# 테스트 데이터는 학습에 사용하지 않고 최종 성능 평가에 사용한다.
train_x, test_x, train_y, test_y = train_test_split(
    df_x, df_y, test_size=0.3, random_state=12, stratify=df_y
)
print('학습/테스트 크기:', train_x.shape, test_x.shape)

# [5단계] RandomForest 모델 생성 및 학습
# 500개의 나무가 각각 부트스트랩 샘플로 학습한다. 샘플 간 중복은 가능하다.
model = RandomForestClassifier(
    n_estimators=500, criterion='gini', random_state=12, n_jobs=-1
)
model.fit(train_x, train_y)

# [6단계] 테스트 데이터 예측 및 정확도 평가
pred = model.predict(test_x)
print('예측한 품질 점수:', pred[:10])
print('실제 품질 점수:', test_y.to_numpy()[:10])
print('정답을 맞힌 개수:', np.sum(test_y.to_numpy() == pred))
# 정확도는 예측 점수와 실제 점수가 정확히 일치한 비율이다.
print(f'테스트 분류 정확도: {accuracy_score(test_y, pred):.4f}')

# [7단계] 독립변수 중요도 확인 및 시각화
# 학습 과정에서 각 변수가 불순도를 줄이는 데 기여한 정도를 나타낸다.
# 중요도의 합은 1이며, 확률이나 인과적 영향력을 뜻하지 않는다.
# 연속형 변수 등에서는 중요도가 높게 평가될 수 있으므로 해석에 주의한다.
feature_df = pd.DataFrame({
    'feature': df_x.columns,
    'importance': model.feature_importances_,
}).sort_values('importance', ascending=False)
print('\n변수별 중요도:\n', feature_df.to_string(index=False))
print('중요도 합:', feature_df['importance'].sum())

plt.figure(figsize=(9, 6))
plt.barh(feature_df['feature'], feature_df['importance'])
plt.gca().invert_yaxis()
plt.xlabel('Feature importance')
plt.ylabel('Feature')
plt.title('Random Forest - Wine Quality')
plt.tight_layout()

# [8단계] 5겹 교차 검증
# 학습 데이터를 5묶음으로 나누어 4묶음으로 학습하고 1묶음으로 검증한다.
# StratifiedKFold는 각 검증 묶음에서도 품질 점수의 분포를 가능한 한 유지한다.
# 테스트 데이터는 제외하여 최종 평가용으로 보존한다.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)
cv_scores = cross_val_score(model, train_x, train_y, cv=cv, scoring='accuracy')
# 내부에서 모델 복사본을 학습하므로 위에서 학습한 model은 변경되지 않는다.
print('\n교차 검증별 정확도:', np.round(cv_scores, 4))
print(f'교차 검증 평균 정확도: {cv_scores.mean():.4f}')
print(f'교차 검증 정확도 표준편차: {cv_scores.std():.4f}')

plt.show()
plt.close()

