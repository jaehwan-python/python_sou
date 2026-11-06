# Kaggle 지원 dataset으로 회귀분석 모델(LinearRegression)을 작성하시오.
# testdata 폴더 : Consumo_cerveja.csv

# Beer Consumption - Sao Paulo : 브라질 상파울루 지역 대학생 그룹파티에서 맥주 소모량 dataset

# feature : Temperatura Media (C) : 평균 기온(C)
#           Precipitacao (mm) : 강수(mm)
# label : Consumo de cerveja (litros) - 맥주 소비량(리터) 를 예측하시오.

# 조건 : NaN이 있는 경우 삭제!

# -----------------------------------------------------------------------------------------------

# [1단계] : 데이터셋 준비_독립변수와 종속변수
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

# 독립변수(feature) - Temperatura Media (C) : 평균 기온(C)
#                   - Precipitacao (mm) : 강수(mm)
# 종속변수(label) : Consumo de cerveja (litros) - 맥주 소비량(리터) 
# "평균기온별 강수량에 따른 맥주 소비량을 예측하시오"

df = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/Consumo_cerveja.csv")
df = df.rename(columns={
    'Temperatura Media (C)': '평균기온(C)',
    'Precipitacao (mm)': '강수(mm)',
    'Consumo de cerveja (litros)': '맥주 소비량(litros)'
})
# 열 이름 변경

df = df.dropna()
# NaN이 있는 행 삭제

features = ['평균기온(C)', '강수(mm)']
label = '맥주 소비량(litros)'
df = df[features + [label]].copy()
# 독립변수 2개와 종속변수 선택
# 그리고 예측에 사용할 열 3개만 선택하여 df에 저장

for column in df.columns:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )
# 쉼표로 표시된 소수점을 변환한 뒤 숫자형으로 변경

print(f"상관계수는 {df.corr()}")
# 결과 : 상관계수는
#                                   평균기온(C)    강수(mm)     맥주 소비량(litros)
#                   평균기온 (C)     1.000000      0.024416        0.574615
#                      강수 (mm)     0.024416      1.000000       -0.193784
#           맥주 소비량 (litros)     0.574615     -0.193784        1.000000


# 모든 모델에서 Overfitting이 발생할 수 있지만, 우리는 선형회귀에 대해서 배우고 있으니 선형회귀에서 Overfitting을 해결하는 4가지 방법을 보자.
# - 1. 변수(feature)를 줄이기
# - 2. 정규화(Regularization) 적용하기 -> L1, L2규제, ElasticNet ... 이 정규화는 선형회귀모델만 검사가 가능하다.
# - 3. Train/Test split
# - 4. 더 많은 데이터 수집하기


# [2단계] : 학습용 70%, 평가용 30%로 분리 - 3. Train/Test split 사용
x = df[features]
y = df[label]
# x는 평균기온·강수량(입력값), y는 같은 행의 맥주 소비량(정답값)이다.
# x와 y를 함께 분리하므로 입력값과 정답값의 행 짝이 유지된다.

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42, shuffle = True)
# test_size = 0.3 : 전체 행의 약 30%는 평가용, 나머지 약 70%는 학습용으로 사용한다.
# shuffle = True : 행을 무작위로 섞어서 나눈다.
# random_state = 42 : 같은 데이터로 실행하면 같은 분할 결과가 나오도록 고정한다.

# x_train : 학습용 평균기온·강수량 
# y_train : 학습용 맥주 소비량

# x_test  : 평가용 평균기온·강수량 
# y_test  : 평가용 맥주 소비량


# [3단계] : 선형회귀모델 생성
model = LinearRegression() # 회귀선 생성
model.fit(x_train, y_train)
# fit(x_train, y_train)에서 학습용 데이터만 사용해 회귀계수와 절편을 구함.

print('회귀계수(slope) :', features, model.coef_)
print('절편(bias) :', model.intercept_)
# 예측y값 = [0.72914518  -0.08334385] * x값 + 10.213140403122448
# 예측 맥주 소비량 = (0.72914518 * 평균기온) + (-0.08334385 * 강수량) + 10.213140403122448


# [4단계] : 평가용 데이터로 예측하고 성능 확인
y_pred = model.predict(x_test)
# predict(x_test)로 학습에 사용하지 않은 입력값의 소비량을 예측

print('r2_score(결정계수) :', r2_score(y_test, y_pred))
# '실제값' : y_test
# '예측값' : y_pred
# 순서를 바꾸어서 적으면 안된다.
# 평가용 실제 소비량과 예측값을 비교하여 실제값에 대해서 예측값이 얼마나 잘나왔고 설명ㅇ르 잘하는지를 나타낸다.
# 결과 :  0.3897154175627777
# 설명력이 38%이다.

print(pd.DataFrame({'실제 소비량': y_test, '예측 소비량': y_pred}).head())
# 결과
#          실제 소비량     예측 소비량
#      193   25.640        26.298083
#      33    31.655        26.966793
#      15    29.938        29.368800
#      309   20.575        24.621049
#      57    26.241        28.129271


# [5단계] : 평균 기온 25도, 강수량 0mm인 경우 예측
new_data = pd.DataFrame({'평균기온(C)': [25.0], '강수(mm)': [0.0]})
print('예측 맥주 소비량 :', model.predict(new_data))
# 결과 : 
#      실제 소비량     예측 소비량
# 193  25.640          26.298083
# 33   31.655          26.966793
# 15   29.938          29.368800
# 309  20.575          24.621049
# 57   26.241          28.129271

# 새로운 데이터의 예측 소비량 : 28.441769966227714
# 평균기온이 25도이고 강수량이 0일때 예측 소비량은 28이다.


# 이렇게 Train / Test split을 사용해보았다.

# 지금까지 우리는 '선형회귀분석'에 대해서 학습하였고 그 때 보이는 3가지 모델로 LinearRegression, ols, Lingress가 있다.
# 이제부터는 '비선형회귀분석'에 대해서 학습할 것이다.


