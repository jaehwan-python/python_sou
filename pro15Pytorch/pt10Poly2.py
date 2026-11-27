# 이번엔 다항회귀모델을 sales데이터셋을 이용하여 표현해보자.
# sales데이터셋 : 광고비에 따른 매출액

# [1단계] : 데이터 불러오기 및 변수 설정
# 1. lib 불러오기
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import torch
import torch.nn as nn
import torch.optim as optim

np.random.seed(7)
torch.manual_seed(7)

# 2. 데이터 불러오기
# 데이터 파일 직접 제작 -csv
# 광고비가 증가하면 매출도 증가하지만, 어느 정도 이후에는 매출 증가폭이 둔화되는 자료
# add_cost : '광고비'
# sales : '매출'
# 이 두 가지에 대해서 값을 설정해보자.
add_cost = np.linspace(0, 100, 80) # 0부터 100까지 균등한 간격으로 80개의 광범위한 데이터(광고비 자료)를 뽑음
sales = -0.06 * (add_cost ** 2) + 7.5 * add_cost + 40 + np.random.normal(0, 25, size=len(add_cost))
#sales = -0.06 *    광고비²     + 7.5 *  광고비  + 40 +              noise ..?  비선형 데이터임을 보여주기 위해서 noise를 줘보았다.
df = pd.DataFrame({'광고비': add_cost, '매출': sales})
print(df.head(3))
# 결과 
#          광고비          매출
#   0    0.000000     82.263143
#   1    1.265823    123.192136
#   2    2.531646    230.309368
df.to_csv("add_sales.csv", index=False, encoding='utf-8-sig') # 라는 파일명으로 csv 자료형으로 저장함.

# 데이터 파일 읽기
df = pd.read_csv("add_sales.csv")
print(df.head(3))
print(df.info)

# 결측치가 있다면 제거
df = df.dropna()
print(df.shape) # (80, 2)

# 3. 변수설정 : 광고비에 따른 매출은?
# x : 광고비
# y : 매출
x = df[['광고비']].values.astype(np.float32)
y = df[['매출']].values.astype(np.float32) # 미리 출력값을 2차원으로 지정

# 데이터 시각화
plt.figure(figsize=(8, 5))
plt.scatter(x, y)
plt.xlabel('광고비')
plt.ylabel('매출')
plt.title("광고비를 준 금액과 매출은 어떤 관계일까?")
plt.grid()
plt.show()

# 4. train / test split()
indices = np.arange(len(x))
np.random.shuffle=True
x = x[indices]
y = y[indices]
train_size = int(len(x) * 0.8)

# x_train : 전체 광고비(x) 중 앞의 80%를 학습용 입력(feature)으로 사용한다. shape은 (64, 1)이다.
x_train = x[:train_size]
x_test = x[train_size:]

# y_train : x_train과 같은 위치의 매출(y) 80%를 학습용 정답(label)으로 사용한다. shape은 (64, 1)이다.
y_train = y[:train_size]
y_test = y[train_size:]

print(x_train.shape, x_test, y_train)

# 5. 표준화 및 정규화(scaling) : train데이터 기준으로 평균과 표준편차를 계산
# 표준화 공식 
# "표준화한 값 = (해당값 - 평균(mean)) / 표준편차(std)"
# 종속변수(x)의 표준화 한 train데이터와 test데이터
x_mean = x_train.mean(axis=0)
x_std = x_train.std(axis=0)
x_train_scaled = (x_train - x_mean) / x_std
x_test_scaled = (x_test - x_mean) / x_std

# 독립변수(y)의 표준화 한 train데이터와 test데이터
y_mean = y_train.mean(axis=0)
y_std = y_train.std(axis=0)
y_train_scaled = (y_train - y_mean) / y_std
y_test_scaled = (y_test - y_mean) / y_std

# 6. 다항 특성 생성 함수 : degree=2dlaus [x, x^2]형태 자료 생성 : 이렇게 하면 모델이 직선뿐 아니라 곡선 관계도 학습할 수 있다
def make_poly_features(x_scaled, degree=2):
    features = [x_scaled ** d for d in range(1, degree+1)]
    return np.concatenate(features, axis = 1).astype(np.float32)

x_train_poly = make_poly_features(x_train_scaled, degree=2) # 입력값(종속변수)이 선형자료인 경우
x_test_poly = make_poly_features(x_test_scaled, degree=2)   # 입력값(종속변수)이 비선형인 경우

print('선형회귀 입력 자료 shape : ', x_train_scaled.shape) 
print('다항회귀(비선형) 입력 자료 shape : ', x_train_poly.shape)
# 결과 : (데이터갯수, feature수)
# (64, 1)
# (64, 2)

# 7. tensor 변환
# 선형회귀는 입력특성이 x(64, 1)이고 비선형회귀(다항회귀)는 입력특성이 x, x²(64, 2)이다
# 선형회귀인 경우)
x_train_scaled_tensor = torch.tensor(x_train_scaled,dtype=torch.float32) 
x_test_scaled_tensor = torch.tensor(x_test_scaled,dtype=torch.float32)

# 비선형 회귀인 경우)
x_train_poly_tensor = torch.tensor(x_train_poly,dtype=torch.float32)
x_test_poly_tensor = torch.tensor(x_test_poly,dtype=torch.float32)

y_train_scaled_tensor = torch.tensor(y_train_scaled,dtype=torch.float32)
y_test_scaled_tensor = torch.tensor(y_test_scaled,dtype=torch.float32)

# 훈련 데이터 전체를 한 번에 사용하는 풀 배치 방식이라서 배치를 나누는 코드가 없다. 즉 batch크기가 64인 셈이다.

# 8. 평가함수 : R2score, MSE, RMSE '직접' 계산으로
# R2score는 1에 가깝고 MSE와 RMSE, MAE는 0에 가까울수록 model의 성능이 좋다.
# 1) R2-score(결정계수)
def r2_score_np_Func(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred)**2) # 잔차제곱합
    ss_tot = np.sum((y_true - np.mean(y_true))**2) # 전체제곱합
    return 1 - (ss_res / ss_tot) # = R2_score(결정계수)

# 2) 모델 평가 후 출력 함수
def evaluate_Model_Func(name, y_true, y_pred):  # (모델이름, 실제값, 예측값)
    mse = np.mean((y_true - y_pred)**2)
    rmse = np.sqrt(mse)
    r2 = r2_score_np_Func(y_true, y_pred) # 실제값(y)과 예측값(y)를 주어주고 이를 함수(우리가 만든 함수)가 계산하도록 함.
    print(f"\n[{name}] MSE는 : {round(mse, 3)}, RMSE는 : {round(rmse, 3)}, R2-score(결정계수)는 : {round(r2, 3)} 입니다~")


# [2단계] : 모델 정의
# 1. 모델 생성 함수
# Model1(선형 회귀 모델) : feature1
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1,1)

    def forward(self, x):
        return self.linear(x)

# Model2(비선형(다중선형)회귀 모델) : feature2
class PolyRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2,1)

    def forward(self, x):
        return self.linear(x)
# 현재 두 가지 모델에 대해서 차이점을 배우고 있기에 두 모델을 불러오는 2개의 클래스가 생겼다.

linear_model = LinearRegressionModel()  # model1
poly_model = PolyRegressionModel()      # model2
print("선형모델 : ", linear_model)
print("비선형(다항회귀)모델 : ", poly_model)
# 결과 :
# 선형모델             :  LinearRegressionModel( (linear): Linear(in_features=1, out_features=1, bias=True) )
# 비선형(다항회귀)모델  :  PolyRegressionModel( (linear): Linear(in_features=2, out_features=1, bias=True) )
# 각 모델의 입력값형태와 출력값형태를 알 수 있다.

# 2. 모델 학습 함수
def train_model_Func(model, x_train_t, y_train_t, epochs = 2000, lr=0.01): # = model이 x_train, y_train데이터를 가지고 0.01의 학습률을 가지고 64개의데이터(1batch)만큼 끊어서 epochs 5000만큼 반복했다. 현재는 전체 데이터를 사용하여 2,000 epoch반복 학습하는 것이다.
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_history = [] # 각 epoch의 손실값(MSE)을 저장할 리스트 : 학습 후 손실 변화 그래프를 그려 손실이 줄어들고 수렴하는지 확인하기 위해 사용

    for epoch in range(epochs):
        model.train()
        y_pred = model(x_train_t)
        loss = criterion(y_pred, y_train_t) # 실제값과 예측값의 차이
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_history.append(loss.item())

        if (epoch + 1) % 50 == 0:
            print(f"epoch:{epoch+1:5d} / {epochs}, loss:{loss.item():.5f}")
            # '5d' : 전체 자릿수는 다섯자리수, ':.5' : 소숫점 아래 다섯자리까지..
    return loss_history


# 모델 학습 : 1(모델 생성), 2(모델 학습)에서 생성한 함수 불러오기
print("\n1. 선형모델 학습")
linear_loss_history = train_model_Func(
    linear_model, x_train_scaled_tensor, y_train_scaled_tensor, epochs = 2000, lr = 0.01
    ) 

print("\n2. 비선형(다항회귀)모델 학습")
poly_loss_history = train_model_Func(
    poly_model, x_train_poly_tensor, y_train_scaled_tensor, epochs = 2000, lr = 0.01
    ) 


# [3단계] : 모델 예측 및 평가(test데이터)
# 1. 예측
linear_model.eval()
poly_model.eval()

with torch.no_grad():
    y_pred_linear_scaled_t = linear_model(x_test_scaled_tensor) # 예측값은 scaled y기준으로 나온다.
    y_pred_poly_scaled_t = poly_model(x_test_poly_tensor)

# 2. 출력값 형태 바꾸기 : torch.tensor  ->  nd.array
# 이렇게 하면 예측값(결과)가 tensor값으로 나온다. 우리는 이를 nd.array로 출력형태를 바꾸어준다.
y_pred_linear_scaled = y_pred_linear_scaled_t.numpy()
y_pred_poly_scaled = y_pred_poly_scaled_t.numpy()

# 3. 표준화/정규화 벗기기 : 표준화된 label을 기존 '매출'단위로 복원시키기
y_pred_linear = (y_pred_linear_scaled * y_std) + y_mean # ... 나누었던 것을 다시 곱하면 됨
y_pred_poly = (y_pred_poly_scaled * y_std) + y_mean

# 4. 모델의 성능 평가 : 두 model의 성능 비교
evaluate_Model_Func('선형회귀', y_test, y_pred_linear)
evaluate_Model_Func('다항회귀 degree=2', y_test, y_pred_poly)

# --------------------------------------------------------------------------------------------------------
# 시각화1 : loss값 시각화
plt.figure(figsize=(8,5))
plt.plot(linear_loss_history, label='선형회귀 손실')
plt.plot(poly_loss_history, label='다항회귀 손실')
plt.xlabel('학습횟수')
plt.ylabel('손실')
plt.legend()
plt.grid()
plt.show()
# 해석 : Linear보다 nonlinear를 비교하면 동일한 데이터셋을 평가할 때 nonlinear모델이 loss값이 더 떨어지게 나왔다 = 성능이 더 좋다!

# 시각화2 : 추세선 시각화
# 추세선시각화 : 현재 비선형 구조로 분포한 데이터들에 대해서 추세선(일차식)을 그어보자.
x_plot = np.linspace(x.min(), x.max(), 300).reshape(-1, 1).astype(np.float32)
x_plot_scaled = (x_plot - x_mean) / x_std
x_plot_poly = make_poly_features(x_plot_scaled, degree=2)

x_plot_scaled_tensor = torch.tensor(x_plot_scaled, dtype=torch.float32)
x_plot_poly_tensor = torch.tensor(x_plot_poly, dtype=torch.float32)

linear_model.eval()
poly_model.eval()
with torch.no_grad():
    y_plot_linear_scaled_tensor = linear_model(x_plot_scaled_tensor) # 예측값은 scaled y기준으로 나온다.
    y_plot_poly_scaled_tensor = poly_model(x_plot_poly_tensor)

    # torch.tensor  ->  nd.array
    # 이렇게 하면 예측값(결과)가 tensor값으로 나온다. 우리는 이를 nd.array로 출력형태를 바꾸어준다.
    y_plot_linear_scaled = y_plot_linear_scaled_tensor.numpy()
    y_plot_poly_scaled = y_plot_poly_scaled_tensor.numpy()

    # 표준화/정규화 벗기기 : 표준화된 label을 기존 '매출'단위로 복원시키기
    y_plot_linear = (y_plot_linear_scaled * y_std) + y_mean # ... 나누었던 것을 다시 곱하면 됨
    y_plot_poly = (y_plot_poly_scaled * y_std) + y_mean

plt.figure(figsize=(8,5))
plt.scatter(x_train, y_train, alpha=0.5, label='train data')
plt.scatter(x_test, y_test, alpha=0.5, label='test data')

plt.plot(x_plot, y_plot_linear, label='선형회귀의 추세선')
plt.plot(x_plot, y_plot_poly, label='다항회귀의 추세선')
plt.xlabel('광고비')
plt.ylabel('판매량')
plt.legend()
plt.grid()
plt.show()
# 비선형데이터가 선형데이터보다 모델을 잘 설명한다. 잔차제곱의 합(SSE)이 최소가 되는 것처럼 보인다.

# 여기까지 DeepLearning의 regression을 알아보았다. 다음시간부터는 DeepLearning의 classification을 알아보자
