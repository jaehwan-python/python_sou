# 클래스의 다중 상속 - 부모 클래스가 복수 (순서에 유의)

class Tiger:
    data = "호랑이 세상"

    def cry(self):
        print("호랑이 : 어흥")

    def eat(self):
        print("맹수는 고기를 좋아해요.")
        print("아침에는 닭고기, 낮에는 소고기, 저녁에는 양고기를 먹어줍니다")



class Lion:
    def cry(self):
        print("사자 : 으르렁")

    def hobby(self):
        print("백수의 왕은 낮잠이 취미에요.")


class Liger(Tiger, Lion): # 부모 class가 2개이다. = 2개 이상을 상속받음 = 다중상속
    pass

a1 = Liger()
# a1. # Liger뒤에 아무것도 부모 class로 지정되지 않았을때 그냥 a1.을 하면 maker에서 만들어둔 최상위 클래스인 object들이 뜬다
print(a1.data)
a1.eat()
a1.hobby()
a1.cry() # tiger와 lion 둘 다 cry라는 메서드를 가지고 있다. 이런 겨우 누구의 메서드를 쓸까? -> 동일 멤버인 경우 첫번째 클래스(tiger)의 멤버를 취한다.

print('-------------------')


def hobby(): # 그냥 함수다.
    print("모듈의 멤버로 일반함수입니다.")

class Liger2(Lion, Tiger):
    data = "라이거 만세" 

    def play(self):
        print("라이거 고유 메서드 - play")

    def hobby(self):
        print("라이거는 공원 산책을 좋아해요. - 오버라이딩")

    def showData(self):
        self.hobby()  # 현재 클래스의 hobby. 없으면 부모 클래스에서 찾는다.
        super().hobby() # Lion의 hobby. hobby를 가지고 있는 최고 부모에서 호출한다.
        hobby()  # 함수 hobby. 클래스 바깥 : 모듈에서 함수를 호출한다. ... 자식 클래스 -> 부모 클래스 -> 일반함수 -> Object(Makers가 만든 클래스)
#                                           이 순서로 클래스를 찾는다. 
        
# 내일은 추상class 그러니 오늘꺼 다 복습하기

a2 = Liger2()
a2.cry()
a2.showData()


