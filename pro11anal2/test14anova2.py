# One-way ANOVA(일원분산분석)으로 그룹 간 평균 차이를 검정
# 검정통계량 = f값

# 실습1) 서초구에 있는 GS 편의점 3개 지역(서초동, 반포동, 양재동)에 근무하는 알바생의 급여의 차이에 대해서 구해보자.

# [1단계] : 가설설정
# 귀무가설 : GS편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 없다.
# 대립가설 : GS편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 있다.

# [2단계] : 평균구하기
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import koreanize_matplotlib
import urllib.request

uri = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3.txt"
# 읽기 방법1
# data = pd.read_csv(uri, header=None)
# print(data.values)

# 읽기 방법2
data = np.genfromtxt(urllib.request.urlopen(uri), delimiter = ",")
print(data)
print(data.shape)

# 3개 그룹에 월급 자료 얻기 - 평균
group1 = data[data[:,1] == 1, 0]
group2 = data[data[:,1] == 2, 0]
group3 = data[data[:,1] == 3, 0]
print(group1, ' ', np.mean(group1))
print(group2, ' ', np.mean(group2))
print(group3, ' ', np.mean(group3))
# 결과에 따른 해석 : 3개 그룹에 차이가 나긴 하는데 ... 이걸 차이가 난다해 만다해..?

# [3단계] : 정규성과 등분산성 확인
# 1. 정규성 확인
print(stats.shapiro(group1).pvalue)
print(stats.shapiro(group2).pvalue)
print(stats.shapiro(group3).pvalue)
# shapiro 결과, 모두 p값이 유의수준(0.05)보다 크므로 모든 집단이 정규성을 만족한다.
# ... 표본이 작거나 정규성을 위반하고 있다면 비모수 검정인 Kruskal-Wallis test를 사용한다.
# print(stats.kruskal(group1, group2, group3))
# 이런식으로 Kruskal-Wallis test(비모수검정)을 사용한다.

# 2. 등분산성 확인 -> levene, bartlett 2가지 방법이 존재하였다. 이 중에서 levene를 많이 쓴다.
print(stats.levene(group1, group2, group3).pvalue)
# 결과 : 0.045846
print(stats.bartlett(group1, group2, group3).pvalue)
# 결과 : 0.3508
# 두 등분산성을 확인했을때 하나라도 만족하면 등분산성이 만족한다고 하고 넘어간다.
# 만약 anova에서 등분산성을 만족하지 않은 경우, 보편적으로 Welch's Anova를 사용하거나 혹은 Brown Forstythe Anova를 쓴다. 
# 혹은 원래의 데이터를 변환하는 방법이 있다. : log변환 /  제곱근 변환 / 표준화
# 즉, 
# 등분산성을 만족하지 못한 경우 사용하는 방법 
# 1. Welch's Anova
# 2. Brown Forstythe Anova
# 3. 데이터 변환 - log 변환
#               - 제곱근 변환
#               - 표준화

print()
# [4단계] : ANOVA 분석
# 일원분산분석 방법1 : anova_lm
df = pd.DataFrame(data=data, columns=['pay', 'group'])
print(df)
lmodel = ols('pay ~ C(group)', data = df).fit()
# group이 "범주형"일때는 C를 앞에 붙인다.
print(anova_lm(lmodel, typ=1))
#             df        sum_sq      mean_sq         F    PR(>F)
# ---------------------------------------------------------------
# C(group)   2.0  15515.766414  7757.883207  3.711336  0.043589
# Residual  19.0  39716.097222  2090.320906       NaN       NaN
# ---------------------------------------------------------------
# type=1,2,3에 따라서 DF모양이 달라진다.
# 해석 : p값이 유의수준보다 작으므로 귀무가설을 기각한다.

# 일원분산분석 방법2 : f_oneway()
f_stat, pv = stats.f_oneway(group1, group2, group3)
print("f_stat : ", f_stat)
# 결과 : 3.711335
print("p-value : ", pv)
# 결과 : 0.043589
# anova_lm을 사용하든 f_oneway 둘 다 p값으로 0.043589를 보여준다. 
# 해석 : 편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 있따.

# 그러면 각 집단별 차이는 얼만큼 나는 것인가...? = 사후검정
# 앞에서 ANOVA를 통해 3개 집단의 차이가 남을 알 수 있었다. 딱 거기까지.
# 그러면 서초동, 반포동, 양재동 지역 간 평균 차이를 알기 위해서는 어떻게 할까? = 사후검정

df['region'] = df['group'].map({1:'서초동', 2:'반포동', 3:'양재동'})
# 지역명을 추가함

from statsmodels.stats.multicomp import pairwise_tukeyhsd
# tukResult = pairwise_tukeyhsd(endog=df.pay, groups=df.group)
tukResult = pairwise_tukeyhsd(endog=df.pay, groups=df.region) # groups = df['region']
print(tukResult)
# 결과 : 
# group1     group2      meandiff      p-adj        lower       upper      reject
# ---------------------------------------------------------------------------------
#  반포동     서초동      -60.1806     0.0355     -116.619     -3.7421        True
#  반포동     양재동       -38.625     0.3215    -104.8404     27.5904       False
#  서초동     양재동       21.5556     0.6802     -43.2295     86.3406       False
# ----------------------------------------------------------------------------------
# Reject는 해당 두 그룹간의 차이가 있다와 없다를 나타낸다. meandiff는 두 집단의 평균의 차이이다.

# 시각화
tukResult.plot_simultaneous(xlabel='급여평균', ylabel='지역평균')
plt.show()


