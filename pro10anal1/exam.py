import numpy as np
import pandas as pd
from pandas import Series, DataFrame

from pandas import DataFrame
data = {"a": [80, 90, 70, 30], "b": [90, 70, 60, 40], "c": [90, 60, 80, 70]}

df = pd.DataFrame(data)
print(df)


df.columns = ['국어', '영어', '수학']
print(df)

print(df['수학'])
# print(data)

# print(data.mean())

# print("\n\n-------------------------------")

# import pymysql 
# import pandas as pd
# import numpy as np
# import sys

# def main():
#     CONFIG = {"host": "127.0.0.1", "user": "root", "passwd": "123", "db": "test", "port": 3306, "charset": "utf8" }

#     conn = pymysql.connect(**CONFIG)
#     cursor = conn.cursor()
#     # DB와 소통하기 위한 연결 객체 생성

#     sql = """
#         select jikwonno, jikwonpay, gogekno  
#         from jikwon outer join gogek 
#         on jikwon.jikwonno = gogek.gogekno
#         where 
#     """
#     cursor.execute(sql)
#     # 내가 원하는 데이터를 DB에서 내 컴퓨터의 RAM으로 가져왔다.

#     # sql문을 통해 DB에서 RAM으로 데이터를 들고와서 DataFrame으로 저장하였다.
#     df = pd.DataFrame(cursor.fetchall(), columns = ['jikwonno', 'jikwonpay', 'gogekno'])


#     # 1. 담당 고객이 없는 직원의 수
#     # print()

#     # 2. 연봉 평균
#     print(np.mean(df.jikwonpay))

#     # 3. 표준편차
#     print(np.std(df.jikwonpay))
    

# if __name__ == "__main__":
#     main()

