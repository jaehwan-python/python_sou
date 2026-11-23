# Pytorch(파이토치)는 파이썬 기반의 오픈 소스 딥러닝 및 머신러닝 프레임워크이다.

# 다음 카페 : TF DL AI의 Tensorflow, PyTorch가서 자료확인 꼭!! 별로 안많음

# 3차 프로젝트(탱크)를 할 때, 그래프 알고리즘의 다익스트라와 A*알고리즘을 사용한다!!

# < 핵심 특징 > 
# 1. 동적 계산 그래프(Dynamic Computational Graph) : 코드 실행 시 연산에 따라 계산 그래프가 동적으로 생성되므로, 조건문과 반복문을 사용해 모델의 연산 흐름을 유연하게 구성할 수 있다.
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

print("11월 23일(월)", "__" * 30)

print("1. python, numpy, pytoch 간 형변환이 가능하다.")
print(7)
print(torch.tensor(7))            # scalar(상수) -> 텐서(tensor)
print(torch.tensor(7).item())     # 텐서(tensor) -> 상수(scalar)
print(torch.tensor([1, 2]).numpy) # 텐서(tensor) -> 배열(numpy)

arr = np.array([1, 2])
torch_arr = torch.tensor(arr)
print(torch_arr)             # tensor([1, 2])
print(torch.from_numpy(arr)) # tensor([1, 2])
# 배열(array)  ->  텐서(tensor)
print()


print("2. 텐서를 사용하는 Pytorch에서의 사칙 연산")
# torch.add(),  torch.subtract(),  torch.multiply(),  torch.divide()
torch_result = torch.add(torch_arr, 5)
print(torch_result)

np_result = np.add(torch_result.numpy(), 2)
print(np_result)
# 이렇게 Tensorflow에 비해 Pytorch는 파이썬을 사용하는 것처럼 쓸 수 있어서 더 유연하다!
print()


print("3. in-place연산이란?")
v1 = torch.tensor(1.0)
print("변경 전 v1 : ", v1, id(v1))  # 결과 : tensor(1.) 2339890596304

# 기존 참조값을 갱신
v1.fill_(100)
print("변경 후 v1 : ", v1, id(v1))  # 결과 : tensor(100.) 2339890596304
# 치환을 의미한다. 원래 객체 1.0이 있는 자리가 100이라는 값으로 덮어씌우기가 된다. 그래서 객체 주소의 값(자릿값)은 변하지 않는다. 

# 새로운 객체를 참조
v1 = 100
print("변경 후 v1 : ", v1, id(v1))  # 결과 : 100  140730456666328
# 원래 객체의 주소(tensor(100.))를 버리고 새롭게 얻은 값의 객체 주소를 가진다. 즉, 새로운 자리의 100이라는 객체 주소가 v1의 자리를 새롭게 가리키게 된다.

# 그 외 연산 메서드(메모리와의 개념을 연결해서 이해하기!)
# fill_,  copy_(),  add_(),  sub_(),  mul_(),  div_() = in-place연산 : 새로운 객체를 참조하는 것이 아니라 기존 참조를 받던 객체의 자리는 유지한 채 값만 바꾼다.
print()

v1 = torch.tensor(1.0)
print(v1.data_ptr())  # 실제 데이터 저장 위치를 출력하는 코드
v1.copy_(torch.tensor(123.0))
print(v1.data_ptr())
print('v1 : ', v1)

v2 = torch.ones((2,)) # (2,) : 원소가 2개인 1차원 형태를 '1'이라는 값으로 칸을 채운다.
print('v2 : ', v2)
print(v2.data_ptr())

v2.copy_(torch.tensor([30.0, 40.0]))
print("v2 : ", v2)
print(v2.data_ptr())

print()

aa = torch.zeros((2,1)) # 모든 원소가 '0'인 2행1열의 2차원 tensor를 만드는 것
print("aa : ", aa)
# 결과 :   aa :  tensor([[0.],
#                        [0.]])

aa.copy_(torch.ones((2,1)))
print('aa : ', aa)
# 결과 :   aa :  tensor([[1.],
#                        [1.]])

aa.add_(torch.tensor([[2.0], [3.0]]))
print("aa : ", aa)
# 결과 :   aa :  tensor([[3.],
#                        [4.]])
# 이 in-place의 핵심은 v2의 저장공간을 유지하면서 내용만 바꾼다는 것이다. [1., 1.]  ->  [30., 40.]

print("\n4. numpy vs tensor", "둘 다 2행 1열인 자료구조를 만들지만 역할이 다르다.")
a = np.zeros((2, 1))
print(type(a))
# 결과 - numpy배열의 ndarray객체(float64)
#      - 연산장치 : CPU 
#      - 자동미분 제공 X ... 수치 계산, 데이터 처리에 사용

b = torch.zeros((2, 1))
print(type(b))
# 결과 - Pytorch텐서의 Tensor객체(float32)
#      - 연산장치 : CPU/GPU
#      - 자동미분 제공 O ... 딥러닝, 수치 계산에 사용
print()
# 아마존 서버 ec2서버, 클라우드, 도커, CI/CD, 아마존에는 '모델'이 다 있어서 직접 생성할 필요X ... 하지만 그래도 그 구조는 알아야 함.
# 11월에는 머신러닝을 배웠고, 12월 달에는 딥러닝의 CNN와 NLP를 배우고 이는 Transformer를 기반으로 하는 LLM의 구조의 이해로 이어진다.


print('5. 난수 처리')
# python, numpy, pytorch에서 사용되는 문법구조(연산, 난수생성, 균등분포 등)의 표현 방법은 모두 서로 다르다!!
torch.manual_seed(42)  # 고정된 난수 재현이 가능하다.
print(torch.rand(1)) # 결과 : tensor([0.8823])
print()


print('6. 균등 분포와 정규분포')
# 1. 균등분포
print(torch.empty(2).uniform_(0, 1)) # 균등분포에서 뽑은 난수 2개. 모두 0 이상 1 미만
print(torch.empty(30000).uniform_(0, 1).mean()) # 균등분포 난수 30,000개의 평균. 0.5에 가까움

# 2. 정규분포
print(torch.randn(3)) # 표준정규분포에서 뽑은 난수 3개. 음수도 나올 수 있음
print(torch.randn(30000).mean()) # 표준정규분포 난수 30,000개의 평균. 0에 가까움
print(torch.empty(3).normal_(mean=0, std=1)) # 평균이 '0'이고 표준편차가 '1'인 정규분포가 생긴다.
print(torch.normal(mean=0.0, std=1.0, size=[3]))
print()

print("**GPU 텐서와 numpy배열에서 알아야 할 점**")
# "GPU 텐서"는 GPU에서 '병렬 연산'과 '자동 미분'을 수행하는 다차원 배열이며, NumPy 배열은 주로 CPU 메모리에서 동작하는 과학 계산용 배열입니다.
# 실무에서 함께 다룰 때 꼭 알아야 할 핵심 사항은 다음과 같습니다.

# 1. 장치(Device) 일치와 변환 규칙
# • 같은 장치끼리 연산: 텐서와 모델(또는 다른 텐서)은 반드시 같은 장치(cpu 또는 cuda)에 있어야 연산됩니다.
# • NumPy 변환 제약: .numpy()로 NumPy 배열을 만들려면 텐서가 CPU에 있어야 합니다. GPU 텐서라면 .cpu().numpy() 순서로 옮긴 뒤 변환해야 합니다.
# • 데이터 복사/공유 주의: torch.from_numpy()는 CPU 텐서로 변환할 때 메모리를 공유하는 경우가 많아 원본 수정 시 영향을 줄 수 있습니다.

# 2. 전송 오버헤드와 연산량
# • 잦은 CPU↔GPU 이동 금지: 데이터를 CPU와 GPU 사이로 자주 옮기면 통신 비용 때문에 오히려 느려질 수 있습니다.
# • 적절한 규모에서 GPU 사용: 작은 배열이나 단순 연산은 전송·커널 실행 오버헤드 때문에 CPU(NumPy)가 더 빠르거나 비슷할 수 있습니다.

# 3. 자동 미분(requires_grad)과 그래프 분리
# • 그래프 추적: PyTorch 텐서는 requires_grad=True일 때 연산 기록을 남깁니다.
# • NumPy 전환 시 분리: 기울기 추적이 활성화된 텐서를 NumPy로 바꾸려면 .detach().cpu().numpy()처럼 계산 그래프에서 먼저 분리해야 합니다.

# cuda는 nvida gpu에서만 돌아가는 cpu이다.
if torch.cuda.is_available():
    gpu_tesnor = torch.tensor([1,2,3], device='cuda') # GPU에서 tensor를 생성한 것이다. 
    np_from_gpu = gpu_tesnor.cpu().numpy() # GPU텐서를 cpu로 이동한 후 numpy배열을 생성한다.
    print(f"gpu텐서  -> numpy배열로 변환 : {np_from_gpu}")
else : 
    print('cuda지원을 하지 않음')

