# 우리는 이제부터 Regression(지도학습), Classification(지도학습), Clustering(비지도학습)을 딥러닝으로 모델을 제작하여 학습할 것이다.
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# **단순선형회귀모델**

# 단순선형회귀모델(Regression)을 딥러닝 모델로 만들어보자
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score
import torch
import torch.nn as nn
import torch.optim as optim
# 앞으로 이 lib는 자주 이용한다!

# 데이터 : feature, label은 2차원 형태로 입력  -> 왜? Pytorch의 linear 계층은 입력 shape을 보통 (데이터 갯수, feature수)형태로 받는다. = 2차원 형태로 받는다.
xdata = np.array([  1,   2,   3,   4,   5], dtype='float32').reshape(-1, 1)
ydata = np.array([1.2, 2.0, 3.0, 3.5, 5.5], dtype='float32').reshape(-1, 1)
print('상관계수 : ', np.corrcoef(xdata.ravel(), ydata.ravel()))
# 결과 :
# 상관계수 :  [[1.          0.97494708]
#              [0.97494708          1.]]
# 두 변수의 상관계수는 0.97이기때문에 강한 양의 상관관계를 띄고 있다.

# numpy배열을 Pytorch Tensor로 변환(딥러닝으로 사용하기 위해 = 동적 그래프를 계산하기 위해서)
# x_tensor = torch.tensor(xdata, dtype=torch.float32, requires_grad=True) # requires_grad = True는 미분이 가능함을 의미
x_tensor = torch.tensor(xdata, dtype=torch.float32) # nn.Linear()내부에 이미 설정이 되어 있기에 굳이 requires_grad=True는 안주어도 된다.
y_tensor = torch.tensor(ydata, dtype=torch.float32)

# 모델 정의(MLP : DeepLearning)
model = nn.Sequential(
    nn.Linear(1, 5),  # feature 1개  ->  은닉 노드 5개(하나의 layer에 5개의 node가 존재한다.)
    nn.ReLU(),        # 활성화함수(activation function) : ReLU함수 사용
    nn.Linear(5, 1)   # 은닉노드 5개  ->  출력 1개.  출력층에 activation function이 없으면 Linear출력
)

# 활성화함수의 종류 -> ReLU(음수는 0, 양수는 그대로 출력), Lekaky ReLu, ELU 
#                     Sigmoid(0~1 사이로 변환), 
#                     Tanh(-1~1 사이로 변환), 
#                     Softmax(여러 출력값을 합이 1인 확률로 변환)
# 활성화함수의 역할 : 신경망의 각 층 사이에 비선형성을 도입하여, 심층 신경망이 더 복잡한 데이터를 효과적으로 볼 수 있게 돕는다.
print(model)
# Sequential(
# (0) : Linear(in_features=1, out_features=5, bias=True)
# (1) : ReLU
# (2) : Linear(in_features=5, out_features=1, bias=True)
# )

# 손실함수와 옵티마이저 정의
criterion = nn.MSELoss()  #  regressuib(정량적 모델) 평균 제곱 오차 이용
optimizer = optim.SGD(model.parameters(), lr = 0.01) # 확률적 경사하강법 ... SGD 대신에 ADAM이나 RMSprob을 사용할 수도 있다
# LR(Learning Rate) : 신경망의 학습 속도를 조절, 너무 크거나(껑충껑충~) 너무 작으면(깨작깨작..) 학습이 잘 안될수 도 있다.

# 모델학습
# 예측값 계산  ->  손실계산  ->  gradient초기화  ->  역전파로 gradient걔산 ->  optimizer로 weight와 bias갱신

epochs = 100 # 전체 학습 데이터를 100번 반복학습
batch_size = 2 # 한번의 가중치 갱신에 데이터를 2개씩 처리함.

# aa = torch.tensor([10, 20, 30, 40, 50])
# indices = torch.randperm(len(aa))
# print(indices)      # tensor([1, 2, 4, 0, 3])
# print(aa[indices])  # tensor([20,30, 50, 10, 40])

for epoch in range(epochs):
    # shuffle=True효과를 주려면 매 epoch마다 데이터 인덱스를 섞는다.
    indices = torch.randperm(len(x_tensor)) # x_data를 인덱스를 무작위 순서로 섞는다.
    total_loss = 0

    # for idx in indices:   # batch size = 1이기 때문에 한 개씩 꺼내볼 수 있다.
    #     x_batch = x_tensor[idx].unsqueeze(0)  # (3, 4)  ->  [[3, 4]]  :  차원을 확대하였다.
    #     y_batch = y_tensor[idx].unsqueeze(0) 

    for i in range(0, len(x_tensor), batch_size):
        # batch_size만큼 인덱스를 슬라이싱
        batch_indices = indices[i:i + batch_size]

        x_batch = x_tensor[batch_indices]
        y_batch = y_tensor[batch_indices]

        # 첫번째 epoch에서 배치 구성 확인하기(batch_size만큼 데이터 묶여서 처리)
        if epoch == 0:
            print('batch_indices : ', batch_indices)
            print('x_batch : ', x_batch)
            print('y_batch : ', y_batch)
            print("x_batch shape : ", x_batch.shape)
            print("~~~" * 10)

        pred = model(x_batch)             # 1) 예측값 계산 : 내부적으로 weight * x + bias를 계산하였다.
        loss = criterion(pred, y_batch)   # 2) 손실값 계산(틀린정도)
        optimizer.zero_grad()             # 3) 이전 gradient 초기화
        loss.backward()                   # 4) 역전파
        optimizer.step()                  # 5) parameter갱신(weight, bias)
        
        total_loss += loss.item()

        print(f"Epoch [{epoch + 1} / {epochs}], loss:{total_loss / len(x_tensor)}")

# 딥러닝 모델 제작 끝!


# 모델 평가 : 평가 또는 예측 시에는 gradient 계산이 필요 없으므로 torch.no_grad() 사용
with torch.no_grad():
    pred_tensor = model(x_tensor) # 학습된 모델에 전체 데이터를 넣어 예측을 한다.
    loss_eval = criterion(pred_tensor, y_tensor)

print('loss_eval : ', loss_eval.item())

# 예측 결과 확인
# pred_tensor.detach() : pred_tensor를 자동미분그래프에서 분리
pred = pred_tensor.detach().numpy()
# pred = pred_tensor.numpy()
print('pred : ', pred.ravel())
print('real : ', ydata.ravel())

print("결정 계수(설명력) : ", r2_score(ydata, pred))

# 시각화
plt.scatter(xdata, ydata, color = 'r', marker='o', label = '실제 데이터')
plt.plot(xdata, pred, 'b--', label='예측 회귀선(추세선)')
plt.xlabel('feature')
plt.ylabel('label')
plt.legend()
plt.show()

# 새로운 값으로 예측(추론(inference))
new_x = np.array([1.5, 5.7, -3.0], dtype='float32').reshape(-1, 1) # reshape(-1, 1) : 열이 1개인 표 형태로 바꾼다.
new_x_tensor = torch.tensor(new_x, dtype=torch.float32)  # Pytorch모델이 계산할 수 있도록 Numpy배열을 Tensor로 바꾼다.
with torch.no_grad():  # 학습이 끝난 상태이므로 역전파를 하지 않는다.
    new_pred_tensor = model(new_x_tensor)

new_pred = new_pred_tensor.numpy()
print("새로운 값 예측 결과 : ", new_pred.ravel())