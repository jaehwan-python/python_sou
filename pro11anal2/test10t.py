# 독립표본 t검정(independent two sample t-test)
# 실습) 두 가지 교육방법에 따른 평균시험 점수에 대한 검정 수행 two_sample.csv

# [1단계] : 대립가설과 귀무가설 설정
# 귀무가설 : 두 가지 교육방법에 따른 평균시험 점수에 차이가 없다.
# 대립가설 : 두 가지 교육방법에 따른 평균시험 점수에 차이가 있다.

# 독립변수(범주형) : method
# 종속변수(연속형) : score

# [2단계] : 평균 구하기
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/two_sample.csv")
# 외부 데이터 가져오기
print(data.head(3))
print(data['score'].isnull().sum())
# score에 대해서만 null값을 확인할 수도 있다!
print(data.isnull().any())
# 전체 데이터에서 true가 적힌 부분은 null로 볼 수 있다.

# "교육방법(method)"과 "점수(score)"만 분리해서보자
ms = data[['method', 'score']]
m1 = ms[ms['method'] == 1] # 교육방법1
m2 = ms[ms['method'] == 2] # 교육방법2
print(m1.head(3))
print(m2.head(3))

# "교육방법(method)"에서 "점수(score)"만 별도로 기억
score1 = m1['score']
score2 = m2['score']
print(score1.isnull().sum())
# 결과 : 0
print(score2.isnull().sum())
# 결과 : 2

# NaN처리? -> 삭제, 0또는 평균값으로 대체!!
score2 = score2.fillna(score2.mean()) # NaN을 평균으로 대체하였다


# [3단계] : 정규성과 등분산성 처리
# 선행조건1) 정규성 확인
print('score1의 정규성 : ', stats.shapiro(score1).pvalue)
print('score2의 정규성 : ', stats.shapiro(score2).pvalue)
# + 정규성 시각화도 해보자...
# 정규성 시각화 방법1 : histplot
import koreanize_matplotlib
# 한글깨짐 방지
plt.figure(figsize=(10, 5))
# 그래프 크기 지정

# 교육방법1
sns.histplot(score1, kde=True, color='red', alpha=0.5, label='교육방법1')

# 교육방법2
sns.histplot(score2, kde=True, color='red', alpha=0.5, label='교육방법2')

plt.xlabel('시험점수') # x축 이름
plt.ylabel('빈도')     # y축 이름

plt.legend() # = label이 보이게 함
plt.show()

# 정규성 시각화 방법2 : Q-Q plot
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
# 교육방법1
stats.probplot(score1, dist='norm', plot=ax[0]) # dist='norm' : 비교기준은 정규분포임을 명시함
ax[0].set_title('교육방법1')
ax[0].set_xlabel('이론적 분위수')
ax[0].set_ylabel("표본 분위수")
ax[0].grid()

# 교육방법2
stats.probplot(score2, dist='norm', plot=ax[1]) # dist='norm' : 비교기준은 정규분포임을 명시함
ax[1].set_title('교육방법2')
ax[1].set_xlabel('이론적 분위수')
ax[1].set_ylabel("표본 분위수")
ax[1].grid()
# = 추세선에 붙어있으니 이후 평균으로 수렴할 것으로 사료됨.
# = 정규분포를 만족함

plt.tight_layout()
plt.show()

# 선행조건2) 등분산성 확인
from scipy.stats import levene, bartlett
print('등분산 만족 여부 : ', levene(score1, score2).pvalue)
# 결과 : 0.456842711297761

# [4단계] : 결과 확인 
# 등분산성을 만족하기 때문에 two-sample t-test(equal_var = True)로 진행한다
# 만약 등분산성을 만족하지 않으면 two-sample t-test(equal_var = False) 진행한다
result = stats.ttest_ind(score1, score2, equal_var=True)
print('result : ', result)
# 결과 : TtestResult(statistic=np.float64(-0.19649386929539883), pvalue=np.float64(0.8450532207209546), df=np.float64(48.0))
# p값(0.84505) > 유의수준(0.05)
# 해석 : 귀무가설을 기각하고 대립가설을 채택한다. 즉, 두 가지 교육 방법에 따른 평균시험 점수에 차이가 없다.