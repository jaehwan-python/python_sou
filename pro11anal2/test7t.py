# 이번엔 t-test이다.

# 집단 간 차이분석 : 평균 또는 비율 차이를 분석
# : 모집단에서 추출한 표본 ㅈ어보를 이용하여 모집단의 다양한 특성을 과학적으로 추론할 수 있다.

# t-test의 종류 
# 1. 단일 표본 t검정
# 2. 독립 표본 t검정
# 3. 대응 표본 t검정

# <단일 표본 t검정>
# 정규분포의 표본에 대한 기대값을 조사하는 검정방법이다.
# 예상 평균값과 표본 자료 간에 평균의 차이를 검정한다
# 독립변수 : 범주형
# 종속변수 : 연속형
# 하나의 집단에 대한 표본 평균이 예측된 평균(모집단)과 같은지 여부를 확인

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 실습1 - "과거 5년간 에이콘 교육센터 2층의 교육생(남성 집단)의 평균적인 키를 검정해보자"(단일 표본 t검정)

# 단일 표본 t-검정 : 하나의 표본집단 평균이 특정기준값(모집단의 가설평균)과 통계적으로 유의한 차이가 있는지 검정한다.

# 귀무가설 : 해당 집단의 평균 키가 177이다. (모수) ... 지난 5년간의 결과로 정립된 하나의 귀무가설
# 대립가설1 : 해당 집단의 평균 키가 177이 아니다.(양측 검정)
# 대립가설2 : 해당 집단의 평균 키가 177보다 크다/작다.(단측 검정)

one_sample = [167.0, 182.7, 169.7, 176.8, 180.0]
print(np.array(one_sample).mean())
# 결과 : 175.24
# 결과가 175.24인 경우 177.0과 차이가 있는가?

# 모수의 평균값이 177인 경우
result = stats.ttest_1samp(one_sample, popmean=177.0)
#                         (    데이터,  모수의 평균값)
print(result)
# 결과 : TtestResult(statistic  = -0.587758298576131,  pvalue  =  0.5882740309252297,   df = 4)
# 해석 : 유의수준0.05 < pvalue=0.5882740 ... 귀무가설 채택
print()

# 모수의 평균값이 160인 경우
result2 = stats.ttest_1samp(one_sample, popmean=160.0)
# 모수의 평균값을 177.0에서 160.0으로 바꿈.
print(result2)
# 결과 : TtestResult(statistic = np.float64(5.089452539943346),   pvalue = np.float64(0.0070341428137976605),   df = np.int64(4))
# 해석 : 유의수준 0.05 >  pvalue=0.026787 ... 귀무가설 기각.

# 그림으로 보자
sns.displot(one_sample, bins=10, kde=False, color='skyblue', edgecolor='black')
plt.axvline(np.mean(one_sample), color = 'green', linestyle = '-', label='표본평균')
plt.axvline(177, color = 'red', linestyle = '--', label='가설평균 177cm')
plt.title("교육생 키 분포")
plt.xlabel("키(cm)")
plt.ylabel("빈도(명)")
plt.legend()
plt.show()
