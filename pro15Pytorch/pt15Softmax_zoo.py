# kaggle의 zoo데이터셋을 이용하여 softmax classification을 해보자.


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
from sklearn.datasets import load_diabetes

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split


# 2. 데이터 불러오기
datas = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/zoo.csv")
print(datas.head(3))
print(datas.info())
# 동물의 특징을 보고 동물의 종류를 분류하는 데이터셋


# 3. 변수설정(feature / label 분리)
x_data = datas.iloc[:, :-1].astype('float32').values
# 종속변수 : 털 유무, 깃털 유무, 산란 여부, 비행 가능 여부, 다리 수 등 16개 특성
y_data = datas.iloc[:, -1].astype('int64').values
# 동물이 속한 7개 분류

print('feature 첫번째 : ', x_data[0], x_data.shape)
print('label 첫번째 : ', y_data[0], y_data.shape)
print('label의 종류 :', sorted(set(map(int, y_data))))

# 털, 깃털, 알을 낳는지, 다리 수 같은 특징을 입력해서 포유류인지 조류인지 등을 예측한다.
# 즉, 16개 특성 → 7개 클래스 중 하나를 예측하는 다항분류 문제라서 Softmax 방식으로 학습한다
np.random.seed(42)
torch.manual_seed(42)


# 4. 사용장치 설정-cpu : 다음주부터는 CNN학습을 위해서 GPU가 필요함. 그래서 내 컴퓨터에서 GPU가 있는지 확인. 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 이 코드로 CNN, RNN에서 하는 병렬연산을 처리하기 위해서는 GPU가 있는지 확인해야 하는데 위 코드가 컴퓨터 내장 GPU를 확인할 수 있다.
print('사용장치 : ', device) # CPU


# 5. label의 index 변환 : label의 인덱스 변환(손실함수가 받을 수 있는 형태로 변환하기 위해서!)
original_labels = sorted(set(y_data))
label_to_index = {label : index for index, label in enumerate(original_labels)}
index_to_label = {index : label for label, index in label_to_index.items()}
y_data_index = np.array([label_to_index[label] for label in y_data], dtype=np.int32)
print('원본 label 목록 : ', original_labels)
print('label -> index 로 매핑 : ', label_to_index)
print('index -> label 로 매핑 : ', index_to_label)
nb_classes = len(original_labels)
print('클래스 갯수 : ', nb_classes)
# 추후 등장하는 criterion(손실함수)의 CrossEntropyLoss는 클래스가 7개라면 
# 정답을 0 ~ 6으로 받는다. 원본 정답이 1 ~ 7이면 다음처럼 대응시켜야 한다.
#     원본 label  :  1  2  3  4  5  6  7
#     변환 인덱스 :  0  1  2  3  4  5  6
# 즉, 원본 데이터의 인덱스의 순서를 1이 아닌 0부터 시작하도록 바꾼다.

# 6. Overfitting 방지  ->  train / test split
# - train / test split() o
# - KFold
# - GridSearchCV
# - L1, L2 규제
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data_index, test_size=0.2, random_state=42, stratify=y_data_index, shuffle=True
)
# stratify = y_data_index  :  클래스별 비율을 유지하는 옵션
# shuffle = True : 데이터의 순서를 무작위로 섞은 뒤 학습용과 테스트용으로 나눔
# 주로 시간의 순서가 있는 순서가 중요한 데이터에 대해서는 shuffle=False로 둔다.


# 7. nd.array  ->   torch.tensor로 변환
# 1) train데이터
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)

# 2) test데이타
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)


# 8. batch 처리 준비
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
# tensor화 시킨 train용 데이터를 모델이 학습할 수 있는 데이터셋으로 만들어주기 위해서
# 우선 하나로 합친다 = TensorDataset
# 그리고 나서 일정한 비율(batch_size = 32)만큼 데이터가 나눠서 학습할 수 있도록 한다 = DataLoader



# [2단계] : 모델 정의
# 1. model정의 방법  ->  nn.module을 상속하는 class  or  nn.Sequential
class ZooModel(nn.Module):
    def __init__(self, input_dim, nb_classes):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),  # 입력층
            nn.ReLU(),
            nn.Dropout(p=0.3),
            # Drop-Out이란? : 특정 비율(30%)의 데이터는 학습에 참여하지 않게 함. 왜? Overfitting방지를 위해

            nn.Linear(32, 16),         # 은닉층
            nn.ReLU(),
            nn.Dropout(p=0.3),

            nn.Linear(16, nb_classes)  # 출력층
        ) # 입력과 출력 노드를 input_dim과 nb_classes로 설정하였다.

    def forward(self, x):
        return self.net(x)

model = ZooModel(input_dim=x_train.shape[1], nb_classes=nb_classes).to(device=device)
print(model)
# ZooModel이 입력받은 zoo데이터셋을 입력층과 출력층에 대해서 설정하고 device(cpu)에서 DeepLearning연산을 함


# 2. 손실함수 & Optimizer
criterion = nn.CrossEntropyLoss()  # 다항분류 시에는 nn.CrossEntropyLoss를 사용한다!
# 이항분류  ->  nn.BCELoss() : Sigmoid를 적용한 확률값(주로 많이쓰임)
#           ->  nn.BCEWithLogitsLoss() : Sigmoid 적용 전의 로짓
# 다항분류  ->  CrossEntropyLoss()

optimizer = optim.Adam(model.parameters(), lr=0.001)
# optimizer : 역전파로 계산한 기울기를 이용해 모델의 parameter(가중치(weight)와 편향(bias))을 갱신하여 손실(loss)을 줄이는 최적화 도구
# 즉, optimizer가 criterion을 사용하여 기울기가 음수라면 오른쪽으로, 기울기가 양수라면 왼쪽으로 옮기는 역할을 하여 parameter를 갱신한다.


# 3. 모델 학습
epochs = 500
train_loss_history = []
train_acc_history = []
# history의 역할 : 1번 epoch마다 학습할 때 나온 손실값(loss)과 정확도(acc)를 저장하는 변수
for epoch in range(epochs): # 101개의 데이터(종속변수)를 32번씩(batch_size) 나눠서 32 - 32 - 32- 5개의 데이터로 학습하는게 1epoch이다. 그 1epoch에서...
    # A. **학습용 데이터(train)로 전환**
    model.train()
    total_loss = 0 
    correct = 0
    total = 0

    # DataLoader(train dataset에서 데이터를 가져올 수 있는 형태)에서 데이터를 batch단위(32개씩)로 가져온다.
    for batch_x, batch_y in train_loader: 
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        # 1) 예측값 계산
        outputs = model(batch_x)

        # 2) 손실값(loss) 계산
        loss = criterion(outputs, batch_y)

        # 3) 이전 gradient(미분기록)초기화
        optimizer.zero_grad()

        # 4) 역전파 : 위의 순전파의 결과로 발생한 loss값을 optimizer를 이용하여 parameter를 최적화
        loss.backward()  #  ->  각 parameter에 대한 손실값(loss)의 기울기를 계산

        # 5) 갱신된 파라미터로 그래프에서 y=wx+b의 기울기가 최적화가 되는 선을 찾는다 = 잔차제곱의 합이 최소가 되는 추세선을 찾는다. lr=0.001을 단위로 찾아간다.
        optimizer.step()  #  ->  위에서 계산된 기울기를 이용하여 parameter 갱신

        # 6) 손실값(loss) 누적 : batch별 평균 손실값에 sample수를 곱하여 누적한다. 마지막 batch의 데이터 갯수가 다를 수 있기 때문!! .. 32-32-32-5
        total_loss += loss.item() * batch_x.size(0)

        # 7) acc계산에 필요한 계수 누적 : 클래스(label = 0 ~ 6)별 점수 중 최댓값의 인덱스로 예측하고, '정답 개수'와 '전체 데이터 개수'를 누적
        pred = torch.argmax(outputs, dim=1)
        correct += (pred == batch_y).sum().item()
        total += batch_y.size(0)

    avg_loss = total_loss / total
    avg_acc = correct / total
    train_loss_history.append(avg_loss)
    train_acc_history.append(avg_acc)
    print(f"Epoch [{epoch + 1:03d} / {epochs}], 손실값(loss):{avg_loss:.4f}, 모델의 분류 정확도(acc):{avg_acc:.4f}")



# [3단계] : 모델 평가 
# pred, prob, actual, acc, loss

model.eval()

with torch.no_grad(): # 모델을 학습할 때는 미분하여 기울기가 더 나아지는 방향을 알아야하지만 예측하거나 평가할 때는 미분하지 않는다.
    x_test_device = x_test_tensor.to(device)
    y_test_device = y_test_tensor.to(device)

    test_outputs = model(x_test_device)
    test_loss = criterion(test_outputs,y_test_device)
    test_pred = torch.argmax(test_outputs, dim=1)
    test_acc = (test_pred == y_test_device).float().mean()

print(f"\n손실값(loss) : {test_loss.item():.4f}, 분류정확도(acc) : {test_acc.item():.4f}")


# 2. 혼동행렬(confusion_matrix)과 분류 리포트(classification_report), 설명계수(r2-score)
y_pred_index = test_pred.cpu().numpy()
y_true_index = y_test_tensor.numpy()

# train용 label(정답)의 index를 원래 label(정답)의 index로 복원('0~6'  ->  '1~7')
y_pred_original = np.array([index_to_label[index] for index in y_pred_index]) # 다시 말하지만 우리는 kaggle데이터가 아닌 원본데이터를 불러와서 사용하여 데이터 컬럼의 순서가 1부터 되어 있다. 그래서 이렇게 label의 컬럼 순서를 바꿔주는 작업이 필요하다.
y_true_original = np.array([index_to_label[index] for index in y_true_index])

# 1) classification_report
print('1) 분류 리포트 : \n')
print(classification_report(y_true_original, y_pred_original))
print()
# 결과 :
# 1) 분류 리포트 : 
#               precision    recall  f1-score   support

#            0       1.00      1.00      1.00         8
#            1       1.00      1.00      1.00         4
#            2       1.00      1.00      1.00         1
#            3       1.00      1.00      1.00         3
#            4       1.00      1.00      1.00         1
#            5       1.00      1.00      1.00         2
#            6       1.00      1.00      1.00         2

# 2) confusioin_matrix
print('2) 혼동행렬 : \n')
cm = confusion_matrix(y_true_original, y_pred_original, labels=original_labels)
print(cm)
# 결과 : 
# 2) 혼동행렬 : 
#           [[8 0 0 0 0 0 0]
#            [0 4 0 0 0 0 0]
#            [0 0 1 0 0 0 0]
#            [0 0 0 3 0 0 0]
#            [0 0 0 0 1 0 0]
#            [0 0 0 0 0 2 0]
#            [0 0 0 0 0 0 2]]

# 3) heat map
# 시각화 -> heat map : 혼동행렬에 대해서 숫자의 크기를 색으로 표현한 그래프. 보통 값이 클수록 진한 색으로 표시
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=original_labels, yticklabels=original_labels)
plt.xlabel('predicted')
plt.ylabel('true')
plt.show()


# [4단계] : 모델예측
print('\n새로운 값으로 예측해보자')
# 예측 예시: 학습에 사용하지 않은 테스트 데이터 1개 (학습 때와 같은 순서의 16개 특성)
new_data = np.array(
    [[0., 1., 1., 1., 1., 1., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0.]], dtype='float32'
)

new_tensor = torch.tensor(new_data, dtype=torch.float32).to(device=device)
model.eval()
with torch.no_grad():
    logits = model(new_tensor) # 위에서 new_tensor로 새로 받은 값을 logit에 저장 ... 이 값은 오즈비를 씌운 값으로 -무한대 ~ +무한대의 값을 가진다
    probs = torch.softmax(logits, dim=1) #  = 분류 예측 확률  /  softmax함수를 씌워서 0~1사이의 값으로 만든다.  
    pred_index = torch.argmax(probs, dim=1).item() # 임의로 생성한 x값에 대한 예측값(y)의 인덱스를 1부터 보게 반환
    pred_label = index_to_label[pred_index] # 그리고 다시 원래의 label로 반환

print('분류 예측 확률 : ', probs.cpu().numpy().ravel())
print('분류 예측 index : ', pred_index)
print('분류 예측 label : ', pred_label)
# 결과 : 
# 분류 예측 확률 :  [6.9540995e-04  9.7388768e-01  2.4752682e-02  9.1819147e-06  4.4507165e-06  4.0388256e-04  2.4674545e-04]
# 분류 예측 index :  1
# 분류 예측 label :  1
# 즉, 사용자가 입력한 16가지는 내가 알고자 하는 동물의 특성(16가지)이다. 그리고 해당 동물의 특성에 대해서 어느 종(7가지 중)이 해당하는 지 모델이 확률로 표시한 것이다.
# 여기서는 1번째인 9.7388768e-01이 가장 확률이 높으므로 사용자가 입력한 특성은 조류(1번째 label인 특성)일 확률이 가장 높음을 의미한다

# **정리** :  16개 특징을 종합해서 7개 종류 중 어디에 속하는지 예측하는 것
# ... one-hot 인코딩 처리
# ----------------------------------------------------------------------------------------------------------------
