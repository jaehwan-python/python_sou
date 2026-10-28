'''사용자 정의 함수
< def 함수명(가인수,,,):   #()안에는 여러 개의 변수가 들어갈 수 있고 이때 그 변수들을 가인수라고 부른다. dummy argument, 매개 변수
            # ...
            return 반환값   # *반환값은 항상 1개만 된다(중요)*, return이 없으면 return None
    함수명(실인수,,,)   # 함수호출 # actual argument

함수 안에는 여러 문장을 적어주고 함수는 들여쓰어줘야한다. return을 써도되고 안써도 된다. 대신 안쓰면 None이 반환된다.
가인수와 실인수는 type이 맞아야 한다. 또한 갯수도 맞아야 한다.
'''

print('뭔가를 실행...')
# 함수 선언



# a. def doFunc1
def doFunc1():
    print('doFun1 수행') # 자, doFunc1은 이거야 선언 ... doFunc1 함수가 호출되면 print('doFunc1 수행')이 출력된다. 

# 함수 호출
doFunc1() # - 함수수행 /  야 아까 정의했던 doFunc1 데려와! ... 이전에 정의했던 함수의 print('doFunc1 수행')을 수행한다
print(doFunc1) # - 함수 주소를 출력 / 
print(doFunc1()) # 함수수행 및 ,return값 반환 / print(함수())는 그 함수의 return값까지 알려준다!
print('어떤 작업 처리')

doFunc1()
print('함수주소는', doFunc1) # 함수뒤에 괄호를 안붙히면 함수의 주소만 나타나고 수행을 하지는 않는다(중요) = 함수의 객체를 알려준다... 
#                             괄호의 유무에 따라 의미가 달라진다!
print('함수주소는', id(doFunc1)) # 함수의 이름도 주소를 기억한다. 16진수로 적힘. id로 적게 되면 10진수로 나타나게됨
print('작업종료')

print()

# 함수명 변경
print(id(doFunc1))
print()

# 1. imsi = doFunc1
imsi = doFunc1 # 함수의 주소 치환
print(id(imsi)) # imsi와 doFunc1 모두 같은 객체함수의 주소를 공유하고 있다. .. 공통된 객체함수의 주소값을 가진다

#2. imsi = doFunc1()
imsi2 = doFunc1() # 함수 실행 결과를 기억
print(id(imsi2))  
'''
imsi = doFunc1
imsi2 = doFunc1()
은 서로 다른 주소를 가진다. 이유 : doFunc1은 함수 그 자체만을 의미하지만 doFunc1()은 함수의 return값을 의미한다.
'''

print(imsi2) #  doFunc1의 결괏값이 함께 출력된다. 

# 지금은 test9.py에서만 doFunc1()을 쓰고 있는데 test10.py에서도 doFunc1()을 쓰려면 새로운 파일을 만들면 된다.
# def가 클래스 안으로 들어가면 메서드, 나오면 함수다..모듈

print('----------------------')

#b. def doFunc2
def doFunc2(name):
    print('name : ', name) # 함수 안에 들어있는 변수는 매개변수라고 부른다! / name = 매게변수 / 호출할 때 name을 적어줘..라는 뜻


'''doFunc2() # ... error : 매개 변수를 안적어서 에러가 뜬다. (name) ... 매개변수(가인수)가 함수명에도 안적혀있으면 실인수값도 
안적으면 되지만 가인수에 값이 있으면 실인수는 무조건 값과 형태를 맞춰서 적어줘야한다.'''
# name이라는 매게변수는 들어오는 자료형에 따라서 자료 type이 바뀐다. - 변수 : 동적이다 
# 함수에 매개변수가 있으면 실인수도 변수값을 지정해줘야한다.
doFunc2(7)
doFunc2("김재환")

print('작업종료')

print('----------------------')

#c. def doFunc3
def doFunc3(arg1, arg2): # 2개의 매게변수를 주면 
    res = arg1 + arg2
    return res # 실행결과로 res를 반환해줄게.
    # pass : 이 함수에 대해서 아무 짓도 하지 말고 곱게 넘어가.

doFunc3("대한", "민국")
print(doFunc3("대한", "민국"))
print(doFunc3(3, 4))
# print(doFunc3(3, "사")) #... error
print(doFunc3("3", "4"))

result = doFunc3("3","3")
print('result : ', result)

print('-----------------------')

#d. def doFunc4
def doFunc4(a1, a2): # 2개의 매게변수가 들어왔다.
    imsi = a1 + a2 # 2개의 수를 더한다
    if imsi % 2 == 1: # 더한 값이 홀수면..
        return        # 함수 내에서 return은 함수의 무조건 탈출 = 자기를 부른 곳으로 되돌아간다. 
#                        / 조건이 참일 경우 return으로 넘어간다. return 뒤에 반환할 값이 없어서 'None'이 실행된 것
    else:             # 더한 값이 짝수면..
        return imsi # return 뒤에 반환할 값이 imsi로 지정했기 때문에 imsi값이 나온다

print(doFunc4(3,4)) # 함수는 별도의 공간을 가지고 있다. 그 공간내에서 수행이 된 것. 
print(doFunc4(4,4))

print('------------------------')

#e. def doFunc5
def triArea(a, b):
    c = (a * b) / 2
    triAreaPrint(c) # 함수 내에서 다른 함수 호출 

def triAreaPrint(arg):
    print('삼각형의 면적은 : ', arg)  # 2개의 함수를 미리 만들어둠

triArea(20,30)
print(triArea(20,30)) # - print()를 함수에 적어주면 return값도 같이 나오게 된다.
print('작업종료')

print()

#f. def passResult(kor, eng):
def passResult(kor, eng):
    ss = kor + eng
    if ss >= 50:
        return True
    else:
        return False

if passResult(20, 50): # passResult함수에 실인수가 가인수자리에 들어가서 나오는 값이 참인지 거짓인지를 따짐. 
#                        자기가 있는 함수로 되돌아가 참거짓을 따진다.
    print('합격')
else:
    print('불합격')

print('작업종료') # print()가 있어야 return값을 반환받을 수 있다!!

print('---------------------------')

#g. def swapFunc(a,b):
def swapFunc(a, b):
    return b, a # = return = (b, a)
a = 10; b = 20
print(a, ' ', b)
print(swapFunc(a,b)) # tuple은 하나의 값이라고 보고 반환함. 함수는 반환값이 반드시 항상 1개(묶음)이다. 
#                      print()가 있어야 return값을 반환받을 수 있다!!

print('--------------------------')

#h. funcTest() : 함수 안에 함수가 들어갈 수 있다.
def funcTest():
    print('funcTest 멤버 처리')
    def funcInner(): # 함수 안에 함수를 Inner Fucntion이라고 부름 / inner함수는 test함수 안에서만 수행 가능하다.
        print('내부함수 funcInner 실행')
    funcInner()
funcTest() # ... 함수 내에 함수가 들어갈 수 있다. 함수를 수행하되 return값은 반환하지 마라.

print(f"funcinner와 functest이해하셨죠잉?")
print('-------------------------')

#i. if 조건식 안에 함수 적용
def isOdd(para):
    return para % 2 == 1 # 홀수이면 True 반환
mydict = {x:x for x in range(11) if isOdd(x)} # 0에서10까지의 값이 들어올텐데 그때 값이 함수 isODd에서 참이면 x:x가 되고
#                                               거짓이면 적지 않는다. 
print(mydict)



print('------------함수의 종류 암기!!--------------')




print('변수의 생존 범위(Scope Rule)')
# 변수가 저장되는 이름공간(name space)은 변수가 어디에서 선언되었는가에 따라 생존시간이 다르다. 
# 변수 - 지역변수 / 전역변수
# 지역변수 : 
# 전역변수 : 
# 함수를 찾는 순서 : 지역변수(Local) > 내부함수(Enclosing Function) > 전역변수(Global) > 내장함수(Built-in) ... 중요!!

player = '전국대표' # 전역변수 : 현재파일(모듈)중 어디서든 호출 가능하다.
name = '신기해'

def funcSoccer():
    name = '이기자' # 지역변수 : 현재함수 내에서만 유효하다.
    city = '서울'
    print(f"이름은 {name}이고 수준은 {player}다. ") # 어디를 먼저 찾아야 하는가? = {name}에 해당하는 놈은 신기해인가 이기자인가?
#                                                    Local에 있는지 확인부터 먼저하는데 존재한다! 
#                                                    name = 이기자 {수준} : local에서 없으면 Global에서 찾는다.
    print(f"지역은 {city}")

funcSoccer() # - return값은 반환하지말고 그냥 함수만 수행시켜!
print(f"이름은 {name}이고 수준은 {player}다. ") # def의 영향을 받지 않는다!
# print(f"지역은 {city}") # ... Global이나 Local 어디에도 {지역}이 없기 때문에 error가 뜬다. 있다해도 Global을 선택하게 된다.

a = 10; b = 20; c = 30
print(f"foo 수행 전 a : {a}, b : {b}, c : {c}입니다.")
def foo():
    def bar():
        print(f"bar 수행 중 a : {a}, b : {b}, c : {c}입니다.") 
    bar()
    print(f"bar 수행 후 a : {a}, b : {b}, c : {c}입니다.")
foo() 
print(f"foo 수행 후 a : {a}, b : {b}, c : {c}입니다.")
# 지역변수와 전역변수의 개념이 없다.


print('\n')

a = 10; b = 20; c = 30 # ... 전역변수

print(f"foo 수행 전 a : {a}, b : {b}, c : {c}입니다.")

def foo():
    a = 7 # ... 지역 변수
    b = 100

    def bar():
        global c # bar의 멤버가 아닌 모듈의 멤버로 c가 정의된다. = 전역변수가 된다... c는 전역변수로 역할을 할 수 있다. bar()안에서 새로운 지역변수를 만드는 것이 아니고 bar()함수 안에서 c라는 이름을 사용하면 전역에 있는 c를 사용하겠다라는 뜻
        nonlocal b # bar내의 지역변수가 아닌 foo의 지역변수가 된다. = 상위함수의 변수가 된다. ... global c, nonlocal b는 빼고 연습해봐
        b = 8 # ... 지역 변수   
        print(f"bar 수행 중 a : {a}, b : {b}, c : {c}입니다.") 
        c = 9 # ... error : c라는 변수를 선언하기 전에 스테이트먼트가 정해져버려 들어갈 자리가 없기 때문 ... global c를 써주면된다. 
        # global c : bar 함수 내에서 전역변수 c(30)의 값을 사용하겠다.
        # c = 9 : global c덕분에 이제 전역변수가 30에서 9로 바뀌었다. 즉, 전역변수 c에 9를 대입
        b = 200 # ... bar내의 지역변수

    bar()
    print(f"bar 수행 후 a : {a}, b : {b}, c : {c}입니다.")

foo() 

print(f"foo 수행 후 a : {a}, b : {b}, c : {c}입니다.")


print('-----------------------------')

g = 1
print('g : ', g)

def fun() :
    global g # ... g = 2가 성립됨
    a = g # g = 1 = a
    g = 2 # g = 2 ... # global g가 있어야 error가 안뜸. 
    return a 

print(fun())


'''
1. 지정함수1
def doFunc1(): 
    print('doFun1 수행')

2. 지정함수2
def doFunc2(name):
    print('name : ', name)
    
3. 지정함수3
def doFunc3(arg1, arg2): 
    res = arg1 + arg2
    return res

4. 지정함수4
def doFunc4(a1, a2): 
    imsi = a1 + a2 
    if imsi % 2 == 1: 
        return        
    else:            
        return imsi

    ''' 