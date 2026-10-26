# Maria DB의 자료를 내 RAM으로 가져와서 DataFrame형태로 만들어 두면 pandas 연산을 통해 해당 자료를 조작 및 연산이 가능하다.

# 원격 DB 연동 : jikwon 자료를 읽어 DataFrame에 저장

import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv

config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '123',
    'database' : 'test',
    'port' : 3306,
    'charset' : 'utf8'
}
# DB연동을 위한 데이터 셋 준비
# 원래는 .env파일에 만들어서 이를 저장하고 나중에 불러와서 사용한다. --- fetchall()

try:
    conn = pymysql.connect(**config)
    # ** : dict자료형을 받는다라는 뜻
    # 위에서 config를 dict형태로 받아줌

    cursor = conn.cursor()
    # DB를 연결

    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay
        from jikwon inner join buser on jikwon.busernum = buser.buserno
    """

    cursor.execute(sql)
    # 연결된 DB에 내가 원하는 데이터를 추출

    # for(jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay) in cursor:
    #     print(jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay)

    # < 이제 내 RAM으로 불러온 데이터를 DataFrame형태로 만들어준다 >

    # DB의 데이터를 RAM으로 가져왔다. 그리고 뽑은 데이터를 sql문으로 표현하였다. 이때 한번 sql문을 execute하면 사라진다.
    # 즉 이후에 작업을 하기 위해서는 다시 sql문을 호출해주어야 한다.

    # [방법1] : "jikwon자료 -> DataFrame 읽는 방법1" : DataFrame에 저장되었다.
    df1 = pd.DataFrame(cursor.fetchall(), columns = ['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwongen', 'jikwonpay'])
    print(df1.head(3))
    # maria DB에서 자료를 RAM으로 불러왔다. 그리고 RAM의 DataFrame에 넣어주었다.
    # 결과 :           jikwonno     jikwonname   busername   jikwonjik   jikwongen   jikwonpay
#               0         1           홍길동       총무부        이사         남        9900
#               1         2           한송이       영업부        부장         여        8800
#               2         3           이순신       영업부        과장         남        7900
    print('연봉의 총합 : ', df1['jikwonpay'].sum())

    print("---------- 이번에는 DataFrame의 자료를 csv 파일로 저장한다.--------------")
    cursor.execute(sql) 
    # 아까 위에서 cursor.execute(sql)을 해주었는데 지금 또 선언하는 이유?
    # 이미 위에서 불러와서 읽은 자료는 DataFrame에 한 행씩 처리 완료되어 RAM에는 자료가 모두 소진되었다.
    # 그래서 다시 읽기가 필요하다. 그래서 cursor.execute(sql)을 다시 넣어주었다.
    # 그러면 pandas16.csv에 값이 들어가게 된다.

    with open('pandas16.csv', mode='w', encoding = 'utf-8') as fobj:
        writer = csv.writer(fobj)
        # writer객체를 만들었다. 두 파일 사이를 오고 갈 객체이다.
        # maria DB의 데이터가 내 컴퓨터의 RAM으로 들어오게 된다. 그때 RAM으로 들어온 데이터는 한 줄 씩 읽으면서 들어간다. 하지만 이제는 다 읽어서 소진되었따. 즉, 다시 읽어주어야 한다.

        for row in cursor.fetchall():
            # fetchall : 실행한 조회결과를 모두 가져오기
            writer.writerow(row)

    # csv파일이 pandas16.csv에 들어가서 DataFrame에 저장되었다.
    dfcsv = pd.read_csv('pandas16.csv', header=None, names=['번호', '이름', '부서', '직급', '성별', '연봉'])
    print(dfcsv.head(3))
    # 결과 :    번호    이름   부서   직급  성별  연봉
#           0    1    홍길동  총무부  이사  남   9900
#           1    2    한송이  영업부  부장  여   8800
#           2    3    이순신  영업부  과장  남   7900


    # [방법2] :  "jikwon자료 -> DataFrame 읽는 방법2" : DataFrame에 저장되었다.
    print("\n\n")
    df2 = pd.read_sql(sql, conn)
    df2.columns = ['번호', '이름', '부서', '직급', '성별', '연봉']
    # sql문을 통해 가져온 데이터들에 대하여 컬럼명을 주어줌
    #  
    print(df2.head(3))
    print()
    
    print(df2[:3])
    print()

    print(df2[:-27])
    # 이 3가지는 모두 동일한 결과값을 가진다.

    print("\n\n ---------------------------------------------")

    # 1. 다양한 형태의 출력
    print('건수 : ', df2['이름'].count(), ' ', len(df2))
    print('부서별 인원수 : ', ' ', df2['부서'].value_counts())
    print('연봉 8000 이상 : ', df2.loc[df2['연봉'] >= 8000])

    # 2. 교차표 출력(성별, 직급별 인원 수)
    ctab = pd.crosstab(df2['성별'], df2['직급'], margins = True)
    print('교차표:\n', ctab)
    # 결과 :        직급  과장  대리  부장   사원  이사  All
    #       성별                          
    #       남             4     3     2     5     1     15
    #       여             2     4     1     8     0     15
    #       All            6     7     3    13     1     30

    # 3. 시각화
    print("직급별 연봉의 평균")
    jik_ypay = df2.groupby(['직급'])['연봉'].mean() 
    print(jik_ypay)
    # 결과 : 
    # 직급
    # 과장    7200.000000
    # 대리    5064.285714
    # 부장    8466.666667
    # 사원    3476.923077
    # 이사    9900.000000
    
    # = 직급별 연봉에 대한 평균
    print()

    # 시각화 할때 plt.pie()메서드를 이용한다.
    plt.pie(jik_ypay, explode = (0.2, 0, 0, 0.3, 0),
            labels=jik_ypay.index, shadow=True)
    plt.show()

    
except Exception as e:
    print('처리 오류 : ', e)

finally:
    cursor.close()
    conn.close()

# < 학습로드맵 >
# 'file'이나 'web' 혹은 'DB'의 데이터를 dict형태로 RAM으로 가져온다. 
# 그때 RAM의 데이터를 DataFrame형태로 변환한다. 
# (RAM에 있는 데이터(DataFrame)를 SSD에 저장할때 .csv파일 형태로 저장한다.)
# 그리고 우리는 RAM에 있는 DataFrame을 조작하고 다룬다.
# 그 때 그 DataFrame을 numpy와 pandas로 다루면서
# 기술통계/추론통계를 이용하여 데이터를 분석한다.!!

