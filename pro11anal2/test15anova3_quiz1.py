# 예제1)

# 빵을 기름에 튀길 때 네 가지 기름의 종류에 따라 빵에 흡수된 기름의 양을 측정하였다.
# 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 존재하는지를 분산분석을 통해 알아보자.
# 조건 : NaN이 들어 있는 행은 해당 칼럼의 평균값으로 대체하여 사용한다.

# 수집된 자료 :  
# kind quantity
# 1 64
# 2 72
# 3 68
# 4 77
# 2 56
# 1 NaN
# 3 95
# 4 78
# 2 55
# 1 91
# 2 63
# 3 49
# 4 70
# 1 80
# 2 90
# 1 33
# 1 44
# 3 55
# 4 66
# 2 77

# ------------------------------------------------------------------------------------------------------
# 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 존재하는지를 분산분석을 통해 알아보자.

# [1단계] : 가설설정
# 귀무가설 : 기름의 종류에 따라 흡수하는 기름의 평균에 차이는 없다.
# 대립가설 : 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 있다 
# 현재 4개의 집단이 존재

# [2단계] : 이상치와 결측값 확인하기
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import koreanize_matplotlib
import urllib.request

# 2-1. 데이터 읽기
data = pd.DataFrame({
    'kind': [1, 2, 3, 4, 2, 1, 3, 4, 2, 1, 2, 3, 4, 1, 2, 1, 1, 3, 4, 2],
    'quantity': [64, 72, 68, 77, 56, np.nan, 95, 78, 55, 91,63, 49, 70, 80, 90, 33, 44, 55, 66, 77]
})
# 주어진 데이터를 DataFrame으로 만들기

# 2-2. 결측값 처리
# 문제 조건에 따라 quantity 열의 전체 평균으로 결측값을 대체한다.
# 평균 = 결측값을 제외한 관측값의 합 / 결측값을 제외한 관측값의 개수
quantity_mean = data['quantity'].mean()
data['quantity'] = data['quantity'].fillna(quantity_mean)
print('결측값 대체에 사용한 평균:', quantity_mean)

# 2-3. 기름 종류별 IQR로 이상치 후보 확인
# Q1 = 제1사분위수(25%)
# Q3 = 제3사분위수(75%)
# IQR = Q3 - Q1

# 하한 = Q1 - 1.5 * IQR
# 상한 = Q3 + 1.5 * IQR
# "관측값 < 하한" 또는 "관측값 > 상한"이면 이상치로 분류한다.
# 집단마다 분포가 다를 수 있으므로 기름 종류별로 계산한다.
for kind, group in data.groupby('kind'):
    q1 = group['quantity'].quantile(0.25)
    q3 = group['quantity'].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = group.loc[
        (group['quantity'] < lower) | (group['quantity'] > upper)
    ]
    print(f'\n기름 종류 {kind}: Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}')
    print(f'하한={lower:.2f}, 상한={upper:.2f}')
    print('이상치 후보:\n', outliers if not outliers.empty else '없음')

# 2-4. 상자그림으로 집단별 분포와 이상치 후보 확인
data.boxplot(column='quantity', by='kind')
plt.title('기름 종류별 흡수량과 이상치 후보')
plt.suptitle('')
plt.xlabel('기름 종류')
plt.ylabel('기름 흡수량')
plt.tight_layout()
plt.show()

# 결측값을 평균으로 대체하였고 
# 이상치는 존재하지 않는다.


# [3단계] : 정규성과 등분산성 확인하기
# 선행조건1) 정규성 확인 - shapiro test사용

# 주어진 DataFrame을 기름 종류(1~4)별로 구분함
group1 = data.loc[data['kind'] == 1, 'quantity']
group2 = data.loc[data['kind'] == 2, 'quantity']
group3 = data.loc[data['kind'] == 3, 'quantity']
group4 = data.loc[data['kind'] == 4, 'quantity']

print(stats.shapiro(group1).pvalue)
print(stats.shapiro(group2).pvalue)
print(stats.shapiro(group3).pvalue)
print(stats.shapiro(group4).pvalue)
# 0.8680405837805181
# 0.5923924912098565
# 0.4860108390043152
# 0.4162161687864798
# 모든 그룹에 대해서 p값이 유의수준보다 크다. = 정규성을 만족한다. ... 등분산성을 확인하러 ㄱㄱ

# 선행조건2) 등분산성 확인
from scipy.stats import levene, bartlett
# levene방법을 사용하ㄹ 것이다.
levene_stat, levene_p = levene(group1, group2, group3, group4)
print('p값 : ', levene_p)
# 결과 :  p값 :  0.3268969935062271
# 해석 : 등분산성을 만족한다!!


# [4단계] : 일원분산분석 모형 적합 및 ANOVA 표 생성

# 독립변수(요인) : kind - 기름 종류 1~4인 범주형 변수
# 종속변수 :   quantity - 기름 흡수량

# 4-1. 최소제곱법(OLS)으로 선형모형 적합
# 수식은 '종속변수 ~ 독립변수' 순서로 작성한다.
# kind는 숫자지만 집단을 나타내므로 C(kind)로 범주형임을 지정한다.
lin_model = ols('quantity ~ C(kind)', data=data).fit()

# 4-2. 적합한 모형으로 ANOVA 표 생성
# typ=1 : 제1유형 제곱합 사용. 이 예제는 요인이 하나인 일원분산분석이다.
result = anova_lm(lin_model, typ=1)
print('\n일원분산분석 결과:\n', result)

# 4-3. ANOVA 표 읽기
# C(kind) : 집단 간 변동, Residual : 집단 내 변동(오차)
# sum_sq : 제곱합(SS), df : 자유도, mean_sq : 평균제곱(MS = SS / df)
# 집단 간 자유도 = k - 1 = 4 - 1 = 3
# 집단 내 자유도 = N - k = 20 - 4 = 16
# F = 집단 간 평균제곱 / 집단 내 평균제곱
# PR(>F) : F검정의 p값. 다음 단계에서 유의수준과 비교한다.
print()


# [5단계] : p값, f값을 통한 가설 검증
# 유의수준을 0.05로 설정한다.
alpha = 0.05

# ANOVA 표의 C(kind) 행에서 F값과 p값을 추출한다.
# F = 집단 간 평균제곱 / 집단 내 평균제곱
f_value = result.loc['C(kind)', 'F']
p_value = result.loc['C(kind)', 'PR(>F)']
print('F값:', f_value)
print('p값:', p_value)

# 귀무가설 : 네 기름 종류의 모집단 평균 흡수량이 모두 같다.
# 대립가설 : 적어도 한 기름 종류의 모집단 평균 흡수량이 다르다.
if p_value <= alpha:
    print('귀무가설 기각')
    print('적어도 한 기름 종류의 모집단 평균 흡수량이 다르다는 통계적 근거가 있다.')
    # 어느 집단끼리 다른지는 필요한 경우 사후검정으로 확인한다.
else:
    print('귀무가설을 기각하지 못함')
    print('기름 종류에 따라 모집단 평균 흡수량이 다르다고 판단할 통계적 근거가 부족하다.')
    # 평균이 모두 같다는 사실을 증명한 것은 아니다.


# [6단계] : 평균 구하기
# 집단 평균 = 해당 기름 종류의 흡수량 합 / 해당 집단의 관측값 개수
# groupby('kind')로 기름 종류별로 묶고 quantity의 평균을 계산한다.
# 2단계에서 평균으로 대체한 결측값도 계산에 포함된다.
group_means = data.groupby('kind')['quantity'].mean()
print('\n기름 종류별 평균 흡수량:')
print(group_means)

# 표본 평균에 차이가 보여도 모집단 평균의 차이가 통계적으로 유의한지는
# 5단계 ANOVA의 p값으로 판단한다.


# [7단계] : 사후검정
# Tukey HSD 방법으로 어느 기름 종류끼리 평균 차이가 있는지 비교한다.
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 이 예제에서는 ANOVA 결과가 유의할 때 사후검정을 진행한다.
if p_value <= alpha:
    tukey_result = pairwise_tukeyhsd(
        endog=data['quantity'],  # 비교할 측정값(흡수량)
        groups=data['kind'],     # 집단을 구분하는 기름 종류
        alpha=alpha              # 다중비교 전체의 유의수준
    )
    print('\nTukey HSD 사후검정 결과:')
    print(tukey_result)

    # group1, group2 : 비교하는 두 기름 종류
    # meandiff : group2 평균 - group1 평균
    # p-adj : 다중비교를 보정한 p값
    # lower, upper : 평균 차이의 동시 신뢰구간 하한과 상한
    # reject=True : 두 집단의 모집단 평균이 같다는 귀무가설 기각
    # reject=False : 두 집단의 평균이 다르다는 근거가 부족함
else:
    print('\nANOVA 결과가 유의하지 않아 Tukey HSD 사후검정을 생략한다.')

