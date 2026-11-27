# 이전시간에는 임의의 우리가 직접 만든 데이터로 classification을 해보았다면 
# 이번에는 실제 데이터셋으로 DeepLearning모델의 classification을 해보자

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
wineDataFrame = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/wine.csv", header=None) # 열 이름이 없을 때, header=None 해주어야 한다.
print(wineDataFrame.head(2))
print(wineDataFrame.info())
# wineDataFrame데이터셋이란? : 와인의 '성분'과 '품질 점수', '와인 종류'를 담은 데이터
#                             한 행이 와인 한 개를 나타내며, 총 6,497행, 13개 열로 구성
#                             12개 열은 UCI Wine Quality에 해당하는 성분 및 품질점수들 = feature
#                             마지막 1개 열에서 '1'은 레드와인, '0'은 화이트와인에 해당 = label
# "이 와인의 성분과 품질을 보고 레드인지 화이트인지 맞힐 수 있을까?"
print(wineDataFrame.iloc[:, 12].unique())
print(len(wineDataFrame[wineDataFrame.iloc[:, 12] == 0])) # 마지막 열 '0'인 와인(화이트와인)의 갯수 : 4898개
print(len(wineDataFrame[wineDataFrame.iloc[:, 12] == 1])) # 마지막 열 '1'인 와인(레드와인)의 갯수   : 1599개

# 3. 변수설정
dataset = wineDataFrame.values
x = dataset[:, 0 : 12].astype(np.float32) # [모든 행, 모든 열] -> [0번 행 : x-1번 행까지, 0번 열 : y-1번 열까지]
y = dataset[:, -1].astype(np.float32) # 맨마지막 열만
print(x[:2])
print(y[:2])

# 4. Overfitting해결
# - train / test split() o
# - KFold
# - GridSearchCV
# - L1, L2 규제
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, stratify=y, shuffle=True, random_state=12
)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
# 결과 : (4547, 12) (1950, 12) (4547,) (1950,)
# train입력 -> 와인 4,547개, 각각 특성 12개 : (4547, 12) 
#  test입력 -> 와인 1,950개, 각각 특성 12개 : (1950, 12) 
# train정답 -> 와인 종류 4,547개            : (4547,) (1950,)
#  test정답 -> 와인 종류 1,950개            : (1950,)
# : train데이터 45

# 5. 표준화 및 정규화(scaling)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train).astype(np.float32)
x_test_scaled = scaler.fit_transform(x_test).astype(np.float32)
# x_train과 x_test를 정규화해줌

# 6. train데이터를 train / validation으로 분리
# 현재 train데이터 : test데이터 = 7 : 3으로 분류되어 있는데 여기서 train데이터를 다시 train데이터 : validation데이터로 분류할 것이다.
x_train_part, x_validation, y_train_part, y_validation = train_test_split(
    x_train_scaled, y_train, test_size=0.2, stratify=y_train, random_state=42
)
# 여기서 y_train이 왜 들어가지...?
print('train용 데이터 : ', x_train_part.shape, y_train_part.shape)
print('validation용 데이터 : ', x_validation.shape, y_validation.shape)
print('test용 데이터 : ', x_test_scaled.shape, y_test.shape)
# 결과 : 6497개의 데이터 중에
# train용 데이터      :  (3637, 12) (3637,)
# validation용 데이터 :  (910, 12) (910,)
# test용 데이터       :  (1950, 12) (1950,)

# wineDataFrame(100%) : 6497개 - train(70%) : 4547개 - train(80%)      : 3637개
#                                                    - validation(20%) : 910개 
#                              - test(30&) : 1950개
print()

# 7. nd.array(2차원)  ->  torch.tensor(2차원)
# 1) train용 데이터(80%)를 tensor자료형으로 바꾸기
x_train_tensor = torch.tensor(x_train_part, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train_part.reshape(-1, 1), dtype=torch.float32)
# y_train_tensor = torch.tensor(y_train_part, dtype=torch.float32).view(-1, 1) # 위와 동일

# 2) validation용 데이터(20%)를 tensor자료형으로 바꾸기
x_validation_tensor = torch.tensor(x_validation, dtype=torch.float32)
y_validation_tensor = torch.tensor(y_validation.reshape(-1, 1), dtype=torch.float32)

# 3) test용 데이터(전체의 30%)를 tensor자료형으로 바꾸기
x_test_tensor = torch.tensor(x_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.reshape(-1, 1), dtype=torch.float32)

# 이렇게 array형태의 2차원 배열을 tensor형태의 2차원 배열로 바꾸어준다! ... 딥러닝을 위해서!

# 8. mini batch 처리 : DataLoader 생성
# DataLoader : 전처리된 데이터를 모델이 들고 갈 수 있게 해주는 녀석
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) 
# TensorDataset에 있는 데이터 객체를 DataLoader가 64개씩 순서를 바꿔가면서 꺼낸다. 


# [2단계] : 모델 정의 및 criterion, optimizer 제작
# 1. 모델 정의(신경망 제작) -> 2가지 방법 - Sequential
#                                       - 클래스 모듈 사용
class WineClassifier(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(12, 32), # 입력층 # feature변수 갯수만큼 들어오게 된다 = 12개!!, 즉 입력층의 node의 갯수는 입력feature변수 갯수와 동일하다.
            nn.ReLU(),

            nn.Linear(32, 24), # 은닉층1
            nn.ReLU(),

            nn.Linear(24, 8),  # 은닉층2
            nn.ReLU(),

            nn.Linear(8, 1)    # 출력층
            # nn.Sigmoid() -> 아래쪽 손실함수(criterion)에서 BCEWithLogitsLoss()를 쓰면 nn.Sigmoid()를 안써도 된다!
        )

    def forward(self, x): # 입력데이터x를 모델에 통과시켜 결과를 반환하는 함수
        return self.net(x) # wineDataFrame에서 와인 특성x(12개)에 따라서 self.net의 각 층에서 계산을 하고 red와인인지 white와인인지 0과 1로 분류하고 그 예측결과를 반환한다.
# 즉, 이 class WineClassifier는 입력값에 따른 예측값을 반환한다!

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
# device : 모델을 cpu에서 계산할지 gpu에서 계산할지 정하는 변수
# 현재 와인 데이터를 학습시키는 '계산'을 gpu에서 할지 아니면 cpu에서 할지 정하려고 함
print("사용장치 : ", device)
# True  -> CUDA gpu사용
# False -> cpu 사용
# 내 컴퓨터는 cpu를 사용함...device라는 변수에 cpu라는 장소(주소)가 저장됨

model = WineClassifier().to(device=device) # device를 class wineClassifier로 옮김
print(model)
# '모델'과 계산에 사용하는 '텐서데이터'는 같은 장치에 있어야 한다. GPU로 학습한다면 입력과 정답도 함께 옮겨야 한다.
# 즉, device를 사용하면 GPU가 있는 환경에서는 GPU로, 없는 환경에서는 CPU로 실행할 수 있다.

# 2. 손실함수, optimizer정의
# 1) 손실함수
# criterion = nn.BCELoss() ... 이걸 적으려면 class WineClassifier의 마지막에 nn.Sigmoid()를 적어주어야 한다.
criterion = nn.BCEWithLogitsLoss() # 그런데 이렇게 내부적으로 sigmoid + BinaryCrossEntropy를 한번에 처리한다. 그래서 위 class WineClassifier에서 nn.Sigmoid()를 적지 않아도 된다!

# 2) optimizer
optimizer = optim.Adam(model.parameters(), lr=0.01)
print()

# [3단계] : 모델 평가 및 예측
# 1. 모델 평가
def evaluate_model_Func(model, x_data, y_data):
    model.eval()
    x_data = x_data.to(device)
    y_data = y_data.to(device)

    with torch.no_grad():
        logits = model(x_data) # pred
        loss = criterion(logits, y_data).item()

        # logits  ->  sigmoid(확률)  ->  0,1
        prob = torch.sigmoid(logits)
        pred = (prob >= 0.5).float() # True:1, False:0
        acc = (pred == y_data).float().mean().item()

    return loss, acc

# 참고로 훈련되지 않은 모델의 정확도를 먼저 확인해보자
train_loss_before, train_acc_before = evaluate_model_Func(
    model, x_train_tensor, y_train_tensor
)
print(f"훈련되지 않은 model의 정확도는 ? : {train_acc_before * 100:.2f}%")
# 결과 : 75.39
# = train으로 학습하지 않은 model의 정확도가 75.39만큼 나온다.
print()

# [4단계] : 조기종료 + 모델 저장 준비
patience = 5
best_validation_loss = np.inf
patience_count = 0

MODEL_DIR = './winemodel/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

modelpath = './winemodel/winmodel_torch.pth'


# [5단계] : 모델 학습
EPOCHS = 5000
history = {
    'loss':[],
    'accuracy':[],
    'validation_loss':[],
    'validation_accuracy':[]
}

for epoch in range(EPOCHS):
    model.train()
    train_loss_sum = 0
    train_correct = 0
    train_total = 0

    for batch_x, batch_y in train_loader:
        # 4547개의 데이터를 batch사이즈(64개)씩 72번 학습하는 것이 1epoch이고 이 epoch을 최대 5000번 반복한다. 
        # 하지만 조기 종료 조건을 만족하면 그 전에 만족한다.
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        logits = model(batch_x) # 예측값 계산 : logits은 -무한대 ~ +무한대 사이의 값을가진다
        loss = criterion(logits, batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss_sum += loss.item() * batch_x.size(0)

        prob=torch.sigmoid(logits) # -무한대 ~ +무한대 사이의 값을 0과 1사이의 정성적인 값으로 바꿈...분류를 위해서 
        pred = (prob >= 0.5).float()

        train_correct += (pred == batch_y).sum().item()
        train_total += batch_y.size(0)

    # epoch 단위 train loss / accuracy 계산
    train_loss = train_loss_sum / train_total
    train_acc = train_correct / train_total

    # validation 평가
    validation_loss, validation_acc = evaluate_model_Func(model, x_validation_tensor, y_validation_tensor)

    history['loss'].append(train_loss)
    history['accuracy'].append(train_acc)
    history['validation_loss'].append(validation_loss)
    history['validation_accuracy'].append(validation_acc)

    print(
        f"Epoch [{epoch+1} / {EPOCHS}]"
        f"loss : {train_loss:.4f}"
        f"accuracy : {train_acc:.4f}"
        f"validation_loss : {validation_loss:.4f}"
        f"validation_accuracy : {validation_acc:.4f}"
    )

    # 최고의 모델 저장
    if validation_loss < best_validation_loss:
        best_validation_loss = validation_loss
        patience_count = 0

        # 최적 모델의 parameter 저장
        torch.save(model.state_dict(), modelpath)
        print(f"최적 모델 저장 : {epoch + 1}, val_loss:{best_validation_loss:.5f}")
    else:
        patience_count += 1

    # 조기 종료 : patience 횟수만큰 validation_loss가 개선되지 않으면 조기 종료
    if patience_count >= patience:
        print(f'조기 종료가 발생했다. ... 어디서?  ->  {epoch + 1}번에서 학습 중단')
        break

print('\n학습완료 ---')
print('전체 학습 횟수 : ', len(history['loss']))
print('최적 학습 횟수 : ', np.argmin(history['loss']) + 1)
print('최소 검증 손실 : ', best_validation_loss)

# 저장된 최적의 모델 읽기 ~~~~~~~
# 이제 winemodel폴더에 새로 생긴 녀석이 학습한 모델이다.

# 저장된 모델(winmodel_torch.pth) 불러오기
best_model = WineClassifier().to(device=device)
best_model.load_state_dict(torch.load(modelpath, map_location=device))
# map_location이 cpu일수도 gpu일수도 있다.

best_model.eval()
# test data로 평가
test_loss, test_acc = evaluate_model_Func(best_model, x_test_tensor, y_test_tensor)

# 이번에는 test데이터로 학습이 된 모델의 최종적인 정확도를 알아보자.
print(f"훈련된 모델의 정확도 : {test_acc * 100:.2f}%")
print(f"test 데이터에 대한 손실(loss) : {test_loss:.4f}") # 99.44%
# 결과 : 
# 전체 학습 횟수 :  12
# 최적 학습 횟수 :  11
# 최소 검증 손실 :  0.008184617385268211
# 훈련된 모델의 정확도 : 99.44%
# test 데이터에 대한 손실(loss) : 0.0447

# 시각화1 - loss값
epoch_len = np.arange(len(history['loss']))
plt.figure(figsize=(8, 5))
plt.plot(epoch_len, history['validation_loss'], c='red', label='validation_loss')
plt.plot(epoch_len, history['loss'], c='blue', label='loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.grid()
plt.show()

# 시각화2 - accuracy값
plt.figure(figsize=(8, 5))
plt.plot(epoch_len, history['validation_accuracy'], c='red', label='validation_acc')
plt.plot(epoch_len, history['accuracy'], c='blue', label='accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.grid()
plt.show()

# 저장된 모델로 예측
new_data = x_test[:5, :]
print("원본 데이터 : ", new_data)

# 스케일링  ->  텐서화
new_data_scaled = scaler.fit_transform(new_data)
new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32).to(device)

with torch.no_grad():
    logits = best_model(new_data_tensor)  # "-무한대 ~ +무한대의 값을
    new_prob = torch.sigmoid(logits)      # 0과 1사이의 확률값으로 바꾸어줌"
    new_pred = (new_prob >= 0.5).int()

print('예측확률 : ', new_prob.cpu().numpy().ravel())
print('예측결과 : ', new_pred.cpu().numpy().ravel())
print('실제정답 : ', y_test[:5].astype(int))
