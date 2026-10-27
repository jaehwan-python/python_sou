# <대응표본 t검정>

# : 서로 대응인 두 집단의 평균 차이를 검정
#   = 대응표본 t검정
#   = 동일집단 표본 t검정
#   = 쌍체 t검정
#   = pairedsample t-test

# 처리 이전과 처리 이후를 각각의 모집단으로 판단하여, 동일한 관찰대상으로부터 처리 이전과 처리 이후로 1:1로 대응시킨 검정방법
# 두 집단으로부터의 표본을 대응표본(pairedsample)이라고 한다.

# 대응인 두 집단의 평균 비교는 동일한 관찰대상으로부터 처리 이전의 관찰과 이후의 관찰을 비교하여 
# 영향을 미친 정도를 밝히는데 주로 사용하고 있다.
# 집단 간 비교가 아니므로 등분산 검정을 할 필요가 없다.


# 실습) 복부 수술 전 9명의 몸무게와 복부 수술 후 몸무게 변화

# [1단계] : 가설 설정
# 대응표본 t검정 가설

# 귀무가설 : 수술 전후 평균 몸무게 차이는 0이다. (차이가 없다)
# 대립가설 : 수술 전후 평균 몸무게 차이는 0이 아니다. (차이가 있다)

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

baseline = [67.2, 67.4, 71.5, 77.6, 86.0, 89.1, 59.5, 81.9, 105.5]
follow_up = [62.4, 64.6,70.4, 62.6, 80.1, 73.2, 58.2, 71.0, 101.0]

df = pd.DataFrame({
    '수술전': baseline,
    '수술후': follow_up
})

df['감소량'] = df['수술전'] - df['수술후']
print(df)
print(df.describe())
print(f"수술 전 평균 : {df["수술전"].mean().mean():.2f}kg")
# 결과 : 78.41kg
print(f"수술 후 평균 : {df["수술후"].mean().mean():.2f}kg")
# 결과 : 71.50kg

result = stats.ttest_rel(baseline, follow_up)

print(f"t통계량 : {result.statistic:.5f}")
print(f"p-value : {result.pvalue:.5f}")
# 결과 : 3.36681
# 해석 : p값 : 0.00633

alpha = 0.05
if result.pvalue < alpha:
    print("귀무가설 기각 : 수술 전후 평균 몸무게에 통계적으로 유의미한 차이가 있다.")
else:
    print("귀무가설 채택 : 수술 전후 평균 몸무게에 차이가 있다라는 주장이 있다는 근거가 부족하다.")

# 몸무게 차이값에 정규성 검정
print('몸무게 감소량 정규성 : ', stats.shapiro(df['감소량']).pvalue)  # 0.116522 만족

# Q-Q plot
stats.probplot(df['감소량'], dist='norm', plot=plt)
plt.grid()
plt.show()

# 몸무게 변화량을 시각화
plt.figure(figsize=(8, 5))
for before, after in zip(baseline, follow_up):
    plt.plot(['수술전', '수술후'], [before, after], marker='o')
plt.title('수술 전후 몸무게 변화')
plt.ylabel('몸무게(kg)')
plt.grid(axis='y', alpha=0.3)
plt.show()


print("-------------------------------------------------------------------------------------------------------------------------------------------")
# [대응표본 t 검정 : 문제4]

# 어느 학급의 교사는 매년 학기 내 치뤄지는 시험성적의 결과가 실력의 차이없이 비슷하게 유지되고 있다고 말하고 있다.
# 이 때, 올해의 해당 학급의 중간고사 성적과 기말고사 성적은 다음과 같다. 점수는 학생 번호 순으로 배열되어 있다.


import numpy as np
from scipy import stats
# 수집된 자료 :  
#    중간 : [80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80]
#    기말 : [90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95]

# 그렇다면 이 학급의 학업능력이 변화했다고 이야기 할 수 있는가?

midterm = np.array([80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80])
final = np.array([90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95])

# 정규성 확인
diff = final -midterm
shapiro_test = stats.shapiro(diff)
print(f"차이값의 정규성 검정 p-value : {shapiro_test.pavlue:.4f}")
# p값(0.3111) > 유의수준(0.05) 정규성 만족

t_stat, p_val = stats.ttest_rel(midterm, final)

print(f"t-통계량 : {t_stat:.4f}")
print(f"p-value : {p_val:.4f}")
# p_value : 0.0235