
'''라이브러리 = 모듈 / 모듈이 곧 하나의 파일로 구성. 그리고 그 모듈이 .py로 기입됨 / python 파일명 py - 인터프리터에서 기계어로 변환된다!!
/ 모듈의 멤버 - 일반 명령어, 제어문(조건판단, 반복), 함수 
함수 : 여러개의 수행문을 하나의 이름으로 묶은 실행단위로 고유의 공간이 있다. 자원의 재활용이 가능하다.
'''

# def 함수명 (가인수) ... 가인수에는 매게변수가 들어간다.
# 함수명(실인수)

# 매개변수 유형
# 종류 - 위치 / 기본값 / 키워드 / 가변 매개변수

# 위치 매개변수 : 인수와 순서대로 대응
# 기본값 매개변수 : 매개변수에 입력값이 없으면 기본값
# 키워드 매개변수 : 실인수와 가인수 간 동일이름으로 대응
# 가변 매개변수 : 인수의 갯수가 동적인 경우

# 파이썬은 객체지향적이기도 하지만 더 나아가 함수지향적 함수이다.

# 문장코드 -> 함수 -> 클래스 -> 모듈

# 하나의 파일의 확장자는 현재 .py이다.

def showGugu(start, end=5):
    for dan in range(start, end+1, 1): # start부터 end+1까지 1을 증가치로 잡는다
        print(str(dan) + '단 출력')
        for i in range(1, 10):
            print(f"{dan} * {i} = {dan * i}, end = ' '")
        print()

showGugu(2,3) # end = 5라는 초기치를 가지지만 3이라는 입력값이 힘이 더 쎄서 교체된다. # 위치 매개변수

showGugu(2) # end = 5에 해당하는 값이 없어서 기존의 값인 5를 그대로 쓴다. # 기본값 매개변수 

showGugu(start = 7, end = 9) # 실인수의 값을 가인수에 직접적으로 이름에 대입함 # 키워드 매개변수

showGugu(end = 11, start = 6) # 실인수와 가인수의 순서가 바뀌어도 키워드로 입력했으면 실인수 순서에 맞추어 들어간다. # 키워드 매개변수

showGugu(7, end = 9) # 순서에 의해서 그대로 들어간다. # 위치 매개변수

# showGugu(start = 7, 9) ... error # 위와 비슷하게 생겼지만 다르다!
# showGugu(end = 5, 7) ... error

# print(showGugu())를 None이 나온다. 함수 showGugu()는 수행하는데 입력값을 받지 못해서 그렇다. 또 print를 적었기에 return값이 나온다
# 함수가 시행되면 함수가 고유의 공간을 기억장치에서 가지게 된다!
# 현재 모듈내에서만 쓸 수 있고 다른 모듈에서 쓸려면 파일로 저장해서 쓴다.

print('-----------가변 매개변수 : 인수의 갯수가 부정확한 경우 = 입력값이 부정확한 경우----------')
def fun1(ar):
    print(ar)

fun1('김밥') # ... 하나의 값을 달래서 하나의 값을 줬기에 이상이 없다.
#func1('김밥', '떡볶이') ... error 개수가 대응이 안되기 때문 ... 그러면 여러 개의 인자를 tuple형태로 묶어서 받고 싶으면 어떡하는가? = 가인수의 정해진 갯수보다 더많은 실인수를 받을 때

# 가인수 앞에 *ar을 붙인다.
    
def func1(*ar):
    print(ar)

func1('김밥')
func1('김밥', '떡볶이') # 함수의 가인수가 여러 개의 값을 받을 수 있다.

# 이렇게 실인수(변수)가 동적인 경우가 있기 때문에 함수의 매개변수에 *을 주어라. 그러면 받은 여러개의 값을 하나의 묶음으로 여겨 처리할 수 있기 때문이다.

print()

def func2(a, *ar): # func2(*ar, a) ... error  *ar : ar이 받은 값은 묶음(튜플)으로 처리한다.
    print(a)
    print(ar)

func2('김밥') # 반대로 2개의 값을 받을 수 있는데 한개의 값만 받을 수 있다면 앞에꺼부터 채워서 들어간다.
func2('김밥', '떡볶이', '오뎅', '순대') # 가인수가 2개일 때, 그 가인수에서 a는 하나의 값만 받고 *이 있는 변수에서는 그 *이 있는 매개변수에 나머지 값들을 모두 받아 tuple형태로 묶인다.

print()

# 개인이 혼자 공부할 때는 input, print를 쓰지만 실제 상품에 대입하려면 XML, JSON, CSV데이터를 받는다. file i/o는 안배운다!!

def func3(weight, height, **other): # **은 tuple이 아닌 dict값으로 받는다
    print(f"몸무게 : {weight}, 신장(키) : {height}")
    print(f"기타 : {other}")

func3(74, 171, irum = '김재환', nai = 23) # ... irum = '김재환', nai = 23를 dict로 바꾸는 법!
# func3(74, 171, {'irum' : '김재환', 'nai' = '23'}) # ... 실인수를 받는 매게변수 **other가 받는 실인수를 dict 자료형으로 만드는 역할까지 하는데 굳이 실인수를 줄 때 dict자료로 줄 필요 없다.

# 몸무게 : 74, 신장(키) : 171
# 기타 : {'irum': '김재환', 'nai': 23}

# 앞으로 함수를 쓸 일이 많다. 이미 짜여져 있는 함수를 디버깅할 줄 아는 것이 중요. 즉, 코드를 읽어내는게 중요하다.
# API를 잘읽어야한다.
# API : 프로그램들이 서로 통신하게 돕는 도구. 
# 코드에 접근하려면 func3()를 불러야한다. 그때 함수와 코드를 연결하는 것이 API이다.

print()
def func4(a,b,*c,**d):
    print(a,b)
    print(c)
    print(d)

func4(1,2)
func4(1,2,3,4,5) # c가 3,4,5를 가지고 d는 비워진다.
func4(1,2,3,4,5, mbc = 11, kbs = 9) # c가 3,4,5를 가지고 d는 mbc : 1, kbs : 9라는 값을 dict형태로 표현한다

print()
# type hint : 함수의 인자와 반환 값에 type를 적어 가독성을 향상한다. 코드를 쉽게 읽기 위해서 써준다.
def typeFunc(num:int, data:list[str]) :# :int와 같은 형태가 type hint ...  실행결과에 아무 영향도 없어 선택적으로 적어주면 된다. 강제성이 없다!(num은 int값만 받아야 해!라는 뜻 아니다. data는 list로 주고 list내 값은 str값이면 좋겠당..이라는 느낌)
    print(num)
    print(data)
    result = {} # 변수의 값은 dict형태이다.
    for idx, item in enumerate(data, start=1): # idx, item이라는 변수에 data와 stat(1부터 시작)이 enumerate된다. enumerate를 사용하면 (번호, 값)형태로 반환한다. start = 1은 item에 들어가는 값이 아니고 enumerate가 붙여주는 번호의 시작값이된다.
        print(f"idx:{idx}, item:{item}")
        result[item] = idx
    return result

rdata = typeFunc(1, ['일','이','삼']) # data값을 리스트 형태로 줌
print(rdata)
print()
rdata = typeFunc('한 개', [10,20,30])
print(rdata)

print('-----------------클로저--------------------')