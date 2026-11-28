# Softmax함수 : 각 클래스의 점수를 0~1 사이의 확률로 변환하며, 모든 클래스의 확률 합은 1 / 입력받은 실수 벡터를 '0'~'1'사이의  확률값으로 변환
# 수식 : softmax(x_i) = exp(x_i) / sum(x_i)

# Classification - 이항분류 : sigmoid방식 : wine데이터셋
#                - 다항분류 : softmax방식 : 

# 이항분류  ->  손실함수(criterion) : BCEWithLogitsLoss
# 다항분류  ->  손실함수(criterion) : CrossEntropyLoss (내부에서 LogSoftmax를 적용하므로 모델의 출력 로짓을 그대로 전달)

# -------------------------------------------------------------------------------------------------------------------------------------------------

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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# softmax함수 수식 : softmax(x_i) = exp(x_i) / sum(x_i)
# 방법1 : 직접 함수 생성
def softmax_Func(a):
    c = np.max(a)
    exp_a = np.exp(a-c)
    sum_exp_a = np.sum(exp_a)
    return (f"f softmax함수의 수식 : {exp_a / sum_exp_a}")

data = np.array([0.12, 2.34, 4.0])
print(softmax_Func(data))
# 결과 : [0.01705566 0.15703715 0.82590719]
print(0.01705566 + 0.15703715 + 0.82590719)
# label의 종류에 따라서 출력결과가 실수값이 나온다. 가장 큰 실수값의 인덱스를 취한다.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 2. 데이터불러오기 : 우리가 직집 데이터 생성
np.random.seed(42)
torch.manual_seed(42)
np.set_printoptions(suppress=True, precision=3)
print()

# 3. 변수설정
xdata = np.random.random((1000, 12)).astype(np.float32) # 12개의 특성을 입력받음 = 12개의 종속변수
ydata = np.random.randint(5, size=(1000,))              # 5개의 클래스 중 하나로 분류
print(xdata[:2])
print(ydata[:2])
# 결과 : 
# [[0.37454012 0.9507143  0.7319939  0.5986585  0.15601864 0.15599452
#   0.05808361 0.8661761  0.601115   0.7080726  0.02058449 0.96990985]  ->  3으로 분류
#  [0.83244264 0.21233912 0.18182497 0.1834045  0.30424225 0.52475643
#   0.43194503 0.29122913 0.6118529  0.13949387 0.29214466 0.36636186]] ->  2로 분류

# 4. tensor로 변환
x_tensor = torch.tensor(xdata, dtype=torch. float32)
y_tensor = torch.tensor(ydata, dtype=torch.long)
# nn.CrossEntropyLoss의 label의 long type이므로 길게 적어준다. : 
print(x_tensor.shape) # torch.Size([1000, 12])
print(y_tensor.shape) # torch.Size([1000])


# [2단계] : 모델 정의(다항분류 모델)
# 1. 모델 정의 -> Sequential  or  클래스
# 입력이 12개, 출려깅 5개이다
class MultiClassClassifier(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(12, 32), # 입력층
            nn.ReLU(),

            nn.Linear(32, 16), # 은닉츧
            nn.ReLU(),
            
            nn.Linear(16, 5)  # 출력층
        )
    
    def forward(self, x):
        return self.net(x)

model = MultiClassClassifier()
print(model)
# 결과 :
# MultiClassClassifier(
#   (net): Sequential(
#     (0): Linear(in_features=12, out_features=32, bias=True)
#     (1): ReLU()
#     (2): Linear(in_features=32, out_features=16, bias=True)
#     (3): ReLU()
#     (4): Linear(in_features=16, out_features=5, bias=True)
#   )
# )

# "이항분류 vs 다항분류"
#       구분                 <이항분류>                 <다항분류>
#   입력데이터(x)        2차원(N, features)         2차원(N, features)  ->  N : 입력데이터 갯수(Batch기준)
#     모델 출력          2차원(N, 1)                2차원(N, C)         ->  C : 분류할 클래스 갯수
#   정답데이터(y)        2차원(N, 1)                1차원(N,)
#   label 자료형         torch.float32              torch.long
#     손실 함수          BCEWithLogitsLoss()        CrossEntropyLoss() 
#    활성화 함수         Sigmoid()                  Softmax()

# : 출력데이터는 예측값을 말하고 정답데이터 모델이 학습을 할 때 받는 정답이다. 이때 정답데이터는 y이고
# 정답데이터는 손실함수(criterion)가 정답을 받는 방식이다.
# 예시) 클래스별 점수 : [[0.1, 0.3, 2.5, 0.2, 0.4],
#                       [0.2, 3.1, 0.1, 0.5, 0.3]]
#               정답 : [2, 1]  ->  첫 데이터는 2번, 두 번째는 1번 클래스

# model은 logit값을 내보낸다!!

logits = model(x_tensor)
print(torch.softmax(logits, dim=1).shape)
prob = torch.softmax(logits, dim=1)
print(prob.shape)
print(torch.argmax(prob, dim=1).shape)

# 2. 손실함수와 optimzer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr = 0.001)


# [3단계] : 모델 학습
EPOCHS = 100
BATCH_SIZE = 32

history = {
    "loss": [],
    "accuracy" : []
    }

data_size = len(x_tensor)

for epoch in range(EPOCHS):
    model.train()
    indices = torch.randperm(data_size)

    epoch_loss_sum = 0
    epoch_correct = 0
    epoch_total = 0

    for start in range(0, data_size, BATCH_SIZE):
        batch_idx = indices[start:start + BATCH_SIZE]
        x_batch = x_tensor[batch_idx]
        y_batch = y_tensor[batch_idx]

        logits = model(x_batch)
        loss = criterion(logits, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss_sum += loss.item() * x_batch.size(0)
        pred_class = torch.argmax(logits, dim=1) # 예측 class

        epoch_correct += (pred_class == y_batch).sum().item()
        epoch_total += y_batch.size(0)

    epoch_loss = epoch_loss_sum / epoch_total
    epoch_acc = epoch_correct / epoch_total
    history["loss"].append(epoch_loss)
    history["accuracy"].append(epoch_acc)
    print(f'Epoch {epoch + 1:04d} / {EPOCHS} - LOSS:{epoch_loss:.4F} - accuracy : {epoch_acc:.4f}')


# [4단계] : 모델 평가
model.eval()

with torch.no_grad():
    logits = model(x_tensor)
    loss = criterion(logits, y_tensor).item()
    pred_class = torch.argmax(logits, dim=1)
    acc = (pred_class == y_tensor).sum().item()

print('모델 평가 결과 : ', [loss, acc])

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history['loss'])
ax1.set_title('loss')
ax1.set_xlabel('epoch')
ax1.set_ylabel('loss')
ax1.grid(True)

ax2.plot(history['accuracy'])
ax2.set_title('accuracy')
ax2.set_xlabel('epoch')
ax2.set_ylabel('accuracy')
ax2.grid(True)

plt.show()