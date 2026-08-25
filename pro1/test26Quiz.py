#1. 
class CoinIn():
    def __init__(self):
        self.cupPrice = 200

    def calc(self, coin, cupCount):
        totalPrice = self.cupPrice * cupCount

        if coin < totalPrice:
            return (None, None) 
        else:
            change = coin - totalPrice
            return cupCount, change

class Machine():
    def __init__(self):
        self.coinIn = CoinIn() # 포함관계

    def showData(self):
        coin = int(input("동전을 입력하세요 : "))
        cup = int(input("몇 잔을 원하세요? : "))
        cupCount, change = self.coinIn.calc(coin, cup)

        if cupCount is None:
            print("요금이 부족합니다.")
        else:
            print(f"커피{cupCount}잔과 잔돈 {change}")

if __name__ == "__main__":
#    machine = Machine()
#    machine.showData()
    Machine().showData()



#2.
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