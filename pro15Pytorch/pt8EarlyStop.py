# 딥러닝으로 다중선형회귀 - Autompg 데이터셋

# 조기종료 (Early Stopping) : loss에 성능이 어느 순간 개선되지 않을 때 학습
# 불필요한 학습을 줄이고, Overfitting을 방지하기 위한 방법 중 하나로 주로 validation으로 많이 한다.

#    train데이터(70%)       test데이터(30%)
#           |
#   ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#   |               |
# train(80%)    validation(20) 
# 이때 train데이터에 대한 loss값을 역전파에 사용된다.
# validation데이터에 대한 loss값은 역전파에 사용되지 않고, 조기 종료 여부를 판단하고 최적의 모델을 선택하는 데 사용된다.
# test데이터는 역전파나 조기 종료 판단에 사용하지 않고, 학습 완료 후 loss값을 통해 모델의 일반화 성능을 최종 평가한다.

# epoch의 수를 우리가 직접 정하자고 하니까 쉽지가 않음. 그래서 early stopping(조기종료)를 통해서
# loss가 줄어들면 model의 성능이 좋아진다 = r2 score(설명력)이 1에 가까워진다 = MSE/RMSE는 0에 가까워진다.
# optimizer가 loss를 줄이는 방향으로 계속 epoch을 늘려가다가 어느순간 loss가 줄어들지 않는 구간이 나온다. 그 구간에서
# 우리는 epoch을 멈추면 된다. 하지만 그 구간을 찾는 것이 힘들다. tensorflow를 이용하여 loss가 떨어지지 않는 구간에서 조기 종료를 시킨다.
# Early Stopping이 된 구간에서의 모델을 RAM에 저장한다.

# [1단계] : 데이터 불러오기 및 변수설정
# 1. lib불러오기 
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

# 2. 재현성 설정
torch.manual_seed(123)
np.random.seed(123) # numpy의 난수 설정

# 3. data loading : 데이터 불러오기
datas = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/auto-mpg.csv", na_values='?')
# 데이터셋에 '?'가 6개 있는데 결측치로 처리한다.
print(datas.head(2))
del datas['car name']
print(datas[datas.isna().any(axis=1)]) # : 결측값(NaN)이 하나라도 있는 행을 찾아서 출력하는 코드
datas = datas.dropna()
print(datas.isna().sum())

# 4. 데이터 전처리 : 편의상 일부 칼럼 제거
datas.drop(
    ['cylinders', 'displacement', 'acceleration', 'model year', 'origin'],
    axis='columns', inplace=True
)
print(datas.head(1))
#     mpg  horsepower  weight
# 0  18.0       130.0    3504

# 5. Overfitting 해결  ->  train / test split : 샘플링으로 처리 : train데이터를 70%로 정의함 
train_dataset = datas.sample(frac=0.7, random_state=123)
test_dataset = datas.drop(train_dataset.index)
print(train_dataset[:1], train_dataset.shape) # (274, 3)  ->  실제 model생성할 때 사용되는 데이터의 수가 274개이다.
print(test_dataset[:1], test_dataset.shape)   # (118, 3)  ->  model생성시 사용되지 않고 test용으로 사용된다.
print()

# 6. 표준화 계산 : (요소값 - 평균) / 표준편차
train_stat = train_dataset.describe()
train_stat.pop('mpg') # 종속변수는 빼고 작업하자...
print(train_stat)
train_stat = train_stat.transpose()
print(train_stat)
# 결과 :
#             count         mean         std     min     25%     50%      75%     max
# horsepower  274.0   104.755474   39.416747    46.0    75.0    94.0   129.00   230.0
# weight      274.0  2981.941606  863.904789  1613.0  2190.0  2831.5  3641.75  4997.0

def stdscale_func(x): # 표준화 계산을 함수로 설정함. lib사용X
    return (x - train_stat['mean']) / train_stat['std']

# train 데이터 표준화
st_train_data = stdscale_func(train_dataset)
st_train_data = st_train_data.drop(['mpg'], axis = 'columns')
print(st_train_data[:3])

# test 데이터 표준화
st_test_data = stdscale_func(test_dataset)
st_test_data = st_test_data.drop(['mpg'], axis = 'columns')
print(st_test_data[:3])
# 원본 데이터를 전처리 하여 train : test = 7 : 3비율로 나누고 이때, train데이터와 test데이터의 feature(입력값)를 표준화하였다

# 7. label분리
train_label = train_dataset.pop('mpg')
print(train_label[:3])
test_label = test_dataset.pop('mpg')
print(test_label[:3])

# 8. tensor로 변환 : 딥러닝 모델이 학습하기 위해서는 입력값(데이터 갯수, feature특성)이 2차원인 tensor형태가 편하기 때문이다.
x_data = torch.tensor(st_train_data.values, dtype=torch.float32)
y_data = torch.tensor(train_label.values, dtype=torch.float32).view(-1, 1) # 뒤에 나올 nn.Linear가 2차원형태를 원하기 때문에 view(-1, 1)를 사용하여 2차원 텐서화 시켜준것이다.
# train데이터의 feature와 label을 tensor자료형으로 변환

x_test_data = torch.tensor(st_test_data.values, dtype=torch.float32)
y_test_data = torch.tensor(test_label.values, dtype=torch.float32).view(-1, 1)

# 9. train데이터셋을 "train" vs "validation"으로 분리 : 학습과 동시에 검증을 진행하기 때문에 모델 성능에 대한 신뢰도가 높아진다.
dataset = TensorDataset(x_data, y_data)
# x_data, y_data(train데이터셋을 tensor형태로 만든 것)을 train, validation으로 분리하기 위해서 우선 하나로 묶음 - TensorDataset

# train / validation split
dataset_size = len(dataset)
vali_size = int(dataset_size * 0.2)
train_size = dataset_size - vali_size

train_subset, vali_subset = random_split(
    dataset, [train_size, vali_size], # TensorDataset으로 묶여있던 x_data, y_data를 dataset(train데이터)를 train_size(80%)와 vali_size(20%)로 구분함
    generator=torch.Generator().manual_seed(123)
)
# dataset을 무작위로 나눙 학습용과 검증용으로 만드는 코드
# dataset: (x₁, y₁), (x₂, y₂), …, (x₁₀₀, y₁₀₀)
#                        ↓ 무작위 분할
# train_subset: 80쌍 → 모델 학습에 사용
# vali_subset:  20쌍 → 검증 및 조기 종료 판단에 사용
print(len(dataset),        len(train_subset),          len(vali_subset))
# 결과 : = 274                   = 220                    = 54
#              (학습용-경사하강법O : w, b를 갱신함)   (검증용-경사하강법X : w, b를 갱신하지 않음-조기종료로 쓰임)  ... 그래서 아래 쪽에 shuffle = True, False로 지정해줌

# 그때 train데이터셋의 loss값과 validation데이터셋의 loss값에 대해서 validation의 loss값이 갑자기 확올라가버리는 순간을 잡기 위해
# Early Stopping을 이용하여 loss값을 잡는다.
# 즉 우리는 70%의 데이터셋이  80%의 데이터셋(validation데이터셋과 구분된 데이터)를 사용하여 경사하강법을 통해 w,b를 갱신한다.

# train_subset(80%, 220개)  vali_subset(20%, 54개)  test_dataset(30%)  

# DataLoader 생성 : Dataset에서 데이터를 꺼내 배치 단위로 모델에 전달하는 역할 
batch_size = 32 # 데이터를 최대 32개씩 묶어서 전달한다

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
vali_loader = DataLoader(vali_subset, batch_size=batch_size, shuffle=False)
test_tensor_dataset = TensorDataset(x_test_data, y_test_data)
test_loader = DataLoader(test_tensor_dataset, batch_size=batch_size, shuffle=False)
print(len(train_loader), len(vali_loader), len(test_loader))
# 결과 : 7   2   4


# [2단계] : 모델 생성 및 학습 
# 1. 모델의 구조와 계산방법 정의(layer정의)
class MpgModel(nn.Module):
    def __init__(self):
        super().__init__()

        # layer정의 : Fully Connected Layer
        self.hidden_layer1 = nn.Linear(2, 32)
        self.hidden_layer2 = nn.Linear(32, 16)
        self.output_layer = nn.Linear(16, 1)

        self.relu = nn.ReLU()

        """
        self.net = nn.Sequential(
            nn.Linear(2, 32)
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
            )
        """

    def forward(self, inputs):
        # 데이터 흐름 정의 : 순전파(forward propagation)
        net = self.hidden_layer1(inputs)
        net = self.relu(net)
        net = self.hidden_layer2(net)
        net = self.relu(net)
        outputs = self.output_layer(net)

        return outputs
    """
    def forward(self, inputs):
        return self.net(inputs)
    """

model = MpgModel()
print(model)
print("전체 parameter 수 : ", sum(p.numel() for p in model.parameters() if p.requires_grad))
# p.numel : 해당 Tensor에 들어 있는 숫자의 총 개수
# 결과 : 641개
# 실제 LLM은 Parameter수가 수천억개가 등장한다.
# = 생성된 모델의 구조 확인

# 2. loss function(손실함수)와 옵티마이저(optimizer) 정의
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
# 손실함수를 MSELoss로 정의하였고 
# 옵티마이저는 SGD와 Adam중 Adam을 사용하였다. 그때 학습율은 0.01을 선택하였다,

mae_metric = nn.L1Loss()
# 절대 평균오차(이후 모델 성능 평가지표로 사용) : 예측값과 실제값의 차이(오차)에 절댓값을 취한 뒤 평균을 낸 값
# ... '0'에 가까울 수록 좋다!

# 3. 모델 학습
# : 매 epoch마다 loss, mae를 기록하고 조기종료를 구현
# 3-1. 모델 생성
def train_model_Func( # : 위에서 생성한 모델(MPGModel)을 학습시키는 절차 - 1epoch에서의 train데이터를 모두 사용하는 각 batch의 연산
    model, train_loader, vali_loader, criterion, optimizer, epochs=5000, patience=10  # patience : 검증에 대한 손실(loss)이 개선되지 않을 때 기다리는 epoch수 = loss값이 더 이상 떨어지지 않을 때 얼마나 기다릴 지를 정함. 실무에서는 10~20번 정도 준다. 만약에 epoch가 5000인데 한 2000번쯤 멈춘다고 하면 2010~2020번째까지는 계속 수행하도록 한다는 뜻이다.
):
    history = {
        "loss" : [], "mae" : [], "vali_loss":[], "vali_mae":[]
    }

    # 3-2. 조기 종료(Early Stopping) 관련 변수 설정
    best_vali_loss = float("inf") # 가장 낮은 검증 손실 저장용
    best_model_state = None       # 최적 모델의 상태 저장
    best_epoch = 0
    wait = 0                      # 성능이 개선되지 않은 연속 횟수

    for epoch in range(epochs): # 5000바퀴를 돌 때, 각 epoch에서..
        # 3-3. **train데이터 모드로 전환**
        model.train()
        train_loss_sum = 0 # 각 batch의 loss를 누적
        train_mae_sum = 0  # 각 batch에 mae를 누적
        
        # DataLoader(train dataset에서 데이터를 가져올 수 있는 형태)에서 데이터를 batch단위로 가져온다.
        for x_batch, y_batch in train_loader:

            # [순전파]
            # 1) 예측값 계산
            pred = model(x_batch)

            # 2) 손실값 계산
            loss = criterion(pred, y_batch)
            
            # 3) 이전 gradient초기화 
            optimizer.zero_grad()

            # [역전파]
            # 4) '역전파' -> 발생한 loss값을 optimizer를 이용하여 parameter(w, b)를 최적화
            loss.backward()
            
            # 5) 파라미터 갱신(weight, bias) ... 그래프에서 y=wx+b의 기울기가 최적화가 되는 선을 찾는다. = 잔차제곱의 합이 최소가 되는 추세선을 찾는다
            optimizer.step()
            
            # 6) loss누적(필수X) : 배치별 평균 loss값에 sample수를 곱하여 누적함. 마지막 batch의 데이터 갯수가 다를 수 있기 때문이다.
            train_loss_sum += loss.item() # .item() : tensor의 값을 python의 값으로 바꾸어야 한다. 

            # 7) mae 평가지표(mae는 평가지표이므로 gradient(미분)계산x)
            with torch.no_grad():
                mae = mae_metric(pred, y_batch)
            train_mae_sum += mae.item() * len(x_batch)
            # ---------------------------------------: 220개의 train데이터를 32개씩(1batch)로 나누어 총 7번을 학습해야 1epoch이 끝난다. 
            # 현재 이 for문은 220개의 데이터를 7번 학습(32, 32, 32, 32, 32, 32, 32, 28)로 학습한 것이다.
        # 모든 train데이터에 대해서 모든 batch(32개씩 220개를 학습)를 처리하면 현재 1epoch의 학습 단계가 끝난다. 배치당 최대 32개를 처리하며, 반복 횟수는 len(train_loader)이다.
        

        # 한 번의 epoch에서 전체 sample기준 "평균 loss와 mae"를 계산해야한다.
        train_loss = train_loss_sum / len(train_loader.dataset)
        train_mae = train_mae_sum / len(train_loader.dataset)


        # 3-4. **validation데이터 모드로 전환**
        # 학습 도중 모델 검증 : validation data를 사용
        model.eval() # 검증용으로 전환
        vali_loss_sum = 0
        vali_mae_sum = 0

        # 검증용이므로 parameter 갱신을 안함(gradient(미분)계산x)
        with torch.no_grad():
            for x_vali, y_vali in vali_loader:# DataLoader(train dataset에서 데이터를 가져올 수 있는 형태)에서 데이터를 batch단위로 가져온다.
                vali_pred = model(x_vali)
                vali_loss = criterion(vali_pred, y_vali)
                vali_mae = mae_metric(vali_pred, y_vali)

                vali_loss_sum += vali_loss.item() * len(x_vali)
                vali_mae_sum += vali_mae.item() * len(x_vali)

        # 1개의 epoch에서 평균 validation loss, mae 계산
        vali_loss = vali_loss_sum / len(vali_loader.dataset)
        vali_mae = vali_mae_sum / len(vali_loader.dataset)

        # history에 학습 결과 기록 -> train용 데이터에 대한 loss와 mae 그리고 validation용 데이터에 대한 loss와 mae를 history에 기록한다.
        history['loss'].append(train_loss)
        history['mae'].append(train_mae)
        history['vali_loss'].append(vali_loss)
        history['vali_mae'].append(vali_mae)

        if (epoch + 1) % 10 == 0:
            print(f"Epoch[{epoch+1:5d}/{epochs}]"
                f"train데이터의 loss : , {train_loss:.5f}"
                f"train데이터의 mae : , {train_mae:.5f}"
                f"vali데이터의 loss : , {vali_loss:.5f}"
                f"vali데이터의 mae : , {vali_mae:.5f}"
                )
            
        # 3-5. Early Stopping - 조기 종료 처리 : train loss 보다는 validation loss를 기준으로 판단한다!
        # 학습 중 특정지표가 더 이상 개선되지 않으면 학습을 중단한다
        if vali_loss < best_vali_loss : 
            best_vali_loss = vali_loss
            best_epoch = epoch + 1

            best_model_state = copy.deepcopy(model.state_dict()) 
            # copy lib를 불러와서 사용함 -> state_dict() : model의 parameter 및 등록된 버퍼 정보
            # 가장 좋은 모델의 상태를 복사해 저장해둔다. - deepcopy()사용
            wait = 0
            # = # validation loss가 이전 최저값보다 낮아졌으므로, 개선되지 않은 연속 epoch 수(wait)를 0으로 초기화한다.

        else:
            wait += 1 # 손실이 개선되지 않았으므로 계속 누적된다.
            if wait >= patience: # patience = 10으로 위에서 설정해두었다. = 즉, loss값이 고정되고 10번 정도는 추가로 학습함. 대신에 10번 후에는 학습이 끝남
                print(f"\n 조기 종료 발생!! ... 학습종료 : {epoch + 1}")
                break

    # 3-6. 최적 모델의 parameter 복원 : 조기 종료(Early Stopping)와 상관없이 가장 성능이 좋은 모델로 복원
    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    print("\n학습완료, 전체 학습 횟수(epoch) : ", len(history['loss']))
    print("최적 epoch은? : ", best_epoch, ', 그리고 최소 validation loss는? : ', best_vali_loss)
        
    return history

# 4. 모델 학습 호출
# history 변수 생성: 는 보통 학습 과정에서 나온 "손실(loss)"이나 "평가 지표(mae)"를 저장하는 변수. 나중에 학습이 잘 진행됐는지 확인하거나 그래프를 그릴 때 사용
history = train_model_Func(
    model, train_loader, vali_loader, criterion, optimizer, 5000, 10
)
# 결과 : 
#  조기 종료 발생!! ... 학습종료 : 102

# 학습완료, 전체 학습 횟수(epoch) :  102
# 최적 epoch은? :  92 , 그리고 최소 validation loss는? :  203.7836552372685

# 해석 : 최대 5,000 epoch으로 설정했지만, 92번째 epoch에서 가장 좋은 검증 성능을 기록했고 이후 10 epoch 동안 개선되지 않아 102번째에서 종료한 것이다.
# 정답인 'MPG(연비)'를 원래 단위로 학습했다면, RMSE가 약 14.28 MPG라는 뜻이다. 오차 규모를 판단할 때 이 값이 더 직관적이다.
# 그리고 조기 종료(Early Stopping)는 지금 충분히 좋은 성능을 보장하는 기능이 아니다. 지금 결과는 “검증 손실(vali_loss)이 203.78로 충분히 작다”가 아니라, 
# ** “이번 학습에서는 그 값(203.78365)이 가장 좋았고 이후 10 epoch 동안 더 개선되지 않았다” **는 의미이다.

# 성능이 좋은지 판단하려면 실제값의 범위를 확인하고, 항상 학습 데이터의 평균 MPG(연비)만 예측하는 단순한 기준 모델보다 오차가 작은지 비교해야 합니다.


# [3단계] 모델 평가
# 1. 모델 평가 함수 생성 (test dataset을 사용)
def evaluate_mode_Func(model, test_loader, criterion):
    model.eval()  # 평가 모드로 전환
    test_loss_sum = 0
    test_mae_sum = 0

    predictions = [] # batch별 예측값과 실제값 저장
    actuals = []

    with torch.no_grad():
        for x_batch, y_batch in test_loader:
            pred = model(x_batch)
            loss = criterion(pred, y_batch)
            mae = mae_metric(pred, y_batch)

            test_loss_sum += loss.item() * len(x_batch)
            test_mae_sum += mae.item() * len(x_batch)

            predictions.append(pred)
            actuals.append(y_batch)

    # 전체 test 데이터(118개)에 대한 평균 MSE, MAE
    test_loss = test_loss_sum / len(test_loader.dataset)
    test_mae = test_mae_sum / len(test_loader.dataset)

    # torch.cat() : 여러 텐서를 기존 차원으로 연결함(batch별로 저장된 tensor를 하나의 tensor로 합침)
    # 예시) (32, 1), (32, 1), (32, 1), (22, 1)  ->  (118, 1)
    pred_tensor = torch.cat(predictions, dim=0)
    actual_tensor = torch.cat(actuals, dim=0)

    return test_loss, test_mae, pred_tensor, actual_tensor

# 2. 모델 평가 함수 호출
eval_loss, eval_mae, pred_tensor, actual_tensor = evaluate_mode_Func(
    model, 
    test_loader, 
    criterion
)

pre = pred_tensor.numpy().ravel()
actual = actual_tensor.numpy().ravel()

print('\n 모델 평가 결과!!')
print(f"설명력(r2-score) : {r2_score(actual, pre)}, MSE : {eval_loss}, RMSE : {np.sqrt(eval_loss)}, MAE(평균절대오차) : {eval_mae}")
# r2-score는 '1'에 가까워야 하고 MSE, RMSE, MAE는 '0'에 가까워야 모델성능이 좋은 것이다!
# 예시) MPG(연비) 예측에서 MAE = '3'이면 예측 MPG(연비)가 실제 MPG(연비)에서 평균적으로 '3'만큼 벗어났다는 뜻이다. 
# 결과 : 설명력(r2-score) : -1.865480661392212, 
#                    MSE : 151.1171148267843, 
#                   RMSE : 12.292970138529757, 
#       MAE(평균절대오차) : 10.511697251917953

# history값을 DataFrame에 저장
historyDF = pd.DataFrame(history)
historyDF['epoch'] = range(1, len(historyDF) + 1)
print(historyDF.head(3))
print(historyDF.tail(3))
print(historyDF.columns)
# 결과 : 
#          loss         mae     vali_loss    vali_mae  epoch
# 0  762.273061  132.317157  16674.178602  118.230977      1
# 1  256.112294   77.600781   5174.127405   71.442667      2
# 2   93.813084   44.960585   2141.845730   37.602409      3
# ...
#          loss        mae      vali_loss    vali_mae  epoch
# 99   5.530174  11.125504     215.169328   12.411077    100
# 100  5.718446  11.229618     220.467748   12.566715    101
# 101  6.039387  11.828090     228.473405   12.793760    102

# vali_loss(검증 손실)이 가장 낮은 epoch은?
best_epoch = np.argmin(historyDF['vali_loss']) + 1
print('최적 학습 횟수 : ', best_epoch) 
# 결과 : 최적 학습 횟수 : 92

# 시각화1
# 모델 학습 정보 시각화
def plt_history(historyDF):
    best_epoch = historyDF.loc[historyDF['vali_loss'].idxmin(), 'epoch']
    plt.figure(figsize=(10, 8))

    # 1. MAE값 시각화
    plt.subplot(2,1,1)   # MAE값
    plt.plot(historyDF['epoch'], historyDF['mae'], label='train mae')
    plt.plot(historyDF['epoch'], historyDF['vali_mae'], label='validation mae')

    # 최적 모델 시점 표시
    plt.axvline(x=best_epoch, color='red', linestyle='--',
                label = f'Best Epoch : {best_epoch}')
    plt.xlabel('Epoch')
    plt.ylabel('MAE[mpg]')
    plt.title('평균 절대 오차(MAE)')
    plt.legend()
    plt.grid(alpha=0.3)


    # 2. MSE값 시각화
    plt.subplot(2,1,2)   # MSE값
    plt.plot(historyDF['epoch'], historyDF['loss'], label='train mae')
    plt.plot(historyDF['epoch'], historyDF['vali_loss'], label='validation mae')

    # 최적 모델 시점 표시
    plt.axvline(x=best_epoch, color='red', linestyle='--', # 선 모양은 '-' 실선, '--' 파선, ':' 점선, '-.' 일점쇄선을 사용할 수 있다
                label = f'Best Epoch : {best_epoch}')
    plt.xlabel('Epoch')
    plt.ylabel('MSE[mpg]')
    plt.title('평균 제곱 오차(MSE)')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

plt_history(historyDF)

# 시각화2
# 실제값과 예측값 비교 시각화 -> 추세선(회귀선)
plt.figure(figsize = (7, 7))
plt.scatter(actual, pre, alpha=0.7)
min_value = min(actual.min(), pre.min())
max_value = max(actual.max(), pre.max())
plt.plot([min_value, max_value], [min_value, max_value],
        'r--', label = '예측값==실제값')
plt.xlabel('실제연비(mpg)')
plt.ylabel('예측연비(mpg)')
plt.axis('equal')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# 실제연비(mpg)와 예측연비(mpg)에 대해서 데이터에 대한 추세선이 생겼다. 
# 이 추세선에 대해서 종속변수의 평균을 그은 선과 비교하여 SST, SSE, SSR을 구할 수 있다.
# SST : data와 종속변수의 평균선 간의 차이
# SSE : data와 회귀선 간의 차이
# SSR : 회귀선과 종속변수의 평균선 간의 차이
# SST = SSR(모델이 설명한 변동) + SSE(모델이 설명하지 못한 변동)

# 이 3가지를 통해 결정계수(R2)와 F값을 알 수 있다!!
# -> 결정계수 = SSR / SST = 1-(SSE/SST)
# -> F값 = (SSR/자유도(모델)) / (SSE/자유도(잔차))

# 시각화3
# 잔차 분포 시각화
# 잔차가 '0'에 가까워지면 예측이 더 정확해진다.
#  MAE : 잔차의 절댓값을 평균
#  MSE : 잔차를 제곱한 값의 평균
# RMSE : MSE에 제곱근을 취한 값
residual = actual - pre
plt.figure(figsize=(8,4))
sns.histplot(residual, bins=20, kde=True)
plt.axvline(x=0, color='red', linestyle='--')
plt.xlabel('잔차')
plt.ylabel('빈도수')
plt.title('잔차 분포')
plt.grid(alpha=0.3)
plt.show()


# 최적 모델의 parameter가 복원된 상태이므로 모델 저장 후 읽기(불러오기) -------
model_path = './mpg_bestmodel.pth'
torch.save(model.state_dict(), model_path)
print('최적 model 저장 완료!')
# model_path에 저장하였다.

# 그러면 저장한 model을 불러와보자!
loaded_model = MpgModel() # 저장 시 사용한 모델과 동일한 구조의 객체를 생성한다.
loaded_model.load_state_dict(torch.load(model_path, weights_only=True, map_location='cpu'))

# 예측을 위해 평가 모드로 전환
loaded_model.eval()
print('loaded_model : ', loaded_model)

# 기존 데이터로 예측
loaded_model.eval()
with torch.no_grad():
    pred_5 = loaded_model(x_test_data[:5])
print('예측값 : ', pred_5.numpy().ravel())
print('실제값 : ', y_test_data[:5].numpy().ravel())
print()
# 결과 :
# 예측값 :  [14.996181 16.056433 16.06724  14.035566 26.713028]
# 실제값 :  [15. 18. 16. 14. 24.]


# 새로운 데이터로 예측
new_data = pd.DataFrame({
    "horsepower" : [111, 155],
    "weight" : [2222, 4444]
})

# 학습 시 표준화를 해주었으므로 새로운 데이터(자료)도 표준화를 해주기!
new_st_data = stdscale_func(new_data)
print('새로운 data를 표준화 한 결과 : ', new_st_data)
new_tensor = torch.tensor(new_st_data.values, dtype=torch.float32)
# new_data(새로운data) -> new_st_data(표준화) -> new_tensor(텐서화)
# 결과 :
#        horsepower      weight
#   0      0.158423   -0.879659
#   1      1.274700    1.692384

loaded_model.eval()
with torch.no_grad():
    new_pred = loaded_model(new_tensor) # 새로운 데이터는 이름이 new_tensor로 바뀌었다.
print('새 값 예측 결과 : ', new_pred.numpy().ravel())
# 결과 : [25.407711 14.525261]

# 새로운 데이터와 예측 결과를 함께 출력
new_data['예측연비(mpg)'] = new_pred.numpy().ravel()
print(new_data)
# 결과 : 
#         horsepower    weight     예측연비(mpg)
#     0         111       2222        25.407711
#     1         155       4444        14.525261

