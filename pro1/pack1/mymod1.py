# projects/pro1/pack1/mymod1.py
# 변수, 함수를 가진다(외부 모듈에서 사용하기 위한 모듈). 실행은 안한다.

tot = 123

def listHap(*ar):
    print(ar)
    if __name__ == '__main__' :
        print('나는 메인 모듈이야.')

# 우린 지금까지 한개의 파일 안에서 여러개의 함수를 수행했다
# 이제부턴 외부 파일을 실행파일(main 모듈)안으로 가져올거다.
# 지금 보고 있는 것도 메인파일에 대한 외부 파일이다!. 그래서 여기 파일(mymod1)에서 실행하는 것은 아니다.
    
def kbsFunc():
    print('대한민국 대표방송')

def mbcFunc():
    print('문화방송')

# 지금 3개의 함수 아무도 부르는 스테이트 먼트가 없다