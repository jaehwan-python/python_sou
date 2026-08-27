'''
class Machine:
    def __init__(self):
        self.coin_input = CoinIn(self)

    def showData(self):
        coin = input('동전 입력')
        count = input('몇 잔 입력')
        self.coin_input.coin = int(coin)
        self.coin_input.calc(int(count))
        change = self.coin_input.change

        if (change >=0) :
            print("커피", count, "잔과 돈", change, "원")
        else:
            print("잔액이 부족합니다")

class CoinIn:
    def __init__(self, coin = 0, change = 0):
        self.price = 200
        self.coin = coin
        self.change = change

    def calc(self, cupCount):
        total = cupCount * self.price
        self.change = self.coin - total

machine = Machine()
machine.showData()
'''


'''
#2.
class ElecProduct:
    volume = 0
    def volumeControl(self, volume):
        pass


class ElecTv(ElecProduct):

    def __init__(self):
        pass

    def buTTon(self):
        print("tv의 버튼은 총 20개다.")

    def volumeControl(self, volume):
        print(f"tv의 소리는 {volume}이다.")
        

        
class ElecRadio(ElecProduct):

    def __init__(self):
        pass

    def soUNd(self):
        print("radio의 소리가 너무 작다.")

    def volumeControl(self, volume):
        self.volume = volume + 2
        print(f"라디오의 소리는 {volume}")
        


if __name__ == "__main__":
    a = ElecProduct()
    a.volumeControl(1)

    button = ElecTv()
    button.buTTon()

    sound = ElecRadio()
    sound.soUNd()
'''

#3.

from abc import ABC, abstractmethod # 추상 클래스를 이용할 것이다.

#1. Employee
class Employee(ABC):
    def __init__(self, irum, nai): # 이름과 나이를 받아야하기 때문에 생성자를 통해서 irun,nai를 생서하였다.
        self.irum = irum
        self.nai = nai

    @abstractmethod
    def pay(self): # 추상 메서드1 정의 - 자식 클래스에서 무조건 수행되어야함.
        pass

    @abstractmethod
    def data_print(self): # 추상 메서드2 정의 - 자식 클래스에서 무조건 수행되어야 함.
        pass

    def irumnai_print(self):
        print(f"이름 : {self.irum}, 나이 : {self.irum}")


#2. Temporary
class Temporary(Employee):

    def __init__(self, irum, nai, ilsu, ildang):
        super().__init__(irum, nai) # super가 있다는 것은 부모 class와 연결된다는 것이다. 즉, 부모class의 생성자를 포함해서 lisu와 ildang 매게변수를 추가!
        self.ilsu = ilsu
        self.ildang = ildang

    def pay(self):
        pass

    def data_print(self, irum, nai, ilsu = 0, ildang = 0):
        self.irum = irum
        self.nai = nai
        self.ilsu = ilsu
        self.ildang = ildang
        print(f"이름 : {self.irum}, 나이 : {self.nai}, 월급 : {self.ilsu * self.ildang}")


t = Temporary('홍길동', 25, 20, 15000)
t.data_print()


#3. Regular
class Regular(Employee):

    def __init__(self, irum, nai, salary): # 어차피 Regular 클래스도 irum과 nai가 필요하기에 부모 class에서 가져온다.
        super().__init__(irum, nai)
        salary = 0

    def pay(self):
        pass

    def data_print(self, salary):
        self.salary = salary
        print(f"이름 : {self.irum}, 나이 : {self.nai}, 급여 : {self.salary}")
    
r = Regular('한국인', 27, 3500000)
r.data_print()


#4.Salseman 
class Saleseman(Regular):
    def __init__(self, irum, nai, salary, sales, commsion): # self는 irum, nai, salary, sales, commsion이 변수를 가지고
        super().__init__(irum, nai, salary) # 최고 class로 부터 irum, nai, salary값을 가져와 최고 class의 객체(irum, nai, salary)를 초기화한다.
        sales = 0
        commision = 0.25

    def pay(self):
        pass

    def data_print(self, irum, nai, sales=0, commision=0):
        self.sales = sales
        self.commision = commision
        print(f"이름 : {self.irum}, 나이 : {self.nai}, 수령액 : {self.salary + (self.sales * self.commision)}")
    
s = Saleseman('손오공', 29, 1200000, 5000000, 0.25)

