# RandomForest 모델은 classsfication을 지원하지만 Regression도 가능하다. sklearn모듈은 대게 그러하다.
# 이번에는 Random Forest를 Regression으로 사용해보자.

# 실습) 캘리포니아 주택가격 데이터로 회귀분석(Boston집값문제)

# [1단계] : 데이터 불러오기 및 변수설정

# [1-1]. Lib설정
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.ensemble import RandomForestRegressor
# from sklearn.ensemble import RandomForestClassifier -> 이번에는 회귀를 할 것이기 때문에 RandomForestRegression을 사용한다.
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.datasets import fetch_california_housing # -> 캘리포니아 주택가격 데이터셋 불러오기

# [1-2]. 데이터 불러오기
housing = fetch_california_housing(as_frame=True)
print(housing.DESCR)

pd.set_option('display.max_columns', None)
df=housing.frame
print(df.head(3))
print(df.info())
print()

# [1-3]. 변수설정
x = df.drop('MedHouseVal', axis=1)
y = df['MediHouseVal']

# [1-4]. 데이터 전처리
# train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42) 


# [2단계] : 모델 생성 및 학습
rfmodel = RandomForestRegressor(n_estimators=200, random_state=42)
rfmodel.fit(x_train, y_train)


# [3단계] : 모델 예측 및 평가
y_pred = rfmodel.predict(x_test)
print(f"MSE : {mean_squared_error(y_test, y_pred):.3f}") 
# 0.254 : 설명력이 매우 높다.
print(f"R2(결정계수) : {r2_score(y_test, y_pred):.3f}")
# 0.807
print()


# [4단계] : 독립변수들의 중요도 시각화
impo = rfmodel.feature_importances_
indices = np.argsort(impo)[::-1]
plt.figure(figsize=(8, 5))
plt.bar(range(x.shape[1]), impo[indices], align='center')
plt.xticks(range(x.shape[1]), x.columns[indices], rotation=45)
plt.xlabel('feature name')
plt.ylabel('feature importance')
plt.tight_layout()
plt.show()

ranking = pd.DataFrame({
    'feature' : x.columns[indices],
    'importance' : impo[indices]
})
print(ranking)
# RandomForest를 사용하면 각 독립변수들의 중요도(기여도)를 확인할 수도 있다. - ex27)확인

