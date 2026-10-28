# 이원 분산 분석
# 가설검정 -> 분산분석 -> 상관분석 -> 회귀분석

# 이원분산분석(two-way ANOVA)-------------------------------
# 독립변인의 수가 두 개 이상일 때 집단 간 차이가 유의한지를 검증하는데 사용한다.
# 상호작용효과(Interaction Effect) : 한 변수의 변화가 결과에 미치는 영향이 다른지

# 실습) : 독의 종류와 처치방법에 따라 실험동물의 평균 생존시간에 차이가 있는지 검증

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import scipy.stats as stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv", index_col = 0)
# 첫번째 열(index 0)을 DataFrame의 인덱스로 사용

print(data.head(3))
print(data.shape)
# 결과 : 
#      time  poison  treat
#   1  0.31     1      A
#   2  0.45     1      A
#   3  0.46     1      A
# (48, 3)

# 데이터 설명
# - poison : 독의 종류 (3개 수준)
# - treat  : 처치방법 (4개 수준)
# - time   : 독에 노출된 실험동물의 생존시간
#
# 독 3종류 × 처치방법 4종류 = 12개 조합 ... 교호작용은 12개의 조합이 된다.
# 각 조합에서 실험동물 4마리 관측 → 총 48개 자료
# 독이 퍼지는 시간이 아니라 '생존시간'을 분석함

# [주효과 가설 1 : 독의 종류] - 요인1
# 귀무(H0) : 독의 종류에 따른 평균 생존시간은 모두 같다.
# 대립(H1) : 독의 종류에 따른 평균 생존시간 중 적어도 하나는 다르다.

# [주효과 가설 2 : 처치방법] - 요인2
# 귀무(H0) : 처치방법에 따른 평균 생존시간은 모두 같다.
# 대립(H1) : 처치방법에 따른 평균 생존시간 중 적어도 하나는 다르다.

# 각각의 요인마다 다시 요인이 존재한다.

# 큰 요인이 2개로 설정될때 교호작용이 생긴다. 
# [교호작용 가설]
# 귀무(H0) : 독의 종류와 처치방법 간 교호작용은 없다.
# 대립(H1) : 독의 종류와 처치방법 간 교호작용은 있다.
# 교호작용이 있다는 의미 : 처치방법에 따른 생존시간 차이가 독의 종류에 따라 달라짐

# 주효과 : 각각의 독립변수에 따라 종속변수의 평균이 달라지는가?
# 교호작용 : 한 독립변수에 따른 평균 차이가 다른 독립변수의 수준에 따라 달라지는가?


# 요인별 표본 수 확인
print("독 종류별 표본 수 : ", data.groupby('poison').size())
print("처치방법별 표본 수 : ", data.groupby('treat').size())
print("독 종류 x 처치방법 = ", data.groupby(['poison', 'treat']).size())
# 독 종류 x 처치방법 =  poison  treat
#                1       A        4
#                        B        4
#                        C        4
#                        D        4
#                2       A        4
#                        B        4
#                        C        4
#                        D        4
#                3       A        4
#                        B        4
#                        C        4
#                        D        4
# dtype: int64
# 모든 조합에서 표본 수가 4로 동일하다 = 균형적으로 설계되었다.

print("\n 요인별 기술 통계")
print("독 종류별 생존 시간 : ", data.groupby('poison')['time'].agg(['count', 'mean', 'std']))
print("처치방법별 생존 시간 : ", data.groupby('treat')['time'].agg(['count', 'mean', 'std']))
# 결과 : 
# 독 종류별 생존 시간 :          count      mean       std
#                      poison                           
#                        1        16     0.617500   0.209428
#                        2        16     0.544375   0.289366
#                        3        16     0.276250   0.062276

# 결과 : 
# 처치방법 별 생존시간    :     count      mean       std
#                       treat                           
#                         A       12   0.314167    0.102288
#                         B       12   0.676667    0.320832
#                         C       12   0.392500    0.167013
#                         D       12   0.534167    0.219440

# 이원분산분석 ------------------
model = ols('time ~ C(poison) * C(treat)', data = data).fit()
# = 모델이 만들어짐
# * : 주효과 + 교호작용
result = anova_lm(model, typ=2)
print("\n 이원분산분석 : \n", result)
# 결과 : 
#                        sum_sq     df           F         PR(>F)
# C(poison)            1.033013    2.0   23.221737   3.331440e-07
# C(treat)             0.921206    3.0   13.805582   3.777331e-06
# C(poison):C(treat)   0.250138    6.0    1.874333   1.122506e-01
# Residual             0.800725   36.0         NaN            NaN

# 해석 
p_poison = result.loc['C(poison)', 'PR(>F)'] 
p_treat = result.loc['C(treat)', 'PR(>F)']
p_interaction = result.loc['C(poison):C(treat)', 'PR(>F)']
alpha = 0.05

if p_poison < alpha:
    print("독 종류 : 귀무가설 기각 : 독의 종류에 따라 평균 생존 시간에는 유의미한 차이가 있다")
else:
    print("독 종류 : 귀무가설을 기각하지 못함 : 독의 종류에 따른 평균 생존시간 차이가 유의하다는 근거가 부족하다.")

if p_treat < alpha:
    print("처치 방법 : 귀무가설 기각 : 처치 방법에 따라 평균 생존시간에 유의한 차이가 있다.")
else: 
    print("처치 방법 : 귀무가설을 기각하지 못함 : 처치 방법에 따른 평균 생존시간 차이가 유의하다는 근거가 부족하다.")

if p_interaction < alpha:
    print("교호작용 : 귀무가설 기각 : 처치 방법의 효과는 독의 종류에 따라 다르다.")
else: 
    print("교호작용 : 귀무가설을 기각하지 못함 : 처치 방법의 효과가 독의 종류에 따라 달라진다는 통계적 근거가 부족하다.")


# 사후검정(Post-hoc test)
print("\n 독 종류별 사후 검정")
tkResult1 = pairwise_tukeyhsd(endog=data['time'], groups=data['poison'], alpha=alpha)
print(tkResult1)

tkResult1.plot_simultaneous(xlabel="평균생존시간", ylabel="독 종류")
plt.title('독의 종류별 생존시간')
plt.show()
plt.close()

print("\n 처치방법 별 사후 검정")
tkResult2 = pairwise_tukeyhsd(endog=data['time'], groups=data['treat'], alpha = alpha)
print(tkResult2)

tkResult2.plot_simultaneous(xlabel='평균생존시간', ylabel='처치방법')
plt.title('처치방법별 생존시간')
plt.show()
plt.close()

