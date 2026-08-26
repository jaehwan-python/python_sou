'''
oop : "객체지향(객체중심)적인 프로그래밍 가능하여 상속, 포함, 다형성 등의 기법 구사가 가능하다"
class : 멤버변수(필드) + 멤버 메소드로 구성
인스턴스에 의해 새로운 이름공간은 가진다.
클래스 -> 포함  ->  상속  ->  오버라이딩  ->  다형성  ->  다중상속
'''
# 모듈의 구성 : 스테이츠먼츠, 변수, 함수, 클래스이다

a = 2

print(a)

def func():
    print('ok')


class TestClass: # ~ 클래스의 헤더 / 클래스의 이름은 대문자로 주자!!_약속!!

    aa = 1  # TestClass의 멤버변수(필드) / TestClass 안에서만 전역변수이다.
    def __init__(self):  # 특별 메서드의 첫 인자(parameter)는 self(키워드)이다. # __init__ : 이미 어떤 기능이 들어가 있는 키워드
        print('생성자 : 객체 생성시 가장 먼저 1회만 호출 - 초기화를 담당')

    def __del__(self): # 특별 메서드
        print('소멸자 : 프로그램 종료시 자동실행, 마무리 작업을 담당')

    def showMessage(self): # 일반 메서드
        name = '한국인'  # 지역변수 : showMessage에서만 유효
        print(name)
        print(self.aa) # ~ 클래스의 바디

print(TestClass)
print('클래스멤버 a :', TestClass.aa)
# TestClass.showMessage()# ... type error ... ()안에 받은게 없어서 작업하지 못함.

# 클래스 생성자를 이용해 객체 생성 후 해당 객체의 주소를 객체변수에 치환한 것이다.
test = TestClass()   # 생성자를 호출한거다. instance를 하는 것이다. -> object가 생성된다 = 하나의 객체가 그려진다.
print('클래스 멤버 a : ', test.aa)

#1. Bound Method Call
test.showMessage() # = 'test'라는 변수가 괄호안에들어간다. # 자동으로 객체변수 test가 메서드의 인수로 담겨 호출이된다.

# Unbound Method Call
TestClass.showMessage(test) # 위와 같은 뜻


print()

# 클래스 내에는 함수가 들어올 수 없다. 클래스 내에는 멤버변수와 메서드만 존재한다. self의 유무로 클래스의 여부를 따진다. self는 키워드다 바꾸면 안된다.
# def 메서드(self):  :   클래스의 형태

# aa : 속성
# 메서드 : 행위


# 다음예시

print(type(1))
print(type(1.0))
print(type('ok'))
print(type(test)) #...새로운 type을 만든다.

print(id(test))  # 주솟값이 서로 다르다
print(id(TestClass)) # 주솟값이 다르다
test2 = TestClass() # 객체 한개 더 생성한겨
print(id(test2))



