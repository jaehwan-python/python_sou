# pytorch에서 사용되는 연산자와 기본 함수

import numpy as np
import torch

x = torch.tensor(7)
y = torch.tensor(3)

print("1. 조건연산")
if x > y:
    result1 = torch.add(x, y)
else:
    result1 = torch.subtract(x, y)
print(result1)  # 결과 : tensor(10)

if x > 5 :
    result2 = "good"
elif x > 9 :
    result2 = "nice"
else:
    result2 = "ok"
# 텐서가 있는 조건문에서도 if가 가능하다!
print()


print('2. 관계연산')
print(torch.eq(torch.tensor(1), torch.tensor(2)))  # = 
print(torch.ne(torch.tensor(1), torch.tensor(2)))  # !=
print(torch.lt(torch.tensor(1), torch.tensor(2)))  # < 
print(torch.gt(torch.tensor(1), torch.tensor(2)))  # >
print(torch.ge(torch.tensor(1), torch.tensor(2)))  # >=
print()


print("3. 논리연산")
print(torch.logical_and(torch.tensor(True), torch.tensor(False)))  # and
print(torch.logical_or(torch.tensor(True), torch.tensor(False)))   # or 
print(torch.logical_not(torch.tensor(True)))                       # not


print("4. 유일값")
kbs = torch.tensor([1, 2, 2, 3, 2])
val = torch.unique(kbs)
print('val : ', val)
val, idx = torch.unique(kbs, return_inverse=True)  # 각 원소에 대응하는 유일값의 인덱스 반환
print("val : ", val)
print("idx : ", idx)
print()


print("5, 차원 떨어트리기(reduce)")
ar = torch.tensor([[1., 2.], [3., 4.]]) # 2차원이다!
print(torch.mean(ar).item()) # 전체 평균 = 2.5 # item은 원소가 한 개인 tensor에서 값이 1개인 출력값을 얻을 때 사용하는 함수이다.
# 2차원 자료 구조를 1차원으로 떨어트림

# 각 열 평균
print(torch.mean(ar, dim=0).numpy())
# 각 행 평균
print(torch.mean(ar, dim=1).numpy())
# 각 열만을 기준으로 평균을 도출할 때 item함수를 사용하면 오류가 남. 
# 왜냐하면 item은 한 개의 값만 도출할 때 쓸 수 있는데 이와 같은 코드는 복수개의 출력값을 반환하기 때문에 
# item을 사용하면 오류가 난다.
print()


print("6. 원소의 값과 순서를 유지하면서 텐서의 모양(shape)을 바꾸기(reshape)")
t = np.array([[[0,1,2], [3,4,5], [6,7,8], [9,10,11]]]) 
# 3차원 구조의 배열이 만들어짐 = (1,4,3) : 행렬1개, 4행/3열
# 원소 3개인 1차원 벡터가 4행으로 이루어져 4행3열 구조를 이룬 2차원 행렬이다
# 그 "2차원 행렬 1개"를 3차원 배열에 담았다.
# 스칼라  ->  벡터('1차원')  -> 행렬('2차원'(몇행/몇열))  ->  배열/텐서(다차원-대괄호로 정함) 
# 즉 위 구조는 그럼 지금 66번째 줄부터는 기존의 0부터 11까지 12개의 스칼라 값을 가진 원소를 3개씩 1차원인 벡터로 끊어서 나열한 1개의 행렬(4행3열)을 3차원으로 표시한 배열이다.
print(t.shape)
t_tensor = torch.tensor(t)
print(t_tensor.shape)
print(torch.reshape(t_tensor, shape=(12,)))
print(torch.reshape(t_tensor, shape=(2, 6)))
print(torch.reshape(t_tensor, shape=(-1, 6))) # 행 갯수 자동 결정
print(torch.reshape(t_tensor, shape=(2, -1))) # 열 갯수 자동 결정
print()


print("7. squeeze : 차원축소(shape에서 크기가 1인 차원을 제거)")
print(torch.squeeze(t_tensor))
print(torch.squeeze(t_tensor).shape)
print()

t2 = np.array([[[0], [3], [6], [9]]])
t2_tensor = torch.tensor(t2)
print(t2_tensor.shape)
print(torch.squeeze(t2_tensor)) 
print(torch.squeeze(t2_tensor).shape)
print()


print("8. unsqueeze : 차원확대")
tarr = torch.tensor([[1,2,3],[4,5,6]])
print(tarr.shape) # torch.Size([2, 3])

# dim=0 : 맨 앞에 크기 1인 차원을 추가하여 (2, 3)을 (1, 2, 3)으로 변경한다. 즉, 2행 3열 행렬 1개를 담은 3차원 텐서가 된다.
sbs = torch.unsqueeze(tarr, dim=0)  # dim=0 자리에 새로운 차원을 생성함
print(sbs.shape)
print(sbs.numpy())

# dim=1 : 두 차원 사이에 크기 1인 차원을 추가하여 (2, 3)을 (2, 1, 3)으로 변경한다. 즉, 1행 3열 행렬 2개를 담은 3차원 텐서가 된다.
sbs = torch.unsqueeze(tarr, dim=1)  # dim=1 자리에 새로운 차원을 생성함
print(sbs.shape)
print(sbs.numpy())

# dim=2 : 맨 뒤에 크기 1인 차원을 추가하여 (2, 3)을 (2, 3, 1)로 변경한다. 즉, 3행 1열 행렬 2개를 담은 3차원 텐서가 된다.
sbs = torch.unsqueeze(tarr, dim=2)  # dim=2 자리에 새로운 차원을 생성함
print(sbs.shape)
print(sbs.numpy())

# dim=-1 : 마지막 위치에 크기 1인 차원을 추가한다. 여기서는 dim=2와 같으며, (2, 3)이 (2, 3, 1)인 3차원 텐서가 된다.
sbs = torch.unsqueeze(tarr, dim=-1)  # dim=-1(마지막 위치)자리에 새로운 차원을 생성함
print(sbs.shape)
print(sbs.numpy())
print()


print("9. type변환 : 자료형변환")
# python자료형  ->  tensor자료형
num = torch.tensor([1, 2, 3])
print(num, num.dtype) # tensor([1, 2, 3]) torch.int64
num2 = num.to(torch.float32)
print(num2, num2.dtype)
print()


print("10. 텐서 합치기 : " \
" -> 1. torch.cat - 텐서 이어 붙이기, " \
" -> 2. torch.stack - 텐서 쌓기")
t1 = torch.tensor([1, 2, 3])
t2 = torch.tensor([4, 5, 6])
# 1. 텐서 이어 붙이기
cat_res = torch.cat((t1, t2), dim=0)
print(cat_res)
print()

# 2. 텐서쌓기
stack_res = torch.stack((t1, t2), dim=0)
print(stack_res)
