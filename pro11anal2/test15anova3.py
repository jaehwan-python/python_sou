# 예제1) 어느 음식점의 매출과 날씨 자료를 이용해 온도에 따른 매출액 평균의 차이 검정
# "이번 예제의 핵심은 데이터가 2개 이상 주어졌을 때 해당 데이터를 공통된 열로 만들어 하나로 합치는 것이다!!"" 
# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여 온도에 따른 매출액의 평균에 차이가 있는지 검정한다.

# 세 집단 : 추움, 보통, 날씨
# 매출 데이터 : tsales.csv (강수량이 있을 때)
# 날씨 데이터 : tweather.csv (맑을 때)

# [1단계] : 가설 설정
# 귀무가설 : 온도에 따른 매출액의 평균에 차이가 없다.
# 대립가설 : 온도에 따른 매출액의 평균에 차이가 있다.

# [2단계] : 세 집단, 각 집단의 평균 구하기(그 전에 두 집단의 데이터를 하나로 합치기)
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

pd.set_option('display.max_columns', None)

# Data1. 매출 데이터 읽기
sales_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv", dtype = {'YMD' : 'object'})
print(sales_data.head(2))
print(sales_data.info())
# dtype = {'YMD' : 'object'}) : 뒤에서 나올 데이터의 공통 컬럼을 찾아서 연결하기 위해 ymd를 object로 바꾸었다.
#                               그러면 이제 뒤에 나올 데이터가 가지고 있는 object이라는 열과 공통 이름의 열을 가지기에
#                               두 열을 하나로 합칠 수 있다.
# 결과 : 
#        "YMD"    AMT  CNT
# 0  20190514      0    1
# 1  20190519  18000    1

# 결과 : 
#      Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0    YMD     328 non-null   int64 --> object 로 바뀌었따.(ymd값이 object로 바뀜!)
#  1    AMT     328 non-null   int64
#  2    CNT     328 non-null   int64
print()

# Data2. 날씨 데이터 읽기
wt_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv")
print(wt_data.head(2))
print(wt_data.info())
# 결과 : 
#    stnId         "tm"  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  2018-06-01   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  2018-06-02   23.4   17.6   30.1    0.0    4.5    2.0    0.0

# 결과 : 
#  #   Column  Non-Null Count  Dtype  
# ---  ------  --------------  -----  
#  0   stnId   702 non-null    int64  
#  1   tm      702 non-null    str    
#  2   avgTa   702 non-null    float64
#  3   minTa   702 non-null    float64
#  4   maxTa   702 non-null    float64
#  5   sumRn   702 non-null    float64
#  6   maxWs   702 non-null    float64
#  7   avgWs   702 non-null    float64
#  8   ddMes   702 non-null    float64
print()

# 날짜별 매출 데이터로 두 데이터를 합쳐야 한다.
# head(2)의 데이터를 보아라.
# sales_data는 "YMD"가 20190514이고, wt_data는 "tm"이 2018-06-01로 날짜끼리 동일하다. 하지만 형태가 동일하지 않기에 형태를 맞추어준다.
# 그래서 우리는 wt_data의 tm에서 '-'를 뺄 것이다.
wt_data.tm = wt_data.tm.map(lambda x:x.replace("-",""))
print(wt_data.head())
# 이제 wt_data에서 tm열의 날짜에 "-"를 빼주어서 sales_data의 YMD의 데이터값들과 동일한 형태가 되었따.
# = 그래서 이제 두 DataFrame을 기준되 pk로 합칠 수 있다.
print()

# 두 데이터 병합!!**중요 ㅈㄴ ㅈ우웅요!
frame = sales_data.merge(wt_data, how='left', left_on='YMD', right_on="tm")
# sales_data를 왼쪽에 두고 YMD를 기준으로 wt_data를 공통된 열인 "tm"을 기준으로 붙여라
# = 왼쪽의 YMD와 오른쪽의 tm 값이 같은 행을 연결하라
print(frame.columns)
# 결과 : Index(['YMD', 'AMT', 'CNT', 'stnId', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn', 'maxWs', 'avgWs', 'ddMes'], dtype='str')
# 각 열에 대한 종류

print(frame.head(3), " ", len(frame))
# 결과 : 
#         YMD    AMT  CNT  stnId        tm  avgTa  minTa  maxTa  sumRn  maxWs  
# 0  20190514      0    1    108  20190514   19.6   12.9   26.9    0.0    4.1   
# 1  20190519  18000    1    108  20190519   19.4   17.9   21.6   22.0    2.7   
# 2  20190521  50000    4    108  20190521   17.2   11.7   23.8    0.0    5.9   

# 이제 데이터 분석을 위해서 YMD, AMT, maxTa, sumRn의 열이 필요하다.
data = frame.iloc[:, [0, 1, 7, 8]]
print(data.head())
# 결과 : 
#         YMD     AMT  maxTa  sumRn
# 0  20190514       0   26.9    0.0
# 1  20190519   18000   21.6   22.0
# 2  20190521   50000   23.8    0.0
# 3  20190522  125000   26.5    0.0
# 4  20190523  222500   29.2    0.0

print('결측치 확인 : ', data.maxTa)
# 그리고 저 4개의 열에 대한 데이터에서 결측지를 확인한다.
# 결과 : 
# YMD      0
# AMT      0
# maxTa    0
# sumRn    0


# -- 규보형꺼|
#%%
# 어느 음식점의 매출과 날씨 자료를 이용해 온도에 따른 매출액 평균의 차이 검정 -------------------------
# 세 집단 : 추움, 보통, 더움
# 두 집단 : 강수량이 있을 때, 맑을 때

# 매출 데이터 : tsales.csv
# 날씨 데이터 : tweather.csv

# 귀무 : 온도에 따라 매출액의 평균에 차이가 없다.
# 대립 : 온도에 따라 매출액의 평균에 차이가 있다.

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

pd.set_option("display.max_columns", None)

# 매출데이터 읽기
sales_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv", dtype={"YMD" : "object"})    # int -> object로 변환해 읽기
print(sales_data.head(2))
print(sales_data.info())    # 328 * 3

wt_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv")
print(wt_data.head(2))
print(wt_data.info())       # 702 * 9


print()
# sales_data : YMD 20190514, wt_data : tm 2018 - 06-01으로 병합을 위해
wt_data.tm = wt_data.tm.map(lambda x  : x.replace("-",""))
print(wt_data.head())
#    stnId          tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  2018-06-01   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  2018-06-02   23.4   17.6   30.1    0.0    4.5    2.0    0.0

print()
# 두 데이터 병함
frame = sales_data.merge(wt_data, how="left", left_on = "YMD", right_on="tm")
print(frame.columns)

# Index(['YMD', 'AMT', 'CNT', 'stnId', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn', 'maxWs', 'avgWs', 'ddMes']
print(frame.head(3)," ",len(frame))     # 328

data = frame.iloc[:,[0,1,7,8]]      # YMD AMT maxTa sumRn
print(data.head())
print("결측치 확인 :", data.isnull().sum())

plt.boxplot(data.maxTa)
plt.show()
