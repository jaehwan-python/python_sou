# 매번 새로운 파일이 open하고 close가 닫을 때마다 귀찮다. close 쓰기가 너무 귀찮귀찮 ... 

# with 구문 - 파일 입출력에서 종종 사용
# with 표현식 as 객체변수:
#       실행문

# 파일 입출력에서는 보통 이런 형태로 사용
# with open("파일명", "모드", encoding='utf-8' as 파일 객체)
# 블럭 종료시 파일 자동 close됨

try:
    # 파일 저장
    with open('ftest3.txt', mode='w', encoding='utf-8') as fobj1: # ftest3.txt을 파일로 저장하고 fobj1변수로 저장
        fobj1.write('파이썬에서 문서 저장\n')
        fobj1.write('with구문은 ~ \n')
        fobj1.write('파일 작업 종료 시 자동close됨\n') # 우리가 따로 close하지 않아도 알아서 닫힌다.

    # 파일 읽기
    with open('ftest3.txt', mode = 'r', encoding = 'utf-8') as fobj2:
        print(fobj2.read())

    # close를 안써도 되기에 강력 추천한다.

    print('저장 완료')

except Exception as e:
    print('err원인 : ', e)




print('-----------------------------------')
print('\n\n 피클링(Pickling) : 일반 객체 및 복합 객체 파일 입출력')

import pickle # 피클 함수를 호출.. 이제 쓸 수 있다.

try:
    dictData = {'Tom' : '111-1111', '길동' : '222-2222'} # 이런객체를 파일로 저장가능하다.
    listData = ['마우스', '모니터']
    tupleData = (dictData, listData)

    with open('hello.dat', mode='wb') as fobj3: # mode = 'wb' : 텍스트 파일이 아닌 바이너리로 저장하였다.
        pickle.dump(tupleData, fobj3) # 저장 : pickle.dump(대상, 파일 객체)
        pickle.dump(listData, fobj3)

    print('특정 객체를 파일로 저장')


    print('\n피클 객체 읽기')
    with open('hello.dat', mode ='rb') as fobj4:
        a, b = pickle.load(fobj4) # pickle.load(파일 개체) # 객체를 저장했고 읽을 때는 load를 사용한다.
        print('a = ', a)
        print('b = ', b)

        c = pickle.load(fobj4)
        print('c = ', c)


except Exception as e2:
    print('피클링 연습 중 오류 발생의 원인은 : ', e2)






