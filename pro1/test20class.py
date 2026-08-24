
# class : 멤버필드(멤버변수) + 메서드
class Car:
    handle = 1 # 멤버필드 ... Car class 안에서 전역변수로 역할한다.
    speed = 0

    def __init__(self, name, speed): # name, speed = 지역변수  ...  생성자
        self.name = name  # 현재 객체의 name에게 name(지역변수) 인자값 치환
        self.speed = speed

    def showData(self):
        km = "킬로미터"
        msg = '속도:'+ str(self.speed) + km
        return msg
    
    def printHandle(self):
        return self.handle

print(Car.handle) # 원형(prototype) 클래스의 멤버 호출

print()


car1 = Car('tom',10) # 생성자 호출을 통해 객체를 생성(인스턴스 화)... (car1, 'tom', 10) ->
print('car1 객체주소 : ', car1)
print('car1 : ', car1.name, ' ', car1.speed, ' ', car1.handle) # 객체변수. 하면 멤버가 보인다.


car1.color = '파랑'
print('car1.color : ', car1.color)

car2 = Car('oscar', 20)
print('car2 객체주소 : ', car1)
print('car2 : ', car1.name, ' ', car1.speed, ' ', car1.handle)

# print('car2.color : ', car2.color) ... eror car2 class에 없어서 공유멤버(Car class)를 찾아봤는데 공유멤버에도 없다

print(Car, car1, car2)
print(id(Car), id(car1), id(car2))


print()

print(Car.__dict__)
print(car1.__dict__)
print(car2.__dict__) # 이런 형태를 기입하면 각 개체의 멤버를 확인가능하다.
# self는 car1으로 갈지 car2로 갈지를 결정한다!!

print()

print('-------------메서드-------------')
print('car1 speed : ', car1.showData()) # 속도 10킬로미터
print('car2 speed : ', car2.showData()) # 속도 20킬로미터
car1.speed = 60
car2.speed = 120
print('car1 speed : ', car1.showData()) # 속도 60킬로미터
print('car2 speed : ', car2.showData()) # 속도 120킬러미터 car1/2에 있는 클래스의 기존 speed값을 덮어씌우기 함

print()

print('car1 handle : ', car1.printHandle()) # ()안에 car1이 들어감
print('car2 handle : ', car2.printHandle())

Car.handle = 2 # car클래스의 원형클래스의 멤버(handle)값을 2로 수정한다.
print('car1 handle : ', car1.printHandle()) 
print('car2 handle : ', car2.printHandle())