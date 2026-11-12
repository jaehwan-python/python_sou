# [1단계] : 데이터 불러오기 및 변수 설정
# 1. Lib불러오기
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import koreanize_matplotlib 

# 2. 데이터 불러오기 및 전처리
df= pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/mushrooms.csv")
print(df.head(2))
print(df.shape)

from sklearn.preprocessing import LabelEncoder

# 3. 데이터 전처리-인코딩
le = LabelEncoder()
for col in df.columns:
    df[col] = le.fit_transform(df[col]) 
print(df.head(2)) #e가 0이면 식용, p가 1이면 독버섯 

# 4. 변수설정
x = df.drop('class', axis=1)
y = df['class']

# 5. 과적합 방지 : train / test split
# - train / test split o
# - KFold
# - GridSearchCV
# - L1, L2 규제
from sklearn.model_selection import train_test_split
x_train, x_test,y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0, stratify=y)
print(x_train.shape, x_test.shape)



# [2단계] : 모델 생성(Ensemble -> RandomForest(DecisionTree)) 및 학습
# 1. 모델 생성
from sklearn.ensemble import RandomForestClassifier 
rf_model = RandomForestClassifier(criterion='gini', n_estimators=500, random_state=12)

# 2. 모델 학습 : train용 x와 y
rf_model.fit(x_train, y_train)


# [3단계] : 모델 예측 및 평가 
# 1.변수 중요도 평가
importances = rf_model.feature_importances_
feat_impo = pd.DataFrame({
    'feature':x.columns, 'importance':importances
}).sort_values(by='importance', ascending=False)
print('feature 중요도')
print(feat_impo)

# 중요도 시각화 
import seaborn as sns
plt.figure(figsize=(8, 5))                     
sns.barplot(x='importance', y='feature', data=feat_impo, orient='h')
plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립 변수')
plt.tight_layout()                            
plt.show()
plt.close()

# -----------------------------------------------------------------------------

# [1단계] : 변수설정 10개 추출 
features = feat_impo['feature'].head(10).tolist() # 상위 10개의 중요변수를 뽑아냄.
print('상위 10개 feature :', features)
# ['odor', 'gill-size', 'gill-color', 'spore-print-color', 'ring-type', 'population', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring', 'bruises']

# [2단계] 모델 생성 및 학습
# 1. 모델 생성(NaiveBayes-GausianNB) 
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
# NaiveBayes알고리즘을 사용하는 model종류
# - GaussianNB : 연속형 수치 데이터, 정규분포(Gaussian), 키, 몸무게, 온도
# - BernoulliNB : 이진 데이터(0, 1), 베르누이 분포, 단어 존재 여부
# - MultinomialNB : 빈도/횟수 데이터, 다항분포, 단어 등장 횟수

# 2. 모델 학습 - train용 x와y
model.fit(x_train[features], y_train)


# [3단계] : 분류 정확도 평가
from sklearn.metrics import accuracy_score, confusion_matrix
pred = model.predict(x_test[features])
print('예측 값 :', pred[:10]) #예측 값 : [0 0 0 0 1 1 0 0 0 1]
print('실제 값 :', y_test[:10].values) #실제 값 : [0 0 1 0 1 1 0 0 0 1]
print('분류 정확도 :', accuracy_score(y_test, pred)) #분류 정확도 : 0.8740771123872026
print('confusion_matrix : \n', confusion_matrix(y_test, pred)) 
#confusion_matrix : 
# [[1151  112]
# [ 195  980]]

# 1. 교차검증
from sklearn.model_selection import cross_val_score

scores = cross_val_score(GaussianNB(), x[features], y, cv=5)
print(f'교차검증에서 각 fold:{scores}, 평균:{scores.mean()}')
#교차검증에서 각 fold:[0.66092308 0.85230769 0.80369231 0.99753846 0.55849754], 평균:0.7745918150814701

# test data 5개로 확인 
sample = x_test[features][:5]
pred1 = model.predict(sample)
prob1 = model.predict_proba(sample)

class_name = ['식용', '독버섯']
for pred_val, real_val, prob in zip(pred1, y_test[:5].values, prob1):
    print(f'예측:{class_name[pred_val]}, 실제:{class_name[real_val]}'
        f'확률:[식용:{prob[0]:.4f}, 독:{prob[1]:.4f}]')