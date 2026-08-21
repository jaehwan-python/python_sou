'''
클래스는 새로운 타입을 만들어 자원 공유가 목적
데이터와 기능을 하나로 단위로 묶어 새로운 사용자 정의 타입을 만들고, 
객체마다 상태를 가지게 하거나 경우에 따라 공용자원을 공유할 수 있다.

모든 가수의 대표노래를 하나씩 저장할 수 없어 type으로 저장해준다.
'''


'''
class Singer:
    title_song = "아 대한민국"

    def sing(self):
        msg = "노래는"
        print(msg, self.title_song)
'''

# import test22Singer
# bts = test22Singer.Singer()

from test22Singer import Singer # 외부 모듈의 멤버 로딩

bts = Singer()
bts.sing()
print(type(bts))

bts.title_song = 'Stay for a night'
bts.co = '빅히트 엔터테인먼트'
bts.sing()
print('bts 소속사 : ', bts.co)

print('------------------------------------------------------')

ive = Singer()
ive.sing()
print(type(ive))
# print('ive 소속사 : ', ive.co) #...존재하지 않아 error가 나온다.
print()
Singer.title_song = "긴 여름은 가고~~~~"
ive.sing() # 노래는 긴 여름은 가고~~~~
bts.sing() # 노래는 Stay for a night

niceGroup = ive
niceGroup.sing() 
