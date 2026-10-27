# 이원카이제곱 분포
# 독립성 검정 / 동질성 검정
# 이번 시간에는 동질성 검정
# 동질성 검정 : 두 집단의 분포가 동일한가? 다른 분포인가?를 검증하는 방법이다. 분포 비율을 확인
# 두 집단 이상에서 각 범주(집단)간의 비율이 서로 동일한가를 검정하게 된다
# 두 개 이상의 범주형 자료가 동일한 분포를 가지는 모집단에서 추출된 것인지 검정하는 방법이다


# 동질성 검정 실습1)
# <교육 방법에 따른 교육생들의 만족도분석(survey_method.csv)> 

# 귀무가설 : 교육 방법에 따른 교육생들의 만족도에 차이가 없다.
# 대립가설 : 교육 방법에 따른 교육생들의 만족도에 차이가 있다.

# scipy : t검정, 분산분석, 등 통계검정과 과학 계산
# scikt-learn : 회귀, 분류, 군집화 등 머신러닝
# statsmodels : 통계모형, 회귀분석 결과와 p값 등 자세한 통계분석

# 1. 데이터 수집 및 가공
import pandas as pd
# 데이터를 수집하고 가공하는 과정은 -> survey_method.csv에서 미리 해둠(강사님 github에 존재)
import scipy.stats as stats

# 만족도에 대한 설문조사 수집 자료 확인...github
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/survey_method.csv")
print(data.head(3))
print(data['method'].unique())
print(data['survey'].unique())

# 2. 주어진 자료형 변환
ctab = pd.crosstab(index=data['method'], columns=data['survey'])
# crosstable이기에 행이름은 method를 기준으로, 열이름은 survey로 잡느다.
ctab.index = ["방법1", "방법2", "방법3"]
ctab.columns = ["매우만족", "만족", "보통", "불만족", "매우불만족"]
print(ctab)
# 결과 :
#          매우만족  만족   보통  불만족  매우불만족
#    방법1     5     8      15      16      6
#    방법2     8    14      11      11      6
#    방법3     8     7      11      15      9

# 3. 표본통계량을 통해서 카이제곱 통계량과 p값 구하기
# 카이제곱통계량(실제 관측된 빈도와 예상한 빈도가 얼마나 다른지 나타내는 값), p값, 자유도, 기댓값(두 변수가 관련 없다고 가정했을때의 기대빈도)
chi2, pv, dof, expected = stats.chi2_contingency(ctab) # chi2_contingency = 교차표를 받아 두 범주형 변수가 관련 있는지 카이제곱 검정을 하는 함수
print(f"chi2 : {chi2}, pv : {pv}, dof : {dof}")
# 결과 : chi2 : 6.544667820529891, pv : 0.5864574374550608, dof : 8

print("expected : \n", expected) # 예측 비율
# 4. 해석 : 유의수준 0.05 < p=0.58645743이므로 귀무가설을 채택한다. = 해당 csv자료는 우연히 발생한 자료이다.

print("\n\n ---------------")



# 동질성 검정 실습2)
# 연령대별 SNS 이용률의 동질성 검정
# "20대~40대까지 연령대별로 서로 조금ㅆ기 그 특성이 다른 SNS서비스들에 대해 이용현황을 조사한 자료를 바탕으로 연령대 별로 홍보전략을 세우고자한다. 
# 그때 연령대 별로 이용현황이 서로 동일한지 알아보자"

# 1. 가설 설정하기
# 귀무가설 : 연령대별 SNS 서비스별 이용률 현황을 동일하다.(동질이다)
# 대립가설 : 연령대별 SNS 서비스별 이용률 현황을 동일하지 않다.

# 2. 데이터 수집 및 가공이 된 자료 가져오기
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/snsbyage.csv")
print(data2.head(3))

# 3. 내가 필요한 ctab형태로 고치기1
print(data2['age'].unique())
print(data2['service'].unique())

# 4. 내가 필요한 ctab형태로 고치기2 = 내가 사용하기 편하게 바꾸기
ctab2 = pd.crosstab(index=data2['age'], columns=data2['service'])
# crosstable이기에 행이름은 method를 기준으로, 열이름은 survey로 잡느다.
ctab2.index = ["20대", "30대", "40대"]
ctab2.columns = ["F", "T", "K", "C", "E"]
print(ctab2)
# 결과 : 
#                F   T    K    C    E
#        20대   81  16   207  111  117
#        30대  109  15   107  236  104
#        40대   32  17    78  133   76

# 5. 검정통계량값들 구하기(chi2, pv, dof, expected)
chi2, pv, dof, expected = stats.chi2_contingency(ctab2)
print(f"chi2 : {chi2}, pv : {pv}, dof : {dof}")
# 결과 : chi2 : 102.75202494484225, pv : 1.1679064204212775e-18, dof : 8

# 6. 해석 : 연령대별 SNS 서비스별 이용률 현황은 동일하지 않다는 의견을 인정함 = 대립가설 채택


print("\n (실습2연장) 위 자료는 샘플 자료이지만 모집단 자료라 가정하고 샘플링 후 검정하기 -------")
# 전체 자료와 샘플 자료로 가설검정을 한 결과에 자리를 확인하기
print("전체 건수 : ", len(data2))
# 결과 : 1439

# 1. 표본으로 뽑은 데이터를 모집단이라고 가정해서 다시 cross table설정하기 
samp_data = data2.sample(n=500, replace = True, random_state = 1).reset_index(drop = True)
# 원래 data2는 표본데이터지만 모집단데이터라고 가정해서 500개로 무작위로 뽑아서 samp_data에 저장함 = 모집단이 이렇다고 가정해보자.
# .reset_index(drop = True) : 인덱스를 새로 부여하기 위해서 index설정을 다시 해줌
print("샘플 건수 : ", len(samp_data))

# 2. 내가 필요한 ctab 형태로 고치기
ctab3 = pd.crosstab(index=samp_data['age'], columns=samp_data['service'])
# 다시 똑같이 행 이름은 method를 기준으로, 열 이름은 survey로 잡는다.
ctab3.index = ["20대", "30대", "40대"]
ctab3.columns = ["F", "T", "K", "C", "E"]
print(ctab3)

# 3. 검정통계량값들 구하기(chi2, pv, dof, expected)
chi2, pv, dof, expected = stats.chi2_contingency(ctab3)
print(f"chi2 : {chi2}, pv : {pv}, dof : {dof}")
# 결과 : chi2 : 36.20748437710444,  pv : 1.6088950709449814e-05,  dof : 8
# 4. 해석 결과는 표본에 대한 검정통계량 값들과 동일하다.
# = 연령대별 SNS 서비스별 이용률 현황은 동일하지 않다는 의견을 인정함

# 즉, 둘 다 결국 같은 데이터에 대해서 표본으로 조사했느냐 모집단으로 조사했느냐에 따라서 결과가 크게 달라지면 안된다.

# 다음은 fpro_coffee로 이동 ㄱㄱ