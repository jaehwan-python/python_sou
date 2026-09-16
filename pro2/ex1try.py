'''
예외처리 : 파일, 네트워크, DB작업, 실행오류 등의 Error에 대처
try ~ except ~ finally는 실행 중 발생할 수 있는 오류(Exception)를 처리해서 프로그램이 갑자기 종료되지 않도록 하는 문법
try에는 오류가 발생할 가능성이 있는 코드를 작성하고, except에는 해당 오류가 발생했을 때 어떠헥 처리할지를 작성한다.

<형태>

try:
    실행할 코드
    ...
except 예외종류:
    오류 처리 코드
finally:
    오류유무와 상관없이 처리할 구문(반드시 실행할 구문)

'''

def divideFunc(a, b):
    return a / b

print('이런 저런 작업을 하다가 ...')
#c = divideFunc(5,2)
#c = divideFunc(5, 0) ... error
# print(c)




# 물건을 사고 결제 버튼을 눌렀는데 에러코드가 남. 우리는 그 결제 화면이 에러코드가 뜨게 하지 않고, 에러가 뜨게 된다면 사람들이 보기 불편한
# 에러 문자들의 나열을 보여주는 것이 아니라, 결제가 원활하지 않습니다. 죄송합니다. 죄송한 마음과 함께 마일리지 1000점을 드리겠습니다.라는 화면이
# 나오게 한다. 이런 처리를 예외처리라고 한다.


try:
    # 실행문을 처리 블록(오류 가능 영역)
    # c = divideFunc(5, 0) # ... error가 없다.
    # print(c)   # 위 문장이 에러가 발생하면 에러가 발생한 부분 아래부터는 출력되지 않는다.
    print("계속")

    # aa = [1,2]
    # print(aa[0])
    # print[aa[3]] # error

    # 보조기억장치에 있는 파일 읽기
    open('c:/work/abc.txt') # c드라이브에 work파일에 ok.txt파일을 열어라라는 뜻..그런데 없다.

except ZeroDivisionError: # index Error는 못잡고 ZeroDivisionError만 잡을 수 있다.
    # 에러 발생시 처리하는 영역
    print('두번째 값은 0을 주면 안돼요.') # 에러가 발생하는 값이라면 이 statesment를 출력해요.

except IndexError as err:
    print('참조 범위 오류 : ', err) # 인덱스 에러 뿐만아니라 에러를 일으키는 부분을 err에 찍는다

# 모든 에러에 대해서 다 except를 적어 줄 순 없다. 그래서 우리는 error처리의 super 클래스인 Exception을 사용한다. 
except Exception as e: # 발생한 일반적인 예외를 한 번에 받아서 처리할 때 사용 # 여러 예외를 포괄적으로 처리한다. # 가장 많이 이용한다!! 그래야 모든 
#                        에러를 잡아주기 때문이다!
    print("에러 : ", e) # 모든 에러에 대해서 e라고 표현하고 그 e에 대한 설명을 보여준다. = 모든 에러를 대비가능

finally:
    print("에러 유무에 상관없이 반드시 수행돼요.") #  에러가 나든 안나든 무조건 이 문장은 수행된다.

# 아까는 무자비한 에러코드와 함께 프로그램이 강제 종료되었지만 try~except문을 사용하니 에러가 떠도 그냥 그 오류를 상기시키고 except문이 뜬다.
