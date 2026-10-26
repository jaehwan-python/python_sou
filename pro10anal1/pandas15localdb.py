# local db (sqlite를 사용) 연동 후 DataFrame에 자료 저장
# = DB에 데이터 넣기(sqlite3)

import sqlite3
import pandas as pd

sql = "create table if not exists extab(product varchar(10), maker varchar(10), weight real, price integer)"
# table이 없어서 내장 DB에 새로 table을 만들었다.
# 4개의 행이 있다.

conn = sqlite3.connect(":memory:")
# ram에만 존재하도록 하는 휘발성이 있다.
# 는 성질을 선언한다.

conn.execute(sql)
# sql과 내 vs code를 연결함

data = [('mouse', 'samsung', 12.5, 5000), ('keyboard', 'lg', 52.5, 35000)]
isql = "insert into extab values(?,?,?,?)"
# 내가 정한 data값을 extab이라는 table에 넣어준다.

conn.executemany(isql, data)
# data에 복수개의 자료가 오기 때문에 executemany가 온다.

data1 = ('pen', 'monami', 5.0, 1200)
conn.execute(isql, data1)

conn.commit()

cursor = conn.execute("select * from extab")
rows = cursor.fetchall()
for a in rows:
    print(a)

# 결과 : 
#       ('mouse', 'samsung', 12.5, 5000)
#       ('keyboard', 'lg', 52.5, 35000)
#       ('pen', 'monami', 5.0, 1200)

print()

print("----------- rows를 DataFrame에 저장 --------")
# < 방법1 >
df1 = pd.DataFrame(rows, columns=['product', 'maker', 'weight', 'price'])
print(df1)
# 결과 : 
#           product    maker   weight   price
#       0     mouse  samsung    12.5     5000
#       1  keyboard       lg    52.5    35000
#       2       pen   monami     5.0     1200

print(df1.describe())
print()

# < 방법2 >
df2 = pd.read_sql("select * from extab", conn)
print(df2)
# 결과 : 
#           product    maker   weight   price
#       0     mouse  samsung    12.5     5000
#       1  keyboard       lg    52.5    35000
#       2       pen   monami     5.0     1200

print(pd.read_sql("select count(*) as 건수 from extab", conn))
# 결과 : 건수   3

# db의 자료를 dataframe에 넣어보았다.

# 이번에는 dataframe의 자료를 db에 넣어보자.
print('\n ------------- DataFrame의 자료를 db(table)에 저장 ----------')
data = {
    'product' : ['연필', '볼펜', '지우개'],
    'maker'   : ['모나미', '모나미', '모나미'],
    'weight'  : [2.3,  3.6,  4.0], 
    'price'   : [1000, 2000, 3000]
}

frame = pd.DataFrame(data)
# dict가 DataFrame이 되었다.

frame.to_sql("extab", conn, if_exists='append', index=False)
# to_sql은 저장을 의미한다.
# dataframe  ->  sqlite3 DB
# 에 넣어주는 sql문 작성

df3 = pd.read_sql("select * from extab", conn)
print(df3)

cursor.close()
conn.close()

# 결과 : 
#             product    maker     weight   price
#       0       mouse   samsung      12.5    5000
#       1    keyboard         lg     52.5   35000
#       2         pen     monami      5.0    1200
#       3        연필      모나미      2.3    1000
#       4        볼펜      모나미      3.6    2000
#       5       지우개     모나미      4.0    3000