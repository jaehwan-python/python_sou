# bike_dataset.csv 으로 파일명을 변경한다. 이 데이터는 어느 지역의 2011년 1월 ~ 2012년 12월 까지 날짜/시간. 기온, 습도, 풍속 등의 정보를 
# 바탕으로 1시간 간격의 자전거 대여횟수가 기록되어 있다.
# train / test로 분류 한 후 대여횟수에 중요도가 높은 칼럼을 판단하여 feature를 선택한 후, 
# 대여횟수에 대한 회귀 예측(RandomForestRegressor)을 하시오.

# 칼럼 정보 :
# 'datetime', 'season'(사계절:1,2,3,4), 'holiday'(공휴일(1)과 평일(0)), 'workingday'(근무일(1)과 비근무일(0)),
# 'weather'(4종류:Clear(1), Mist(2), Snow or Rain(3), Heavy Rain(4)),
# 'temp'(섭씨온도), 'atemp'(체감온도), 'humidity'(습도), 'windspeed'(풍속),
# 'casual'(비회원 대여량), 'registered'(회원 대여량), 'count'(총대여량)
# 참고 : casual + registered 가 count 임.

# 출력 사항 : 예측값 / 실제값, 결정계수, 예측 결과

# RandomForest 모델은 classsfication을 지원하지만 Regression도 가능하다. sklearn모듈은 대게 그러하다.
# 이번에는 Random Forest를 Regression으로 사용해보자.


# [1단계] : 데이터 불러오기 및 변수설정
# 1. Lib설정
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.ensemble import RandomForestRegressor
# from sklearn.ensemble import RandomForestClassifier -> 회귀를 할 것이기 때문에 RandomForestRegression을 사용한다.
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# 2. 데이터 불러오기
bike = pd.read_csv("bike_dataset.csv")
print(bike.head(5))
pd.set_option('display.max_columns', None)
df = bike.frame
print(df.head(10))

# 3. 변수설정
x = df.drop('count', axis=1)
y = df['count']

# 4. 데이터 전처리
# train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42) 


# [2단계] : 모델 생성 및 학습
rfmodel = RandomForestRegressor(n_estimators=200, random_state=42)
rfmodel.fit(x_train, y_train)


# [3단계] : 모델 예측 및 평가
y_pred = rfmodel.predict(x_test)
print(f"MSE : {mean_squared_error(y_test, y_pred)}") 
print(f"R2(결정계수) : {r2_score(y_test, y_pred)}")





