# [1단계] 대립가설과 귀무가설 설정 
#              = "두 집단 간 평균의 차이는 존재한다/존재하지 않는다." 
#              그때 독립변수는 범주형이고 종속변수는 연속형이다. 독립변수가 하나라면 '단일표본 t검정'이고
#              2개라면 '독립 표본 t검정'을 쓴다.
#              독립변수(범주형) : 
#              종속변수(연속형) : 

# [2단계] 두 집단, 각 집단의 평균 구하기
#        "두 개"의 집단에 대한 표본 자료를 조사한 것이므로 "독립 표본 t검정을 사용한다!"

# [3단계] "정규성"과 "등분산성" 확인 
#             선행조건1) 정규성 확인 - 두 집단이 각각 정규분포를 따라야한다.
#                        - shapiro test
#                        - histplot (정규성 시각화 방법1)
#                        - Quantitle-Quantitile plot(Q-Q plot) (정규성 시각화 방법2)
#                             그때 정규성을 만족(O) ->  two-sample t-test(모수검정) 
#                                  정규성을 만족(X) ->  Mann-whitney-test(비모수검정)
#             선행조건2) 등분산성 확인 : 두 집단의 분산이 같다는 가정이 필요하다. = 등분산성
#                        from scipy.stats import levene, bartlett
#                        # levene : 정규성과 상관없이 사용가능하고 이상치에 민감하다. 
#                                   하지만 어떤 분포도 사용이 가능하다.
#                        # bartlett : 정규성이 있을 때만 사용하고 이상치에 덜 민감하다. 
#                                     대신 정규분포일 때만 사용가능하다.
#                        levene_stat, leven_p = levene(male, female)
#                        print('p값 : ', leven_p)
#                        그때 등분산성을 만족(O)  ->  two_sample = stats.ttest_ind(male, female, equal_var=True)
#                             등분산성을 만족(X)  ->  two_sample = stats.ttest_ind(male, female, equal_var=False)

# [4단계]. 어느 가설을 기각하고 채택할 것인지 결정한다.

#----------------------------------------------------------------------------------------------------------------

# 예제1) 어느 음식점의 매출과 날씨 자료를 이용해 강수 여부에 따른 매출액 평균의 차이 검정
# "이번 예제의 핵심은 데이터가 2개 이상 주어졌을 때 해당 데이터를 공통된 열로 만들어 하나로 합치는 것이다!!"" 
# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여 강수 여부에 따른 매출액의 평균에 차이가 있는지 검정한다.

# 두 집단 : 강수량이 있을 때, 맑을 때
# 매출 데이터 : tsales.csv (강수량이 있을 때)
# 날씨 데이터 : tweather.csv (맑을 때)

# [1단계] : 가설 설정
# 귀무가설 : 
# 대립가설 : 

# [2단계] : 두 집단, 각 집단의 평균 구하기(그 전에 두 집단의 데이터를 하나로 합치기)
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

print('결측치 확인 : ', data.isnull().sum())
# 그리고 저 4개의 열에 대한 데이터에서 결측지를 확인한다.
# 결과 : 
# YMD      0
# AMT      0
# maxTa    0
# sumRn    0

# 독립표본 t검정
# print(data['sumRn'] > 0) # 강수량이 있으면 True

# 칼럼 추가 : rain_yn < "강수량이 있으면 1, 없으면 0"
# <방법1>
# data['rain_yn'] = (data['sumRn'] > 0).astype(int)
# print(data.head())
# 결과 : 
#         YMD     AMT  maxTa  sumRn  rain_yn
# 0  20190514       0   26.9    0.0        0
# 1  20190519   18000   21.6   22.0      "1" -> 해당 날짜에 비가 옴
# 2  20190521   50000   23.8    0.0        0
# 3  20190522  125000   26.5    0.0        0
# 4  20190523  222500   29.2    0.0        0
# print()

# ** print(True * 1, ' ', False * 1)
# 결과 :  1     0  ...  즉, True와 False가 연산에 참여하면 1과 0의 값을 가진다.
# 여기서 우리는 비가 오면 True, 비가 오지 않으면 False라고 본다.

# <방법2>
data['rain_yn'] = (data.loc[:, ('sumRn')] > 0) * 1
# data.loc[:, ('sumRn')] > 0  ... 이게 bool값으로 True나 False를 반환한다. 그 값에 * 1을 하면 True나 False값에 대하여 1과 0이 부여된다.
print(data.head())
# 결과 : 
#         YMD     AMT  maxTa  sumRn  rain_yn
# 0  20190514       0   26.9    0.0        0
# 1  20190519   18000   21.6   22.0        1
# 2  20190521   50000   23.8    0.0        0
# 3  20190522  125000   26.5    0.0        0
# 4  20190523  222500   29.2    0.0        0

# 데이터 분포 box plot으로 시각화
sp=np.array(data.iloc[:, [1,4]]) # AMT, rain_yn
print(sp)
# 전체 DataFrame이 조회됨

tg1 = sp[sp[:, 1] == 0, 0] # 집단1 : 강수 없을 때 매출액
tg2 = sp[sp[:, 1] == 1, 0] # 집단2 : 강수 없을 때 매출액
print(tg1[:3])
# 결과 : [     0  50000 125000]
print(tg2[:3])
# 결과 : [ 18000 274000 318000]

print('tg1 : 강수 없을 때 매출액 평균 : ', np.mean(tg1))
# 결과 : 761040.25
print('tg2 : 강수 없을 때 매출액 평균 : ', np.mean(tg2))
# 결과 : 757331.52

# 위 결과를 그래프로 보여줘~
plt.boxplot([tg1, tg2], meanline=True, showmeans=True, notch=True)
plt.show()

# [3단계] : 정규성과 등분산성 확인
# 3-1. 정규성 확인
print(len(tg1), ' ', len(tg2))
# 결과 : 236   92
print(stats.shapiro(tg1).pvalue)
# 결과 : 0.0560506373373866
print(stats.shapiro(tg2).pvalue)
# 결과 : 0.8827503186867454
# 해석 : 정규성을 만족한다.

# 3-2. 등분산성 확인
print(stats.levene(tg1, tg2).pvalue)
# 결과 : 0.7123452333011152
# 해석 : 등분산성을 만족ㅎ나다.

# [4단계] : 결과 해석
print(stats.ttest_ind(tg1, tg2, equal_var=True))
# 결과 : TtestResult(statistic=np.float64(0.10109828602924716), pvalue=np.float64(0.9195345877221959), df=np.float64(326.0))
# p값(0.919534) > 유의수준(0.05)
# 해석 : 수집된 데이터는 우연히 발생한 데이터로 대립가설은 기각하고 귀무가설을 유지한다.