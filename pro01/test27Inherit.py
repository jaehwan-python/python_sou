# <1교시>

'''
상속 : 자원의 재활용을 목적으로 특정 클래스의 멤버를 가져다 쓰는 것 - 코드 재사용이 가능해지는 것이다.

특징
확장성 - 기존 클래스에 새 기능을 추가한 새로운 클래스 생성
구조적 설계 - 공통개념은 부모 클래스(Animal), 구체적 내용은 자식 클래스(Horse)에서 구현
다형성 구사 - 메서드 오버라이딩

부모가 자신에게 집을 주는 것 = move의 개념
부모class가 자식class에게 멤버필드(변수)나 메서드(행위)를 줄 수 있다 (자원의 재활용 목적) = copy의 개념

class와 class의 관계 : 포함관계는 느슨하지만 상속관계는 끈끈하다.

-명명법-
부모 class : 부모, 조상 super, parent, 상위 클래스
자식 class : 자식, 자손, sub, child, 파생, 하위 클래스

*객체지향적 프로그래밍은 자원의 재활용을 목적으로 한다.

파이썬은 접근 지정자가 없어 부모가 가져다 쓰는 변수와 메서드를 그냥 가져다 쓸 수 있다. 상속은 copy의 개념이다.

다중 상속 : 하나의 클래스는 여러개의 부모 클래스를 가질 수 있다.
추상 클래스 : 내용이 없는 메서드를 가지고 있는 클래스를 추상 클래스라고 한다. 스스로 객체를 만들 수 없다. 단, 부모클래스가 자식클래스에게 상속은 가능하다.
다형성

목요일 시험 후 file input/output 수업 -> 5일 정도 SQL 수업 -> 나머지 파이썬 프로그래밍 수업 예정
'''

class Animal : # 동물들이 가져야 할 공통 속성(멤버필드)과 행위(메서드)를 선언
    age=1

    def __init__(self):
        print('Animal 생성장')

    def move(self):
        print("움직이는 생물")


class Dog(Animal) : # Dog의 부모클래스는 Animal클래스로 새로 정의된다. 
# 이렇게 class Dog()괄호안에 부모class를 적어주면 해당 클래스(Dog)는 이 클래스(Animal)의 자식 클래스가 되고 
# 자식클래스는 부모클래스의 필드멤버와 메서드를 쓸 수 있다.

    def __init__(self):
        print('Dog 생성자')

    def my(self):
        print('댕댕이라고 해요~')

dog1 = Dog() # Dog()클래스에 대해서 객체1 생성
dog1.my() # class Dog(Animal)로 상속관계로 만들어 준 이후 dog1.을 누르면 사용할 수 있는 필드멤버와 메서드가 늘어난 것을 알 수 있다. 부모 class의 변수와 메서드인 age와 move()가 생겨남 
dog1.move()
print("age : ", dog1.age)

print()

dog2 = Dog() # Dog()클래스에 대해서 객체2 생성
dog2.my
dog2.move()
print("dog2 age : ", dog2.age)


class Horse(Animal):
    pass # 이번에는 자식 클래스가 아무것도 가지고 있지 않을 때 부모클래스를 받는 경우다.

horse1 = Horse() # Horse() 클래스에 대해서 객체1 생성
horse1.move() # horse1는 move라는 부모 클래스의 메서드를 가지게 되었다!
# 자식의 생성자가 없을 경우 부모 생성자 수행

# <2교시>

