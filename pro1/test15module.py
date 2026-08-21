# 현재 모듈은 다른 package에 있는 모듈의 멤버를 사용해
# 실행을 통해 어떤 결과를 확인할 수 있는 실행파일!!
# 실행파일은 > python 파일명.py  <== 이파일은 main 모듈이다.
# test15.py가 main 모듈로 여기로 불러올거다.

print('사용자 정의 모듈( : 내가 필요한 함수를 직접 만듬)작성 후 호출 연습')

imsi = 100 
print('------------------경로 지정 방법1 : import 모듈명-----------------------')

import pack1.mymod1
print(dir(pack1.mymod1)) # dir() : 사용가능한 모듈의 멤버(함수)들(목록들)이 보인다.
print(pack1.mymod1.__file__) # 경로명 및 파일명 확인할 때 쓰임
print(pack1.mymod1.__name__) # 모듈명을 확인할 때 쓰임

# test15.py보다 같은 경로면 패키지 없이 부를 수 있고 하위 경로면 pack1. 해서 부른다. 상위 경로는 부를 수 없다(중요)

list1 = [1, 2]
list2 = [3, 4, 5] # 하위 경로인 mymod1.py에 합을 구하는 함수를 저장해둠
pack1.mymod1.listHap(list1, list2) # ([1, 2], [3, 4, 5])

'''
def listHap(*ar):
    print(ar)
    if __name__ == '__main__' :    ... 수행안됨 ... 메인모델에서 수행한 것이 아니기 때문
        print('나는 메인 모듈이야.')
'''

if __name__ == '__main__' :   # ... 수행안됨 ... 메인모델에서 수행한 것이 아니기 때문 
    print('나는 메인 모듈이야.')

# mymod1.py는 메인 모듈이 아니라서 수행이 안됬지만 여기서 직접 지정해주니 수행이 되었다.

print('\n -----------------------경로 지정 방법2 : from 모듈명 impor 모듈방법, ...---------------------------')
from pack1.mymod1 import kbsFunc   
kbsFunc()

from pack1.mymod1 import mbcFunc, tot
mbcFunc()
print('tot : ', tot) 

from pack1.mymod1 import kbsFunc as 케이비에스별명 # kbsFunc as 케이비에스별명 = kbsFunc의 함수명을 케이비에스별명으로 바꿈
케이비에스별명() # 호출명도 바뀌게 됨 # 가독성을 위해서 as + 별명으로 써도 된다.

print('\n -------------------------경로 지정 방법3 : import 하위패키지...(여러개 있을 수 있다.), 모듈명-----------------------------')
import pack1.subpack.sbs
pack1.subpack.sbs.sbsManse() # 패키지명을 모두 써주고 sbsManse()라는 함수를 적어줌
import pack1.subpack.sbs as 난별명이야 # 경로에 별명을 세워 줄 수 있다. pack1.subpack.sbs를 '난별명이야'로 바꾸고 '난별명이야'모듈안의 sbsManse()함수를 부른다.
난별명이야.sbsManse()

from pack1_other import mymod2
imsi = mymod2.Hap(3,4) # momod2.Hap()에 return이 있기 때문이다.
print(imsi)

from pack1_other.mymod2 import Cha as chachacha
print(chachacha(5,2)) # return한 값을 print로 찍는다.


print('\n -------------------------경로 지정 방법4 : 경로(path)설정이 된 폴더에 모듈이 저장된 경우-----------------------------')
# 경로가 설정된 어느 폴더에 내가 지정한 파일(mymod3)를 넣었기에 이젠 경로를 적을 필요가 없다. 그냥 모듈명만 적어주면 그 모듈 경로까지 적을 번거로움 없이 쓸 수 있따.
# envs - myprojet - lib에 mymod3를 넣음.. 이제부턴 경로를 적어줄 필요가 없다.
import mymod3
print(mymod3.Gop(4,5)) # .을 찍으면 이젠 그곳에 함수도 나온다

import numpy
print(numpy.mean([3,5,7,9]))

# 전문가들이 만들어 둔 모듈을 알아보자
