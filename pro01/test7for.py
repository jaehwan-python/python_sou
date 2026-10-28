'''반복문 for 
for target in object: target에 object의 요소들을 하나씩 대입시켜라! ... 묶음형 자료를 반복!!(일반형 자료X)
        statement

target : 내가 임의로 정한 변수 .. 위에서 따로 target = ~ 할 필요가 없다!
object : 메모리에 저장된 객체 .. 묶음형 자료를 쓴다.
target은 object의 객체의 주소값을 저장한다.
object자리에 묶음형 자료가 온다 .. list[], set{}, tuple() ...* dict형태는 못받는다. 그래서 datas.item()을 통해 리스트 속 튜플 형태의 값으로 형변환을
해준다!
''' 

for i in [1, 2, 3, 4, 5, 5, 5]: # range안에 있는 자료들이 순서대로 i에 대입되고 모두 대입되어 대입해야 할 자료가 없으면 탈출한다.
    print(i, end = ' ')

for i in (1, 2, 3, 4, 5, 5, 5): # tuple
    print(i, end = ' ')

for i in {1, 2, 3, 4, 5, 5, 5}: # set은 중복이 안된다.
    print(i, end = ' ')

# 집합형 데이터를 순서대로 하나씩 꺼내 대입시킬 때 for를 쓴다. 리스트, 집합, 튜플 모두 가능하다. 또한 중복자료도 가능하다.
print('\n\n')

'''
# 편차 제곱합의 평균 = 분산 ... 제곱근(분산) = 표준편차 ... 평균 = 전체 점수 / 전체 갯수
                                                        분산 = 
print('분산 / 표준편차 ---')
numbers1 = [1, 3, 5, 7, 9] # 합은 25, 평균은 5.0
total = 0
for a in numbers1:
    total = total + a 증가치
print(f"합은 {total}이고 평균은 {total / len(numbers1)}")


numbers2 = [3, 4, 5, 6, 7] # 합은 25, 평균은 5.0
total = 0
for a in numbers2:
    total = total + a 증가치
print(f"합은 {total}이고 평균은 {total / len(numbers2)}")


numbers3 = [-3, 4, 5, 6, 12] # 합은 25, 평균은 5.0
for a in numbers3:
    total = total + a .. 이런꼴은 직전에 한 계산을 지금 할 계산과 더할 수 있다는 뜻이다.. 앞으로 자주 나올테니 기억해두도록!
print(f"합은 {total}이고 평균은 {total / len(numbers3)}")

# 데이터가 다른데 합과 평균이 서로 같음에 같은 데이터로 인식하기 쉽다. ... 편차를 알아야 한다.
'''

numbers = [1,2,3,4,5]
avg = sum(numbers) / len(numbers) # .. 평균
# 편차제곱의 합 

hap = 0
for i in numbers : 
    hap = hap + (i - avg) ** 2 
print(f"편차제곱의 합 : {hap}")
var1 = hap / len(numbers)
print(f"분산은 {var1}")
print(f"표준편차는 {var1**0.5}") # 분산은 모두 0이 나오기 때문에 분산들을 제곱한 값을 더하면 무조건 양수만 나올 수 있다.


print()

colors = ['빨강', '초록', '파랑']
for v in colors:
    print(v, end = ' ')

print()

print(f"'iter()' : 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태를 만들어 주는 함수") # iterate : '반복하다'
iterator = iter(colors) # iter함수를 사용해도 변수에 리스트 값의 요소를 넣을 수 있다.
# iter(colors)하면 colors 안에 있는 객체들을 하나씩 꺼내서 쓴다.
# iterator = iter(colors)를 하면 colors안에 있는 객체들을 하나씩 가리키는 화살표이다. iter()는 빨-초-파를 순서대로 가리키고 다시 원래대로 돌아가지 않는다.
x = next(iterator) # 빨강을 가리키고 다음 객체를 가리켜
y = next(iterator)
print(x, y)
for v in iterator : # iterator는 순서대로 뽑아쓴다. 위에서 빨강과 초록을 뽑아썻기에 남은 친구인 파랑만 나오게 된다.
    print(v, end = ' ') # 내가 원할때 하나씩 꺼내서 쓸 수 있다. 주로 next와 함께쓴다

print()

for idx, d in enumerate(colors): # enumerate : colors의 집합형 자료에서 하나씩 빼주는데 인덱스도 같이 나온다! 인덱스와 값을 반환한다.
    print(idx, ' ', d)

for idx, d in enumerate(colors, start = 1): # start = 1하면 처음 시작하는 인덱스를 1로 바꾼다.
    print(idx, ' ', d)

print()

print('사전형-----------------------')
datas = {'파이썬' : '만능언어', "java" : '웹용언어', 'maria DB' : 'RDBMS'} # 이번에는 어떤 변수가 리스트가 아닌 dict형태의 자료형의 객체 주소를 저장하고 있다.
print(datas.items()) #변수.items() : 리스트 안에 dict를 키:value 형태로 만들어준다. 리스트 안에 튜플 형태로 만들어준다.
# dict의 자료형들을 for반복문(for반복문은 묶음형자료를 받지만 dict형태는 못 받기 때문!)에서 쓰기위해 형변환을 해준것임 ㅇㅇ [("key1", "value1"), ("key2", "value2"), ("key3", "value3")] 리스트 속 튜플 형태로 만들어주는 것이 .items
# datas.items() = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]

for i in datas.items(): # dict형태가 리스트 속 튜플 형태로 만들어서 순서가 생겼다. 01234...(파이썬, 만능언어), (java, 웹용언어), (mariaDB, RDMS) 순서로 튜플끼리 짝지어진다
    print(i[0], ' ~~ ', i[1]) # datas가 items()함수를 통해서 리스트 속 튜플 자료로 바뀌었다.
    # [("key1" = i[0], "value1" = i[1]), ("key2" = i[0], "value2" = i[1]), ("key3" = i[0], "value3" = i[1])
    # i[0] : key값 , i[1]은 value값이다.

print()

for k, v in datas.items(): # 집합형 자료의 요소가 복수라면 변수를 2개를 써서 따로 값을 받아 사용할 수 있다.
    print(k, ' ~~ ', v)

print()

for k in datas.keys(): 
    print(k, end = ' ') # 파이썬 java mariaDB - key만 받고 싶을 때 "변수.keys()"함수 이용

print()

for v in datas.values(): 
    print(k, ' ~~ ', v) # 만능언어 웹용언어 RDBMS - value만 받고 싶을 때 "변수.values()"함수 이용


'''
datas.items() : datas라는 dict 집합형 자료에서 key:value값을 리스트 속 튜플 형태로 빼낸다.
datas.keys() : datas라는 dict 집합형 자료에서 keys값만 뽑아낸다.
datas.values() : datas라는 dict 집합형 자료에서 values값만 뽑아낸다.
'''

print()
print('다중 for ---------------------------') # for문 안에 for문이 들어갈 수 있다.
for n in [2, 3]:
    print(f"{n}단 ~~~")
    for su in [1,2,3,4,5,6,7,8,9]:
        print(f'{n} * {su} = {n * su}') # for문 안에 for문 넣기 {n = 2}에 대해서 {su = 1,2,3,4,5,6,7,8,9}가 대입되고 나서 {n = 3}에 대해서 
#                                         {su = 1,2,3,4,5,6,7,8,9}이 대입된다.

# 안쪽 반복문이 끝나고 바깥쪽 반복문을 수행한다.

# for문은 집합형 자료가 없으면 반복을 할 수 없다. 대신 while과 다르게 초기값과 증가치를 따로 설정해줄 필요가 없다. 어차피 주어진 집합형 자료가 초기값이고 모든 요소에 대해서 값을 대입시켜야 하기 때문에 증가치는 필요가 없기 때문이다.
print()

print('다중 for ----, continue / break')
nums = [1,2,3,4,5]
for i in nums:
    if i == 2 :
        continue # 2는 건너뜀
    else:
        if i == 4:
            break # ... 탈출 : 1찍고 3찍고 탈출함
    print(i, end = ' ')
else: # break를 만났으면 else가 나오고 break가 없으면 나타나지 않는다. = break는 선택적으로 쓸 수 있다.
    print('정상종료')

print("\n\n")


print(f"정규표현식 + for 연습")
message = """ 
안녕하세요 저는 김재환이구요 저는 20040629입니다. 주민번호는 040629 3abcdef이에요 만나서 다들 반갑습니다. 오늘은 2026년 08월 22일 이네요 
저는 현재 톰홀튼 카페에서 파이썬을 공부중입니다... ㄷㄷ 너무 많네요.... 하지만 열심히 해보겠습니다 현재 시간은 16시 33분입니다
... 웹에서 주워온 임의의 데이터 ... 가공이 필요!!
"""
print(message)
# 정규표현식을 쓰면 데이터에서 내가 원하는 데이터만 쏙 뽑아낼 수 있다.
# 내가 필요한 정규표현식을 파이썬에서 라이브러리로 지원하고 있다. 우선 내가 정규표현식(re)을 쓰겠다고 주기억장치로 가져와야한다.
import re # 정규표현식을 쓰기 위한 라이브러리 불러와! re도 함수이다. 그래서 라이브러리에 저장된 re함수(전문가들이 만들어둠)를 불러온다.

print()
# 1. re.sub()
message2 = re.sub(r'[^가-힣\s]', '', message)# 정규표현식에 패턴을 고를려면 r로 시작해야한다. 한글과 공백을 제외한 나머지 자료만 나오게 함 
# 패턴과 일치하는 문자엶을 다른 문자열로 치환(message -> message2) # 가-힣그리고 공백을 빼고 모두 substitute한다. 즉, 한글과 공백만 나오게한다.
print(message2)
# ^[] : 시작 글자 
# [^] : 부정(=제외)
# \s : 공백
# * 정규표현식에 쓰이는 함수 꼭 알기


print()
# 2. 변수.split : 공백을 기준으로 자르는 함수
import re
message2 = re.sub(r'[^가-힣\s]', '', message)
print(message2)
message3 = message2.split(' ') # 공백을 기준으로 문자열들을 정리한다 
print(message3)


print()
# 3. 단어별 빈도수 출력 - dict사용
import re
message2 = re.sub(r'[^가-힣\s]', '', message)
print(message2)
message3 = message2.split(' ') # 공백 기준 문자열 정리 
print(message3, ' ', len(message3))


print()
# 4. for문을 이용해서 내가 원하는 자료가 몇 번 나오는지 확인
cou = {} #- dic가 될 수도 set이 될 수도 있다..!
for i in message3: # for문을 써서 내가 지정한 각 단어들이 몇 번씩 나오는지 dict 자료형으로 확인가능하다.
    if i in cou:
        cou[i] = cou[i] + 1 # 같은 단어가 있으면 누적
    else :
        cou[i] = 1 # 최초의 단어일 경우 ex) '단어' : 1
print(cou)

print()


# 5. 정규표현식을 이용하는 함수 findall / sub / match 등등이 있다. 데이터 분석을 위해서는 굉장히 중요하다!!
print("정규표현식 좀 더 ...")
for imsi in ['111-1234', '일이삼-일이삼사', '222-1234', '333&1234']:
    if re.match(r'^\d{3}-\d{4}', imsi) :
        print(imsi, '전화번호 맞네')
    else :
        print(imsi, '전화번호 아니야')
# ^ : 숫자로 시작한다   # \d : 숫자1개   # {} : 숫자 몇 개   # $ : 숫자로 끝난다. 
# imsi에서 숫자3자리로 시작해서 4자리로 끝나는 형태를 정규표현식을 이용해서 들고와라.

print()


# 6. comprehension
print('comprehension : 반복문 + 조건문 + 값 생성을 한 줄로 표현')
a = [1,2,3,4,5,6,7,8,9,10]
li = [] # 밑의 조건에 충족하는 수들을 빈칸[]에 채워넣어라
for i in a: # li에 a값들을 하나씩 밀어넣는다. 밀어넣어진 값들은 li에 저장되어 리스트 형태로 저장된다.
    if i % 2 == 0:
        li.append(i) # li라는 변수에 i값을 추가해라.
print(li)# li값의 주소가 반환되어 나타난다.

print()

# 파이썬 컴프리핸션으로 위 코드와 동일한 값을 낸다.
print(i for i in a if i % 2 == 0) # a의 값들을 i에다가 넣는다 / 만약 a로부터 받은 i값들이 짝수라면 / i를 그대로 출력해라

print()

datas = [1,2,'a', True, 8.3]
li2 = [i for i in datas if type(i) == int] # datas에 있는 값들을 i에 넣는다 / 만약 datas로 받은 i값들의 유형이 정수형이라면 / i를 그대로 출력해라
print(li2) # ... if문의 삼항연산과 비슷하다.

print()

id_names = {1 : 'tom', 2 : 'james'} # 키와 value값을 뒤집고 싶다!
print(id_names)
names_id = {val : key for key, val in id_names.items()} # 리스트 속 튜플 형태로 바뀐 원래 dict형태의 id_names[(1,'tom'), (2,'james')]가 key와 
#                                                         val값에 하나씩 들어가서 / val : key 형태를 이룬다 
# id_names.keys() : dict자료형(id_names)에서 key값만 뽑아냄 
# id_names.values() : dict자료형(id_names)에서 value값만 뽑아냄
# id_names.items() : dict자료형(id_names)에서 key:value 모든 값을 뽑아냄.  - 리스트 속 튜플 형태로
print(names_id)

print()

aa = [(1,2), (3,4), (5,6)] # 리스트 안에 튜플자료가 들어 있는 형태 ... .items()를 썼다고 가정
for a, b in aa:
    print(a + b)
# 아래의 식도 동일하다
print([a + b for a, b in aa])

print(*[a,b])
#묶음형 자료에 *을 붙이면 묶음이 풀린다 - unpack 
print(*[a + b for a, b in aa], sep ='\n') # sep ='\n' : 앞에 나온 값을 옆이아닌 아래로 내려서 적게 함 ... end = ' '와 반대성격

print()


# 7. range : 수열생성
print('수열생성 : range(start, stop, step)')
print(list(range(1,6)))
print(list(range(1,6,1))) # 1부터 5까지 증가치1을 단위로 올라간다. 자료를 list형태로 나타냄
print(set(range(1,6,1))) # 자료를 set형태로 나타냄
print(tuple(range(1,6,1))) # 자료를 tuple형태로 나타냄

print(set(range(6))) # 초기치를 주지 않으면 0부터 시작한다. # 증가치를 주지 않으면 1단위로 시작한다.
print(list(range(0,6,1)))
print(list(range(-10, -100, -20)))
# for i in range()
for i in range(6): # 0부터 5까지 변수에 대한 값을 i가 받는다.
        print(i, end = ", ")

print()

for _ in range(6): # for다음에 나오는 변수값을 사용하지 않을 것이다. 그러면 언더바(_)를 사용한다.
    print('반복')

print('1~10까지 정수의 합')
tot = 0
for i in range(1,11): # 1부터 10(11-1)까지의 수 중에서 i라는 묶음형 자료를 대입하여 반복한다.
    tot = tot + 1
print('tot :', tot, sum(range(1,11))) # sum은 내장함수

print()

for i in range(1, 10):
    print(f"2*{i} = {2*i}")

print('2~9단의 구구단 출력(같은 행단위 출력)')
for i in range(2, 10):
    for j in range(1, 10):
        print(f" {i} * {j} = {i * j}", end= ' ')

print()

print('주사위를 두 번 던져 나온 숫자들의 합이 4의 배수가 되는 경우만 출력')
print("방법1")
for i in range(6):
    n1 = i + 1
    for j in range(6):
        n2 = j + 1
        n = n1 + n2
        if n % 4 == 0:
            print(n1, n2)

print()

print("방법2")
for i in range(1, 7, 1):
    for j in range(1, 7):
        hap = i + j
        if hap % 4 == 0:
            print(i, j)



