# 단일 모집단의 평균에 대한 가설검정(One Sample t-test)

# 실습예제2)
# A중학교 1학년 1반 학생들의 시험결과가 담긴 파일을 읽어 처리(국어점수 평균 검정)

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 실습예제1)
# a중학교 1학년 1반 학생들의 시험결과가 담긴 파일을 읽어 처리(국어점수 평균검정)

# 귀무가설 : 학생들의 국어점수의 평균은 80이다.(지금까지 알려진 평균)
# 대립가설1 : 학생들의 국어점수의 평균은 80이 아니다.
# 대립가설2 : 학생들의 국어점수의 평균은 80보다 크거나 작다.

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/student.csv")
print(data.head(3))
print(data.describe())
print(data['국어'].mean())
# 결과 : 72.9
# **그때 평균인 80과 72.9가 차이가 있는거야 없는거야..?**
# ... 이를 검정해주는 것이 one-sample t-test이다.
# 그때 정규성 검정을 만족하면 one-sample t-test이다.


print(len(data))
# 결과 : 20
# 30행이 넘으면 '중심극한정리'에 의해 정규성을 따른다고 가정.
# 중심극한정리 : 모집단의 원래 분포형태와 상관없이 표본의 크기(n)가 충분히 커지면 표본평균들의 분포가 정규분포에 가까워진다.
# 표본크기(n)의 조건 : 일반적으로 표본의 크기가 n >= 30 정규분포에 충분히 가까워진다고 본다.
# 30개가 넘지 않으므로 "정규성 검정"을 선행한다.
# 정규성 검정 : 데이터가 정규분포를 따르는지 검사하는 것
# 많은 통계기법들이 정규성검정을 기준으로 사용한다. 
# 정규성 검정 중 "샤피로-윌크 검정"으로 데이터가 정규분포를 따르는지 확인하는데 사용한다.
print(stats.shapiro(data["국어"])) # 국어의 정규성 검정
# 결과 : ShapiroResult(statistic=np.float64(0.8724170172545651), pvalue=np.float64(0.012959753376032153))
# 우리는 이 중 pvalue만 신경쓴다. p값 = 0.0129597
# alpha(0.05) > p값(0.0129597)
# "p값은 alpha(0.05)보다 커야 정규성을 따른다고 할 수 있다!!"
# 정규성을 만족하지 못함 ... p값은 alpha(0.05)보다 커야 정규성을 따른다고 할 수 있다!!

# a) 정규성을 만족한 경우 : ttest_1samp()수행
ttest_result = stats.ttest_1samp(data["국어"], popmean=80)
print(ttest_result)
# 결과 : TtestResult(statistic=np.float64(-1.3321801667713216), pvalue=np.float64(0.1985605182478525), df=np.int64(19))
# 해석 : a(0.05) < p값(0.19)
# "귀무가설을 채택한다."

# b) 정규성을 만족하지 못한 경우 대안 : wilcoxon-test
from scipy.stats import wilcoxon
wilcoxon_result = wilcoxon(data["국어"] - 80)
# 윌콕슨은 평균값을 빼준다.
print(wilcoxon_result)
# 결과 : WilcoxonResult(statistic=np.float64(74.0), pvalue=np.float64(0.39777620658898905))
# p값 0.39777이 나왔따.
# 해석 : a(0.05) < p값(0.3)
# "귀무가설을 채택한다. 즉 평균의 차이가 없다."

# 만약 표본 수가 크다면 그냥 ttest_1samp를 써도 된다.

# 결론 : 정규성은 부족하나 귀무가설 채택이라는 동일한 결론을 얻는다
# 먄약 표본 수가 크다면 그냥 ttest_1samp를 써도 된다.
# 보고서 작성시에는 "'shapiro-wilk'검정 결과 정규성 가정이 다소 위배되었으나 비모수검정(wilcoxon) 결과도 동일하므로 ttest_1samp결과를 신뢰할 수 있다"라고 명시한다.

print("-------------")
# 실습예제2)
# 여아 신생아 몸무게의 평균검정 수행 
# 여아 신생아의 몸무게느 ㄴ평균이 2800g으로 알려져왔으나 이보다 더 크다는 주장이 제기 됨
# 표본으로 여아 18명을 뽑아 체중을 측정하였다고 할 때 새로운 주장이 맞는지 검증
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/babyboom.csv")
print(data2.head(3))
# 결과 : 
#    time  gender  weight  minutes
# 0     5       1    3837        5
# 1   104       1    3334       64
# 2   118       2    3554       78

pd.set_option("display.max_columns", None)
print(data2.describe())
# 결과 : 
#               time     gender       weight      minutes
# count    44.000000  44.000000    44.000000    44.000000
# mean   1296.000000   1.590909  3275.954545   788.727273
# std     690.704561   0.497350   528.032458   416.066931
# min       5.000000   1.000000  1745.000000     5.000000
# 25%     792.750000   1.000000  3141.500000   482.750000
# 50%    1406.500000   2.000000  3404.000000   846.500000
# 75%    1918.500000   2.000000  3571.750000  1158.500000
# max    2355.000000   2.000000  4162.000000  1435.000000
print()

fdata = data2[data2.gender == 1]
# 결과 : 1:여아, 2:남아
#        time  gender  weight  minutes
#   0      5       1    3837        5
#   1    104       1    3334       64
#   5    405       1    2208      245
#   6    407       1    1745      247
#   12   814       1    2576      494
#   13   909       1    3208      549
#   15  1049       1    3746      649
#   16  1053       1    3523      653
#   21  1406       1    3430      846
#   22  1407       1    3480      847
#   23  1433       1    3116      873
#   24  1446       1    3428      886
#   28  1742       1    2184     1062
#   30  1825       1    2383     1105
#   36  2010       1    3500     1210
#   41  2217       1    3866     1337
#   42  2327       1    3542     1407
#   43  2355       1    3278     1435

print(fdata,' ', len(fdata))
# 결과 : 18

# 1. 평균 구하기 
print("여아 신생아 몸무게 평균 : ", np.mean(fdata.weight))
# 결과 : 3132.44

# 2. 표준편차 구하기
print("여아 신생아 몸무게 표준편차 : ", np.std(fdata.weight))
# 결과 : 613.787

# 이때 평균 2800과 실제 평균값 3132는 평균에 차이가 있는가? ... t-test로 검정!!

# < One sample t-test >
result2 = stats.ttest_1samp(fdata['weight'], popmean=2800)
print("result2 : ", result2)
# 결과 : TtestResult(statistic=np.float64(2.233187669387536), pvalue=np.float64(0.03926844173060215), df=np.int64(17))

# 해석1 (p값 사용) : 유의수준0.05 > p값0.039268이므로 귀무가설을 기각하고 대립가설을 채택한다.
# 해석2 (t분포표를 사용) : 
#                         t값 : 2.2331, alpha : 0.05, cv(임계값) : 1.740
#                         t분포표로 임계값을 얻고 임계값을 기준으로 t값이 채택역에 있는지 기각역에 있는지 판별한다 
#                         현재 t갑싱 임계값보다 크므로 오른쪽에 존재하무르 귀무가설을 기각하고 대립가설을 채택한다.

#                         임계값을 기준으로 검정통계량이 오른쪽에 있는지(바깥쪽) -> 기각역 ... 대립가설 채택
#                                                      왼쪽에 있는지(안쪽)     -> 채택역 ... 귀무가설 유지

print()

print("t-test 선행 조건으로 정규성을 확인(n < 30)...3가지 방법")

# 방법1 : 정규성 확인 방법1 : "shapiro test"
print(stats.shapiro(fdata['weight']))
# p값0.0179847 < 유의수준0.05
# 이므로 정규성을 만족하지 못함.

# 이런 정규성 만족여부를 그래프로 확인가능하다. 
# 방법2 : 정규성 확인 방법2 : "histplot"
sns.histplot(fdata['weight'], kde=True) 
# 왜곡된 데이터 분포를 확인할 수 있다. = 정규성을 가지지 않는 데이터 분포 양상을 보임
plt.show()
# 해당 그래프가 정규분포 그래프와 가까워야하는데 그러헥 보이지 않는다.
# = 즉, 이렇게 시각적으로 정규분포를 따르는지 따르지 않는지 확인할 수 있다.

# 방법3 : 정규성 확인 방법3 : "Quantitle-Quantitile plot(Q-Q plot)"
stats.probplot(fdata['weight'], plot=plt)
# Q-Q plot 상에서 잔차가 정규성을 만족 못하였다.
plt.show()
# 평균을 나타내는 추세선에서 마지막 값이 빠져나가고 있다.
# 값이 다시 돌아올지 안돌아올지 모른다. = 정규성을 만족하지 않는다.
# 그때 추세선(평균선)과 각 데이터값들의 차이를 "잔차"라고 한다.

# 정규성을 만족하지 못하였기 때문에 
# "wilcoxon 검정"을 사용한다.
result3 = wilcoxon(fdata['weight'] - 2800)
print("result3 : ", result3)
# 결과 : result3 :  WilcoxonResult(statistic=np.float64(37.0), pvalue=np.float64(0.03423309326171875))
# p값:0.03 > 유의수준0.05
# 해석 : p값이 0.05보다 작으므로 귀무가설을 기각한다.

# 핵심!!
# = " 정규성을 만족하면 t-test(모수검정)를 쓰고 정규성을 만족하지 못하면 wilcoxon검정(비모수검정)을 써라"

# 1. 대립가설과 귀무가설 설정 = "표본 데이터의 평균과 모집단의 평균(예상)은 차이가 있다(고정)/없다(고정)"
# 2. 표본 데이터에서 '평균'과 '표준편차' 구하기
# 3. 정규성 확인 : 표본 데이터와 모집단의 평균(예상)이 차이가 있는지 없는지 확인(3가지 방법)을 하기 위해 정규성을 확인해야함.
#                 - shapiro test
#                 - histplot
#                 - Quantitle-Quantitile plot(Q-Q plot)
#                 ** 정규성을 확인하는 이유 : 다음 과정에서 t검정을 할 때, 
#                                            t검정의 p값을 믿고 해석할 수 있는 조건인지 
#                                            확인하려고 정규성을 살펴보는 것이다.
# 4. 그때 정규성을 만족(O) ->  t-test(모수검정) 
#         정규성을 만족(X) ->  wilcoxon(비모수검정)
# 5. 어느 가설을 기각하고 채택할 것인지 결정한다.