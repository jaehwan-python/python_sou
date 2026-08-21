# 함수 장식자 : 기존의 함수코드를 수정하지 않고도 함수의 앞뒤에 새로운 기능이나 추가 작업을 더해주는 파이썬 프로그래밍 기법
# 함수 위에 @ 장식자 이름 기호를 붙여서 간단히 사용

# 장식자의 주요 특징기능 
# - 기능 추가 : 원래 함수를 바꾸지 않고 실행 전후로 로그 기록 시간측정, 권한 확인을 수행한다.
# - 코드 중복 줄이기 : 여러 함수에서 공통으로 쓰는 기능을 하나로 묶어 재사용성을 높인다.
# - 가독성 향상 : @기호를 사용해 코드를 깔끔하고 직관적으로 유지한다.

# 기본 작동 원리
# : 장식자는 함수를 인자로 받아 내부에서 새로운 함수(보통 wrapper)를 감싸서 반환한다.

def make2(fn):
    return lambda : "안녕"+ fn() # 람다함수의 매개변수가 없음


def make1(fn):
    return lambda : "반가워"+ fn()

def helloFunc():
    return "홍길동"

# 3개의 함수가 존재 

hi = make2(make1(helloFunc)) # 데코레이터 없이 시행한 경우 # make1은 helloFunc의 주소를 받음(클로저), make2는 make1의 주소를 받음(클로져)
#                             ... 함수가 함수를 감싸는 wrapper형태다.
print(hi())

# 다음 함수로 주소를 넘겨준다.

print()


# @를 써서 데코레이터를 썼다.
@make2
@make1
def helloFunc2():
    return "고길동"

print(helloFunc2())

print("-----------------------------------------")

def traceFunc(func):
    def wrapperFunc(a,b):
        r = func(a,b)
        print(f'함수명은 {func.__name__} (a={a}, b={b}) - > {r}')
        return r
    return wrapperFunc # 함수의 주소를 반환 = 클로져

@traceFunc # 데코레이터 : 함수를 감싸서 기능을 발휘한다.
def addFunc(a, b):
    return a + b

print(addFunc(10,20))


