kor = 100 # 모듈의 멤버 : 전역변수

def abc():
    kor = 0 # 함수 내의 지역변수
    print('모듈의 멤버 함수')

class My:  # 클래스는 멤버변수나 메서드가 들어있다
    kor = 80 # My 클래스의 멤버변수(My type 객체의 공유자원)

    # def __init__(self):   # 생성자를 호출 .. 초기화 작업이 없는 경우, 생성자는 생략 가능하다.
        #  pass
    

    def abc(self):
        print('My 클래스 멤버 메서드')

    def show(self):
        # kor = 77  # 메서드 내의 지역변수
        print(kor)
        print(self.kor)
        abc()
        self.abc()
myObj = My() # ...My의 설계도 획득
myObj.show() # myObj가 show로 들어간다. kor값은 77(지역변수)이 나온다. self.kor(myObj객체에서 찾아봐)은 없다. myObj안에 값이 없어 클래스 내 전역변수인 80이 나온다.
# 만약 kor = 77이 없으면 kor값은 전역변수인 100dl skdhrh self.kor 값으로 80이 나온다.
print('------------------------------------')

myObj2 = My()
print(myObj2.kor)
myObj2.kor = 99
print(myObj2.kor) # 99

print('-----------------------------------')

myObj3 = My()
myObj3 = My()
print(myObj3.kor) # 80