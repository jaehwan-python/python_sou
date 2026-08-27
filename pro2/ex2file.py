print("파일 처리 : 입출력")
import os # 운영체제(os)와 관련된 기능을 제공

try:
    print('-----파일 읽기-----')
    print(os.getcwd()) # C:\works\projects\pro2   # 현재 있는 파일(모듈)의 경로를 가르쳐 준다.

#   읽을 파일 C:\works\projects\pro2\ftest.txt
#    f1 = open(os.getcwd() + r'\ftest.txt', mode = 'r', encoding = 'utf-8')  # 외부 파일을 읽을 때 경로를 알려줘야함.mode는 읽기
#    f1 = open(r'C:\works\projects\pro2\ftest.txt', mode = 'r', encoding = 'utf-8')
#   위 두가지 statesment 모두 가능하지만 위에 statesment를 보면 os.getcwd()를 통해서 현재있는 내가 속해 있는 파일의 이름을 지정해준다. 그리고 우린 파일명만 적어주면 된다.

    f1 = open(os.getcwd() + r'\ftest.txt', mode = 'r', encoding = 'utf-8')
    print(f1)
    print(f1.read()) # 해당 파일을 읽음
    f1.close() # open하여 파일을 열고 작업을 하고 파일을 다시 닫는다.(권장) 

    print('-------새로운 파일을 만들고 파일에 값 저장--------')
    f2 = open(file = 'ftest2.txt', mode='w', encoding = 'utf-8') # w 이기에 새로운 파일을 만들어 저장한다. ftest2.txt가 pro2에 새로 생겼다.
    f2.write('내 친구들\n')
    f2.write('신기해, 이기자\n')
    f2.close()
    print('파일 저장 성공')

    print('--------파일에 값 추가--------')
    f3 = open(file = 'ftest2.txt', mode = 'a', encoding = 'utf-8')
    f3.write('\n사오정')
    f3.write('\n손오공')
    f3.write('\n저팔계')
    f3.close()
    print('파일 추가 성공')

    print('~~~~~~~~~~~~~~~~~')
    # ftest2.txt 읽기
    f4 = open(file = 'ftest2.txt', mode ='r', encoding = 'utf-8')
    print(f4.read())
    print('------')
    f4.close() # file open()이 있으면 무조건 닫아라close() ... 매번 close()를 쓰기 힘들다..ㅠㅠ
    
except Exception as e:
    print("처리 오류(원인) : ", e)

