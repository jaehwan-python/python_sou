# 2. 반복문 while 조건 : 조건(if)이 참인 동안 블럭을 수행한다.  가장 큰 특징 1. 초기치와 증가치가 있다. 2. while뒤에 있는 조건이 거짓이 될때까지 들여쓰기 된 부분을 수행! ..이걸 증가치가 자제해준다.

a = 1 # 조건에 초기치를 준 것. while문 이전에는 초기값을 설정해주는 작업이 필요!!
while a <= 5: # 초기 a값으로 1을 받음. a는 5보다 작거나 같다. 조건이 참!
    print(a, end = ' ') 
    a = a + 1 # 이게 없으면 위에서 수행을 a가 5보다 작거나 같을 때까지 계속 수행하지 못한다. = while문에서 못나온다. # 조건에 증가치를 준 것 = while문을 탈출하게 함.
    # 참인 동안 블럭을 계속 수행한다.
else: # 이 else문은 선택적으로 수행한다 : 조건에 따른 종료시 수행한다. # 조건이 거짓이면 else로 옴
    print('수행 성공')

print('끝')

print()

# 내가 설정해준 조건(while 뒤에 붙는 조건)이 참이면 아래 들여쓰기 된 문장을 반복하고 아니라면 탈출한다.

i = 1
while i <= 3: # while뒤의 문장이 참이기 때문에 조건이 참이다. 그래서 아래 들여쓰기 된 부분이 거짓이 될 때까지 반복한다.
    j = 1
    while j <= 4:
        print('i = ' + str(i) + ', j = ' + str(j))
        j = j + 1         # j에 대한 while반복문이 거짓이 될때까지 반복하고(그러면 밖으로 탈출) 다 하면 
    i = i + 1             # i에 대한 while반복문이 거짓이 될때까지 반복한다.

# if문 안에 if문이 들어갈 수 있는 것처럼 while문 안에 while문이 들어온 경우
# 안에 while문이 모두 수행하여 완료되면 다시 바깥쪽 while문을 수행한다.
# int('1') = 숫자 1
# str(1) = 문자 1
# i는 처음에 1이다. 참이다. 다음 while문으로 온다. j는 1이다. j = j + 1을 통해 참이 끝날 때까지 반복한다. i = 1일때 j에 대한 값이 충족될 때까지 조건이 참이 되면 그 다음 i를 만족시켜준다. i = i + 1을 통해 참이도리 때까지 반복한다!!

print('끝')

print()

print('1~100 사이의 정수 중 3의 배수의 합은?') # 3의 배수 : 3으로 나눈 나머지가 0이 되는 값

su = 1
hap = 0

while su <= 100: # su가 1이기 때문에 조건이 참이다! ... = su가 100이 될때까지 수행해라.
    if su % 3 == 0: # 1~100까지 숫자 중 3으로 나눈 나머지가 0인 수들이 모이게 됨.
        hap = hap + su # 그 3의 배수들을 모두 더함.
    su = su + 1 # su값이 1부터 100까지 시행한다. = 증가치

print('합은 ', hap)

print('끝')

print()

colors = ["r", "g", "b"] # colors는 ["r","g","b"]라는 하나의 리스트의 주솟값을 가지고 있다.
num = 0 # 변수가 0부터 시작할거다. len(colors) = 3
while num < len(colors): # num이 colors의 리스트의 갯수보다 작다면...
        print(colors[num]) # colors[num]을 입력해라(해당 번째의 colors변수의 리스트 순서에 해당하는 값을 꺼내라). # colors[0]이라고 적어도 되지만 그러면 0으로 계속 값이 고정되어 colors[]괄호 속에 숫자가 변할 수가 없다.
        num = num + 1 # 그리고 아래식을 만족하고 다시 while로 올라가라. # num이 2가 될때까지 수행한다.
print('끝')

print()

print('if 블럭 내에 while문을 써보자구~')
import time # 시간을 불러오는 함수를 쓴다.
print ('a')
time.sleep(5) # 위에 꺼를 하고 5초동안 쉬다가 그 후에 시행한다.
print('b')

sw = input('폭탄 스위치를 누를까요?[Y/N]', ) # .. 만약 내가 Y, y도 N, n도 아닌 다른 걸 누른다면? else로간다.
if sw == 'Y' or sw == 'y':
    count = 5
    #pass # 수행할 능력이 없을 때 pass를 적어준다. 안하면 error가 뜬다.
    while 1 <= count:
        print('%d초 남았어요' %count) # = print(f"{count}초 남았어요")
        time.sleep(2)
        count = count - 1
    print('쾅!!! 뿌와왕! 뿌수수수슈ㅠ...')

elif sw == 'N' or sw == 'n':
    print('작업취소')

else:
    print('y또는 n을 누르시오')

'''# 주석다는 법은 우물정자도 있지만  ~ 로 큰따옴표 3개를 함께 써서 주석을 달 수도 있다.'''


print()

# 3. continue, break - 그냥 지나칠 때 continue, 갑자기 확 종료해야할 때, break를 쓴다.

print('\ncontinue / break')
a = 0
while a < 10: # a = 0이라 while문 조건에 충족한다. 다음 문장 진행
    a = a + 1 # a = 0 부터 집어넣어서 10미만까지 반복 
    if a == 7 : break # 반복문 무조건 탈출한다. ... # a =  0  1  2  3  4  5  6  끝
    if a == 5 : continue # 아래 문을 무시하고 while로 이동한다.  ... # a = 0  1  2  3  4  6  7  8  9 
    print(a) # ... a =  0  1  2  3  4  6    
print('끝')

print()

print('\n 키보드로 정수를 입력 받아 홀수, 짝수 출력(무한 반복)')
while True: # 조건이 없기에 무한 수행이 가능하다.
    mysu = int(input('확인할 정수 입력(예:5)', ))
    if mysu == 0 :
        print('프로그램 종료')
        break # while문은 조건이 거짓이 될때까지 계속 반복하는거다. 중간에 끊어주려면 break를 사용한다
    elif mysu % 2 == 0 :
        print(f'{mysu} : 짝수')
    elif mysu % 2 == 1 :
        print(f'{mysu} : 홀수')

print('끝')

print()

# 4. 반복문 for
# 일반형 자료는 while, 집합형 자료는 for를 이용해 반복문을 쓴다.












