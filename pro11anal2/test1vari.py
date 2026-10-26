# 표준편차와 분산의 중요성
# 두 반의 시험성적이 있을 때 "평균이 같다고 성적 분포가 동일한가?"
# 실제로 표준편차의 대소에 따라 성적 편차가 다를 수 있다.

# 표본 통계량을 통해서 모집단을 추정한다.
# 그때 모집단에서 표본을 구하는 방법이 여러가지가 존재한다

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(42)

# 목표 평균
target_mean = 60
std_dev_small = 10
std_dev_large = 20

# 데이터 생성
class1_raw = np.random.normal(loc=target_mean, scale=std_dev_small, size = 100)
class2_raw = np.random.normal(loc=target_mean, scale=std_dev_large, size = 100)
# 1반과 2반의 평균은 같지만 2반은 표준편차가 더 크다. 

# 평균 보정
class1_adj = class1_raw - np.mean(class1_raw) + target_mean
class2_adj = class2_raw - np.mean(class2_raw) + target_mean

# 정수화 및 범위 제한np.clip(배열, 최소값, 최대값)
class1 = np.clip(np.round(class1_adj), 10, 100).astype(int)
class2 = np.clip(np.round(class2_adj), 10, 100).astype(int)

print(class1)
print(class2)

print()

# 데이터가 준비되었다.

# 통계 계산
mean1, mean2 = np.mean(class1), np.mean(class2)
std1, std2 = np.std(class1), np.std(class2)
var1, var2 = np.var(class1), np.var(class2)

print("1반(성적 편차가 적음)")
print(f"평균 : {mean1}, 표준편차 : {std1}, 분산 : {var1}")
print()
print("2반(성적 편차가 적음)")
print(f"평균 : {mean2}, 표준편차 : {std2}, 분산 : {var2}")

print()

# 자료를 파일로 저장
df = pd.DataFrame({
    'class':['1반'] * 100 +['2반'] * 100,
    'score' : np.concatenate([class1, class2])
})
print(df.head())
df.to_csv("test1.csv", index=False, encoding= 'utf-8-sig')

print("시각화 --------")
x1 = np.random.normal(1, 0.05, size=100)
x2 = np.random.normal(2, 0.05, size=100)

plt.figure(figsize=(10, 6))
plt.scatter(x1, class1, alpha=0.8, label=f"1반(평균 = {mean1:2f}, 표준편차 = {std1:2f})")
plt.scatter(x2, class2, alpha=0.8, label=f"2반(평균 = {mean2:2f}, 표준편차 = {std2:2f})")

plt.hlines(target_mean, 0.5, 2.5, colors='red', linestyles='dashed', label=f"공통평균={target_mean}")
plt.xticks([1,2], ["1반", "2반"])
plt.ylabel("시험 점수")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.boxplot([class1, class2], label=["1반", "2반"])
plt.grid(True)
plt.show()

# 여기까지는 기술통계의 내용이다.

print()

# 국어 선생님 입장에서 말하길/
# 전통적 주장(귀무가설) : "늘 내가 가르치는 학생들의 점수는 매년 두 반의 국어 점수 평균(편차)의 차이가 없다"
# 그런데 누군가가 실험을 통해 데이터를 수집한 후 두 반의 평균 점수에 차이가 있다는 새로운 의견을 제시함.
# = 대립 가설 : "두 반의 국어 점수의 평균은 차이가 있다"
# 위 주장에 대해 누가 옳은지 "가설검정"을 통해 판정을 내린다.(t-test와 anova 사용)

print("-----------------------------------")

from scipy import stats

# < 독립표본 t검정 >
t_stat, p_value_t = stats.ttest_ind(class1, class2, equal_var=False) # Welchi's Test
print(f"t-통계값(t-test) : {t_stat:4f}")
print(f"p값(p-value) : {p_value_t:4f}")

if p_value_t < 0.05:
    print("유의확률(p)가 유의수준(α, 95% 신뢰구간에서 0.05)보다 작으므로 두 반의 평균은 차이가 있다. = 유의미하다.")
else:
    print("유의확률(p)가 유의수준(α, 95% 신뢰구간에서 0.05)보다 크므로 두 반의 평균은 차이가 있다. = 무의미하다. = 선생님 말이 맞음 ㅇㅇ")        
# = 귀무가설 채택, 대립가설 기각]


# 주요 개념 용어 및 큰 흐름 정리

# 기술통계 / 추론통계 / t-test / anova / 유의확률과 유의수준 / 가설검정 / 카이제곱 테스트 / 선형회귀 / 머신러닝 / 신경망 / 딥러닝 / 

# 다음카페 - R analysis - 데이터 분석 및 검정 방법 구분 
# : 여기서 시험에 나올 만한거 많이 나와 있다.

# 회귀분석  ->  y=mx+b 
# 이때 mx가 내적곱을 이용(numpy)

# 독립변수(feature)/종속변수(label)  ->  사용되는 분석방법들 .. 그 중 로지스틱 회귀분석이 중요(*회귀분석*)
# # 주로 독립변수는 여러 개 종속변수는 하나이다

# 귀무가설/대립가설

# 신뢰수준 / 유의수준(α) / 유의확률(p-value) / 기각역

# < 가설검정 순서 >
# 1. 대립가설 설정
# 2. 귀무가설 설정
# 3. 귀무가설이 옳다고 가정 = 귀무가설을 지키려고 노력을 해야함
# 4. 유의수준 설정(보통 5%)
# 5. 대립가설을 고려한 기각역 설정(양측검정/단측검정)
# 6. 데이터로 판단 
#       검정통계량이 기각역 안 쪽 : 귀무가설 기각하고 대립가설 채택  
#       검정통계량이 기각역 밖 쪽 : 귀무가설을 그대로 수용

# 제 1종 오류, 제 2종 오류

# 점추정과 구간추정

# scipy : t검정, 분산분석, 등 통계검정과 과학 계산
# scikt-learn : 회귀, 분류, 군집화 등 머신러닝
# statsmodels : 통계모형, 회귀분석 결과와 p값 등 자세한 통계분석