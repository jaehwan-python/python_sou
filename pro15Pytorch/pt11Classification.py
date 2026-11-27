# 딥러닝으로 제작한 classification model

# 분류의 종류 - 이항분류 -> sigmoid
#            - 다항분류 -> softmax

# 손실함수의 종류
# Regression - linear regression -> MSELoss
#            - nonlinear reression -> MSELoss
# classification - sigmoid -> "BCELoss"
#                - softmax -> CrossEntropyLoss (내부에 LogSoftmax 계산이 포함되므로 모델 출력 logits를 그대로 전달)
# Regression과 classification의 큰 흐름은 비슷하다 criterioin(손실함수)지정이 다르다는 것만 알고있자!

# classification의 알고리즘
# - Logistic Regression
# - Decision Tree
# - Ensemble - bagging -> RandomForest
#            - boosting -> XGBoost
# - svm
# - pca
# - Naive-Bayes
# - K-Nearest Neighbor

# ---------------------------------------------------------------------------------------------------------
# 이번에는 이항분류를 학습해보자!

# [1단계] : 데이터 불러오기 및 변수 설정
# 1. lib 불러오기
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import r2_score
from sklearn.datasets import load_diabetes

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
import copy

# 2. 데이터 불러오기
np.random.seed(42)
torch.manual_seed(42)

# 3. 변수설정
x_data = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]], dtype=np.float32)
y_data = np.array([[0], [0], [0], [1], [1], [1]], dtype=np.float32)

# 4. tensor변환
x_tensor = torch.tensor(x_data, dtype=torch.float32)
y_tensor = torch.tensor(y_data, dtype=torch.float32)

# 5. 두 모델에 대한 학습 공통 함수
def train_model_Func(model, x_train, y_train, epochs=20, lr=0.01, batch_size=1):
    criterion = nn.BCELoss() # 이항분류이기 때문에 Binary Cross Entropy를 쓴다!
    optimizer = optim.Adam(model.parameters(),lr=lr)
    data_size = len(x_train)

    for epoch in range(epochs):
        indices = torch.randperm(data_size) # 매 epoch마다 데이터 섞기
        total_loss = 0

        for i in range(0, data_size, batch_size):
            # 섞은 index에서 미니batch에 사용할 번호를 뽑아 데이터를 가져옴
            batch_idx = indices[i : i+batch_size]

            x_batch = x_train[batch_idx]
            y_batch = y_train[batch_idx]

            # 순전파
            pred = model(x_batch) 
            loss = criterion(pred, y_batch) # 손실값 계산
            optimizer.zero_grad()

            # 역전파
            loss.backward() 
            optimizer.step()
            total_loss += loss.item()
    return model

# 공통 평가 함수
def evaluate_model_Func(model, x, y):
    criterion = nn.BCELoss()

    with torch.no_grad():
        pred = model(x)
        loss = criterion(pred, y).item()
        pred_class = (pred >= 0.5).float() # 확률값을 0또는 1로 변환
        print('pred_class : ', pred_class)
        accuracy = (pred_class == y).float().mean().item()

    return loss, accuracy


print("\nmodel제작1 : Sequential 클래스 사용") # seq_model사용
seq_model = nn.Sequential(
    nn.Linear(in_features=2, out_features=4),
    nn.ReLU(),
    nn.Linear(in_features=4, out_features=1),
    nn.Sigmoid()
)
print(seq_model)
# 결과 : 
# Sequential(
#   (0): Linear(in_features=2, out_features=4, bias=True)
#   (1): ReLU()
#   (2): Linear(in_features=4, out_features=1, bias=True)
#   (3): Sigmoid()
# )

# 모델 학습
seq_model = train_model_Func(
    model = seq_model, x_train=x_tensor, y_train=y_tensor, epochs=20, lr=0.01, batch_size=1
)

# 모델평가
loss, acc = evaluate_model_Func(model = seq_model, x = x_tensor, y=y_tensor)
print(f'방법1 평가 결과 : 손실={loss:.4f}, 분류정확도={acc:.4f}')
# 방법1 평가 결과 : 손실=0.5834, 분류정확도=0.5000


print("\nmoddel제작2 : 모듈class로 모듈을 상속") # mymodel사용
class MyClassModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.dense1 = nn.Linear(in_features=2, out_features=4)
        self.relu = nn.ReLU()
        self.dense2 = nn.Linear(in_features=4, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, inputs):
        net = self.dense1(inputs)
        net = self.relu(net)
        net = self.dense2(net)
        net = self.sigmoid(net)
        return net
    # = 메서드 오버라이드

mymodel = MyClassModel()
print(mymodel)

mymodel = train_model_Func(
    model=mymodel, 
    x_train = x_tensor,
    y_train = y_tensor,
    epochs=20,
    lr=0.01,
    batch_size = 1
    )

loss2, acc2 = evaluate_model_Func(mymodel, x_tensor, y_tensor)

print(f'방법2 평가 결과 : loss(손실)={loss:.4f}, 분류정확도={acc:.4f}')
# 방법2 평가 결과 : loss(손실)=0.5834, 분류정확도=0.5000

# --------------------------------------------------------------------------
# 예측값과 확률값으로 시각화
# 2차원 입력(x1, x2)을 가진 모델을 x2는 고정하고 x1만 변화한며 sigmoid형태의 출력
x1_range = np.linspace(0, 6, 100).astype(np.float32)
x2_fixed = 2.5
x_vis = np.column_stack([
    x1_range, np.full_like(x1_range, x2_fixed)
])
x_vis_tensor = torch.tensor(x_vis, dtype=torch.float32)

# 예측확률 계산
with torch.no_grad():
    y_prob = seq_model(x_vis_tensor).numpy()

x1_real = x_data[:, 0]
y_real = y_data.ravel()

plt.figure(figsize=(7, 5))
plt.plot(x1_range, y_prob, label='sigmoid curve')
plt.scatter(x1_real, y_real, color='red', label='True Data')
plt.xlabel('x_data')
plt.ylabel('probability')
plt.legend(loc='lower right')
plt.grid()
plt.show()
# 해석 : 0.5를 기준으로 반을 잘라서 0.5 이상인 값은 1, 이하인 값은 0으로 1과0으로 이항분류가 되도록 하였다.
# ---------------------------------------------------------------------------------------------------
