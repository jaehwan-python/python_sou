# 냉장고 객체에 음식 객체 저장하기
# 바깥에서 객체를 만들고 Fridge를 만들고 foods에 밀어넣어 할 수 있는 클래스의 포함의 다른 예시이다.

class FoodData: # 냉장고 안에 들어갈 음식 클래스이다.
    def __init__(self, name, expiry_date):
        self.name = name
        self.expiry_date = expiry_date


class Fridge: # 음식을 보관하는 냉장고 클래스이다.
    isOpened = False
    foods = [] # 음식들이 이 리스트에 들어갈 것이다.

    # 생성자는 생략
    def open(self):
        self.isOpened = True
        print('냉장고 문이 열림')

    def close(self):
        self.isOpened = False
        print('냉장고 문이 닫힘')

    def foodList(self): # 냉장고 문이 열린 경우 음식물(클래스) 확인 메서드
        for f in self.foods:
            print(f" - {f.name} {f.expiry_date}")

    def put(self, thing):
        if self.isOpened: 
            self.foods.append(thing)
            print(f"냉장고에 {thing.name} 넣음")
            self.foodList()
        else:
            print('냉장고 문이 닫혀있음')

fObj = Fridge() # 냉장고 객체를 만들었다.

apple = FoodData("사과", "2026년 9월 6일까지")
fObj.put(apple) # 문이닫혀있음
fObj.open()
fObj.put(apple)
fObj.close()

print()

cola = FoodData('콜라', '2027년 5월5일')
fObj.put(cola) 
fObj.open()
fObj.put(cola)
fObj.close()

# 로또 : 45개의 공을 기계에 넣고 6개를 뽑은 그 수의 나열과 내가 적은 숫자의 나열이 맞으면..나는 벼락부자 ㅎ
# 45개의 공도 객체, 공을넣는 기계도 객체이다.





