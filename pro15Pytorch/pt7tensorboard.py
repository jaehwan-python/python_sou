# **Tensorboard**
# 텐서보드는 머신러닝실험에 필요한 시각화 및 도구를 제공한다
# 손실 및 정확도와 같은 측정항목 추적 및 시각화
# 모델 그래프(작업 및 레이어) 시각화
# 시간의 경과에 따라 달라지는 가중치, 편향, 기타 텐서의
# 
# python -m pip install tensorboard 입력하기 ... tensorboard를 쓸 수 있는 lib

# 딥러닝 모델 제작 <핵심 요약>
# [1단계] : 데이터 불러오기, 입력(X)·정답(y) 설정 및 전처리
# [2단계] : train / validation / test dataset 분리 및 Dataset·DataLoader 구성
# [3단계] : 학습 함수 정의(예측 → 손실 계산 → 역전파 → 가중치 수정, 검증 및 history 기록)
# [4단계] : 평가 함수 정의(test 데이터의 예측값과 손실값 반환)
# [5단계] : 모델 생성, 손실함수 및 옵티마이저 설정 그리고 학습·평가 실행
# [6단계] : test 데이터의 최종 평가 결과 출력(MSE, RMSE, R²)
# -----------------------------------------------------------------------------------

# 실습) 당뇨병 데이터를 이용해 회귀 모델을 만들고, 학습 과정을 TensorBoard로 시각화해보자.

# - xdata : (442, 10) —>  442명의 age(나이), 성별(sex), 체질량지수(BMI), 혈압(bp), s1(총콜레스테롤), s2(저밀도 지단백(LDL)), s3(고밀도 지단백(HDL)), s4(총 콜레스테롤/HDL비율), s5(중성지방 수치의 로그값), s6(혈당) 등 입력 특성 10개
# - ydata : (442, 1)  —>  각 사람의 1년 후 질병 진행 정도를 나타내는 정답값 1개 = s6로 삼는다.
# 즉, 당뇨병 여부를 분류하는 게 아니라 질병 진행 정도를 숫자로 예측하는 회귀 문제이다. Classification이 아니라 Regression이다.

# [1단계] : 데이터 불러오기 및 변수설정
# 1. lib불러오기
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import r2_score
from sklearn.datasets import load_diabetes

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter # tensorboard의 기록을 저장하는 lib이다.

import datetime
import os

# 2. 변수설정
# data load : 당뇨벙 환자의 1년 후 질병 진행정도를 나타내는 정량적 수치
diabetes = load_diabetes()
xdata = diabetes.data                  # (442, 10) : 442개의 데이터가 10개의 특성(feature)으로 구분되어 있는 2차원 자료임
ydata = diabetes.target.reshape(-1, 1) # (442,  1) : 442개의 데이터가 1개의 특성(label)으로 구분되어 있는 2차원 구조 = s6(혈당수치)
print(xdata[:2], ' ', xdata.shape)    
print(ydata[:2], ' ', ydata.shape)
print('feature names : ', diabetes.feature_names)

# ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
# age : 나이, 
# sex : 성별, 
# bmi : 체질량지수, 
#  bp : 평균 혈압
#  s1 : 총 콜레스테롤,
#  s2 : 저밀도 저단백 콜레스테롤, 
#  s3 : 고밀도 저단백 콜레스테롤, 
#  s4 : 총 콜레스테롤 / HDL비율, 
#  s5 : 혈청 중성지방 수치의 로그값으로 추정, 
#  s6 : 혈당 수치 -> 종속변수(label)

# 3. 표준화 및 정규화(해도되고 안해도 돼!) : Deep Learning에서는 feature의 scaling(정보는 유지하면서 숫자의 범위만 바꾸는 것)을 강력 추천한다.
# diabetes은 사실 표준화 되어 있으나 연습을 위해서 표준화를 하자!
scaler = StandardScaler()
xdata_scaled = scaler.fit_transform(xdata)

# 4. 과적합 문제 방지
# train/test split o
# KFold
# GridSearchCV
# L1, L2 규제
x_train, x_test, y_train, y_test = train_test_split(xdata_scaled, ydata, test_size=0.3, shuffle=True, random_state=42)

# 5. Tensor로 변환 : 딥러닝 모델이 학습할 수 있는 데이터type으로 바꿔주기
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# 6. train data의 일부를 validation data로 분리(Validation dataset을 설정)
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
validation_size = int(len(train_dataset) * 0.2)
train_size = int(len(train_dataset) - validation_size)

train_subset, validation_subset = random_split(
    train_dataset, [train_size, validation_size],
    generator = torch.Generator().manual_seed(123)
)


# [2단계] : 데이터 묶고 불러오기(batch, Dataloader) -> 나중에 모델이 불러올 수 있게 만들어주기
batch_size = 32

train_loader = DataLoader(
    train_subset, batch_size=batch_size, shuffle=True
)

validation_loader = DataLoader(
    validation_subset, batch_size=batch_size, shuffle=False
)

print(len(train_loader.dataset), len(validation_loader.dataset))


# 모델 정의
class DiabetRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.hidden_layer1 = nn.Linear(10, 64)
        self.hidden_layer2 = nn.Linear(64, 32)
        self.hidden_layer3 = nn.Linear(32, 16)
        self.output_layer1 = nn.Linear(16, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        net = self.relu(self.hidden_layer1(x))
        net = self.relu(self.hidden_layer2(net))
        net = self.relu(self.hidden_layer3(net))
        net = self.output_layer1(net)
        return net

model = DiabetRegressionModel()
print(model)

# loss function, optimizer정의
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr = 0.001)

# **TensorBoard 로그 저장**
log_dir = os.path.join(
    "runs", "diabet_regression", 
    datetime.datetime.now().strftime("%Y%D%D-%H%M%S")
    )

writer = SummaryWriter(log_dir=log_dir)  # 저장 로그 위치 지정
print("Tensorboard 로그 저장 위치 : ", log_dir)
# 텐서보드에 모델 그래프를 기록한다.
sample_input = x_train_tensor[:1]
writer.add_graph(model, sample_input)

epochs = 200

train_loss_history = []
validation_loss_history = []

for epoch in range(epochs): # 200번 epochs을 한다.
    model.train()
    train_loss_sum = 0

    for x_batch, y_batch in train_loader:
        pred = model(x_batch)  # 예측값 계산
        loss = criterion(pred, y_batch) # 손실 계산
        optimizer.zero_grad() # gradient 초기화
        loss.backward() # 역전파 ... parameter(weight, bias)갱신을 해야함
        optimizer.step() # parameter가 갱신됨
        train_loss_sum += loss.item()

    train_loss = train_loss_sum / len(train_loader)
    model.eval()
    validation_loss_sum = 0

    with torch.no_grad():
        for x_validation, y_validation in validation_loader:
            validation_pred = model(x_validation)
            validation_loss = criterion(validation_pred, y_validation)
            validation_loss_sum += validation_loss.item()

    validation_loss = validation_loss_sum / len(validation_loader)

    train_loss_history.append(train_loss)
    validation_loss_history.append(validation_loss)

# train(70%) - train(80%) 
#            - validation(20%)   
# test(30%) 

    # --- 텐서보드에 기록 ---
    writer.add_scalar("Loss/train", train_loss, epoch) # (태그명, 기록값, x축값)
    writer.add_scalar("Loss/validation", validation_loss, epoch) # (태그명, 기록값, x축값)

    # 각 layer의 weight histogram기록
    for name, param in model.named_parameters():
        writer.add_histogram(name, param, epoch) # 여러 parameter값들의 분포 변화 기록
    # ------------------------

    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch + 1} / {epochs}] train_loss : {train_loss:.4f}, validation_loss : {validation_loss:.4f}")

# test data로 학습이 끝난 모델 검증
model.eval()
with torch.no_grad():
    test_pred = model(x_test_tensor)
    test_loss = criterion(test_pred, y_test_tensor)

print("test loss : ", test_loss.item())
test_pred_np = test_pred.numpy()
print('설명력(R2) : ', r2_score(y_test, test_pred_np))

# 텐서보드에 최종 test loss 기록
writer.add_scalar("Loss/test", test_loss.item(), epochs)
writer.close()

# loss 시각화
plt.plot(train_loss_history, label = 'train loss')
plt.plot(validation_loss_history, label = 'validation loss')
plt.xlabel('학습횟수')
plt.ylabel('손실(loss)')
plt.legend()
plt.show()

# 예측값 일부 확인
print("예측값 : ", test_pred_np[:5].ravel())
print("실제값 : ", y_test[:5].ravel())

# 터미널창에 tensorboard --logdir runs 를 입력하면 우리가 만든 model의 구조를 웹에서 확인할 수 있다.

# 지금까지 diabets 데이터셋을 가지고 다중선형회귀모델을 학습하면서 tensorboard를 사용해보앗다.