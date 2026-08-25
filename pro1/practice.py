# .py이나 .txt파일로 올리기


'''
class Machine:

    def __init__(self, cupCount=1): 
        self.coin_input = CoinIn() # Machine클래스로 인해서 새로 생긴 객체 mac
        self.cupCount = cupCount

    def showData(self):
        print('-------------------')
        coin = int(input("동전을 입력하시오"))
        self
        print(coin)
        cup = int(input('몇 잔을 원하세요?'))
        print(cup)
        self.coin_input.culc(cup)


class CoinIn: # CoinIn이 새로 만든 객체가 Machine과 연결된다.

    def __init__(self, coin = 0, change = 0):
        self.coin = coin
        self.change = change

    def culc(self, cupCount): # 잔돈에 대한 계산
        self.change = 
        # 잔돈 = 넣은금액 - 전체 금액
        # 전체 금액 = 한 컵당 가격 * 갯수


mac = Machine() # 
mac.showData(int(input("몇잔을 원하세요?", )))
coinin = CoinIn.culc(int(input('코인을 입력하세요', )))
'''


        


        

'''
  elif self.coin == 1: # 100원
            print('요금부족')

        elif self.coin % Machine.cupCount*100 == 0: # 
            print(f"커피 {self.coin / 200}잔 출력, 거스름돈 : {self.coin - (Machine.cupCount*100)}원을 받으세요")

        elif self.coin % Machine.cupCount*100 == 1: # 300원
            print(f"커피 {self.coin / 200}잔 출력, 거스름돈 {self.change - (Machine.cupCount*100)}원을 받으세요.")
        else : 
            print('거스름돈은 0원입니다.')
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














'''자료형 - 숫자(실수/정수) / 문자 / bool형 / 집합형 
핵심 키워드 : 연산자 / 예약어(키워드) / 함수 / 메서드
* 연산자 - 산술 / 비교 / 논리 / 대입 / 멤버십 / 식별 / 비트연산자'''

'''
a = "김재환"
A = "권민석"
b = 30
B = 60
my_pro1 = "내 파이썬 공부 자료"
print(a)
print("a") # : a라는 문자열이 나오게 된다.
print("a = ", a) # "a ="은 문자열, a는 변수의 값("김재환")을 출력한다.

# 변수 vs 상수 
# 1. 변수와 상수 모두 기억장소를 저장하는데 변수는 변할 수 있는 값이고 상수는 영구적으로 고정된 값이다.
# 2. 변수의 시작은 소문자와 대문자로 구별가능 / 숫자로 시작할 수 없음 / 띄어쓰기가 안되기 때문에 언더바(_)를 사용한다.

aa = 100
bb = 100
print(aa is bb, aa == bb, id(aa), id(bb)) # True True ... aa와 bb가 같은 100이라는 값의 기억장소를 기억하고 있기 때문.
# id()는 기억장소의 주소를 알려준다.
aa = [100]
bb = [100]
print(aa is bb, aa == bb, id(aa), id(bb)) # False True ... 리스트의 내용은 같지만 리스트의 주소는 다르다. 
# 숫자형 자료가 리스트 자료가 되면서 두 자료의 주소가 달라짐.

import keyword
print("파이썬에서 쓸 수 있는 keyword(예약어)는", keyword.kwlist ,"이런 종류가 있습니다. 잘알아두세요.")

print("\n")
print("이번엔 자료형을 확인해보자구요")
# 자료형 - 숫자형(실수형/정수형) / 문자열 / bool형 / 집합형자료
# 실수형(float) / 정수형(int) / 문자열(str) / bool형(bool) / 집합(list / tuple / set / dict)
print("* print할 때 이런식으로 큰 따옴표를 써도 되지만 f-string을 쓰자!")
print(f"이렇게 print하구 {aa}와 {bb}는 서로 다른 주솟값을 기억하고 있다고 했죠잉?") # 변수는 {}로 표시

print("\n"f"지금부터 값에 대한 자료형을 알려줄게요. '1.2'는 {type(1.2)}이고, '10'은 {type(10)}이고, '김재환'은 {type("김재환")}이고, 'True/False'는 {type(True)}입니다. ")
print(f"다음은 집합형 자료들이에요. 이 친구들은 괄호에 따라서 자료형이 달라져요")
print((1,), type((1,))) # 소괄호 - 튜플
print({1}, type({1}))
print({'key : 1'}, type({'key : 1'})) # 중괄호 - 셋 / 딕셔너리
print([1], type([1])) # 대괄호 - 리스트
# 메서드 : 특정 객체에 소속된 함수 - 변수.메서드(값) 형태이다.
# 함수 : 독립적으로 존재 / 특정작업 수행 / 함수는 객체에 소속되지 않는다. - print()

v1 = 10, 20, 30
print('v1 = ', v1) # 하나의 변수는 하나의 값밖에 받지 못한다. 하지만 v1이 출력한 이유. 저런 경우 컴퓨터는 v1을 ()가 생략된 튜플값으로 인식한다. 그래서 
print(type(v1)) # 튜플값
v2 = 40
print('v2 = ', v2)
v1, v2 = v2, v1
print(f"v1의 값은{v1}, v2의 값은{v2}로 바뀌었어용")

*v1, v2, v3 = 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
print(v1, v2, v3)

v1, v2, *v3 = 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
print(v1, v2, v3)

print("안녕", end = ' '"내 이름은 김재환")

print(divmod(12,3)) # 몫과 나머지를 알려준다.

print('aa\tbb') # \t
print(r'aa\tbb') 
print('aa\bbb') # \b : 그다음 문자 삭제
print(r'aa\bbb')
print('aa\abb') # \a : 소리 울림

"\n"

print("방법1")
scores = [95, 80, 53, 92, 65]
avg = sum(scores) / len(scores)
if avg >= 80:
    print("다들 잘했어여")
elif avg >= 70:
    print("그럭 저럭~")
else:
    print("공부를 안한거니?")

print("\n")

print("방법2")
scores = [95, 80, 53, 92, 65]
bunja = sum(scores) 
bunmo = len(scores)

avg = bunja / bunmo

if avg >= 80:
    print("다들 잘했어여")
else:
    if avg >= 70:
        print("그럭 저럭~")
    else:
        print("공부를 안한거니?")
print("고생했다.")

print("\n")

print("방법3")
# input(str(input("내가 태어난 년도는? : ")))
jumsu = float(input("시험점수를 입력하시오 : "))
if jumsu >= 90:
    print("오늘은 고기반찬이다.")
elif jumsu >= 80:
    print("머..고생했다.")
elif jumsu < 80:
    print("넌 뭐하는 ㅅㄲ냐")
else:
    print("나가")

print("\n")

print("방법4")
year = int(input("내가 태어난 해는? : "))
if year >= 2004:
    print("젊은 사람")
elif 2000 < year <= 2003:
    print("살짝 나이 든 사람")
elif 1990 < year <= 1999:
    print("옛날 사람")
else:
    old = int(input("당신은 살아있습니까..? 몇살이요..? : "))
    if 23 <= old <= 42:
        print("완즈히 옛날 사람! 늙크크")
    else:
        print("wow..무병장수 man")

'''
'''
def func1(arg1, arg2):
    result = arg1 + arg2
    return result

arg1 = int(input('첫번째 정수를 입력하시오 : ',  ))
arg2 = int(input('두번째 정수를 입력하시오 : ',  ))

print('result : ', func1(arg1, arg2))
'''

'''

a = 10; b = 20; c = 30

print(f"foo 수행 전 a : {a}, b : {b}, c : {c}입니다.")

def foo():
    a = 7 # ... 지역 변수
    b = 100

    def bar():
        b = 8 
        print(f"bar 수행 중 a : {a}, b : {b}, c : {c}입니다.") 

    bar()
    print(f"bar 수행 후 a : {a}, b : {b}, c : {c}입니다.")

foo() 

print(f"foo 수행 후 a : {a}, b : {b}, c : {c}입니다.")

print('--------------------------------')

a = 10; b = 20; c = 30

print(f"foo 수행 전 a : {a}, b : {b}, c : {c}입니다.")

def foo():
    a = 7 # ... 지역 변수
    b = 100

    def bar():
        global c
        nonlocal b
        b = 8 
        print(f"bar 수행 중 a : {a}, b : {b}, c : {c}입니다.") 
        c = 77
        b = 88


    bar()
    print(f"bar 수행 후 a : {a}, b : {b}, c : {c}입니다.")

foo() 

print(f"foo 수행 후 a : {a}, b : {b}, c : {c}입니다.")

'''