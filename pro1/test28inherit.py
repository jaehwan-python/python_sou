# <2교시>
'''
고조할아버지  ->  증조할아버지  ->  할아버지  ->  아버지  ->   나   ->   아들   ->  손자
'''

class Person: # 부모 클래스로 사용할 예정 
# 멤버 : say, nai
# 메서드 : printInfo, helloMethod
    say = "난 사람이야~"
    nai = '20'
    __msg = "'good' =  Private 멤버 - 현재 클래스에서만 유효, 접근 권한이 상당히 제한적. 형태는 '__'로 시작"

    def __init__(self, nai):
        print('person 생성자')
        self.nai = nai

    def printInfo(self):
        print(f"나이 : {self.nai}, 이야기 {self.say}") # 여기서 self.nai는 __init__과 Person class에서 동일한 수준의 __init__으로 가서 nai값을 받는다.

    def helloMethod(self):
        print('안녕')
        print('hello : ', self.say, self.nai, self.__msg) # self.say, self.nai : Public 멤버 // self.__msg : Private 멤버

print(Person.say, Person.nai) # 원형 클래스로 멤버를 호출 한다 ... 비권장하는 방법! 클래스의 이름으로 멤버의 이름을 부르는 방법은 좋지 않다.
# 설계도.함수 x

# -opp-
# 변수 = 설계도 # 객체를 우선 만들고 그 이름으로 함수를 호출한다.
# 변수.함수.함수...로 수행
# Person.printInfo() ... error : self를 만족시키지 못했기 때문이다.

per = Person('23') # 문자열 형태로 줘야 함.
per.printInfo()
per.helloMethod()
# 객체 변수로 필드멤버/메서드 호출하는 방법 = 권장!!

print('---------------------------')

class Employee(Person):
    subject = '근로자'
    say = '일하는 동물' #  = hiding = shadowing : 부모클래스가 가지고 있는 멤버와 자식클래스갸 가지고 있는 멤버가 같은 경우, 자식킆래스가 가지고 있는 멤버가 우선시 되어 나온다.

    def __init__(self):
        print('Employee 생성자')

    def printInfo(self): #부모의 메서드와 자식의 메서드 같은 것(내용은 다름)을 메서드 오버라이딩(overriding)이라고 한다. ... 추후에 다형성과 연결된다.
        print('Employee 클래스의 printInfo 호출됨.')

    def ePrintInfo(self):
        print(self.subject, self.say, self.nai)
#       print(self.__msg) # 부모 클래스의 Private 멤버를 호출한 것이다. ... AttributeError : 현재 클래스에는 없다. 부모 클래스에 있다. 그런데 왜 안가져와? __msg는 Person class 내에서만 사용할 수 있는 Private 멤버이기 때문이다
        self.helloMethod() # 이런 경우 helloMethod 메서드 안에는 Private가 있지만 출력되는 이유는 우리가 self.helloMethod를 통해 부모 메서드를 불러주었고 그 부모 메서드 안에서 __msg를 호출한 것이기 때문에 출력 가능하다.
        self.printInfo() # 현재 클래스에서 먼저 검색 후 없으면 부모 클래스에서 메서드를 호출한다.
        super().printInfo() # 현재 클래스가 아니라 무조건 부모메서드를 바로 호출
        print(self.say, super().say) # 일하는 동물 난 사람이야~

emp = Employee() # emp 객체 생성
print(emp.subject, emp.nai, emp.say)
emp.printInfo()
emp.ePrintInfo()

print('------------------------')
class Worker(Person):
#   def __init(self):
#   pass
    def __init__(self, nai): 
        print('Worker 생성자')
        super().__init__(nai) # 부모 클래스의 생성자로 간다. 

    def wPrintInfo(self):
        print('Worker - wPrintinfo 처리')
        self.printInfo()
        super().printInfo()

wor = Worker('30') # 이런 경우 Person 생성자로 들어간다. 
print(wor.say, wor.nai)
wor.wPrintInfo()

print()

print('----------------')
class Programmer(Worker):
    def __init__(self, nai):
        print('Programmer 생성자')
#       super().__init__(nai) # 부모 클래스의 생성자 호출 # Bound Method Call
        Worker.__init__(self, nai) # Unbound Method Call

    def pPrintInfo(self):
        print('Programmer - pPrintInfo() 처리함')

    def wPrintInfo(self):
        print('Programmer 클래스에서 오버라이딩함') # 부모와 같은 이름의 메서드가 있다 그때 이것을 오버라이딩이라고 한다.

pro = Programmer('35')
print(pro.say, pro.nai) 
# Programmer에 say가 있으면 그대로 쓸것이지만 없다. 부모 클래스인 Worker로 간다. nai가 있다. 근데 그 때 nai는 
# super()가 있기 때문에 가장 높은 부모인 Person으로부터 nai를 받는다.
pro.pPrintInfo()
pro.wPrintInfo()



print()
print("클래스 타입 확인 -------")
a = 3; print(type(a)) # <class 'int'> : Maker가 만든 기본 타입이다
print(type(pro))      # <class '__main__.Programmer'> 메인환경에서 프로그래머 타입의 클래스가 실행됨
print(type(wor))      # <class '__main__.Worker'> 메인환경에서 워커 타입의 클래스가 실행됨

print(Person.__bases__)     # (<class 'object'>,) : Person의 상위 클래스는 object이다. ... 모든 클래스의 최종 상위 클래스는 Maker가 만든 object이다. 
print(Employee.__bases__)   # (<class '__main__.Person'>,)
print(Worker.__bases__)     # (<class '__main__.Person'>,)
print(Programmer.__bases__) # (<class '__main__.Worker'>,) 각 클래스의 상위 클래스를 확인할 수 있다.

# print(자식 클래스.__bases__) : 부모 클래스의 위치를 알 수 있다.
