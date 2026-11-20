# Pytorch(파이토치)는 파이썬 기반의 오픈 소스 딥러닝 및 머신러닝 프레임워크이다.

# 다음 카페 : TF DL AI의 Tensorflow, PyTorch가서 자료확인 꼭!! 별로 안많음

# 핵심 특징
# 1. 동적 계산 그래프(Dynamic Computational Graph) : 코드 실행 시
# 2. 텐서 및 자동 미분(autograd) : GPU/가속기 연산을 지원하는 다차원 텐서와 역전파를 위한 자동 미분을 제공한다.
# 3. 성능 최적화 및 분산 학습 : torch.compile을 통한 컴파일 최적화와 torch.distributed기반의 대규모 분산학습을 지원한다.
# 하드웨어 호환성 : CUDA(NVIDA GPU), ROCm, MPS등 다양한 가속환경을 지원한다.

# Perceptron과 mlp의 개념을 알아야 한다!!
# Perceptron :
# mlp(multi layer perceptron)

# 모듈 설치
# pip install torch torchvision torchaudio
# pip install tensorflow

# Tensor  ->  Numpy 차이 : 형변환 -> Tensor값 변경  ->  in-place연산  ->  난수 흐름

import numpy as np
import torch
print("GPU 사용 가능 여부 : ", torch.cuda.is_available())
print("GPU장치 정보 : ", torch.cuda.get_devide_name(0) if torch.cuda.is_available() else[])
# 내 실행환경 = Intel·AMD 내장 그래픽만 있는 경우로 일반적인 NVIDIA CUDA 환경을 사용할 수 없다
# 그리고 NVIDA의 CUDA 지원 없이 Pytorch가 설치된 것이다. 그런데 굳이 설치할 필요없다. 왜?
# 우리가 사용하는 Pytorch(!=Tensorflow)는 기본적으로 Eager Execution(즉시 실행) 방식으로 동작한다.
# 나는 intel(R) iris(R)로 내장 GPU라서 NVIDA용 CUDA를 사용할 수 없다. 그냥 우리는 내장 GPU를 사용하는 것이다.

print('\nTensor : 데이터를 Pyroch에서 데이터를 담는 기본 자료구조(숫자 데이터 저장용 다차원 배열)')
# Tensor는 ndarray와 유사하나 Pytorch 연산에 사용되도록 만들어진 객체(딥러닝 연산, GPU연산, 자동미분..들이 가능해진다.)
print(12, type(12))            # 결과 : <class 'int'> : 파이썬 상수로 파이썬이 직접
print(torch.tensor(12))        # 결과 : tensor(12) : 0차원 텐서 = scalar
print(torch.tensor([12]))      # 결과 : tensor([12]) : 1차원 텐서 = vector
print(torch.tensor([[12]]))    # 결과 : tensor([[12]]) : 2차원 텐서 = matrix
print(torch.tensor([[12, 1]])) # 결과 : tensor([[12,  1]]) : 다차원 텐서

# 딥러닝 연산 시 반드시 tensor로 바꾸어 주어야만 한다!! 

print('\nTensor 속성 확인(텐서의 차원 수 확인)')
# 우리의 최종 목표 : **Pytorch에서 Regression과 Classificationi을 연산하는 방법**
print(torch.tensor([[12, 1]]).dim())
t = torch.tensor([[1,2,3], [4,5,6]], dtype=torch.float)
print('shape : ', t.shape)
print('dtype : ', t.dtype)
# 결과 : 
# shape : torch.Size([2, 3])
# dtype : torch.int64
print()

imsi = np.array([1, 2])
print(imsi, type(imsi))  # 결과 : <class 'numpy.ndarray'>
imsi[0] = 10
print(imsi)

# Pytorch Tensor
a = torch.Tensor([1, 2]) 
print(type(a))  # 결과 : <class 'torch.Tensor'>
a[0] = 10
print(a)
print()

# tensor 요소 더하기
a = torch.tensor([1, 2])
b = torch.tensor([3, 4])
c = a + b
print(c)
# 결과 : tensor([4, 6])

# tensor연산 - Broadcasting도 가능하다.
d = torch.tensor([3])
e = c + d
print(e)
# 결과 : tensor([7, 9])


