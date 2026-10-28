'''
추상 클래스(abstract class)
추상 메서드를 가진 클래스를 추상 클래스라고 하면
얘는 인스턴스 할 수 없다.(객체 생성 불가)
부모 크랠스로만 사용됨
추상클래스는 "직접 객체를 만들려고 존재하는 클래스가 아니라, 자식 클래스들이 반드시 지켜야 할 공통 규칙을 정하는 클래스"이다.
'추상 클래스' = 자식 클래스에게 규칙을 강제(메서드 오버라이딩)하는 부모 클래스

클래스 = 속성과 행위(둘 중 하나만 있어도 된다)

어느 객체에서 수행되는지 알기 위해 self를 사용한다.
생성자는 객체에 대해서 초기화작업만 한다. 선언만 하는 작업이다.
자원의 재활용을 목적으로 클래스를 사용한다. 파이썬은 함수 중심적인 프로그램이기 때문이다.

클래스가 클래스를 부를 수 있다. - 포함관계, 상속관계
포함관계 : 클래스내에서 마치 자기 자신의 메서드인 마냥 다른 클래스를 넣어서 쓸 수 있는 방법
상속관계 : 부모 클래스와 자식 클래스 간의 관계를 정의한 것. 
- 메서드 오버라이드(부모의 메서드와 동일한 메서드를 선언하고 내용을 다르게 한다.)
- 다형성(자식메서드에서 부모메서드를 오버라이드하는 것은 강요가 아니라 선택이다. 그때 동일한 이름으로 된 메서드를 호출하면 다양한 결과를 도출한다.)
- 다중상속()

class A를 만들 때 메서드 이름을 꼭 abc()로 만들어라. 그때 class A의 부모 클래스(Parent class)를 만들고 그 부모 클래스는 abc()메서드만 가지고 나머지는pass이다.
clas A와 부모 클래스를 공통으로 가진 다른 class B, classC 또한 오버라이딩을 통해 동일한 메서드가 존재한다. 근데 class B와 class C는 abc()가 아닌 def()로 메서드를 짜왔다.
...미친놈... 결국 다시 짜야함. 다형성이 안됨. 이러한 문제를 해곃하기 위해 Parent 클래스의 abc()를 추상 메서드로 만든다. 그러면 Parent 클래스는 추상 클래스가 된다.
그때부터 Parent 클래스는 인스턴스가 되지 않는다. = 객체생성을 할 수 없다. = 안에 abc()를 수행할 수 없다. = 자기 스스로는 아무 것도 할 수 없다. = 부모 클래스로써만 역할을한다.
class A, B, C는 부모가 가진 추상 클래스를 반드시 오버라이딩 해야한다. 이제부턴 오버라이딩이 선택에서 필수가 되었다.
즉, 부모클래스의 메서드가 추상메서드로 정의되면 자식클래스는 무조건 부모클래스의 추상메서드를 오버라이딩 해야만 한다.
즉, 추상메서드가 정의되면 오버라이딩이 선택에서 강요가 된다.
'''

# from abc import * # 을 해주면 Makers가 만든 모든 Object들을 import하는데 비추한다.
# 그래서   
from abc import *

class AbstractClass(metaclass = ABCMeta): # 이 클래스는 추상 클래스이다. = 객체를 만들 수 없다.
    # metaclass = ABCMeta로 추상 클래스를 정의하고 @abstractmethod를 통해 추상메서드를 정의한다.

    @abstractmethod 
    def abcMethod(self): # 추상 메서드가 된다. : 자식 클래스에서 오버라이딩을 강요한다.
        pass  # 이 형태만 보고 이 친구는 부모 클래스임을 판단한다. 부모 클래스인 AbstractClass에서 자식클래스의 abcMethod를 오버라이딩 해야한다.
#               추상 메서드는 오버라이딩을 강요하기 때문에 내용이 없어야만 한다.
    def normalMethod(self):
        print("추상클래스 내의 일반 메서드 : 자식 클래스에서 오버라이딩이 선택적이다.")

# parent = AbstractClass() # TypeError: Can't instantiate abstract class AbstractClass without an implementation for abstract method 'abcMethod' = 추상클래스는 인스턴스 할 수 없다. = 객체생성을 할 수 없다.
# 추상클래스 이지만 일반메서드만 가지고 있으면(추상 메서드 X) 객체 생성이 가능하다. 하지만 그런 경우는 의미가 없다. = 추상의 의미가 사라진다.


class Child1(AbstractClass):
    name = '난 Child1이야 ~'

    def abcMethod(self):
        print('부모가 가진 추상 메서드를 재정의하였어요. 강요당했어요...')


# c1 = Child1() # TypeError: Can't instantiate abstract class Child1 without an implementation for abstract method 'abcMethod' = 부모가 추상이기에 자식도 추상의 마법에 빠지게 된다. 오버라이딩을 해야 그 마법에서 빠져 나올 수 있다.
# 추상 클래스를 받았는데 오버라이딩을 하지 않으면 객체를 생성할 수 없다. 아직 추상 메서드를 오버라이딩 하지 않았다.
ch1 = Child1()
print("name : ", ch1.name)
ch1.abcMethod()
ch1.normalMethod() # 자식 클래스가 가지고 abcMethod와 normalMethod 메서드를 가지고 있지 않지만 상속관계이기에 부모 클래스의 동일명 메서드를 찾을 수 있다 = 상속 받은 메서드를 사용함 ... 오버라이딩 아님. 일반 메서드만 오버라이드하고 추상메서드는 오버라이드 하지 않음.


class Child2(AbstractClass):

    def abcMethod(self): # 오버라이딩을 강요 당함
        print("오버라이딩 함 : Child2에서 수행할 로직 작성")

    def normalMethod(self): # 오버라이딩을 선택함.(자의적 선택)
        print("부모의 일반 메서드를 내 맘대로 내용을 변경 해서 사용")

    def show(self): # Child2만이 가지고 있는 고유의 메서드
        print("Child2의 고유 메서드")

ch2 = Child2()
ch2.abcMethod()
ch2.normalMethod()
ch2.show()

print('------------------------------------------------------')

happy = ch1
happy.abcMethod()

happy = ch2
happy.abcMethod() # 동일한 메서드지만 결과가 다르다. = 다형성