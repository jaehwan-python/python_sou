# 딥러닝 모델 학습의 기본은 
# 1. 입력데이터를 모델에 전달하여 예측 결과를 얻고
# 2. 지속적으로 그 결과와 실제값 간에 오차를 줄이기 위한 모델의 파라미터(weight, bias)를 갱신하는 과정이다.

# ------------------------------------------------------------
# 실습1) 택시 요금 예측 모델 : "y = 2x + 5"
# 기본 요금(bias) : 5000원  +  거리 당(weight) 2000원 추가

print('거리에 따른 택시요금이 얼마나 나올까?(모델의 예상) ')
def taxi_fare_model(distance):  # distance : 이동거리
    weight = 2   # 1km당 2000원
    bias = 5     # 기본요금 5000원
    fare = weight * distance + bias  
    return fare

distance = 5  # 이동거리 = 5km
predicted_fare = taxi_fare_model(distance)
print(f"{distance}km 이동 시 예상 택시 요금 : {predicted_fare},000원")  #  = 순전파가 이루어짐!
print()

print('그런데 실제 taxi요금값이 13,000원이 나왔다.') # 예측한 값과 2,000원 차이가 난다.
# 즉, 모델의 오차(실제값-예측값)의 보정이 필요하다. 
# 즉, 가중치(weight)수정이 필요하다!!
print()

actual_fare = 13
predicted_fare = 15
cost_error = predicted_fare - actual_fare
print(f"오차 : {cost_error},000원(너무 비싸게 예측)")
# 택시요금의 기본값(bias)가 5000원이었으므로 bias는 냅두고 weight만 조정한다.
# 파라미터를 수정해야한다 = 역전파 과정이다

# 역전파 작업(Parameter갱신(weight와 bias갱신작업))

# 경사하강법 정리해두기!
# ------------------------------------------------------------
# <역전파 - Parameter갱신 방법 >
# 직접 수식으로 구현해보거나 혹은 Pytorch lib를 사용하여 parameter(weight, bias)를 조정해보자.

print("[방법1] : 직접 수식으로 구현")
# [방법1] : 직접 수식으로 구현 -> learningrate와 epoch를 조율
weight = 2
bias = 5
distance = 5
learning_rate = 0.01 # 학습률 : 1회 학습할 때, weight와 bias를 얼마나 수정할지 결정하는 수. 이 학습률을 사용하여 직접 parameter를 조정한다.

new_weight = weight - learning_rate * cost_error * distance  # = (2 - 0.01) * 2 * 5
new_bias = bias - learning_rate * cost_error
# 학습율이 1회 적용된 새로운 w,b값
print(f"새로운 weight : {new_weight:.2f}")
print(f"새로운 bias : {new_bias:.2f}")

# 새로운 가중치와 편향으로 다시 예측
new_predicted_fare = new_weight * distance + new_bias
print(f"새로운 예상 택시요금 : {new_predicted_fare:.2f}천원") # = 14.48 = 14480원

print("\n 택시 요금 모델 반복학습 -> cost(오차(실제값-예측값))를 줄이기 위한 노력")
actual_fare = 13
weight = 2
bias = 5

for i in range(10):
    predicted_fare = weight * distance + bias  # 현재 모델로 예측
    error = predicted_fare - actual_fare # 실제값과의 오차
    print(f"{i + 1}회 학습 전 -> 예측 : {predicted_fare}천원, 오차 : {error:.2f}")

    # 오차를 이용하여 weight, bias를 갱신하였다(역전파르 통한 갱신)
    weight = weight - learning_rate * error * distance
    bias = bias - learning_rate * error

print("\n반복 완료")
print(f"최종 weight : {weight :.4f}, 최종 bias : {bias:.4f}")
# 최종 갱신된 weight, bias로 예측
final_fare = weight * distance + bias
print(f"반복 완료 후 최종 예상 택시 요금 : {final_fare:.2f}천원")
# 결과 :
#  택시 요금 모델 반복학습 -> cost(오차(실제값-예측값))를 줄이기 위한 노력
#  1회 학습 전 -> 예측 : 15천원,                 오차 : 2.00
#  2회 학습 전 -> 예측 : 14.48천원,              오차 : 1.48
#  3회 학습 전 -> 예측 : 14.095199999999998천원, 오차 : 1.10
#  4회 학습 전 -> 예측 : 13.810448000000001천원, 오차 : 0.81
#  5회 학습 전 -> 예측 : 13.599731519999999천원, 오차 : 0.60
#  6회 학습 전 -> 예측 : 13.443801324799999천원, 오차 : 0.44
#  7회 학습 전 -> 예측 : 13.328412980351999천원, 오차 : 0.33
#  8회 학습 전 -> 예측 : 13.243025605460481천원, 오차 : 0.24
#  9회 학습 전 -> 예측 : 13.179838948040755천원, 오차 : 0.18
# 10회 학습 전 -> 예측 : 13.133080821550159천원, 오차 : 0.13

# 반복 완료
# 최종 weight : 1.6343, 최종 bias : 4.9269
# 반복 완료 후 최종 예쌍 택시 요금 : 13.10천원

# 해석 :
# 오차가 10회 학습을 하게 되면서 오차는 점점 줄어들고 처음의 값인 15000원에서 점점 13000원으로 실제값에 가까워지고 있다.
# cost가 최소화되고 있따.  =  잔차제곱의합이 작아지고 있다.  = 아! 많이 학습할수록 좋구나~
# 단, 그렇다고 해서 너무 많이 학습하는 것은 좋지 않다. 괜히 자원을 낭비한느 것
# 즉, 학습횟수는 너무 적으면 오차가 커지고 너무 크면 자원을 낭비하는 것이다. 그러니까
# Learningrate와 epoch을 조율하여 학습횟수를 적절하게 정해야한다.
print("\n\n")
# ------------------------------------------------------------

print("[방법2] : Pytorch lib사용")
# [방법2] : pytorch의 backward메서드
import torch

# 택시 요금 모델 y = weight * distance + bias
distance = torch.tensor(5.0)  # 입력값 : 이동거리 5km
actual_fare = torch.tensor(13.0) # 실제 택시요금 : 13000원

# 학습해야할 값(weight, bias)  : 미분을 사용함
weight = torch.tensor(2.0, requires_grad=True) # autograd기능 : requires_grad=True를 입력하면 그래프에서 자동미분을 진행한다.
bias = torch.tensor(5.0, requires_grad=True) # autograd기능 O
# 즉, weight와 bias를 조정할 때 미분을 사용해야 하는데 그때 requires_grad=True를 사용한다.
# Pytorch Autograd는 신경망 학습을 위한 자동 미분 엔진으로, requires_grad=True인 텐서의 연산을 추적하여,
# 동적 계산 그래프(DAG)를 만들고 .backward()호출시 연쇄 법칙으로 기울기를 자동 계산한다.

# 학습율
learning_rate = 0.01  # 학습률
for i in range(10):
    # 1. 순전파(forward학습) : 현재 weight와 bias를 이용해 요금예측
    predicted_fare = weight * distance + bias
    error = predicted_fare - actual_fare  # 오차
    loss = 0.5 * error **2  # 손실함수 ... 제곱을 해주었기에 손실함수 값(loss)는 모두 양수가 나온다. = 학습의 방향을 결정한다.
    
    print(f"\n{i+1}회 학습 전  ->  예측 : {predicted_fare.item():.2f}천원, \
                                오차 : {error.item():.2f}, \
                                손실함수값 : {loss.item():.4f}")
    # error : 예측값과 실제값의 단순한 차이
    # loss : 위 차이(error)를 모델 학습에 사용할 수 있도록 수치화한 학습목표
    # **경사하강법은 error 자체가 아니라 loss가 최소가 되도록 weight, bias를 갱신하는 것이다.**

    # 실제값 : 13000     예측값 : 15000     error : 0.5     loss : 2  
    # error : 예측값과 실제값의 차이(오차)
    # loss : 그 오차가 얼마나 나쁜지를 보여준다.
    # 순전파로 error와 loss를 계산하였고 weight와 bias값이 맘에 들지 않아 다시 계산과정을 loss부터 역으로 올라간다. 
    # 왜냐하면 loss가 최소가 되도록 parameter(weight, bias)를 조정하기 위해서이다.


    # 2. 역전파(backpropargation) : loss기준으로 weight, bias의 기울기를 자동 계산(미분 사용)
    # 미분은 weight, bias를 조금 변화시켰을 때, loss가 얼마나 변하는지를 알기 위해 사용한다.
    loss.backward() # loss부터 거꾸러 계산하면 각 학습파라미터의 미분값을 자동으로 구한다.
    print('weight에 대한 기울기 : ', weight.grad.item()) # 기울기 > 0  ->  우로 갈수록 loss증가, 그럴때는 좌로 이동해야 loss가 감소한다.
    print('bias에 대한 기울기 : ', bias.grad.item())

    # weight(가중치)와 bias(편향) 수정 : gradient 계산 과정은 기록하지 않도록 no_grad사용
    with torch.no_grad(): # with 블록 안에서 실행되는 계산은 자동미분 기록에서 제외하자.
        weight -= learning_rate * weight.grad  # 가중치 수정
        bias -= learning_rate * bias.grad
        
    # 이전 gradient 초기화 : 왜냐하면 .backward()를 실행할 때, gradient를 누적하기 때문이다.
    weight.grad.zero_()
    bias.grad.zero_()

    print("\n학습 완료")
    print(f"최종 weight : {weight.item():.4f}")
    print(f"최종 bias : {bias.item():.4f}")

# 학습된 weight와 bias로 다시 요금을 예측한다.
final_fare = weight * distance + bias
print(f"\n최종 예상 택시 요금 : {final_fare.item():.2f}천원")
print("\n\n")
# 결과 : 
# 최종 weight : 1.6343
# 최종 bias : 4.9269
# 최종 예상 택시 요금 : 13.10천원
# ------------------------------------------------------------

print("[방법3] : Pytorch학습 코드를 사용하여 모델을 생성")
import torch.nn as nn
import torch.optim as optim

# 택시 요금 모델 : "y = weight * distance + bias"
distance = torch.tensor([[5.0]]) # 입력값 이동거리를 2차원형태로 줌 (nn.linear가 입력을 2차원 형태를 원한다)
actual_fare = torch.tensor([[13.0]]) # 실제값 택시요금을 2차원형태로 줌

# 1. 모델 생성
model = nn.Linear(1,1) # 입력층 1개, 출력층 1개, 은닉층은 없다.
# 편의상, 기존 예제와 동일하게 초기값 설정 : weight=2, bias=5로 설정
# 지금은 학습계산이 아니라 초기값을 직접 설정하는 작업이라 자동미분 기록X
with torch.no_grad():
    model.weight.fill_(2.0) # 텐서의 모든 값을 2.0으로 채움
    model.bias.fill_(5.0) # 텐서의 모든 값을 5.0으로 채움

# 2. 손실함수
loss_fn = nn.MSELoss() # 손실함수로 예측값과 실제값의 차이(오차)의 제곱의 평균값을 이 함수가 계산해준다.

# 3. 옵티마이저 : weight, bias를 자동으로 수정
optimizer = optim.SGD(model.parameters(), lr=0.01)

for i in range(10):
    # 순전파
    predicted_fare = model(distance)
    error = predicted_fare.item() - actual_fare.item() # 현재 예측 오차
    # 손실계산(손실함수)
    loss = 0.5 * loss_fn(predicted_fare, actual_fare)
    print(f"\n{i+1}회 학습 전  ->  예측 : {predicted_fare.item():.2f}천원,\
                                    오차 : {error:.2f},\
                                    손실함수값 : {loss.item():.4f}")
    
    optimizer.zero_grad() # 이전 gradient 초기화
    loss.backward()  # 역전파
    optimizer.step() # weight, bias의 실제 수정은 optimizer.step()가 한다.

print("\n학습 완료")
print(f"최종 weight : {model.weight.item():.4f}")
print(f"최종 bias : {model.bias.item():.4f}")

# 학습된 모델로 요금 예측
final_fare = model(distance)
print(f"최종 예상 택시 요금 : {final_fare.item():.2f}천원")
# 결과 :
# 최종 weight : 1.6343
# 최종 bias : 4.9269
# 최종 예상 택시 요금 : 13.10천원
# 앞으로 실습 시에는 3번 방법을 사용한다!!
