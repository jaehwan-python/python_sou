'''
재귀함수(Recusive Function) : 함수가 자기 자신을 호출 - 반복 처리가 가능하다.

'''
#1
def countDown(n):

    countDown(n) # ...자기가 자기 자신을 부르면 자기함수에서 못빠져나온다.

#2
def countDown(n):
    if n == 0 :
        print('완료')
        return # ... 함수를 빠져나온다.
    else :
        print(n, end = ' ')
    countDown(n-1)  # 재귀

countDown(5)


print()

#3
print("-----------1부터 n까지의 정수의 합 구하기-------------")

def totFunc(n):
    if n == 1 :
        print('완료')
        return 1  # ... 함수를 빠져나온다.
    
    return n + totFunc(n-1) # 재귀함수
# totFunc를 빠져나가면서 n을 반환함. + 재귀함수의 매개변수에 n-1값을 받음.
# 호출하면서는 연산하지 않고 거슬러 올라가면서 연산한다. 계단식으로 연산한다. 
result = totFunc(10)
print('result : ', result)

print()

print('-----------------------------------------------------')

print('팩토리얼')
'''팩토리얼(계승) : 1부터 어떤 자연수 n까지의 모든 자연수를 차례대로 곱하는 것이다.
'''
# 3! = 3 x 2 x 1

def facFunc(a):
    if a == 1: 
        return 1 
    print(a)
    return a * facFunc(a-1)

result2 = facFunc(5)
print('result2 : ', result2) # for문이나 while문을 쓰면 5000을 넣어도 연산이 가능하지만 재귀함수는 계속 메모리를 만드는 것이기에 깊은 계산이 힘들다


'''
5 x facFunc(4)
    4 x facFunc(3)
        3 x facFunc(2)
            2 x facFunc(1)
이때는 연산하지 않는다.
'''

'''
저기서 거슬러 올라가면서 연산한다.
'''
