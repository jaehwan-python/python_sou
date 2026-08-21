# 기본 자료형 : int, float, bool, complex
# 묶음 자료형 : str, list, tuple, set, dict ... 여러 개의 자료의 모음
# 데이터를 저장하는 핵심 단위

# Str : 문자열 저장 단위, 순서o, 수정x
s = "sequence"
print("길이(크기) : ", len(s))  # len(s) : 변수의 길이를 알려준다. 각 단어가 8바이트를 사용하고 있다. 
# a를 아스키코드 97로 받아들이고 8개 스위치 중 어딘가에 불이 들어오게 해서 a임을 알게 한다. 
# # 모든이미지를 숫자로 인식해서 그 숫자에 불이 들어오게 해서 이미지를 인식한다. 쪼개서 하나씩 만들어 한 칸을 숫자화 시켜 한줄로 세워 인식한다. 
#   = 컴퓨터가 인식하는 방법
# 파이썬은 함수 중심적 언어(인터프리트 방식) vs 자바, C언어 - 클래스 중심적 언어(컴파일러 방식)
print("포함횟수 : ", s.count('e'))  # s.count('e') : s에 저장된 문자에서 'e'가 존재하는 개수
print('검색위치 : ', s.find('e'), s.find('e', 3), s.rfind('e'))  # s.find('e') :  s.rfind('e')
print('첫글자 유무 : ', s.startswith('s'), s.startswith('a'))  #s.startswith('s')
# 색인 s / e / q / u / e / n / c / e : 각 문자에 숫자를 매기는 것 '0'부터 시작
# 함수들의 종류를 알려주는 코드를 부를줄 알면 모든 함수를 암기할 필요가 없다.

print()
ss = "mbc"
print(ss, id(ss))
ss = "abc"
print(ss, id(ss)) # 사람은 m을 a로 바꾼 것 처럼 보이지만 컴퓨터는 mbc를 abc로 바꾼걸로 인식한다. 
# mbc 1488037803040
# abc 1488037964192 로 나온다.
# 뒤에 있는 숫자코드가 ascii code는 아니다. id()는 변수가 가리키는 객체가 누구인지 확인하는 번호 = 식별값을 확인한다.
# ss는 기존 객체인 'mbc'의 주소(식별값)를 기억하고 다시 받은 새로운 객체 'abc'의 주소(식별값)를 기억한다. = 수정이 안되는 정보다. = 상수

print()
print('s / e / q / u / e / n / c / e ')
print('인덱싱 / 슬라이싱') 
print(s[0], s[5], s[-1]) # s라는 기억장치의 0번째 값 = 인덱싱 : 순서가 있는 데이터에서 원하는 값을 쏙 뽑아냄
print(s[0:4], s[:4], s[-4:-1]) # s라는 기억장치의 범위를 지정함 = 슬라이싱 : 범위를 지정하여 그 값들의 집합을 보여줌 / 0이상 4미만(sequ) 
#                                                                          / 4번째 전까지(sequ) -4에서 -1까지(enc)
print(s[::]) # s의 모든 값이 다 나옴
print(s[::2]) # 증가치
print(s[0:8:3]) # 0번째부터 8번째 전까지 2개씩 증가하면서
print(s[0:len(s):1]) # 증가체가 안적혀 있으면 1로 고정

print() # 파이썬 문자열 함수
print('*'*20) # 별 20개 찍어 = 줄만들기
print()

# List : 다양한 종류의 자료 묶음형, 순서ㅇ, 수정ㅇ, 중복ㅇ
a = [1, 2, 3] # list는 무조건 중괄호 안에 넣기. 중괄호 안에는 다양한 데이터가 들어올 수 있다.
print(a, a[0], a[0:3])

b = [10, a, 10, 20.5, 'uam', '문자열', True] # a는 이전에 저장된 a list를 넣었다. 즉, 리스트 안에 리스트가 들어갈 수도 있다.
print(b)
print(b, b[0], b[1], b[1][1]) # *b[1][1] : b list의 1번째 중 1번째 값을 지정
print()

family = ['mom', 'dad', 'brother', 'me']
print(family)
print(family, id(family))

#1
family.append('daughter(imagine)') # 해당리스트에 (내용)을 맨 마지막에 추가할 수 있다.
print(family, id(family)) # 바뀌어도 주소가 같다. 대체가 아닌 수정을 한 것이기 때문. 데이터가 달라진다고 해서 기존 주소가 바뀌지는 않음. 
#                           = 주소 중복이 가능

#2
family.remove('daughter(imagine)')
print(family, id(family)) # 해당리스트에 (내용)을 삭제 = 수정이 가능함! 여기서도 데이터가 달라진다고 해서 기존 주소가 바뀌지 않는다. 
#                                                     = 주소가 중복가능하다.

#3
family.insert(0,'grandmother') # 삽입 : 내가 지정하는 순서(번째)에 해당 값을 부여한다.
print(family, id(family))

#4
family.extend(['uncle, aunt']) # 추가
print(family, id(family))
family += ['dog : PPO PPI'] # 추가(누적)
print(family, id(family))

#5 
family.remove('dad') # 값에 의한 삭제
del family[2] # 순서에 의한 삭제 # dad가 사라지고 brother가 2번째로 와서 삭제됨
print(family, id(family))

print()

#6
kbs = ['123','34', '234']
kbs.sort() # sort : 문자열을 정렬한다. 문자열 값을 오름차순으로 정리한다.
print(kbs)

#7
mbc = [123, 34, 234] # 이번엔 숫자형 자료들이다.
mbc.sort()  # 숫자형 자료들을 오름차순으로 정렬한다. - 리스트 값 순서가 바뀜. 영구적으로 고정됨.
print(mbc) # [34, 123, 234]
mbc.sort(reverse = True) # 숫자형 자료들을 내림차순으로 정렬한다.
print(mbc) # [234,123,24]

#8
sbs = [123, 34, 234]
ytn = sorted(sbs) # sorted(똑같이 오름차순으로 정리됨)를 쓰면 원본의 변화 없이 그대로 써도 원본이 유지가 된다
print(ytn) 
print(sbs)

print()
print('*' * 20)
print()

# tuple : 리스트와 유사 / 읽기 전용 - 수정X
t = (1, 2, 3, 4)
t = 1, 2, 3, 4 # 위 아래 문장 둘 다 같은 뜻
# 대괄호[]는 리스트, 중괄호{}는, 소괄호()는 튜플
print(t, type(t))

k = 1  # int
print(k, type(k))

k = (1)  # tuple # 데이터 값이 하나밖에 없을 때 int로 인정받고 싶으면 ,를 적어줘야한다.
print(k, type(k))

k = (1,)
print(k, type(k))

print()

print(t[0], t[1:3]) #  이때 대괄호는 인덱싱을 위한 대괄호지 리스트의 대괄호가 아니다. 주의!
# t[0] = 9 ...error
print(t) # tuple은 수정불가해 error가 뜬다. 리스트와 달리 마음대로 수정이 불가능하다. 그래서 중요한 데이터를 담아 둘 때는 리스트보다 튜플에 담아둔다. 
# 튜플은 인덱싱과 슬라이싱만 가능하다!! 수정은 안된다.
# 그러면...
# 튜플값을 수정할 때는 리스트로 형변환을 사용한다.
imsi = list(t) # t의 자료형의 type을 튜플에서 리스트로 바꿈
print(type(imsi))
imsi[0] = 9 # t(튜플)을 imsi(리스트)로 바꾸었고 imsi(리스트)의 0번째 값을 9로 바꾸었다.
t = tuple(imsi)
print(t, type(t)) # 다시 리스트를 튜플로 바꿈  

print()
print('*' * 20)
print()

# set : 순서x, 중복x ,수정ㅇ
ss= {1, 2, 3, 2} # set은 중괄호를 이용한다. set은 중복데이터가 사라진다. - 최고 장점
print(ss, type(ss))
ss2 = {3, 4}
print(ss2)
print(ss.union(ss2)) # union은 합집합(ss와 s2)
print(ss.intersection(ss2)) # intersection은 교집합(ss와 ss2)
print(ss - ss2, ss | ss2, ss& ss2 ) # 차집합, 합집합, 교집합

ss.update({6,7})
print(ss)
ss.discard(7) # 값 삭제
ss.discard(7) # 값 삭제 : 해당 값 없으면 그냥 통과(이전 단계에서 이미 지움)
ss.remove(6) # 값 삭제 : 해당 값 없으면 error
print(ss)

print()
print('*' * 20)
print()

li = ['aa', 'aa', 'bb', 'cc', 'aa'] 
print(li)
imsi = set(li) # list를 set으로 바꿔 중복데이터를 없애줌.
li = list(imsi) # set을 다시 list로 바꿈.
print(li) # ['aa', 'cc', 'bb']

print()
print('*' * 20)
print()

# dict : 사전 자료형 - 추가 및 삭제가 가능ㅇ
# 형태 : {'키' : 값}형태

# 방법1
mydic = dict(k1 = 1, k2 = 'ok', k3 = '1234') # 해당 key에 대한 그 값을 지정한다. # 웹상에서 데이터를 주고 받을때 JSON을 많이 사용함. 
#                                              그때 키 값을 많이 사용한다.
print(mydic, type(mydic))

# 방법2
dic = {'파이썬' : '뱀', '자바' : '커피', '번호' : 123}
print(dic, type(dic))
print(len(dic))
print(dic['자바']) #키로 값을 검색함
print(dic.get('자바')) # value로 키를 검색함.
# print(dic[0]) ... error : dict은 인덱싱이 불가능하다. 왜냐하면 순서가 없기 때문이다.

dic['금요일'] = 'wow' # 추가가 가능하다
print(dic)

del dic['번호'] # 삭제가 가능하다.
print(dic)
print(dic.keys())
print(dic.values())

# 4가지 자료형 - list / tuple / set / dict의 특징 파악하기 중요!