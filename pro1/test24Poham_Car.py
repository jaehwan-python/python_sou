'''
여러 개의 부품 객체를 조립해 완성된 차를 생성
클래스의 퐇마 관계 사용 (자원의 재활용)
포함관계 : 다른 클래스(객체)를 마치 자신의 멤버처럼 선언하고 사용
'''

'''
import test24Poham_Handle
from test24Poham_Handle import Poham_Handle
'''

'''
test24Poham_Handle.Poham_Handle.quantity
Poham_Handle.quantity
'''



from test24Poham_Handle import Poham_Handle

class Poham_Car:
    turnShowMessage = '정지'

    def __init__(self, ownerName):
        self.ownerName = ownerName 
        self.handle = Poham_Handle()  # 클래스의 포함관계
        # Poham_Car에서 Poham_Handle의 객체변수를 생성해서 self.handle이 받게 된다. = 포함관계(has-a)관계이다.

    def turnHandle(self, q):
        # 회전량(q) : 양수면 우회전, 음수면 좌회전, 0이면 직진이라고 정의해보자.
        if q > 0: # 우회전
            self.turnShowMessage = self.handle.rightTurn(q) # 포함car에는 없지만 포함handle이 rightTurn을 가지고 있어서 그곳에서 불러온다.
        elif q < 0:
            self.turnShowMessage = self.handle.leftTurn(q)
        elif q == 0:
            self.turnShowMessage = "직진"

if __name__ == "__main__":  # 응용프로그램의 시작이 이곳이 맞는가?
    tom = Poham_Car("미스터 톰")
    tom.turnHandle(10)  # 양수를 주어줌
    print(tom.ownerName + "의 회전량은 " + tom.turnShowMessage + " " + str(tom.handle.quantity)) 

print()

john = Poham_Car("미스 존")
john.turnHandle(-10)  # 이번에는 음수를 주어줌
print(john.ownerName + "의 회전량은 " + john.turnShowMessage + " " + str(john.handle.quantity)) 