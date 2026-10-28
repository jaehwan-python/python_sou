v1 = 10, 20, 30
print('v1 : ', v1) # v1 : (10, 20, 30)
print()
v1, v2 = 10, 20
v2, v1 = v1, v2 # 기억장소의 값 맞교환
print(v1, v2)
print()
print('값 할당 packing')
v1, *v2 = 1, 2, 3, 4, 5 # *은 나머지 값들을 묵어서 리스트로 만든다. 즉, v1은 1을 기억하고 v2는 [2,3,4,5]를 기억한다
print(v1, v2) # 1 [2, 3, 4, 5]
print()

*v1, v2 = 1,2,3,4,5
print(v1, v2) # [1,2,3,4] 5  # *표가 없는 부분이 하나의 값을 가짐. *표가 있는 변수는 나머지 값들을 list로 가짐

*v1, v2, v3 = 1,2,3,4,5
print(v1, v2, v3) # [1,2,3] 4, 5
v1, *v2, v3 = 1,2,3,4,5
print(v1, v2, v3) # 1, [2,3,4], 5
v1, v2, *v3 = 1,2,3,4,5
print(v1, v2, v3) # 1, 2, [3, 4, 5]
print()
print("print 함수 알아보기")
print(format(123.45678, '10.3f'))
print(format(123.45678, '10.3'))
print('서식에 의한 자료 출력 %s %d %f'%('문자열', 5, 23.4))
name = "마우스"
price = 5000; 
# ';(세미콜론)'여기서 하나의 명령문이 끝난거다. 국어로 따지면 마침표같은 역할이다. 있어도 되고 없어도 된다.하지만 여러 명령문을 한줄에 쓰고 싶으면 쓴다.
# 명령문이 너무 길면 \를 넣어 다음줄로 넘길 수 있다.
print(f"이름:{name}, 가격:{price}") # 문자열 앞에 f를 붙이면, 문자열 안에서 {}(중괄호)를 사용해 변수나 표현식의 값을 바로 넣을 수 있다.
print()
print('abc')
print('def')
# abc
# def
print('abc', end ='') # ' end = '공백을 주고 이어 쓰기
print('def')
# abc, def
print('\n\n')
print('연산자 연습 계속')
print(5+3, 5-3, 5*3, 5/4, 5//3, 5%3, 5**3) # '/' : 실수값 : '//' : 몫만 나타남 '%' : 나머지
print(123456789 ** 12) # 자바에서는 이런 연산이 불가능하지만 파이썬은 가능하다.
print(divmod(5,3)) # 몫과 나머지를 알려준다.
print(3+4*5, (3+4)*5) 
# 연산자 우선순위 : (  )   ->   **   ->   * / // %   ->   + -   ->   비교연산자  ->  not(논리연산자)  ->  and  ->  or  ->   = 
# *, / 는 우선순위가 없어 왼쪽부터 계산한다.
# 소괄호가 가장 우선순위가 높다. 즉, 항상 소괄호 안에 있는 연산을 우선시 한다.
print()
print('비교(관계) 연산자')
print(5 > 3, 5 == 3, 5 != 3) # ! : 같지 않다. 5와 3은 같지 않다. = True

print()
print('논리 연산자')
print(5 > 4 and 4 < 3, 5 > 4 or 4 < 3, not(5 > 4)) # and : 둘 다 참이어야 참, or : 둘 중 하나만 참이어도 참, not : 부정 = False, True, False

print()
print('문자열 더하기') # 숫자뿐만아니라 문자도 더할 수 있다.
print('한' + '국' + "만세")
print('한국' * 5)

print()
print('누적')
a = 10
a = a + 1 # a = 11 ... 증감 연산자
a += 1 # 'a += 1' = 'a = a+1' 연산에 변수가 참여해 누적이 가능하다.
print('a는', a) # = print(f"a는 {a}")이런식으로 간편하게 문자열과 숫자를 구분할 수 있다.
print(f'a는 {a}') 

print()
print('부호 변경 : ', a, a*-1, -a, --a, ---a) 

print()
print('boolen 처리 : ', bool(123), bool(1), bool(-3.5), bool(True)) # bool()안에 0이외의 값이 들어있으면 무조건 True
print('boolen 처리 : ', bool(0), bool(0.0), bool(False), bool(None)) # 0, False, None은 모두 False불의 형태
print('boolen 처리 : ', bool([]), bool({}), bool(set())) # 묶음형 데이터들은 모두 False불의 형태
# python에서 유의미한 정보가 있으면 True

print()
print('이스케이프 문자') #아스케이프 문자 : 특별한 의미를 표현하기 위한 문자 조합
print('aa \t bb') # aa bb # \t : 그냥 띄어쓰기
print(r'aa\tbb') # aa\bb # r : 이스케이프가 취소된다. \t가 문자열 형태로 표출된다.
print('aa\bbb') # abb
print(r'aa\bbb') # aa\bbb #\가 문자열 형태로 그대로 표현된다. ... # r은 기존에 있던 이스케이프 문자를 무력화시킨다.
print('aa\nbb') # aa       #\n은 줄바꾸기
                #  bb
print(r'aa\nbb') # aa/nbb
print('c : \a\abc.txt') # c: bc.txt
print('c : \n\abc.txt') # c:
                        # bc.txt
                