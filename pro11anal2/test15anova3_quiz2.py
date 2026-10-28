# [ANOVA 예제 2]
# DB에 저장된 buser와 jikwon 테이블을 이용하여 
# 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 있는지 검정하시오. 
# 만약에 연봉이 없는 직원이 있다면 작업에서 제외한다.

# 귀무 : 연봉 평균에 차이가 없다.
# 대립 : 연봉 평균에 차이가 있다.

import pandas as pd
import numpy as np 
import pymysql
import scipy.stats as stats
import matplotlib.pyplot as plt

config = {"host": "127.0.0.1", 
        "user": "root", 
        "passwd": "123",
        "db": "test", 
        "port": 3306, 
        "charset": "utf8"
}

conn = pymysql.connect(**config)
# [1단계] : 데이터 조회 및 결측값 제외
try:
    df = pd.read_sql(
        "select jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay "
        "from jikwon inner join buser on jikwon.busernum = buser.buserno "
        "where jikwonpay is not null", conn
    )
finally:
    conn.close()

# [2단계] : 부서별 집단 구분 및 유의수준 설정
names = ['총무부', '영업부', '전산부', '관리부']
df = df.loc[df['busername'].isin(names)].copy()
gr1 = df.loc[df['busername'] == '총무부', 'jikwonpay']
gr2 = df.loc[df['busername'] == '영업부', 'jikwonpay']
gr3 = df.loc[df['busername'] == '전산부', 'jikwonpay']
gr4 = df.loc[df['busername'] == '관리부', 'jikwonpay']
groups = [gr1, gr2, gr3, gr4]
alpha = 0.05

# [3단계] : 기초 통계 및 이상치 후보 확인
print(df.groupby('busername')['jikwonpay'].agg(['count', 'mean', 'median', 'std']))
# 수염 밖의 점은 이상치 후보이며 자동으로 삭제하지 않는다.
plt.boxplot(groups, showmeans=True, meanline=True)
plt.xticks([1, 2, 3, 4], names)
plt.title('부서별 연봉 분포')
plt.xlabel('부서')
plt.ylabel('연봉')
plt.show()

# [4단계] : 독립성 및 정규성 확인
# 관측값의 독립성은 자료 수집 구조를 통해 확인한다.
# Shapiro 귀무가설 : 해당 집단의 자료가 정규분포를 따른다.
# p <= 0.05 : 정규성 기각 / p > 0.05 : 정규성을 기각하지 못함
for name, group in zip(names, groups):
    print(name, 'Shapiro p값:', stats.shapiro(group).pvalue)
# 기존 결과에서는 총무부와 영업부의 정규성이 기각되었다.
# 분석 방법은 표본 크기, 분포 모양, 이상치도 함께 고려하여 선택한다.

# [5단계] : 등분산성 참고 확인 및 분석 방법 선택
# Levene 귀무가설 : 네 집단의 모집단 분산이 모두 같다.
print('Levene p값:', stats.levene(*groups).pvalue)
# Kruskal-Wallis는 등분산 검정을 통과해야 사용할 수 있는 검정이 아니다.
# 이 예제에서는 정규성 점검 결과를 참고하여 Kruskal-Wallis를 선택한다.
# 정규성을 기각하지 못한 집단도 포함하여 네 부서를 모두 비교한다.

# [6단계] : Kruskal-Wallis 검정 및 가설 판단
# ANOVA의 평균 동일성 가설과 구분한다.
# 귀무가설 : 네 부서의 연봉 분포가 같다.
# 대립가설 : 적어도 한 부서의 연봉 분포가 다르다.
# 분포 모양과 퍼짐이 비슷할 때 위치(중앙값) 차이로 해석할 수 있다.
result = stats.kruskal(*groups)
print('H 통계량:', result.statistic)  # F값 대신 H값 사용
print('p값:', result.pvalue)
if result.pvalue <= alpha:
    print('귀무가설 기각: 적어도 한 부서의 연봉 분포가 다르다는 근거가 있다.')
else:
    print('귀무가설을 기각하지 못함: 부서별 연봉 분포가 다르다는 근거가 부족하다.')
    # 평균이 같다는 사실을 증명한 것은 아니다.

# [7단계] : 유의한 경우 사후검정
# 집단 쌍별 Mann-Whitney U 검정에 Holm 다중비교 보정을 적용한다.
# 각 쌍의 귀무가설 : 두 집단의 분포가 같다.
from itertools import combinations
from statsmodels.stats.multitest import multipletests

if result.pvalue <= alpha:
    comparisons = []
    raw_pvalues = []
    for i, j in combinations(range(len(groups)), 2):
        pair_result = stats.mannwhitneyu(groups[i], groups[j], alternative='two-sided')
        comparisons.append((names[i], names[j]))
        raw_pvalues.append(pair_result.pvalue)
    reject, adjusted_pvalues, _, _ = multipletests(raw_pvalues, alpha=alpha, method='holm')
    posthoc = pd.DataFrame(comparisons, columns=['부서1', '부서2'])
    posthoc['원래 p값'] = raw_pvalues
    posthoc['Holm 보정 p값'] = adjusted_pvalues
    posthoc['귀무가설 기각'] = reject
    print(posthoc)
else:
    print('Kruskal-Wallis 결과가 유의하지 않아 사후검정을 생략한다.')
