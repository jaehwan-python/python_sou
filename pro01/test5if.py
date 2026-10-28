
# 1. 조건 판단문 if

var = 1 # var이 1이라는 객체를 참조한다. 즉, 1이라는 값이 저장된 그 주소를 기억한다.
if var >= 3:  # 만약 var이 3이상이라는 조건이 참이라면
    print("크네") # "크네"라고 답한다             # 들여쓰기가 된 블럭은 위 조건이 참일 때만 수행한다.
    print("흠 크군") # "흠 크군"이라고 답한다.    # 조건이 참일 때 수행하는 문장이 2개이다.
print("끝") # 만약 var이 3이상이라는 조건이 거짓이면 곧바로 "끝"을 출력한다.

# 조건에 비교연산자가 들어가면 T/F로 나온다

print()

if var >= 3:
    print("크구나") # 조건이 참일때는 이걸 수행
else:
    print("작구나") # 조건이 거짓일 때는 이걸 수행
print("끝")

# if 뒤의 스테이트먼츠가 참이면 아래 들여쓰기 된 문장 수행
# if 뒤의 스테이트먼츠가 거짓이면 else 수행


print()

money = 200
age = 23


# 들여쓰기가 된 부분은 모두 해당 if가 참일 때만 수행한다.

if money >= 500: # money가 500 이상인가? 참이면 아래 수행 / 거짓이면 밑에 같은 행의 else 수행(item = 복숭아)
    item = "사과" # money 변수가 500보다 크다면 item은 "사과"이고 만약 그때~
    if age <= 30: # money가 500이상일때, 나이가 30이하인가? 참이면 아래 수행 / 거짓이면 밑에 같은 행의 else 수행(msg = '참 거짓')
        msg = '참 참'
    else: # 그때 나이가 30살보다 많으면..
        msg = "참 거짓"
else:
    item = "복숭아"
    if age >= 20:
        msg = '거짓 참'
    else:
        msg = "거짓 거짓"
print(f"중복 if 수행 후 결과 {item} {msg}")
print("끝")

print()

data = input('점수입력 : ') # 프로그램 입력 도중 잠깐 중단시키고 데이터 값을 입력받는 표준 입력 장치이다. input앞에 아무것도 없으면 받은 문자는 문자열이 된다.
print(data, type(data)) # 키보드로 값을 받음. # 내가 입력한 값과 그 값의 데이터 유형이 출력됨. * 우리는 아라비아 숫자 모양의 문자열을 입력한거다. type이 str이 나옴!!...int로 바꾸어야한다.
print(int(data), type(int(data)))
# print(data + 5) ...error int와 str을 연산이 불가능 = type mismatch
print(int(data) + 5) # type이 str이라면 앞에 문자변환형 메서드를 붙여주면서 연산하면 가능하다. 

jumsu = int(input('점수입력 : ')) # int를 둘렀기에 나올 때 int형으로 나온다. 내가 입력한 데이터가 int로 바뀜.
print(jumsu)

if jumsu >= 90: # 내가 입력한 데이터가 90점이상이라면
    print("우수") # 우수를 입력하고
else: # 그렇지 않으면(90점 이하면)
    if jumsu >= 80: # 80점이상이라면(80점과 90점사이)
        print("보통") # 보통을 입력한다.
    else: # 80점이상도 아니라면(90점 이상도 아니고 80점 이상도 아니면)
        if jumsu >= 70: # 70점 이상이라면(80과 70사이)
            print("못함") # 못함이라고 출력해라

# if jumsu >= 90:
#      print("우수")
# elif jumsu >= 80:
#      print("보통")   = 위와 같다. else + if = elif로 쓴다!!

# if jumsu >= 80:
#      print("우수")
# elif jumsu >= 90:
#      print("보통") ... 잘못된 코드 / 내가 98이라고 입력하면 무조건 우수밖에 안나오기 때문!! 문장간 상관성 파악하기!!

if jumsu >= 90:
    print("우수")
elif jumsu >= 80: # 그렇지 않고 만약 점수가 80점 이상이라면# if와 else/elif는 항상 줄맞춤을 한다!
        print("보통")
else:
    print("못함")

print("끝")

print()

jumsu = 80
if 90 <= jumsu <= 100: # 파이썬의 장점 : 조건에 범위를 정할 수 있다.
    print('A')
elif 70 <= jumsu <= 90:
    print('B')
else:
    print('C')
print('끝')

print('--------------------')

names = ['홍길동', '신기해', '이기자'] # 변수가 3가지의 값의 주소를 참조한다.(X) -> 한가지 변수는 한가지 값밖에 받지 못한다. 저런 경우에는 묶음형 자료 자체를 하나의 값으로 보고 변수는 리스트형 자료의 객체를 참조한다. = 주소값을 가지게된다.

if '홍길동' in names: # 집합형 데이터 'names'안에 (in) 해당 데이터가 있다면 참/거짓
    print('친구 이름이야')
else:
    print('누구야?!')
print('끝')

if (count := len(names)) >= 3: # :+ 대입표현식  ...  이런 식으로 표현하면 위에서 count = len(names)라는 식으로 따로 변수를 표현하지 않아도 된다.
    print(f"인원수가 {count}명이므로 단체 할인 적용")
else:
    print("ㅠㅠ")
print('끝')

scores = [95, 88, 76, 92, 81]
if (avg := sum(scores) / len(scores)) >= 80: # len(변수) : 변수의 길이 = 변수의 갯수를 나타낸다!!
    print(f"우수반  평균점수 : {avg}") # 점수의 합을 점수의 갯수로 나누면 평균이 나온다. avg값이 80이상인가?

print('끝')

# 대입 표현식 이해하기(중요)
print()

print('삼항연산')
a = 'kbs' 
b = 9 if a == 'kbs' else 11# 만약 a라는 변수가 kbs라면 if 절 이전의 b=9를 시행한다. 거짓이면 else를 시행한다.
print('b : ', b)

# if a == 'kbs':
#    b=9
#    print(b)
# else:
#     b=11     # 삼항연산의 원래모양
#     print(b)
print()

print("--------삼항연산 연습-------")

a = 11
b = 'mbc' if a == 9 else 'kbs'
print('b : ', b)

print()

a = 3
print(0 if a < 5 else 1 if a < 10 else 2) # 조건이 참이라면 0을 찍고 조건이 거짓이면 elif를 찍고 수행한다.
print('끝1')

#위 코드를 풀어쓰면 ..

if a < 10:
    if a < 5:
        0
    else:
        1
else:
    2
print('끝2')


# 삼항연산보다 풀어쓰기를 더 연습








