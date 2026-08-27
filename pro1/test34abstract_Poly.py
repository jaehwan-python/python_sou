# 추상클래스를 사용해 다형성 구현 : ex) 배송(일반 vs 퀵 vs 직접 수령)
# 유틸리티 클래스

from abc import ABC, abstractmethod # 추상 클래스를 이용한다.

# 공통 규격(틀)의 클래스를 만든다. : 모든 배송 클래스는 배송비를 가져야 한다는 규칙 

class Delivery(ABC): # Delibery는 ABC를 상속받는다.

    @abstractmethod
    def get_fee(self, distance):
        return 0

# 일반배송
class NormalDelivery(Delivery): # ABC의 자식 class인 Delivery의 자식 class인 NormalDelivery / 일반배송
    def get_fee(self, distance):
        return 3000 # 기본 배송비

#퀵배송
class QuickDelivery(Delivery): # 퀵배송
    def get_fee(self, distance):
        return 3000 + distance * 1000 # 거리를 고려한 배송비
#직접배송
class Pickup(Delivery): # 직접수령
    def get_fee(self, distance):
        return 0

#배송비
class DeliveryUtil:# 어떤 배송 객체든 Util이 배송비 출력을 담당한다
    def print_fee(delivery, distance):
        fee = delivery.get_fee(distance)

        print("배송방식 : ", delivery.__class__.__name__)
        print("배송거리 : ", distance, 'kilometer')
        print("배송요금 : ", fee, fee, '원')

c1 = NormalDelivery()
c2 = QuickDelivery()
c3 = Pickup()
# 3개 객체의 get_fee라는 값에 대해서 모두 다르게 나온다.

DeliveryUtil.print_fee(c1,5) # DeliveryUtil 클래스 내의 print_fee 함수 실행.
print()
DeliveryUtil.print_fee(c2,5)
print()
DeliveryUtil.print_fee(c3,5)









