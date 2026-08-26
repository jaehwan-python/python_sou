'''
"메소드 오버라이딩을 통한 다형성(Polymorphism) 구현"

카드결제, 현금결제, 포인트결제를 각 클래스에서 결제 메서드를 오버라이딩하기
'''

class Payment:  # 부모 클래스 : 결제라는 공통기능pay()를 정의

    def pay(self, amount):
        print(f"{amount}원 결제를 진행합니다.")
        # pass : 내용 없이 만들 수 있다.

# 이하 자식 클래스
class CardPayment(Payment): # 카드 결제 클래스 : 카드 수수료 2%를 계산하여 결제하기
    def __init__(self):  # 이 코드는 생략 가능하다.
            pass 

    def abc():
        print("CardPayment 고유 메서드")

    def pay(self, amount):  # 메서드 오버라이딩 : 강요는 아니다(선택적)
        fee = amount * 0.02
        total = amount + fee
        print(f"[카드결제]")
        print(f"상품 금액 : {amount}원")
        print(f"수수료 : {fee}원")
        print(f"최종 결제 금액 : {total}원")


class CashPayment(Payment) :  # 현금 결제 클래스 : 현금 결제 시 할인5%를 적용하여 결제

    def pay(self, amount):
        discount = amount * 0.05
        total = amount - discount
        print(f"[현금결제]")
        print(f"상품 금액 : {amount}원")
        print(f"할인 금액 : {discount}원")
        print(f"최종 결제 금액 : {total}원")

class PointPayment(Payment) :  # 포인트 결제 클래스 : 금액만큼 포인트를 사용한다.
    def pay(self, amount):
        print(f"[포인트 결제]")
        print(f"{amount}포인트를 사용합니다.")

#    메서드 오버라이딩 : 부모와 메서드는 같은데 내용이 다른 것



# 클래스 공통 처리 함수 : 전달받은 객체의 pay()를 호출
def process_payment(paymentADDr:Payment, amount:int) -> None :  # 여기서부터는 Function이다. 힌트 : 가독성을 위해서 ' :Payment/int'를 주었다. 
#                                                                 반환값은 None이다
    paymentADDr.pay(amount)

if __name__ == "__main__":
    p1 = CardPayment()
    p2 = CashPayment()
    # p3 = PointPayment()

    process_payment(p1, 10000)
    print()
    process_payment(p2,10000)
    print()
    process_payment(PointPayment(),10000)  # process_payment(PointPayment( ), 10000) 이렇게 표현해도 된다!

# 오버라이딩이 있어야 다형성을 이해할 수 있다. 클래스 -> 상속 -> 오버라이딩 -> 다형성 ->  다중상속



        


