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
