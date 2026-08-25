# 오버라이딩 vs 다형성 vs 다중상속

'''
메소드 오버라이딩(재정의) 
부모 클래스에서 정의된 메서드를 자식이 동일명의 메서드로 내용만 변경해 사용하는 경우이다
부모 메서드의 기능을 대체하는 새로운 기능을 구현할 수 있다.
동작의 구체화(공통된 틀은 부모가, 실제 행동은 자식)를 실현한다.

Polymorphism(다형성) : 같은 메서드이나 객체에 따라 다른 기능을 수행
확장, 유지보수에 도움 - 부모 코드는 유지한 채 자식 코드만 변경한다.

'''


class Parent: # 용도 : 부모 클래스
    # 생성자가 없기에 따로 객체를 만들지 않는다.
    def printData(self): # 내용이 없는 메서드 ... 왜? 자식 클래스에서 오버라이딩을 기대하기 위해서
        pass

# class Child1: ... 이러면 Parent와 Child1은 서로 독립된 class이다
class Child1(Parent):
    def abc():
        print("Child1 클래스의 고유 메서드")

    def printData(self): # 메서드 오버라이딩(Method-Overriding)
        su = 6
        su = 5 + su 
        # 뭔가를 함...
        print("Child1에서 printData를 오버라이드를 하였다.")

class Child2(Parent):
    good = 'ok'
    def printData(self): # 메서드 오버라이딩(Method-Overriding)
        print("Child2에서 printData를 재정의함.")
        msg = "부모와 동일 메서드명이나 내용은 다름."
        print(msg)

# 공통된 틀은 부모가, 실제 행동은 자식이 한다. 

c1 = Child1()
c1.printData()

c2 = Child2()
c2.printData()


print()


print("---------다형성 구현------------")
par = Parent()
par = c1
par.printData()

par = c2
par.printData()

# par.printData()는 서로 같은 statements이지만 다양한 결과를 구현해 낼 수 있다.
