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
# 이 두가지에 대해서 값을 설정해보자.
add_cost = np.linspace(0, 100, 80) # 0부터 100까지 균등한 간격으로 80개의 광범위한 데이터(광고비 자료)를 뽑음
sales = -0.06 * (add_cost ** 2) + 7.5 * add_cost + 40 + np.random.normal(0, 25, size=len(add_cost))
#sales = -0.06 *    광고비²     + 7.5 *  광고비  + 40 +              noise
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

# 3. 변수설정
# x : 광고비
# y : 매출
x = df[['광고비']].values.astype(np.float32)
y = df[['매출']].values.astype(np.float32)

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

# 5. 표준화 및 정규화