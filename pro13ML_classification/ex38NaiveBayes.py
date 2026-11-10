# Naive base algorithm을 이용한 분류
# 실습1) weather데이터 : 기온, 습도, 기압 등 기상 정보를 이용하여 다음 날 비가 올지 안올지(RainTomorrow)를 예측하는 이진 분류 

# [1단계] : 데이터 불러오기 및 변수 설정
# 라이브러리 설정
import numpy as np
import pandas as pd

# 1. 데이터 불러오기
df = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/weather.csv")
print(df.head(2))
print(df.info())
# 결과 :
#   Column  Non-Null       Count          Dtype  
#    ---     ------     --------------    -----  
#     0       Date       366 non-null      str    
#     1     MinTemp      366 non-null    float64
#     2     MaxTemp      366 non-null    float64
#     3    Rainfall      366 non-null    float64
#     4    Sunshine      363 non-null    float64
#     5   WindSpeed      366 non-null     int64  
#     6    Humidity      366 non-null     int64  
#     7    Pressure      366 non-null    float64
#     8      Cloud       366 non-null     int64  
#     9      Temp        366 non-null    float64
#    10    RainToday     366 non-null      str    
#    11  RainTomorrow    366 non-null      str   

# 2. 데이터 전처리 
df = df.drop('Date', axis=1)
df['Sunshine'] = df['Sunshine'].fillna(df['Sunshine'].mean()) # 결측치를 평균값으로 채움
# date열은 없애기
# sunshie열의 결측치는 평균값으로 채우기

# 범주형 처리
df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No' : 0})
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes': 1, 'No' : 0})
print(df.head(2))
# 0과 1값으로 채움
# 결과 :
#           MinTemp  MaxTemp  Rainfall  Sunshine  WindSpeed  Humidity  Pressure  Cloud  Temp   RainToday  RainTomorrow
#     0        8.0     24.3       0.0       6.3        20       29     1015.0      7    23.6          0             1
#     1       14.0     26.9       3.6       9.7        17       36     1008.4      3    25.7          1             1

# 3. 변수설정
x = df.drop('RainTomorrow', axis=1) # RainTomorrow열을 뺀 모든 열이 독립변수이다. = 10개
y = df['RainTomorrow'] # 위에서 뺀 RainTomorrow열이 종속변수이다.                 = 1개

# Overfitting(과적합) 점검 방법1 : 데이터 분할과 교차 검증
# - train_test_split() : 학습용 / 테스트용 데이터를 나누어 일반화 성능 평가
# - KFold : 데이터를 K개로 나누고, 각 부분을 한 번씩 검증용으로 사용
# - GridSearchCV : 교차 검증으로 최적의 하이퍼파라미터 조합을 찾는 방법

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)


# [2단계] : NaiveBayes알고리즘에 따른 생성 및 학습
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
# GaussianNB : 연속형 수치 데이터, 정규분포(Gaussian), 키, 몸무게, 온도
# BernoulliNB : 이진 데이터(0, 1), 베르누이 분포, 단어 존재 여부
# MultinomialNB : 빈도/횟수 데이터, 다항분포, 단어 등장 횟수
# 우리는 GaussianiNB사용!!

# 1. 모델 생성
model = GaussianNB()

# 2. 모델 학습
model.fit(x_train, y_train)
# fit(학습용x, 학습용y)  


# [3단계] : NaiveBayes모델 예측 및 평가
from sklearn.metrics import accuracy_score, confusion_matrix
# 1. 모델 예측
pred = model.predict(x_test)

# 2. 모델 평가
print('분류 정확도 : ', accuracy_score(y_test, pred))
print('confusion_matrix : \n', confusion_matrix(y_test, pred))
print() 

# 3. 교차 검증
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x, y, cv=5)
print(f"교차 검증에서 각 fold:{scores}, 평균:{scores.mean()}")
# 결과 :
# 교차 검증에서 각 fold : [0.72972973 0.82191781 0.79452055 0.8630137  0.83561644],  평균 : 0.8089596445760829
print()

# 4. feature 중요도 분석 : 어떤 feature가 label이 결과를 매기는데 큰 영향을 주었을까?
# GaussianNB의 멤버로 theta_ : 각 클래스별 feature 평균을 반환
mean_0 = model.theta_[0]  # RainTomorrow=0 : 비 안오는 날 평균
mean_1 = model.theta_[1]  # RainTomorrow=1 : 비 오는 날의 평균

# 각 feature가 '비 안오는 날'과 '비 오는 날'에서 얼마나 차이가 나는지를 비교한다.
importance = np.abs(mean_1 - mean_0)
# 두 평균의 차이의 절댓값

# feature의 기여도
feat_impo = pd.DataFrame({'feature' : x.columns, 'importance' : importance}).sort_values(by='importance', ascending=False)
print('feature의 중요도 : \n', feat_impo)
# 결과 : 
#       feature  importance
# 5   Humidity   15.756059
# 6   Pressure    6.070088
# 3   Sunshine    3.698378
# 0    MinTemp    3.448954
# 7      Cloud    2.623589
# 2   Rainfall    1.151417
# 1    MaxTemp    0.745820
# 8       Temp    0.296384
# 9  RainToday    0.157575
# 4  WindSpeed    0.094734
# 해석 : 습도(Humidity(16%)))와 기압(Pressure(6%))이 다음날 날씨에 비가 올지 안올지에 영향을 크게 미친다.

# 시각화(feature 중요도)
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.figure()
plt.bar(feat_impo['feature'], feat_impo['importance'])
plt.xlabel('features(독립변수들)')
plt.ylabel('중요도(평균의 차이)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 5. 새로운 자료에 대한 예측(점검)
print('새로운 자료에 대한 예측')
newdata = pd.DataFrame([{
    'MinTemp' : 1.3,
    'MaxTemp' : 15.0,
    'Rainfall' : 0.0,
    'Sunshine' : 10.0,
    'WindSpeed' : 3.0,
    'Humidity' : 40,
    'Pressure' : 1000.0,
    'Cloud' : 3,
    'Temp' : 20.0,
    'RainToday' : 0
}])
# 학습 데이터와 동일한 열 순서로 맞춤
newdata = newdata[x.columns]

# 새로운 데이터셋에 대해서 예측해보기
newpred = model.predict(newdata)
print('예측결과 : ', '비 온다.' if newpred[0] == 1 else '비 오지 않는다.')
print('Tomorrow에 비가 올 확률은 : ', model.predict_proba(newdata)[0, 1])
# 결과 : 
# 예측결과  :  "비 오지 않는다."
# Tomorrow에 비가 올 확률은  :  0.07213687918227131