# Mnist 손글씨 숫자 이미지 분류 모델 작성
# feature은 총 784개이다. : 이미지의 각 픽셀 밝기 값들
# label은 총 10개이다. : 0부터 9까지의 숫자

# mnist의 주요기능
# 1. 손으로 쓴 숫자 이미지가 학습용 60000개, 테스트용 10000개로 총 70000개 있다
# 2. 모든 이미지는 하나의 숫자를 담은 28x28 grey scale 이미지이며, 


# -----------------------------------------------------------------------------------

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
from sklearn.metrics import confusion_matrix, classification_report, r2_score
from sklearn.datasets import fetch_openml

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split


# 2. 사용장치 설정 ... 이미지 처리를 위해서는 gpu가 있으면 편하기 때문
np.random.seed(42)
torch.manual_seed(42)

# 사용장치 설정-cpu : 다음주부터는 CNN학습을 위해서 GPU가 필요함. 그래서 내 컴퓨터에서 GPU가 있는지 확인. 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 이 코드로 CNN, RNN에서 하는 병렬연산을 처리하기 위해서는 GPU가 있는지 확인해야 하는데 위 코드가 컴퓨터 내장 GPU를 확인할 수 있다.
print('사용장치 : ', device) # CPU


# 3. 데이터 불러오기 : MNIST
mnist = fetch_openml('mnist_784', version=1, as_frame=False)


# 4. 변수설정
x = mnist.data.astype('float32')
y = mnist.target.astype('int64')
print(x.shape, y.shape)
# print(x[0])
# print(y[0])


# 5. train / test split()
x_train = x[:60000]
y_train = y[:60000]
x_test = x[60000:]
y_test = y[60000:]
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

"""
# 시각화
img = x_train[0].reshape(28, 28)
plt.imshow(img, cmap='gray')
plt.title(f"label={y_train[0]}")
plt.axis('off')
plt.show()
"""

# 6. 정규화(scaling)
x_train = x_train / 255
x_test = x_test / 255
print(x_train[0], x_train.shape) # (60000, 784)의 자료구조

print(set(map(int, y_test))) # {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


# 7. validation data 구성
# train : 60000개 중 뒤쪽 10000개를 validation data로 사용
x_validation = x_train[50000:60000]
y_validation = y_train[50000:60000]
x_train = x_train[0:50000]
y_train = y_train[0:50000]
print(x_validation.shape, x_train.shape)
# 결과 : (10000, 784) (50000, 784)


# 8. nd.array  ->  torch.tensor로 변환 
# 1) train용 데이터
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)

# 2) validation용 데이터
x_validation_tensor = torch.tensor(x_validation, dtype=torch.float32)
y_validation_tensor = torch.tensor(y_validation, dtype=torch.long)

# 3) test용 데이터
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)


# 9. batch 처리
batch_size = 128

# 1) TensorDataset : x, y데이터를 하나로 묶음
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
validation_dataset = TensorDataset(x_validation_tensor, y_validation_tensor)
test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
# x, y데이터를 TensorDataset을 이용하여 하나로 묶음

# 2) DataLoader : 묶은 x,y데이터(dataset)를 batch_size에 맞게 나눌 수 있게 함
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
validation_loader = DataLoader(validation_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
# 그때 validation데이터와 test데이터는 Dataset에서 무작위로 뽑게 함(shuffle=False)



# [2단계] : 모델정의 및 학습
# 1. 모델 정의  ->  모듈 상속 클래스  or  Sequential
class MNISTModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(784, 64),  # 입력층  ->  입력값은 feature개수가 들어간다 : "784개의 픽셀"
            nn.ReLU(),
            nn.Dropout(p=0.2),

            nn.Linear(64, 32),   # 은닉층
            nn.ReLU(),
            nn.Dropout(p=0.2),

            nn.Linear(32, 10)    # 출력층  ->  최종 출력값은 label 10가지가 들어간다 : "숫자 0 ~ 9"
        )

    def forward(self, x):
        return self.net(x)  # 입력 x를 각 층에 통과시켜 클래스별 점수 텐서를 반환

model = MNISTModel().to(device=device)
print(model)


# 2. 손실함수, optimizer 정의
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)


# 3. 학습
epochs = 30
history = {
    "loss" : [],
    "accuracy" : [],
    "validation_loss" : [],
    "validation_accuracy" : []
}
# history의 역할 : 1번 epoch마다 학습할 때 나온 손실값(loss)과 정확도(acc)를 저장하는 변수

for epoch in range(epochs): # 784개의 데이터(종속변수)를 128개씩(batch_size) 나눠서 128 - 128 - 128 - 128 - 128 - 128 - 125개의 데이터로 학습하는게 '1'epoch이다. 그 1epoch에서...
    # A. **학습용 데이터(train)로 전환**
    model.train()
    train_total_loss = 0.0 
    train_correct = 0
    train_total = 0

    # DataLoader(train dataset에서 데이터를 가져올 수 있는 형태)에서 데이터를 batch단위(128개씩)로 가져온다.
    for batch_x, batch_y in train_loader: 
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        # 1) 예측값 계산
        outputs = model(batch_x)

        # 2) 손실값(loss) 계산 - criterion이용
        loss = criterion(outputs, batch_y)

        # 3) 이전 gradient(미분기록)초기화 - optimizer이용
        optimizer.zero_grad()

        # 4) 역전파 : 위의 순전파의 결과로 발생한 loss값을 optimizer를 이용하여 parameter를 최적화
        loss.backward()   #  ->  각 parameter에 대한 손실값(loss)의 기울기를 계산

        # 5) 갱신된 파라미터로 그래프에서 y=wx+b의 기울기가 최적화가 되는 선을 찾는다 = 잔차제곱의 합이 최소가 되는 추세선을 찾는다. lr=0.001을 단위로 찾아간다.
        optimizer.step()  #  ->  위에서 계산된 기울기를 이용하여 parameter 갱신

        # 6) 손실값(loss) 계산에 필요한 계수 누적 : batch별 평균 손실값에 sample수를 곱하여 누적한다. 마지막 batch의 데이터 갯수가 다를 수 있기 때문!! .. 32-32-32-5
        train_total_loss += loss.item() * batch_x.size(0)  #  -> 학습 손실 누적. size(0)은 '크기'를 '정수'로 반환 : ex) [128] -> 128

        # 7) acc계산에 필요한 계수 누적 : 클래스(label = 0 ~ 6)별 점수 중 최댓값의 인덱스로 예측하고, '정답 개수'와 '전체 데이터 개수'를 누적
        pred = torch.argmax(outputs, dim=1)
        train_correct += (pred == batch_y).sum().item()  # 학습 정답 갯수 누적
        train_total += batch_y.size(0) # 학습 데이터 갯수 누적

    # 8) train데이터셋에 대한 "평균 손실값"과 "평균 분류 정확도"
    train_avg_loss = train_total_loss / train_total
    train_avg_acc = train_correct / train_total


    # B. **모델을 평가 모드로 전환하여 검증(validation) 진행** - Dropout이 비활성화된다.
    # Dropout은 학습할 때 일부 뉴런의 출력을 무작위로 0으로 만들어, 특정 뉴런에만 의존하는 것을 줄이고 과적합을 방지한다.
    # 검증할 때도 출력을 무작위로 끄면 같은 입력의 예측이 달라질 수 있으므로, 평가 모드에서는 Dropout으로 출력을 끄지 않는다.
    # 즉, 학습한 모델을 실제 예측할 때와 같은 조건에서 평가하기 위해 model.eval()을 호출한다.
    # eval()은 데이터 자체를 바꾸거나 기울기 추적을 끄는 기능은 아니다. 검증 데이터는 validation_loader에서 받고, 기울기 추적은 아래 no_grad()로 끈다.
    model.eval()
    
    validation_total_loss = 0.0 
    validation_correct = 0
    validation_total = 0

    with torch.no_grad(): # 검증하는 단계이기 때문에 no_grad()를 사용
    # DataLoader(train dataset에서 데이터를 가져올 수 있는 형태)에서 데이터를 batch단위(128개씩)로 가져온다.
        for batch_x, batch_y in validation_loader: 
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
    
            # 1) 예측값 계산
            outputs = model(batch_x)
    
            # 2) 손실값(loss) 계산 - criterion이용
            loss = criterion(outputs, batch_y)

            # **검증 단계이기때문에 3) 이전 gradient(미분기록)초기화, 4) 역전파, 5) optimizer가 없다!**
    
            # 6) 손실값(loss) 계산에 필요한 계수 누적 : batch별 평균 손실값에 sample수를 곱하여 누적한다. 마지막 batch의 데이터 갯수가 다를 수 있기 때문!! .. 32-32-32-5
            validation_total_loss += loss.item() * batch_x.size(0)  #  -> 학습 손실 누적. size(0)은 '크기'를 '정수'로 반환 : ex) [128] -> 128
    
            # 7) acc계산에 필요한 계수 누적 : 클래스(label = 0 ~ 6)별 점수 중 최댓값의 인덱스로 예측하고, '정답 개수'와 '전체 데이터 개수'를 누적
            pred = torch.argmax(outputs, dim=1)
            validation_correct += (pred == batch_y).sum().item()  # 학습 정답 갯수 누적
            validation_total += batch_y.size(0) # 학습 데이터 갯수 누적

        # 8) validation데이터셋에 대한 "평균 손실값"과 "평균 분류 정확도"
        validation_avg_loss = validation_total_loss / validation_total
        validation_avg_acc = validation_correct / validation_total

        # 학습하면서 검증하는 데이터 = validation dataset

        # 평균 손실값(avg_loss) : 정답과 예측의 차이가 얼마나 큰지 나타낸다. 낮을수록 좋고, 학습 과정에서 줄어드는지 확인한다.
        # 평균 분류 정확도(avg_accuracy) : 전체 데이터 중 정답을 맞힌 비율. 높을수록 좋다.
        
        # train 데이터셋에 대한 평균 손실값과 평균 분류 정확도가 있고
        # validation 데이터셋에 대한 평균 손실값과 평균 분류정확도를 구분 짓는 이유는..
        # -> train은 모델이 정답을 보고 가중치를 수정하며 공부한 데이터이고, validation은 가중치 수정에 쓰지 않고 실력을 확인만하는 데이터이기 때문이다.
        #    train 성적만 좋으면 공부한 문제를 외운 것인지, 처음 보는 문제도 잘 푸는 것인지 구분하기 어렵다.
        #  ex) train 정확도가 99%인데 validation 정확도가 80%라면, 학습한 데이터에만 지나치게 맞춰진 과적합을 의심할 수 있다.
        #      두 데이터의 손실이 함께 줄고 정확도가 함께 높아지는지 비교하면, 새로운 데이터에도 적용할 수 있는 규칙을 배우는지 판단하는 데 도움이 된다.
        #      특히 train 손실은 계속 줄지만 validation 손실이 커지기 시작하면 과적합의 신호일 수 있어,
        #      "조기 종료"나 "모델 조정"을 고려한다.

        # 이렇게 train데이터에 대한 평균 손실값과 평균 분류정확도, validation데이터에 대한 평균 손실값과 평균 분류정확도가 나왔다.

        # 나온 값을 history에 저장!
        history["loss"].append(train_avg_loss)
        history['accuracy'].append(train_avg_acc)
        history['validation_loss'].append(validation_avg_loss)
        history['validation_accuracy'].append(validation_avg_acc)

        print(
            f'Epoch [{epoch + 1:02d} / {epochs}]'
            f'loss : {train_avg_loss:.4f}'
            f'validation_loss : {validation_avg_loss:.4f}'
            f'validation_accuracy : {validation_avg_acc:.4f}'
        )

# 여기까지 하고 한번 시행해봐라. 만약 두 데이터셋에 대해서 공통적으로 손실값이 줄고 정확도가 올라간다면 정상적이다.
# 이렇게 모델이 완성되었으므로 test data로 모델을 다시 한 번 검증한다.
# train데이터로 모델을 학습시키고 학습을 시키면서 validation데이터를 이용하여 학습과 동시에 검증한다.
# 이후에 test데이터를 이용하여 다시 한번 2차 검증을 거친다.



# [3단계] : 모델 평가
# model이 완성되었다. 이번엔 2차검증으로 test데이터를 이용해서 마지막 검증을 거치자!
# 1. 모델 평가 - test데이터
model.eval()
test_total_loss = 0.0  # 테스트 데이터의 손실 합계
test_correct = 0      # 테스트 데이터에서 맞힌 개수
test_total = 0        # 평가한 테스트 데이터 개수

with torch.no_grad(): # 검증하는 단계(2차 검증 by test데이터)이기 때문에 no_grad()를 사용
    # DataLoader(train dataset에서 데이터를 가져올 수 있는 형태)에서 데이터를 batch단위(128개씩)로 가져온다.
    for batch_x, batch_y in test_loader: 
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)
    
        # 1) 예측값 계산
        outputs = model(batch_x)
    
        # 2) 손실값(loss) 계산 - criterion이용
        loss = criterion(outputs, batch_y)

        # **마찬가지로 검증 단계(2차 검증)이기때문에 3) 이전 gradient(미분기록)초기화, 4) 역전파, 5) optimizer가 없다!**
    
        # 6) 손실값(loss) 계산에 필요한 계수 누적 : batch별 평균 손실값에 sample수를 곱하여 누적한다. 마지막 batch의 데이터 갯수가 다를 수 있기 때문!! .. 32-32-32-5
        test_total_loss += loss.item() * batch_x.size(0)  #  -> 학습 손실 누적. size(0)은 '크기'를 '정수'로 반환 : ex) [128] -> 128
    
        # 7) acc계산에 필요한 계수 누적 : 클래스(label = 0 ~ 6)별 점수 중 최댓값의 인덱스로 예측하고, '정답 개수'와 '전체 데이터 개수'를 누적
        pred = torch.argmax(outputs, dim=1)
        test_correct += (pred == batch_y).sum().item()  # 학습 정답 갯수 누적
        test_total += batch_y.size(0) # 학습 데이터 갯수 누적

# 8) test데이터셋에 대한 "평균 손실값"과 "평균 분류 정확도"
test_avg_loss = test_total_loss / test_total
test_avg_acc = test_correct / test_total

# 이제는 train데이터와 validation 뿐만아니라 test데이터에 대한 평균손실값(avg_loss)과 평균분류정확도(avg_acc)가 생겼다!
print(f"test용 평균 손실값(test_avg_loss) : {test_avg_loss}")
print(f"test용 평균 분류정확도(test_avg_acc) : {test_avg_acc}")

# 학습 결과 시각화 
plt.plot(history['loss'],label='train loss')
plt.plot(history['validation_loss'], label='validation loss')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()


# 모델 저장
torch.save(model.state_dict(), 'mnist_model.pth')
print("모델 저장 완료 : mnist_model.pth")
# --- 데이터 분석가(과학자)가 할 일 끝 ---

# 모델 불러오기 - 모델이 필요한 누구던지
mymodel = MNISTModel().to(device=device)
mymodel.load_state_dict(torch.load('mnist_model.pth', map_location=device))
mymodel.eval()
print('모델 읽기 성공')

# 기존 test 데이터로 예측
with torch.no_grad():
    sample_x = x_test_tensor[1:2].to(device=device)
    logits = mymodel(sample_x)
    pred_prob = torch.softmax(logits, dim=1)
    pred_label = torch.argmax(pred_prob, dim=1).item()

print('pred : ', pred_prob.cpu().numpy())
print('예측값 : ', pred_label)
print('실제값 : ', pred_label)
# 결과 : 
# pred :  [[1.0340995e-10   5.1687163e-04   9.9942905e-01   5.2033465e-05   5.3772851e-07  6.7314602e-07   5.2729422e-07   2.3544258e-07   1.2965011e-08   5.0160483e-13]]
# 예측값 :  2
# 실제값 :  2
# 즉, 입력 이미지가 숫자 0~9 중 무엇인지, 모델이 예측한 확률 10개다. 
# 앞에서부터 순서대로 숫자 0, 1, 2, …, 9에 해당

# 예측 이미지 시각화 
plt.imshow(x_test_tensor[1].reshape(28,28),cmap='gray')
plt.title(f'pred:{pred_label}, true :{y_test_tensor[1].item()}')
plt.show()