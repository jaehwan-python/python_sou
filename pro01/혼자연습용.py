'''
a = 1
b = 2
c = 3
def kbs():
    a = 20
    b = 30
    def mbc():
        global c
        nonlocal b
        print('mbc 내의 a : {}, b :{}, c:{}'.format(a,b,c))
        c = 40
        b = 50
    mbc()
kbs()

*v1, v2, v3 = {1, 2, 3, 4, 5, 1, 2, 3, 4, 5}
print(v1)
print(v2)
print(v3)

print(list(range(1, 6, 2)))
'''

'''
year = 0
while  True: 
    yun_year = int(input('연도 입력'))
    if yun_year % 4 == 0:
        print(f'{yun_year}년은 윤년')
        if yun_year % 100 == 0:
            print(f'{yun_year}년은 평년')
            if yun_year % 400 == 0:
                print(f"{yun_year}년은 윤년")
            else:
                print(f'{yun_year}년은 평년')
        else:
            print(f'{yun_year}년은 윤년')
    else:
        print(f"{yun_year}는 평년")
        break
'''

dot = 1
star = 10

while star <= 10:
    print(star * '*', sep = '')
    star = star - dot

class Gugudan:
    def print_dan(self):
        dan = 3
        i = 1
        while dan <= 9:
            if dan % 2 == 1:
                result = dan * i
                print(result)
        dan = dan + 1



gugu = Gugudan()
gugu.print_data())