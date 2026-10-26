# pandas를 이용한 file i/o
import pandas as pd

pd.set_option('display.max_columns', None)
# pandas의 옵션으로 모든 컬럼을 전부 다 ...없이 모두 보여주게 한다.

df = pd.read_csv('test.csv')
# csv 파일이 같은 경로에 있으면 가져와라.
print(df)

# csv파일을 그대로 읽어 dataframe의 형태로 만들어 준다.
print(df, type(df))
# 결과 : DataFrame

print()


# web에서 데이터를 가져와보자
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex1.csv")
print(df, type(df))
print()

# 1. ex1.csv 불러오기
df = pd.read_table("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex1.csv", sep=',', skip_blank_lines=True) 
# ,를 기준으로 자른다
# skip_blank_lines=True : 칼럼명, 데이터 앞에 공백 제거
print(df, type(df))
# 그냥 하나의 문자열로만 반환하였다.
print()

# 2. ex2.csv 불러오기1
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv")
print(df)
# 첫번째 행을 제목 행으로 사용한다.
print()

# 3. ex2.csv 불러오기2
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv", header = None)
print(df)
print()
# 첫번째 행을 제목 행으로 사용한다.

# 4. ex2.csv 불러오기3
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv", header = None, skiprows=1)
print(df)
print()

# 5. ex2.csv 불러오기4
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv", header = None, names = ['a', 'b', 'c', 'd', ' e'])
print(df)
print()

# 6. ex3.txt불러오기
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt")
print(df)
print()

# 7. ex3.txt 불러오기2
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt", sep=r'\s+') # 정규표현식 가능
# 정규표현시에는 r꼭 붙이는 습관 들이기
print(df)
print()

# 8. ex3.txt 불러오기3
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt", sep=r'\s+', skiprows=[1,3]) # 정규표현식 가능
# skiprows = range(1,3)과 동일
# skiprows = lamda x:x in [1, 3]
print(df)
print()

# 9. data_fwt.txt 불러오기
df = pd.read_fwf("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/data_fwt.txt", header = None, widths = (10, 3, 5), names = ('날짜', '상호', '가격'), encoding = 'utf8')
print(df)
print(df['날짜'].head(2))
print(df.iloc[:, 0].tail(0))
print()
# 고정된 문자 폭으로 열 구분
# utf 대신 cp949나 euc-kr로 써도 된다.

print("\n 'Chunk' : 대량의 데이터를 부분씩(일정크기) 메모리로 읽어 처리하는 단위")
# 대용량 자료 전체로딩 시 메모리 초과 오류 발생 방지 목적
# 스트리밍 방식(일부만 순차 처리)으로 읽기, 분산처리의 효과
# 여러 번 반복해서 읽어야하므로 속도는 느리다. - 시간을 체크하기 위해서 import time을 해보자

import time
import numpy as np
n_rows = 100000
data = {
    'id' : range(1, n_rows + 1),
    'name' : [f'Student_{i}' for i in range(1, n_rows + 1)],
    'score1' : np.random.randint(50, 101, size = n_rows),
    'score2' : np.random.randint(50, 101, size = n_rows)
}
df = pd.DataFrame(data=data)
print(df)

csv_fname = 'pandas5student.csv'
df.to_clipboard()

df.to_csv(csv_fname, index=False)
# dataframe을 파일로 저장하였다.
# 이제 이 실행하면 해당 csv파일이 생겼다.

print('-------------------------------------')
# chunk 연습을 해보자.
# csv 파일 읽기 : 전체 한 번에 읽기
start_all = time.time()
df_all = pd.read_csv(csv_fname)
average_all_1 = df_all['score1'].mean()
average_all_2 = df_all['score2'].mean()
print(f'전체 처리 score1 평균 : {average_all_1:3f}')
print(f'전체 처리 score2 평균 : {average_all_2:3f}')
time_all = time.time() - start_all

# < chunk로 읽기 > : 
chunk_size = 1000
# chunk 1000개를 기준으로 끊어서 자료를 읽는다.
total_score1 = 0
total_score2 = 0
total_count = 0

start_chunk_total = time.time()
for i, chunk in enumerate(pd.read_csv(csv_fname, chunksize=chunk_size)):
    start_chunk = time.time()
    
    # chunk 처리 중 첫번째 학생 정보를 출력
    first_student = chunk.iloc[0]
    print(f"chunk {i + 1} 첫번째 학생 : ID = {first_student['id']}, 이름 = {first_student['name']}",
            f"score1={first_student['score1']}, score2 = {first_student['score2']}")
    
    total_score1 += chunk['score1'].sum()
    total_score2 += chunk['score2'].sum()
    total_count += len(chunk)

    end_chunk = time.time()
    elasped = end_chunk - start_chunk
    print(f"    처리 시간 : {elasped:7f}") # 청크 단위 처리 시간

time_chunk_total = time.time() - start_chunk_total
average_chunk1 = total_score1 / total_count
average_chunk2 = total_score2 / total_count


print('\n 처리 결과')
print(f" 전체 학생 수 : {total_count}")
print(f" score1 총합 : {total_score1}, 평균 : {average_chunk1:3f}")
print(f" score2 총합 : {total_score2}, 평균 : {average_chunk2:3f}")
# :3f  =  소수점 셋째자리까지

print(f" 전체 한번에 처리한 시간 : {time_all:7f}초")
print(f" chunk로 처리한 총 시간 : {time_chunk_total:7f}초")

# 전체 한번에 처리한 시간과 chunk로 처리한 총 시간을 비교하면 chunk가 더 시간이 오래 걸린다(평균적인 시간은 같지만). 그럼에도 불구하고 
# chunk를 사용하는 이유는
# 방대한 양의 데이터를 부.분.적.으로 RAM에 끌어오기 때문에 chunk를 쓴다.
# 즉, 메모리 절약 차원에서 이를 사용한다.
# 결국 'chunk'란 긴 텍스트 데이터를 AI가 처리하기 좋은 작은 의미 단위(보통 512~1024 토큰 등)의 조각으로 나눈 것을 말한다.



# < chunk 처리 시간 시각화 >
# 아직 안배웠지만 함 해보자.

# pip install koreanize-matplotlib를 터미널 창에 이력하여 matplotlib를 설치해준다.
import koreanize_matplotlib
import matplotlib.pyplot as plt

labels = ['전체 한번에 처리', '청크로 처리']
times = [time_all, time_chunk_total]

plt.figure(figsize = (6,4))
bars = plt.bar(labels, times, color = ['skyblue', 'red'])
for bar, time_val in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width() / 2, \
            bar.get_height(), f'{time_val:3f}초', \
            ha = 'center', va = 'bottom', fontsize = 10)
plt.ylabel('처리시간(초)')
plt.grid(linestyle = '--')
plt.tight_layout()
plt.show()
