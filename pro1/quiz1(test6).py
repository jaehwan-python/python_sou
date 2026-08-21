#문제1. 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 합을 출력
print('문제1 : 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 합을 출력하시오.')
# 1 ~ 100 사이의 정수 ㅇ
# 3의 배수이나 2의 배수가 아닌 수 ㅇ
# 그 수들의 합 ㅇ

a = 1
b = 0 
while a <= 100: # 1 ~ 100 사이의 정수 선택 
    if a % 3 == 0 and a % 2 != 0: # 3의 배수이거나 2의 배수가 아닌 수 선택
        print(a, end = ' ')
        b = b + a # 그 수들의 합 = 3의 배수이거나 2의 배수가 아닌 수(1) + 3의 배수이거나 2의 배수가 아닌 수(2) + ... 
    a = a + 1 # while 반복문에 대해서 a가 100이 될 때까지 반복
print('합은', b)

print()



#문제2. 2~5까지의 구구단 출력
print('문제2 : 2 ~ 5단까지의 구구단')
# 구구단 체계
# 곱하는 수(1~19)와 곱해지는 수(2~5) 구분하기
# 연결하기
# 출력하기

c = [2, 3, 4, 5]

c = 1
d = 0
while c <= 19:
    while d <= 19:

        d = d + 1  # 

print(c)

# 문제3. 1 ~ 100사이의 정수 중 "짝수는 더하고, 홀수는 빼서" 최종결과 출력
print(f'문제3. : 1 ~ 100사이의 정수 중 짝수는 더하고, 홀수는 빼서 최종결과 출력') 
# 1 ~ 100사의 정수 선택
# 짝수끼리 더함.
# 홀수끼리 뺌.
# 각각의 값 출력

jak = 1
hol = 1
while jak <= 100 and hol <= 100:
    if a % 2 == 0 :
        a = a + 1

'''
문제1) 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 합을 출력

문제2) 2 ~ 5 까지의 구구단 출력

문제3) 1 ~ 100 사이의 정수 중 “짝수는 더하고, 홀수는 빼서” 최종 결과 출력

문제4) -1, 3, -5, 7, -9, 11 ~ 99 까지의 모두에 대한 합을 출력

문제5) 1 ~ 100 사이의 숫자 중 각 자리 수의 합이 10 이상인 수만 출력
예) 29 → 2 + 9 = 11 (출력)

문제6) 1부터 시작해서 누적합이 처음으로 1000을 넘는 순간의 숫자와 그때의 합을 출력
힌트: 언제 멈출지 미리 모름 → while 적합

문제7) 구구단을 출력하되 결과가 30을 넘으면 해당 단 중단하고 다음 단으로 이동

문8) 1 ~ 1000 사이의 소수(1보다 크며 1과 자신의 수 이외에는 나눌 수 없는 수)와 그 갯수를 출력
힌트: 이 문제는 반복이 두 단계다. 2부터 1000까지 하나씩 검사한다. 각 숫자마다 소수인지 확인한다.
그래서 while 안에 while 구조가 필요하다.


continue 연습 문제

문제1) 1부터 50까지의 숫자 중 3의 배수는 건너뛰고 나머지 수만 출력하라

문제2) 1부터 100까지 출력하되 4의 배수, 6의 배수는 건너뛴다. 그 외의 수 중 5의 배수만 출력하고 그들의 합도 출력하라'''

# 문1) 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 합을 출력
i=0
sum=0
while i<100:
    i+=1
    if i%2==0:continue
    if i%3==0:continue
    print(i)
    sum=sum+i
else:
    print(sum)

i=0
total=0

while i <= 100:
    if i % 3 == 0 and i % 2 != 0:
        print(i, end = ' ')
        total += i
    i += 1

print(f"합은 {total}")

# 문2) 2 ~ 5 까지의 구구단 출력
dan = 2
while dan <= 5:
    j = 1
    while j <= 9:
        print(f'{dan} * {j} = {dan*j}', end =' ')
        j += 1
    print()
    dan += 1


# 문3) 1 ~ 100 사이의 정수 중 “짝수는 더하고, 홀수는 빼서” 최종 결과 출력
i = 1
sum = 0
while i <= 100:
    if i%2==0:
        sum=sum+i
    else:
        sum=sum-i
    i+=1
print(f'최종결과 = {sum}')

# 문4) -1, 3, -5, 7, -9, 11 ~ 99 까지의 모두에 대한 합을 출력
n = 1
sign = -1 # 곱하면 부호가 바뀜
total = 0

while n <= 99:
    value = sign * n
    total = total + value # total의 누적값

    sign *= -1
    n += 2
print(total)

''' 이런 방법도 된다!!
i = -1
sum = 0
while abs(i) <= 99:
    sum=sum+i
    if i<0:
        i-=2
    else:
        i+=2
    i*=-1

print(sum)
'''

#문5) 1 ~ 100 사이의 숫자 중 각 자리 수의 합이 10 이상인 수만 출력
#예) 29 → 2 + 9 = 11 (출력)
i=10
while i<=100:
    str_i=str(i)
    hap=sum((int(str_i[0]),int(str_i[1])))
    if hap>=10:
        print(f'{str_i}일 때 {hap}')
    i+=1

num = 1
while num <= 100:
    temp = num
    digit_sum = 0

    while temp > 0:
        digit_sum += temp % 10
        temp //= 10
    if digit_sum >= 10:
        print(num, end = ' ')
    
    num += 1

print()

# 문6) 1부터 시작해서 누적합이 처음으로 1000을 넘는 순간의 숫자와 그때의 합을 출력
# 힌트: 언제 멈출지 미리 모름 → while 적합
s = 0
i = 1
while s < 1000:
    s += i
    i += 1

print("수자:", i-1)
print("합:", s)

# 문7) 구구단을 출력하되 결과가 30을 넘으면 해당 단 중단하고 다음 단으로 이동
dan = 2
while dan <= 9:
    i = 1
    while i <= 9:
        result = dan * i
        if result > 30:
            break
        print(dan, "*", i, "=", result)
        i += 1
    print()
    dan += 1

# 문8) 1 ~ 1000 사이의 소수(1보다 크며 1과 자신의 수 이외에는 나눌 수 없는 수)와 그 갯수를 출력
# 힌트: 이 문제는 반복이 두 단계다. 2부터 1000까지 하나씩 검사한다. 각 숫자마다 소수인지 확인한다.
# 그래서 while 안에 while 구조가 필요하다.
num = 2
count = 0
while num <= 1000:
    i = 2
    is_prime = True
    while i < num:
        if num % i == 0:
            is_prime = False
            break
        i += 1
    if is_prime:
        print(num, end = ' ')
        count += 1
    num += 1

print('갯수 : ', count)

# continue 연습 문제
# 문제1) 1부터 50까지의 숫자 중 3의 배수는 건너뛰고 나머지 수만 출력하라
print()
i = 1
while i <= 50:
    if i % 3 == 0:
        i += 1
        continue
    print(i, end= ' ')
    i += 1

# 문제2) 1부터 100까지 출력하되 4의 배수, 6의 배수는 건너뛴다. 그 외의 수 중 5의 배수만 출력하고 그들의 합도 출력하라
print()
i = 1
total = 0
while i <= 100:
    if i % 4 == 0 or i % 6 == 0 or i % 5 != 0: # 5의 배수가 아닌 녀석도 건너 뛴다.
        i += 1
        continue # 출력이 안되게 함.
    print(i)
    total += i
    i += 1

print('total : ', total)  