# 이원카이제곱(Chi-Square Test of Independence) - 교차분할표 이용
# : 두 개 이상의 변인(집단또는범주)을 대상으로 검정을 수행한다. 변인이 2개이다!!
# 분석대상의 집단 수에 의해서 독립성 검정과 동질성 검정으로 나뉜다.

# 독립성(관련성)검정- 동일 집단의 두 변인(학력수준과 대학진학여부)을 대상으로 관련성이 있는가 없는가?- 독립성 검정은 두 변수 사이의 연관성을 검정한다.

# 일원 카이제곱 검정 = 적합도 검정
# 이원 카이제곱 검정 = 독립성 검정 / 동질성 검정
# 이번시간에는 독립성 검정에 대해서만 보자

# 실습 : 하나의 집단 내에서 교육 수준과 흡연율 간의 관련성 분석 : smoke.csv

# 귀무가설(H1) : 교육수준과 흡연율 간에 관계가 있다. (독립이다. 연관성이 없다.)
# 대립가설(H0) : 교육수준과 흡연율 간에 관계가 있다. (독립이 아니다. 연관성이 있다.)

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/smoke.csv")
print(data.head(3))
print(data.tail(3))
print(data['education'].unique())
print(data['smoking'].unique())

# 학력수준 별 흡연 빈도 수 : 교차표 작성
ctab = pd.crosstab(index=data['education'], columns=data["smoking"]) # 빈도 수
# ctab = pd.crosstab(index=data['education'], columns=data["smoking"], normalize=True) # 비율로 출력

ctab.index = ['대학원졸', '대졸', '고졸']
ctab.columns = ['과한흡연', '보통', '노담']
print(ctab)
# 결과 :
#               과한흡연       보통         노담
#     대학원졸   0.143662    0.259155     0.191549
#        대졸    0.061972    0.059155     0.025352
#        고졸    0.121127    0.078873     0.059155

# 이원카이제곱 검정 시작 = 독립성 검정
# chi_result = [ctab.loc['대학원졸'], ctab.loc['대졸'], ctab.loc['고졸']]
chi_result = ctab
# 위 두 줄은 같다
chi2, pv, dof, expected = stats.chi2_contingency(chi_result)
print(f"chi2 : {chi2:.7f}, pv : {pv:.7f}, dof : {dof}")
print(f"expected :\n {expected}")

# 판정1 : 유의수준:0.05 > p:0.0008183 이므로 귀무가설 기각
#        = 교육 수준과 흡연율 간에 관계가 있다. smoke.csv(수집자료)는 우연히 발생된 자료가 아니다.
# 판정2 : chi:18.9109157, dof:4, cv:9.49
#        = 카이제곱 분포표(cv)를 통해 확인해보니 chi2값이 임계치 우측에 있으므로 (귀무 기각역) 귀무 기각, 대립 가설이 채택된다.



print("\n\n 독립성 검정 2 -----------")
# 남성과 여성의 스포츠 음료 선호도 검정

# 귀무 : 성별과 음료 선호는 서로 관련이 없다.
# 대립 : 성별과 음료 선호는 서로 관련이 있다.

# 교차표 생성
data = pd.DataFrame({
    "포카리스웨트" : [30, 20],
    "칠성사이다" : [20, 30],
    "비타 500" : [10, 30],
    "포도 에이드" : [10, 30]
}, index=['남성', '여성'])

print(data)
# 결과 :
#            포카리스웨트  칠성사이다  비타 500  포도 에이드
#       남성      30     20      10      10
#       여성      20     30      30      30

chi2, pv, dof, expected = stats.chi2_contingency(data)
print("p-value : ", pv)
print("chi2 : ", chi2)
print("dof : ", dof)
print("expected : ", expected)
# p-value와 카이제곱은 반비례관계이다.
#   p-value :  0.0011909784272200567
#   chi2 :  15.896103896103902
#   dof :  3

# 판정 : 유의수준:0.05 > p-value:0.0033880이므로 귀무가설을 기각하고 대립가설을 채택한다.
#       = 성별과 음료선호는 서로 관련이 있다.

# 모집단의 평균을 알고 있으면 자유도는 그대로 사용하고
# 표본분산의 평균을 알고 있으면 n-1로 사용한다.

# 히트맵 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
sns.heatmap(data=data, annot=True, fmt='d', cmap="Blues")
# 해당 인원이 많을수록 그래프의 색깔이 진해진다.
plt.title("성별에 따른 음료 선호 분석")
plt.title("음료 종류")
plt.title("성별")
plt.show()



