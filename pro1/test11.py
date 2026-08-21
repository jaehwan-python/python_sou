'''
Closure(클로저) : Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드블럭이다.
내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기
'''
def funcTimes(a,b):
    c = a*b
    print('c = ', c)
    return c

print(funcTimes(2,3))
# print('c = ', c) #...c는 def 내의 지역변수이지 전역변수가 아니다. =즉 c라는 값은 def밖에 존재하지 않는다.
# 함수 밖에서 함수 내에는 접근할 수 없다...하지만 난..하고 싶다..!!

#1.
kbs = funcTimes(2,3) # 열린 괄호 내에 값이 있다는 것은 괄호 내의 값을 수행해라. # 실행결과를 치환함
print(kbs)

#2.
kbs = funcTimes # 주소를 내놔라
print(kbs) # (2,3)이 없으면 16진수 형태의 주소가 나옴. # 함수주소를 치환(별명이 하나 생김)

#3.
print(kbs(2,3)) # = "kbs = fucTimes(2,3)"

#4. 
print(id(funcTimes), id(kbs)) # 두 값의 주소는 같다

mbc = sbs = kbs # 세 개의 값은 모두 동일한 주소를 가진다.

del funcTimes # 함수도 결국 변수의 일종이다. 객체의 주소를 기억한다. 이렇게 함수명을 삭제할 수 있다. 창조 변수 삭제

#print(funcTimes(2,4)) # ...error
print(kbs(3,4))
print(mbc(3,4))
print(sbs(3,4)) # ... 함수는 사라져도 함수의 주소는 기억하고 있기에 수행가능하다. 함수의 주소(식별값)가 저장되어 있어 창조 함수가 사라져도 
#                     다른 변수에 저장해두었으면 그 저장해둔 변수로 다시 함수를 수행가능하다. 


print("내가 한 함수를 지정했어. 그리고 그 함수를 a라고 저장하고 a = b = c라는 코드를 만들고 나서 기존 창조 함수를 del(삭제)했어. " \
"그래도 다시 print(a), print(b), print(c)하게 되면 삭제된 원래 함수를 가동하게 돼. " \
"이 이유는 함수가 삭제되어도 a,b,c가 창조함수의 식별값'주소'를 기억하고 있기에 그 식별값으로 값을 도출하는거야")

print()

print('--------------클로저를 사용하지 않은 경우----------------')
def out():
    count = 0
    def inn():
        nonlocal count # ...count는 inn이 아니고 out의 지역변수다. ... global전역변수가 되는것 아니다!
        count = count + 1
        return count # "count = count + 1 ... return count"값이 out함수로 나오게 된다.
    print(inn())

print(out()) # ... out을 호출하면 count는 0으로 저장된 값이 inn함수에 의해서 1로 바뀜



print("\n")
print('------------------클로저를 사용한 경우--------------------')

def outer():
    count = 0
    def inner():
        nonlocal count
        count = count + 1
        return count # inner의 count를 nonlocal을 써서 outer의 변수로 꺼냄.
    return inner # 요것이 클로저 : 내부함수의 객체의 주소를 반환함 ... inner뒤에 ()가 없기에 주소만 반환함. 왜? 함수 내의 count를 수정하기 위해서 # outer()는 실행하면 inner의 주소값을 가지게된다.return inner : inner뒤에()가 없기 때문에 함수를 실행하는 것이 아닌 함수 자체의 주소를 반환한다. 파이썬에서 함수 이름도 결국 함수 객체를 가리키는 이름표이기 때문에, inner라고만 쓰면 그 함수 객체를 가라키는 참조를 그대로 넘기는 것이다.
var1 = outer() #... var1은 outer함수를 수행하는데 outer함수의 결과는 inner함수의 주솟값만 반환한다. 그래서 var1도 inner의 주솟값만 찍힌다.

print(var1) # inner의 주소만 나옴 # outer의 주소가 아닌 inner의 주소가 나온다.
print('count : ', var1())
print('count : ', var1()) # 호출할 때마다 count가 늘어난다! ...이건진짜 모름 왜?
# count라는 내부함수의 변수를 함수 밖에서 접근할 수는 없다. 그래서 클로저를 이용하여 함수 밖에서 사용할 수 있게 만든다.
# print(var1.count)와 같이 외부에서 직접적인 접근은 불가능하다.
print(var1.__closure__) # __명령__ : 파이썬 고유 명령 : 파이썬 내부 확인은 가능 # (<cell at 0x00000159A3F7BBB0: int object at 0x00007FF80BFEE498>,)

myvar = var1()
myvar = var1()
print(myvar) # 내부함수의 주소를 가진다. = 주소를 넘겨받는다. = 야너도? 야나도? 의 주소를 가짐 = 계속 그 주솟값을 이어 받음
var2 = outer() # 새로운 객체(inner함수) 생성
print(var2())
print(var2()) # 새로운 변수에 대해서는 그 값을 다시 처음부터 카운트한다.

print("\n")

print ("수량 * 단가 * 세금한 결과를 출력하기")
def outer2(tax) : # tax는 지역변수
    def inner2(su, dan):
        amount = su * dan * tax 
        return amount
    return inner2 #outer2함수는 inner2의 값을 반환하여 

# 1분기에는 금액 ( = su * dan)에 대한 tax는 0.1 부과한다.
q1 = outer2(0.1) # inner2의 주소값을 가진다... 클로저때문에
result1 = q1(5,50000)
print('result1 : ', result1)  
result2 = q1(2, 10000)
print('result2 : ', result2)

'''
# 2분기에는 금액 ( = su * dan)에 대한 tax는 0.05 부과한다.
q2 = outer(0.05) # inner2의 주소를 기억하고 q2에 대해서는 다시 시작한다. # tax가 0.05일 때
result3 = q2(5,50000) # q2는 내부함수인 inner2의 주솟값을 가지고 있기에 (5, 50000)값을 q2에 대입한다
print('result3 : ', result1)  
result4 = q2(2, 10000)
print('result4 : ', result4)
'''
print()

print('----------------일급함수(일급객체)-----------------')

# 일급합수 : 프로그래밍 언어에서 함수를 일반적인 값이나 변수처럼 다루는 것. 
# 즉 함수를 변수에 넣거나 다른 함수의 인자로 넘기거나 결과값으로 돌려받을 수 있는 성질이 있다. 변수할당 / 인자전달 / 반환값 사용 / 자료구조 저장
# 개발자가 되기 위한다면 go언어를 알아두는 것도 좋다.

print("일급함수 : 함수를 변수나 상수에 저장, 함수 안에 함수, 인자로 함수 전달, 반환값으로 사용, 자료구조를 저장한다")
print("\n")

#1. 함수를 변수나 상수에 저장한 경우
def func1(a, b):
    return a + b

func2 = func1 # ... 1. 함수의 주소를 넘긴것 ... '''모든 변수는 주소를 기억하고 있기 때문이다'''... 값을 넘긴 것이 아니다. 모든경우가 그럼ㅇㅇ
print(func1(2,3))
print(func2(2,3))

#2. 인자로 함수를 전달
def func3(fu): # 2. 인자로 함수 전달 받음
    def func4(): # 3. 함수 안에 함수 선언
        print('나는 내부 함수야 ~~~')
    func4()
    return fu # 4. 변환값이 함수

mbc = func3(func1) # 인자로 함수를 전달함 = 치환
print(mbc(6,7))

# 치환 - 등호로 치환하는 것  
#      - 실인수를 가변수에 넣어주는 것

# 값이 아니라 주소로 생각하기!!

print()

print('-----------------람다-------------------')
print('축약함수(Lamda Function) : 프로그래밍에서 여러 줄의 함수 정의를 한 줄로 간단하게 줄이는 익명 함수')
# 축약함수의 특징 : 이름이 없다 / 한줄 선언 / 일회용 사용
# 이전에 함수들은 한번 저장하면 그 메모리가 계속 유지되는데 난 그 유지가 싫어. 딱 한번만 쓰고 싶어. 영구적으로 존재X
# 형식 -- lambda 매개변수1, 매개변수2 , ... : 표현식 ... return 없이 결과 반환
# lambda 매개변수 : 반환할_값 의 형태
def hapFunc(x, y): # 프로그램 종료시까지 메모리 기억
    return x + y

print(hapFunc(1,2))
#람다로 표현하면
print((lambda x, y : x + y)(1,2)) # 단발성(휘발성) : 실행과 동시에 메모리가 사라짐 # 람다 함수는 이름이 없다.
# x,y를 매게변수로 가지는 람다함수는 x+y를 return한다.

gg = lambda x, y : x + y # gg가 람다를 기억
print(gg)
print(gg(1,2))
print()
print(gg(1,2))
print(gg(3,4))

gg2 = lambda x,y : x+y
print(id(gg), id(gg2)) # 두 람다 함수의 주소는 다르다
print((lambda x, y : x + y) is (lambda x,y : x+y)) # is는 주솟값을 비교한다. # False가 나온다.

print()

kbs = lambda a, su = 10 : a + su
print(kbs(5, 6)) # 5가 a로 6이 su로 들어간다. 기존의 su = 10은 6으로 바뀐다.

print()

sbs = lambda a, *tu, **di : print(a, tu, di)
sbs(1,2,3,var1=4, var2=5)

print()
print("임의의 함수에서 람다 사용하기")
# filter() # filter는 반복가능한 객체(리스트, 튜플)에서 특정 조건에 맞는 요소만 골라낼 때 사용가능하다.
# 구조 : filter(함수, 반복가능한 객체) # 두 개의 변수가 존재한다.
print(list(filter(lambda a:a<5, range(10)))) # 반복가능한 객체에서 일차함수를 사용한경우
print(list(filter(lambda a:a % 2, range(10)))) # a를 2로 나누었을 때 나오는 값이 0이면 bool형태로 False이다.
print(bool(0), bool(1))# .. True 값만 출력한다. 위의 람다함수에서도 마찬가지로 a를 2로 나눴을 때 참이되는 값만 도출....이것도 진짜 모름

print()
# filter를 이용해 1~100 사이의 정수 중 5의 배수이거나 7의 배수만 출력(리스트 형태로)
print(list(filter(lambda a : a%5 == 0 or a%7 == 0, range(1, 101))))

print()

print('----------------------함수 장식자---------------------------')
# 함수 장식자 : 기존의 함수코드를 수정하지 않고도 함수의 앞뒤에 새로운 기능이나 추가 작업을 더해주는 파이썬 프로그래밍 기법
# 함수 위에 at기호를 붙여서 아주 간단하게 사용 가능

