'''
모듈 : 소스 코드의 재사용을 가능하게 하며, 소스코드를 하나의 이름 공간으로 구분하고 관리할 수 있다.
하나의 파일은 하나의 모듈이 된다. .. 함수 -> 클래스 -> 모듈(라이브러리)
모듈의 멤버 : 모듈, 함수, 클래스, 변수, 실행문
표준 모둘, 사용자 작성 모듈(우리가 직접 만듬), 제3자 모듈(전문가가 만들어 우리가 유료로 이용)로 구분
'''
print(print.__module__) # bulitins : 내장 모듈이다. 메모리로 가져와줘야하지만 자동으로 가져와진다. = 즉, 기본적으로 지원되기 때문에 import에서 불러오지 않아도 된다.

print('뭔 작업을 하다가...외부 모듈 사용하기') # builtins말고 다른 모듈을 사용한다!

#print(sys.path) #모듈의 경로를 알고 싶다.
# sys에 빨간줄..지원안하는 모델로 import해야 한다.
import sys
print(sys.path)
# builtins 이외의 모듈들은 import해 불러와서 쓴다. # sys 파일 안에 path와 exit가 들어있다.
'''sys.exit'''
#print('종료') ... 프로그램 실행 도중에 프로그램은 무조건 종료된다. print('종료')가 안찍힌다. 이미 sys모듈내에 있기 때문이다.
# path는 변수고 exit는 함수다. 그래서 sys.path : sys가 import된 경로를 가져와라. 라는 뜻이다.
'''
sys파일은 보조기억장치에 있고 import sys해서 주기억장치로 끌어올라온거다. path와 exit는 모두 sys파일(모듈)에 존재하는 것이다. 
밑에서 나온 여러 코드(보조기억장치) 중 어딘가에 있는 sys파일을 import하여 끌어올린겨.
다시 정리하면 import sys print(sys.path) sys.exit에서 sys파일은 보조기억장치에 있어. 
주기억장치가 실행되는 환경에서 파이썬 인터프리터인 VS code에서 import sys를 하게 되면 보조기억장치에 존재하는 sys모듈이 주기억장치로 올라와서
sys모듈안에 있는 함수나 변수, 클래스 등을 사용할 수 있게 돼. 대신 builtins 되어 있는 모듈과는 다르게 sys는 
보조기억장치에 있기에 내가 불러와야한다는 점이야.

보조기억장치에 있던 sys.py가 import하게 되면 RAM으로 가져와서 사용할 수 있다. 
'''
# ex1.
q = 'n'
if q == 'y':
    sys.exit()
print('end')
'''
sys.exit : 실행 중인 프로그램이 밖으로 나오는 수준이 아닌 완전한 종료
'''

'''
수학 관련 모듈 읽기
자주 쓰이지 않는 모듈은 보조기억장치에 있어 내가 vs code에서 쓸려면 주기억장치로 끌어올려야 한다. import해서.
'''

# ex2.
import math
print(math.pi)
print(math.sin)
print(math.sin(math.radians(30))) # sin 30의 값이 출력
print('종료') # 파이와 사인은 math 모듈에 있다.

'''
달력 출력
'''

# ex3.
import calendar
print(calendar.MONDAY)
calendar.setfirstweekday(6)
calendar.prmonth(2026, 8) # 8월달 달력이 나온다
del calendar


'''
시간 기다리기
'''

# ex4. 
import time
print('시작')
time.sleep(5) # 5초 쉬고 계속
print('계속')

'''
난수 출력(규칙 없는 숫자 출력)
'''
# ex5.
import random
print(random.Random()) # random.하고 나오는 여러개 실행가능한 값들 옆에 그림을 통해 . 뒤에 오는게 함수인지 변수인지 상수인지 구별! 함수면 실행할 때 ()를 붙여야 한다.
print(random.randrange(1, 10)) # 1~10 사이의 예측할 수 없는 값(난수) 출현
print('종료')

# 위 방식과 아래 방식이 같다. 
'''
import random  ... 일부 멤버(내가 필요한)만 로딩
print(random.randint(1, 23))
print(random.randange(1, 23))
=
from random import randint, randrange, choice  ... 일부 멤버(내가 필요한)만 로딩
print(randrange(1,23))
print(randint(1,23))
from random import *  ... 전체 멤버 로딩 ... 메모리 낭비가 매우 심함! ... 쓰지마!
'''

#
from random import random # random모듈로부터 내가 원하는 값을 가져옴. # 모듈명을 안쓰고 함수만 써줘도 된다. from 모듈명 import 그 모듈의 멤버 
print(random)

#
from random import randint, randrange, choice # 
print(randrange(1,23))
print(randint(1,23))
'''

'''


