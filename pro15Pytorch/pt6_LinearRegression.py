
# 인공지능(AI) - 머신러닝 : 데이터에서 규칙(패턴)을 학습
#                     - 선형회귀
#                     - 로지스틱회귀
#                     - 결정트리, 랜덤포레스트
#                     - 신경망(Perceptron) - 딥러닝 : 여러 층을 쌓은 깊은 신경망

# 머신러닝과 딥러닝 모두 회귀와 분류가 가능하다.
# 회귀 ->   머신러닝 : 선형 회귀, 랜덤 포레스트 등
#           딥러닝 : 	숫자를 출력하는 신경망
# 분류  ->  머신러닝 : 로지스틱 회귀, 랜덤 포레스트 등
#           딥러닝 : 범주별 점수·확률을 출력하는 신경망

# 우리가 일반적으로 한 머신러닝 생성과정 : 데이터 불러오기 및 변수 설정  →  모델 생성 및 학습  →  모델 예측 및 평가
# 신경망(딥러닝)은 '모델 생성 및 학습'part에서 
# 입력 데이터(batch)
#        ↓
# 모델이 예측
#        ↓
# 정답과 비교해서 loss 계산
#        ↓
# 역전파로 기울기 계산
#        ↓
# optimizer가 가중치 수정
#        ↓
# 다음 batch로 반복
# 로 바뀐다.

# 즉, 
# [1단계] : 데이터 불러오기 및 변수 설정 
# [2단계] : 딥러닝 구조로 모델 학습 : 입력데이터 → 모델이 예측 → 정답과 비교해서 loss계산 → 역전파로 기울기 계산 → optimizer가 가중치 수정 → 다음 batch로 이동하여 반복
# [3단계] :


# **다중선형회귀**

# 다중선형회귀모델을 사용하여 딥러닝 모델을 만들어보자 : tv, radio, newspaper가 sales에 얼마나 영향을 주는가?

# 다중선형회귀모델을 딥러닝 모델로 만들기
# [1단계] 데이터 불러오기 및 변수 설정
# 1. lib불러오기
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import r2_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
# 이 lib는 딥러닝을 위해서 고정이다.

# 2. 데이터 불러오기
data = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head(2))

# 3. 불러온 데이터 전처리 : 'no'열 처리
del data['no'] # = python명령어
# data.drop('no', axis=1, inplace=True) # 위와 동일 # = pandas명령어
print(data.head(2))

# 4. 독립변수와 종속변수 설정(feature, label분리)
fdata = data[['tv', 'radio', 'newspaper']]
ldata = data.iloc[:, 3] # sales
print(fdata.head(2))
print(ldata.head(2))

# 5. 표준화 및 정규화
# feature(독립변수) 정규화 - model성능 향상에 효과적이다.
fnomaldata = minmax_scale(fdata, axis=0, copy=True) # 컬럼(axis=0)기준으로 0에서 1사이의 범위로 '정규화'함
print(fnomaldata[:2])

# 6. Overfitting 해결
# - train/test split O
# - KFold
# - GridSearCV
# - L1, L2규제
x_train, x_test, y_train, y_test = train_test_split(fnomaldata, ldata, shuffle=True, test_size=0.3, random_state=1)

# 7. Tensor로 변환 : 딥러닝 모델이 학습할 수 있는 데이터type으로 바꿔주기
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).reshape(-1, 1)
y_test_tensor = torch.tensor(y_test.to_numpy(), dtype=torch.float32).reshape(-1,1)
# y_train_tensor, y_test_tensor는 해당 값만 가져와야하기 때문에 .values나 .to_numpy()를 붙인다.  
# .reshape(-1, 1)을 하여 2차원으로 바꿔주어야한다. train과 test데이터의 차원을 같게(2차원으로) 만들어 주어야한다!
# = numpy배열로 반환해준 다음 tensor배열로 바꾼다.

# 8. Validation dataset을 설정
# 전체 200개의 데이터를 140개와 60개로 나누었다 : train : test = 7 : 3
# 우리는 train데이터 140개를 다시 내부적으로 나눌 것이다. = KFold
# train데이터에서 구간을 나누어서 140개 중 특정 부분이 train이라면 나머지는 validation dataset으로 설정한다. 
# Validataion dataset(검증용 데이터셋)에 대해서 '20%'를 학습 중 검증 데이터로 사용해보자.
# TensorDataset : 입력데이터(x)와 츨력데이터(y)를 하나의 Dataset으로 묶었다. 그 다음에 train/validation으로 나눈다(Randomsplit이용)
# feature와 label을 같은 인덱스끼리 한 쌍으로 묶어 pytorch의 데이터셋으로 만들었다.
train_dataset = TensorDataset(x_train_tensor, y_train_tensor) 
validation_size = int(len(train_dataset) * 0.2)
train_size = len(train_dataset) - validation_size

train_subset, validation_subset = random_split(
    train_dataset, 
    [train_size, validation_size], 
    generator=torch.Generator().manual_seed(123)
)
# 학습용 데이터셋을 하나로 붂었다(train_dataset) 그리고 묶인 train_dataset을 train_subset, validation_subset으로 나누었다.
# train data(70%) : 140개  ->  train_subset(80%)      : 112개
#                          ->  validation_subset(20%) : 28개
# test data(30%) : 60개
print(len(train_dataset), '-->', len(train_subset), len(validation_subset))

# train : 모델의 학습에 사용,
# validation : 학습 도중 평가에 사용
# test : 마지막 최종 평가에 사용


# [2단계] : 데이터 묶고 불러오기(batch, Dataloader) -> 나중에 모델이 불러올 수 있게 만들어주기
# batch란? : 모델이 한 번에 학습하는 데이터 묶음 = 한번에 처리하는 데이터의 양 = 1epoch동안 처리하는 데이터의 양
# DataLoader : data를 미니batch 단위로 꺼내주는 역할
# - 전체 데이터를 한방에 모델에 주지 않고, 지정한 수 만큼 잘라서 반복적으로 모델에 공급한다.
# - GPU나 CPU의 병렬 연산을 극대화 할 수 있다.

# 1. 데이터를 일정 단위로 묶고 꺼내기
batch_size = 32 # 미니batch의 크기
# 이제 데이터셋을 32개를 기준으로 묶었다.

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
validation_loader = DataLoader(validation_subset, batch_size=batch_size, shuffle=True)
# 32개를 단위로 묶은 데이터를 32개씩 꺼내오기 = DataLoader

test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
# 학습데이터만 shuffle한다!!
# shuffle이란? : 데이터를 batch로 나누기 전에 순서를 섞을지 정하는 옵션
# 보통 학습데이터(train)는 순서에 따른 영향을 줄이기 위해서 섞고 평가데이터(test)는 섞지 않는다.

# 이렇게 train_loader, validation_loader, test_loader가 만들어졌다.
print()


# [3단계] : 모델 학습 함수 정의 : 모델을 학습시키고, 매 epoch마다 loss 계산 (train데이터셋, validation데이터셋)
# 학습할 '신경망 모델' 생성 ... 함수로 구현함
def train_model_Func(model, train_loader, validation_loader, criterion, optimizer, epochs=500):
    # 모델을 학습  ->  예측값 계산  ->  손실계산  ->  gradient초기화  ->  역전파  ->  파라미터 갱신  ->  loss계산
    
    # 1. 손실값을 저장할 칸[] 만들기 = history
    history = {
        "loss" :[],
        "validation_loss" : []
        }

    # 2. 모델을 학습모드로 변경 : train데이터셋(A)과 validation데이터셋(B)에 대해서 손실값(loss)구하기
    for epoch in range(epochs):

        # A. train 데이터셋
        model.train()
        train_loss_sum = 0  # 각 batch의 loss를 누적

        for x_batch, y_batch in train_loader: # data_loader에서 batch단위로 데이터를 가져온다.
            # 1) 예측값 계산
            pred = model(x_batch)

            # 2) 손실값 계산
            loss = criterion(pred, y_batch)

            # 3) 이전 gradient초기화
            optimizer.zero_grad()

            # 4) 역전파
            loss.backward()

            # 5) 파라미터 갱신(weight, bias)
            optimizer.step()

            # 6) loss누적(필수X)
            train_loss_sum += loss.item()

        # **학습용 데이터 손실(loss)값의 평균**
        train_loss = train_loss_sum / len(train_loader)
        # 1개의 epoch에서 평균loss가 만들어진다.
        

        # B. validation 데이터셋 :  검증/평가 mode로 전환(직접 평가를 수행하는 것X, 단순히 선언)
        model.eval()

        validation_loss_sum = 0  
        # validation데이터에 대한 loss를 누적

        with torch.no_grad():
            for x_validation, y_validation in validation_loader:
                validation_pred = model(x_validation)
                validation_loss = criterion(validation_pred, y_validation)
                validation_loss_sum += validation_loss.item()
                # validation에 대한 loss값을 구함
        
        # **검증용 데이터 손실(loss)값의 평균**
        validation_loss = validation_loss_sum / len(validation_loader)
        # 1개의 epoch에서 validatioin loss의 평균을 계산한다.

        history["loss"].append(train_loss)
        history["validation_loss"].append(validation_loss)

        # 학습 진행 상황 출력
        if (epoch + 1) % 10 == 0:
            print(
                f"\nEpoch(반복횟수) :  [{epoch + 1} / {epochs}]"
                f"train_loss값 : [{train_loss:.5f}]"
                f"validation_loss값 : [{validation_loss:.5f}]"
            )
            
    return history

# [4단계] : 모델 예측 및 평가 함수 정의(test데이터셋)
# 모델 평가 ... 함수로 구현함
def evaluate_model_Func(model, x_test_tensor, y_test_tensor, criterion):
    model.eval() # 평가 모드로 전환(빼도 되지만 관습저긍로 적는다)
    with torch.no_grad(): # 평가만 하고 역전파로 미분을 하는 것은 아니기 때문에 no_grad, 즉, 미분안함을 적어준다.
        pred = model(x_test_tensor)
        loss = criterion(pred, y_test_tensor)

    return loss.item(), pred # 손실값과 예측값을 둘 다 돌려주는 것임


print()
# [5단계] : model생성 - 3가지 중 첫번째 방식 ... 위 [4단계], [5단계]에서 사용할 model을 생성한다.
# 1. model 작성 방법1 : Sequential 클래스 사용
model1 = nn.Sequential(
    nn.Linear(3, 16), # 3개 노드가 있는 하나의 입력층이 16개의 노드를 가지고 있는 은닉층과 연결된다. 
    nn.ReLU(),
    nn.Linear(16, 8), # 16개의 노드를 가지고 있는 1번 은닉층이 8개의 노드를 가지고 있는 은닉층과 연결된다.
    nn.ReLU(),
    nn.Linear(8, 1) # 8개의 노드를 가지고 있는 2번 은닉층이 1개의 노드를 가지고 있는 출력층과 연결된다.
)
# Dense층을 늘리면 생기는 효과
# 1. 표현력 증가에 유리하다 : 층이 많아지면 더 복잡한 비선형 관계를 학습할 수 있다. 특히 입력과 출력 사이의 복잡한 패턴이 있는 경우
# 2. 과적합 위험 증가 : 데이터가 적은데 층을 많이 쌓으면 학습 데이터만 너무 잘 맞고, 실제 테스트 데이터는 성능이 나쁠 수 있다
# 3. 학습시간증가 : 파라미터가 많아지면 학습 시간이 길어지고, 최적화가 어려워질 수 있다.
# 4. 데이터 크기 영향 : 적은 수의 샘플만 있는 아주 작은 dataset인 경우 층을 늘려봤자 오히려 과적합이 더 심해질 가능성이 크다.

# 정성적model은 layer를 많이 줘도 상관없지만 정량적model은 많이 줄 필요가 없다.
# 실전에서는 많은 층(layer)을 주고 그다음에 줄여나가는 방식을 쓴다.
print(model1)

# 2. 손실함수와 옵티마이저 정의(학습율)
# 손실함수 : 얼마나 틀렸는지 오차를 계산하는 함수 = 예측과 정답의 차이(오차)를 어떻게 계산할 지
# 옵티마이저 : 오차를 줄이도록 모델의 가중치를 수정한느 도구 = 어떤 parameter를 어떤 방식(SGD/Adam/AdaGrad)으로 수정할지
criterion = nn.MSELoss()
optimizer = optim.Adam(model1.parameters(), lr=0.01) # lr은 0.001이 기본값이다. 그래서 우리가 직접 조정해가면서 사용한다.
# 모델의 예측값과 실제값에 차이가 발생하면 이 차이(오차)를 손실함수가 계산한다. 그리고 나서 '역전파'가 시작된다.
# '역전파' : 오차를 줄이려면 가중치를 어느 방향으로 바꿔야 하는지 계산하는것
# 이 역전파 과정에서 '옵티마이저'는 오차의 정보를 이용하여 가중치를 수정한다.

# 3. 모델 학습 ... [4단계]와 이어짐
history = train_model_Func(
    model=model1, 
    train_loader=train_loader, 
    validation_loader=validation_loader, 
    criterion=criterion, 
    optimizer=optimizer, 
    epochs=500
) # [4단계]에서 만든 함수(def train_model_Func)를 불러옴

# 4. 모델 평가 ... [5단계]와 이어짐
evaluation_loss, pred_tensor = evaluate_model_Func(
    model = model1,
    x_test_tensor = x_test_tensor,
    y_test_tensor = y_test_tensor,
    criterion = criterion
) # [5단계]에서 만든 함수(def evaluate_model_Func)를 불러옴


# [6단계] : test 데이터에 대한 최종 평가 결과 출력(MSE, RMSE, R²)
# test데이터로 평가를 수행하는 함수에 대한 값
print("test 데이터의 손실값 : ", evaluation_loss)

# 1. MSE, RMSE, R2 확인 : 예측값이 실제값과 얼마나 차이나는지 보여주는 값
pre = pred_tensor.numpy()
actual = y_test_tensor.numpy()
print('MSE : ', evaluation_loss)
print('RMSE : ', np.sqrt(evaluation_loss))
print('설명력 : ', r2_score(actual, pre))
# 결과 :
# test 데이터의 손실값 :  25.43218994140625
# MSE :  25.43218994140625
# RMSE :  5.043033803317825
# 설명력 :  0.03198683261871338
# RMSE를 본다.
# 해석 : test데이터에 대해서 예측값과 실제값의 차이가 5.04정도 차이가 난다.

# 2. history값 확인
# history : 학습하면서 나온 손실값을 epoch마다 저장하는 기록장 ... 146번째 코드
# print('history validation_loss : ', history['validation_loss'])
# print('history loss : ', history['loss'])

# 3. 손실함수값 시각화
plt.plot(history['validation_loss'], label="validation_loss")
plt.plot(history['loss'], label='loss')
plt.legend()
plt.show()


# 딥러닝모델 제작 <핵심 요약> 
# [1단계] : 데이터 불러오기 및 변수 설정
# [2단계] : 데이터 묶고 불러오기(batch, Dataloader)
# [3단계] : 모델 학습 함수 정의
# [4단계] : 모델 예측 및 평가 함수 정의
# [5단계] : model생성
# [6단계] : test 데이터에 대한 최종 평가 결과 출력(MSE, RMSE, R²)

# =

# 딥러닝 모델 제작 <핵심 요약>
# [1단계] : 데이터 불러오기, 입력(X)·정답(y) 설정 및 전처리
# [2단계] : train / validation / test dataset 분리 및 Dataset·DataLoader 구성
# [3단계] : 학습 함수 정의(예측 → 손실 계산 → 역전파 → 가중치 수정, 검증 및 history 기록)
# [4단계] : 평가 함수 정의(test 데이터의 예측값과 손실값 반환)
# [5단계] : 모델 생성, 손실함수 및 옵티마이저 설정 그리고 학습·평가 실행
# [6단계] : test 데이터의 최종 평가 결과 출력(MSE, RMSE, R²)


print("\n\n")
# [5단계] : model생성 - 3가지 중 두 번째 방식 ... 위 [4단계], [5단계]에서 사용할 model을 생성한다.
# 2. model 작성 방법2 : nn.Module 클래스를 상속받아서 사용한다.
class AdverRegressionModel(nn.Module):
    # 1. 딥러닝 모델의 구조 선언
    def __init__(self):
        super(). __init__()

        # layer 정의
        self.hidden_layer1 = nn.Linear(3, 16)
        self.hidden_layer2 = nn.Linear(16, 8)
        self.output_layer = nn.Linear(8, 1)

        # Activation Function 정의
        self.relu = nn.ReLU()

    # 2. 데이터의 흐름을 정의
    def forward(self, inputs):
        net = self.hidden_layer1(inputs)
        net = self.relu(net)

        net = self.hidden_layer2(net)
        net = self.relu(net)

        outputs = self.output_layer(net)

        return outputs
    # Multi Layor Perceptron구조를 보임. 즉 MLP는 딥러닝모델이라고 부를 수 있다!!
    # MLP = DeepLearning Model

model2 = AdverRegressionModel()
print(model2)

for param in model2.parameters(): # model2의 parameter를 뽑는다.
    print(param)

for name, param in model2.named_parameters(): # 각 parameter의 이름을 확인한다.
    print(name, ":", param.data)
# weight와 bias를 확인할 수 있다.

# 2. 손실함수와 옵티마이저 재정의(model2를 위한 새로운 optimizer)
criterion = nn.MSELoss()
optimizer2 = optim.Adam(model2.parameters(), lr=0.01) 

# 3. 모델 학습 ... [4단계]와 이어짐
history2 = train_model_Func(
    model=model2, 
    train_loader=train_loader, 
    validation_loader=validation_loader, 
    criterion=criterion, 
    optimizer=optimizer2, 
    epochs=500
) # [4단계]에서 만든 함수(def train_model_Func)를 불러옴


# 4. 모델 평가 ... [5단계]와 이어짐
evaluation_loss2, pred_tensor2 = evaluate_model_Func(
    model = model2,
    x_test_tensor = x_test_tensor,
    y_test_tensor = y_test_tensor,
    criterion = criterion
) # [5단계]에서 만든 함수(def evaluate_model_Func)를 불러옴

print("evaluation_loss2 : ", evaluation_loss2)

# [6단계] : test 데이터에 대한 최종 평가 결과 출력(MSE, RMSE, R²)
# 1. MSE, RMSE, R2 확인 : 예측값이 실제값과 얼마나 차이나는지 보여주는 값
pre2 = pred_tensor2.numpy()
actual = y_test_tensor.numpy()
print('MSE : ', evaluation_loss2)
print('RMSE : ', np.sqrt(evaluation_loss2))
print('설명력 : ', r2_score(actual, pre2))
# 결과 : 
# evaluation_loss2 :  0.3714103400707245
# MSE :  0.3714103400707245
# RMSE :  0.6094344427998178
# 설명력 :  0.9850699305534363


# model1과 model2의 설명력에 차이가 생기는 이유
# model1과 model2의 설명력에 차이가 생기는 이유
# 두 모델은 층 구조(3 → 16 → 8 → 1), ReLU, Adam(lr=0.01), 학습 횟수(500 epoch)가 같다.
# 1. 초기값 차이 : 모델을 따로 생성하므로 nn.Linear의 무작위 초기 가중치와 편향이 다르다.
#                 model2는 model1이 학습한 가중치를 이어받지 않고 새 초기값에서 학습한다.
# 2. 학습 순서 차이 : train_loader의 shuffle=True로 매 epoch마다 batch 구성과 순서가 달라진다.
#                    같은 DataLoader를 사용해도 model1과 model2가 같은 순서로 학습하는 것은 아니다.
# 3. 데이터 분할은 동일 : 두 모델은 같은 train·validation·test 데이터를 사용한다.
#                       random_state=1과 분할용 generator의 manual_seed(123)은 데이터 분할을 고정한다.
#                       이 설정이 두 모델의 초기 가중치와 학습 순서까지 같게 만드는 것은 아니다.

# 따라서 초기값과 학습 순서 차이 → 최종 가중치 차이 → 예측값 차이 → RMSE와 R² 차이가 생긴다.
# Sequential 방식과 nn.Module 상속 방식 자체가 성능 차이의 원인은 아니다.
