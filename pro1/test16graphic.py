# 전문가들이 만들어 둔 파이썬 지원 그래픽 모듈 사용

from turtle import * # 기본적으로 그림 모듈은 지원되지 않지만 turtle그래픽은 가능하다.

p = Pen()
p.color('red', 'yellow')
p.begin_fill()

while True:
    p.forward(200)
    p.left(170)
    if abs(p.pos()) < 1:  # 메서드와 함수에서 뒤에 괄호를 치는 것의 의미는?
        break

p.end_fill()
input()

# 이렇듯 모듈을 이용하면 파이썬으로 할 수 없는 작업을 할 수 있다.