# 로또 : 45개의 공을 기계에 넣고 혼합한(난수가 생성) 후 6개를 뽑은 그 수의 나열과 내가 적은 숫자의 나열이 맞으면..나는 벼락부자 ㅎ
# 45개의 공도 객체, 공을넣는 기계도 객체이다. 

# 로또 번호 출력기

import random # 난수 생성

class LottoBall:
    def __init__(self, num):
        self.num = num

class LottoMachine:
    def __init__(self):
        self.ballList = []
        for i in range(1, 46, 1):
            self.ballList.append(LottoBall(i)) # 클래스의 포함관계

    def selectBalls(self):
#        for a in range(45):
#            print(self.ballList[a].num, end = ' ')

        random.shuffle(self.ballList) #shuffle은 내장함수 : 입력받은 값을 섞는다. = 볼 섞기

#        for a in range(45):
#            print(self.ballList[a].num, end = ' ') # 볼 섞은 값 출력

#        print('여섯 개 출력 : ', self.ballList[0:6]) # self.ballList[0:6]그냥 이렇게만 적어주면 객체의 주소만 찍힌다. 숫자를 받으려면

        return self.ballList[0:6] # 볼을 섞은 후 6자릿수 값 출력

class LottoUI :
    def __init__(self):
        self.machine = LottoMachine() # 클래스의 포함관계
    def playLotto(self):
        input("로또를 시작하려면 엔터키를 누르세요.")
        selectedBalls = self.machine.selectBalls()
        for ball in selectedBalls: # selectedBalls는 LottoBall의 객체이다
            print(ball.num)


if __name__ == "__main__":
#    machine = LottoMachine()
#    machine.selectBalls()
#   lot = LottoUI() # 로또유아이를 가지고 플레이로또를 가져오기 위해 객체변수를 썼다.
#   lot.playLotto()
    LottoUI().playLotto() #위 두줄과 실행결과 같음

# 클래스 문제 받아서 공유파일에 올리기