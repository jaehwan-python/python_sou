# 어딘가에서 필요한 부품으로 핸들 클래스를 작성한다. 자동차 부품 중 핸들(클래스)부품만 뽑아옴
class Poham_Handle:
    quantity = 0 # 핸들 회전량

    def leftTurn(self, quantity):
        self.quantity = quantity
        return '좌회전'

    def rightTurn(self, quantity):
        self.quantity = quantity
        return '우회전'

    