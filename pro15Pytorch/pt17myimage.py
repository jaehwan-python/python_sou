# 이미지 분류(처리)
# 이미지를 작은 칸으로 나눈다고 생각하면, 그 칸 하나가 픽셀이다. MNIST 이미지는 가로 28칸, 세로 28칸으로 총 784칸이다.
# 각 칸에는 밝기를 나타내는 숫자가 들어 있다. 원본 MNIST는 0이 검정, 255가 흰색이며 중간값은 회색이다.
# 이미지를 Linear층에 바로 넣는 방식에서는 28행x28열의 밝기값을 첫 행부터 차례대로 이어 붙여 
# 숫자 784개의 한 줄로 만든다.
# 예: [[0, 255], [128, 0]]처럼 2×2인 이미지를 펼치면 [0, 255, 128, 0]이 된다. 밝기 값은 유지되고 모양만 바뀐다.
# 실제로 펼치는 작업은 nn.Flatten()이나 reshape로 하고, Linear(784, ...)는 펼쳐진 784개 숫자를 입력받아 계산한다.

# 이러한 작업을 Linear가 한다. 하지만 이 linear만 사용하면 성능이 잘나오지 않는다.
# 그래서 해당 이미지의 특징만 뽑는다.
# 그리고 원본 이미지를 흐릿하게 만들고 윤곽(특징)만 뽑아서 각 칸을 줄을 세워서 연산한다. 
# 그럼 원본이미지를 곧바로 넣어서 예측하는 것보다 더 성능이 좋다.

# 그럴려면 원본이미지에서 특징만 뽑아서 흐릿하게 만드는 것이 중요하다.
# 이 작업을 CNN이 한다. 

# CNN이 이미지를 분류하는 것이 아니다.
# CNN이 이미지에서 특징을 뽑아 흐릿하게 만들고 그리고 나서 Linear가 예측/분류를 한다!
# RNN도 마찬가지이다.

# 이미지 처리 : CNN(원본 이미지에서 특징 뽑기 + 흐릿하게 만들기)  ->  Linear(예측하기)
# 자연어 처리 : RNN(단어를 순서대로 처리하며 이전 정보를 반영해 문맥과 순서에 따른 특징 추출)  ->  Linear(예측하기)
# 즉, 모든 최종 예측/분류/회귀는 Linear를 사용한다!

# 단순히 Linear만 가지고도 이미지 분류를 할 수는 있다. 하지만 cnn과정이 없으면 분류의 정확성이 떨어진다.
# 이번시간에는 linear만을 가지고(cnn없이) 이미지를 분류하는 방법으로 보자.
# -------------------------------------------------------------------------------------------------------------
# mnist라는 손글씨로 표현한 숫자 데이터셋(1부터 9까지의) 70000만 장이 존재한다.
# mnist 데이터셋으로 학습시키고 내가 만든 number.png를 알아보는지 확인해보자!

# [1단계] : 데이터 불러오기 및 변수 설정
# 1. lib 불러오기
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from PIL import Image
import torch 

# 2. 데이터(이미지) 불러오기
im = Image.open("number.png")

# 이미지 크기 변경 및 흑백 전환(반전)
# mnist dataset의 크기가 가로x세로 = 28x28이다. 그러므로 우리가 가진 데이터도 28x28로 크기를 재설정한다.
img = im.resize((28, 28), Image.Resampling.LANCZOS).convert("L") # conver("L")은 흑백 반전을 설정하였음을 의미한다.
# '컬러 이미지'는 픽셀마다 빨강·초록·파랑 3개의 값(RGB)을 가지지만, "L" 모드는 픽셀마다 "밝기 값" 하나만 가진다
# "밝기 값"
# - 0: 검정
# - 255: 흰색
# - 그 사이: 회색
# MNIST처럼 흑백 이미지로 학습한 모델에 입력 형식을 맞추기 위해서 내가 그린 그림을 밝기값으로 설정한 것이다.
#  예를 들어 28×28 이미지는 RGB라면 (28, 28, 3), "L"로 변환하면 (28, 28)이 된다.

# image파일을 numpy배열로 변환!
img_np = np.array(img)
print(img_np.shape)
print(img_np)
# 나오는 그림이 가로 28칸 세로 28칸으로 되어있다.

# 원본 이미지 시각화
plt.imshow(img_np, cmap='Greys')
plt.title('original image')
plt.show()

# 3. nd.array  ->  torch.tensor로 변환 : numpy 자료형을 pytorch자료형으로 변환  ...  Deep Learning을 하기 위한 Pytorch를 사용하기 위해
img_tensor = torch.tensor(img_np, dtype=torch.float32)
print(img_tensor.shape)
print(img_tensor)

# 4. 표준화 및 정규화(Scaling) : 0~255의 값을 0~1사이값으로 변환  ...  정규화/표준화를 해야 모델의 성능이 올라감
img_tensor = img_tensor / 255.0
print(img_tensor)

# 5. 분류 모델에 넣을 때는 한줄로 나란히 배치 = 즉 2차원을 1차원 형태로 차원을 떨어뜨려야 함  ->  Flatten() 사용
data = img_tensor.reshape(1, 784)
print(data)
print(data.shape)
# 결과 : (1, 784)
# 기존에 28행, 28열짜리 2차원 이미지 자료형을 0행, 784열의 이미지 자료형으로 바꾸었다.
# 그때 이 한 행(한 줄)에는 숫자 '4'에 해당하는 패턴이 생겼다. 이제 컴퓨터는 이 패턴을 학습한다.

# 정규화된 784열 tensor(이미지에 대한 밝기 자료)를 28x28 형태로 변환(원본 복원)한 후 다시 시각화
plt.imshow(data.reshape(28, 28), cmap='Greys')
plt.title('Normalized image')
plt.show()
