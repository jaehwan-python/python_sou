# [two-sample t 검정 : 문제1] 

# 다음 데이터는 동일한 상품의 포장지 색상에 따른 매출액에 대한 자료이다. 
# 포장지 색상에 따른 제품의 매출액에 차이가 존재하는지 검정하시오.

# 수집된 자료 :  
#    blue : [70 68 82 78 72 68 67 68 88 60 80]
#    red  : [60 65 55 58 67 59 61 68 77 66 66]

# [1단계] 대립가설과 귀무가설 설정 
#              = "두 집단 간 평균의 차이는 존재한다/존재하지 않는다." 
#              그때 독립변수는 범주형이고 종속변수는 연속형이다. 독립변수가 하나라면 '단일표본 t검정'이고
#              2개라면 '독립 표본 t검정'을 쓴다.
#              독립변수(범주형) : 
#              종속변수(연속형) : 
# 귀무가설 : 포장지 색상에 따른 평균 매출액의 차이가 없다.
# 대립가설 : 포장지 색상에 따른 평균 매출액의 차이가 있다.

# [2단계] 두 집단, 각 집단의 평균 구하기
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# blue를 가진 제품의 평균
blue = np.array([70, 68, 82, 78, 72, 68, 67, 68, 88, 60, 80])
print('blue 평균:', np.mean(blue))
# 결과 : blue 평균: 72.81818181818181

# red를 가진 제품의 평균
red = np.array([60, 65, 55, 58, 67, 59, 61, 68, 77, 66, 66])
print('red 평균:', np.mean(red))
# 결과 : red 평균: 63.81818181818182
#        "두 개"의 집단에 대한 표본 자료를 조사한 것이므로 "독립 표본 t검정을 사용한다!"

# [3단계] "정규성"과 "등분산성" 확인 
#             선행조건1) 정규성 확인 - 두 집단이 각각 정규분포를 따라야한다.
#                        - shapiro test
#                        - histplot (정규성 시각화 방법1)
#                        - Quantitle-Quantitile plot(Q-Q plot) (정규성 시각화 방법2)
#                             그때 정규성을 만족(O) ->  two-sample t-test(모수검정) 
#                                  정규성을 만족(X) ->  Mann-whitney-test(비모수검정)
print('red의 정규성 : ', stats.shapiro(red).pvalue)
# 결과 : 0.5347933238609744
print('blue의 정규성 : ', stats.shapiro(blue).pvalue)
# 결과 : 0.5102310071741448
# 해석 : 둘 다 p값 보다 크기에 정규성을 만족한다.

#             선행조건2) 등분산성 확인 : 두 집단의 분산이 같다는 가정이 필요하다. = 등분산성
#                        from scipy.stats import levene, bartlett
#                        # levene : 정규성과 상관없이 사용가능하고 이상치에 민감하다. 
#                                   하지만 어떤 분포도 사용이 가능하다.
#                        # bartlett : 정규성이 있을 때만 사용하고 이상치에 덜 민감하다. 
#                                     대신 정규분포일 때만 사용가능하다.
#                        levene_stat, leven_p = levene(male, female)
#                        print('p값 : ', leven_p)
#                        그때 등분산성을 만족(O)  ->  two_sample = stats.ttest_ind(male, female, equal_var=True)
#                             등분산성을 만족(X)  ->  two_sample = stats.ttest_ind(male, female, equal_var=False)
levene_stat, levene_p = stats.levene(blue, red)
print('등분산성 검정 p값:', levene_p)
# 결과 : 0.43916444685083794

# [4단계]. 어느 가설을 기각하고 채택할 것인지 결정한다.
result = stats.ttest_ind(blue, red, equal_var=(levene_p > 0.05))
print('t검정 결과:', result)
# 결과 : TtestResult(statistic=np.float64(2.9280203225212174), pvalue=np.float64(0.008316545714784409), df=np.float64(20.0))
# p값(0.008) < 유의수준(0.05)
# 해석 : 대립가설을 채택한다!! 즉, 포장지 색상에 따른 평균 매출액의 차이가 있다.




print("-------------------------------------------------------------------------------------------------------------------------------------------------")
# [two-sample t 검정 : 문제2]  

# 아래와 같은 자료 중에서 남자와 여자를 각각 15명씩 무작위로 비복원 추출하여 혈관 내의 콜레스테롤 양에 차이가 있는지를 검정하시오.

# 수집된 자료 :  
#   남자 : [0.9 2.2 1.6 2.8 4.2 3.7 2.6 2.9 3.3 1.2 3.2 2.7 3.8 4.5 4 2.2 0.8 0.5 0.3 5.3 5.7 2.3 9.8]
#   여자 : [1.4 2.7 2.1 1.8 3.3 3.2 1.6 1.9 2.3 2.5 2.3 1.4 2.6 3.5 2.1 6.6 7.7 8.8 6.6 6.4]


# [1단계] 대립가설과 귀무가설 설정 
#              = "두 집단 간 평균의 차이는 존재한다/존재하지 않는다." 
#              그때 독립변수는 범주형이고 종속변수는 연속형이다. 독립변수가 하나라면 '단일표본 t검정'이고
#              2개라면 '독립 표본 t검정'을 쓴다.
#              독립변수(범주형) : 
#              종속변수(연속형) : 

# 귀무가설 : 남자와 여자의 평균 콜레스테롤 양에 차이가 없다.
# 대립가설 : 남자와 여자의 평균 콜레스테롤 양에 차이가 있다.

# 독립변수(범주형) : 성별(남자, 여자)
# 종속변수(연속형) : 혈관 내 콜레스테롤 양


# [2단계] 두 집단, 각 집단의 평균 구하기
#        "두 개"의 집단에 대한 표본 자료를 조사한 것이므로 "독립 표본 t검정을 사용한다!"
male_data = np.array([
    0.9, 2.2, 1.6, 2.8, 4.2, 3.7, 2.6, 2.9, 3.3, 1.2,
    3.2, 2.7, 3.8, 4.5, 4, 2.2, 0.8, 0.5, 0.3, 5.3,
    5.7, 2.3, 9.8
])

female_data = np.array([
    1.4, 2.7, 2.1, 1.8, 3.3, 3.2, 1.6, 1.9, 2.3, 2.5,
    2.3, 1.4, 2.6, 3.5, 2.1, 6.6, 7.7, 8.8, 6.6, 6.4
])

# 시드를 고정하여 실행할 때마다 같은 표본을 추출한다.
rng = np.random.default_rng(42)

# replace=False : 같은 사람을 중복으로 뽑지 않는 비복원 추출
male = rng.choice(male_data, size=15, replace=False)
female = rng.choice(female_data, size=15, replace=False)

print('남자 표본:', male)
print('여자 표본:', female)
print('남자 평균:', np.mean(male))
print('여자 평균:', np.mean(female))

# 서로 다른 사람으로 구성된 두 집단이므로 독립 표본 검정을 사용한다.



# [3단계] "정규성"과 "등분산성" 확인 
#             선행조건1) 정규성 확인 - 두 집단이 각각 정규분포를 따라야한다.
#                        - shapiro test
#                        - histplot (정규성 시각화 방법1)
#                        - Quantitle-Quantitile plot(Q-Q plot) (정규성 시각화 방법2)
#                             그때 정규성을 만족(O) ->  two-sample t-test(모수검정) 
#                                  정규성을 만족(X) ->  Mann-whitney-test(비모수검정)
#             선행조건2) 등분산성 확인 : 두 집단의 분산이 같다는 가정이 필요하다. = 등분산성
#                        from scipy.stats import levene, bartlett
#                        # levene : 정규성과 상관없이 사용가능하고 이상치에 민감하다. 
#                                   하지만 어떤 분포도 사용이 가능하다.
#                        # bartlett : 정규성이 있을 때만 사용하고 이상치에 덜 민감하다. 
#                                     대신 정규분포일 때만 사용가능하다.
#                        levene_stat, leven_p = levene(male, female)
#                        print('p값 : ', leven_p)
#                        그때 등분산성을 만족(O)  ->  two_sample = stats.ttest_ind(male, female, equal_var=True)
#                             등분산성을 만족(X)  ->  two_sample = stats.ttest_ind(male, female, equal_var=False)
# 선행조건1) Shapiro 검정으로 각 집단의 정규성 확인
# 귀무가설 : 해당 집단의 자료가 정규분포를 따른다.
# p값 > 0.05이면 정규성 가정을 기각할 근거가 부족하다.
alpha = 0.05
male_normal_p = stats.shapiro(male).pvalue
female_normal_p = stats.shapiro(female).pvalue

print('남자 정규성 p값:', male_normal_p)
print('여자 정규성 p값:', female_normal_p)

normal = male_normal_p > alpha and female_normal_p > alpha

# 선행조건2) Levene 검정으로 등분산성 확인
# 귀무가설 : 두 집단의 분산이 같다.
# p값 > 0.05이면 등분산을 가정한다.
levene_stat, levene_p = stats.levene(male, female)
print('등분산성 검정 p값:', levene_p)


# [4단계]. 어느 가설을 기각하고 채택할 것인지 결정한다.
alpha = 0.05  # 유의수준 5%
if normal:
    # 두 집단 모두 정규성 가정이 기각되지 않은 경우
    # 등분산이면 일반 독립 표본 t검정, 아니면 Welch t검정
    result = stats.ttest_ind(male, female, equal_var=(levene_p > alpha))
    print('t검정 결과:', result)

    if result.pvalue < alpha:
        print('귀무가설 기각 : 남자와 여자의 평균 콜레스테롤 양에 차이가 있다.')
    else:
        print('귀무가설 기각 못함 : 평균 차이가 있다고 볼 근거가 부족하다.')
else:
    # 정규성 가정이 기각되면 Mann-Whitney U 검정을 사용한다.
    # 이 검정은 평균 차이가 아닌 두 집단의 분포 차이를 검정한다.
    result = stats.mannwhitneyu(male, female, alternative='two-sided')
    print('Mann-Whitney U 검정 결과:', result)

    if result.pvalue < alpha:
        print('귀무가설 기각 : 남자와 여자의 콜레스테롤 분포에 차이가 있다.')
    else:
        print('귀무가설 기각 못함 : 분포 차이가 있다고 볼 근거가 부족하다.')


print("-------------------------------------------------------------------------------------------------------------------------------------------------")
# [two-sample t 검정 : 문제3]

# DB에 저장된 jikwon 테이블에서 총무부, 영업부 직원의 연봉의 평균에 차이가 존재하는지 검정하시오.
# 연봉이 없는 직원은 해당 부서의 평균연봉으로 채워준다. = DB에서 데이터 불러오기

# [1단계] 대립가설과 귀무가설 설정 
#              = "두 집단 간 평균의 차이는 존재한다/존재하지 않는다." 
#              그때 독립변수는 범주형이고 종속변수는 연속형이다. 독립변수가 하나라면 '단일표본 t검정'이고
#              2개라면 '독립 표본 t검정'을 쓴다.
#              독립변수(범주형) : 
#              종속변수(연속형) : 

# 귀무가설 : 총무부와 영업부 직원의 평균 연봉에 차이가 없다.
# 대립가설 : 총무부와 영업부 직원의 평균 연봉에 차이가 있다.

# 독립변수(범주형) : 부서(총무부, 영업부)
# 종속변수(연속형) : 직원의 연봉


# [2단계] 두 집단, 각 집단의 평균 구하기
#        "두 개"의 집단에 대한 표본 자료를 조사한 것이므로 "독립 표본 t검정을 사용한다!"
from scipy import stats
import numpy as np
import pandas as pd
import pymysql

conn = pymysql.connect(
    host='127.0.0.1',       # DB 서버 주소
    user='root',        # DB 사용자명
    password='123',    # DB 비밀번호
    database='test',
    port=3306,
    charset='utf8mb4'
)

try:
    with conn.cursor() as cursor:
        # 직원 테이블과 부서 테이블을 부서번호로 연결한다.
        sql = """
            SELECT b.busername, j.jikwonpay
            FROM jikwon AS j
            INNER JOIN buser AS b
                ON j.busernum = b.buserno
            WHERE b.busername IN (%s, %s)
        """
        cursor.execute(sql, ('총무부', '영업부'))

        df = pd.DataFrame(
            cursor.fetchall(),
            columns=['부서명', '연봉']
        )
finally:
    conn.close()

# 연봉을 숫자로 변환하고, 변환할 수 없는 값은 결측값으로 처리한다.
df['연봉'] = pd.to_numeric(df['연봉'], errors='coerce')

# 연봉이 없는 직원은 해당 부서의 평균 연봉으로 채운다.
# transform('mean') : 각 행에 해당 직원이 속한 부서의 평균을 대응시킨다.
df['연봉'] = df['연봉'].fillna(
    df.groupby('부서명')['연봉'].transform('mean')
)

# 부서 전체의 연봉이 결측이면 평균을 구할 수 없으므로 확인한다.
if df['연봉'].isna().any():
    raise ValueError('연봉이 모두 결측인 부서가 있는지 확인하세요.')

general = df.loc[df['부서명'] == '총무부', '연봉'].to_numpy()
sales = df.loc[df['부서명'] == '영업부', '연봉'].to_numpy()

# Shapiro 검정에는 집단별로 최소 3개의 자료가 필요하다.
if len(general) < 3 or len(sales) < 3:
    raise ValueError('각 부서에 연봉 자료가 최소 3개 필요합니다.')

if np.var(general) == 0 or np.var(sales) == 0:
    raise ValueError('부서 내 연봉이 모두 같아 정규성 검정이 어렵습니다.')

print('총무부 연봉:', general)
print('영업부 연봉:', sales)
print('총무부 평균 연봉:', np.mean(general))
print('영업부 평균 연봉:', np.mean(sales))

# 서로 다른 직원으로 구성된 두 집단이므로 독립 표본 검정을 사용한다.
# 평균으로 결측값을 채우면 분산이 줄어들 수 있으므로 해석에 유의한다.


# [3단계] "정규성"과 "등분산성" 확인 
#             선행조건1) 정규성 확인 - 두 집단이 각각 정규분포를 따라야한다.
#                        - shapiro test
#                        - histplot (정규성 시각화 방법1)
#                        - Quantitle-Quantitile plot(Q-Q plot) (정규성 시각화 방법2)
#                             그때 정규성을 만족(O) ->  two-sample t-test(모수검정) 
#                                  정규성을 만족(X) ->  Mann-whitney-test(비모수검정)
#             선행조건2) 등분산성 확인 : 두 집단의 분산이 같다는 가정이 필요하다. = 등분산성
#                        from scipy.stats import levene, bartlett
#                        # levene : 정규성과 상관없이 사용가능하고 이상치에 민감하다. 
#                                   하지만 어떤 분포도 사용이 가능하다.
#                        # bartlett : 정규성이 있을 때만 사용하고 이상치에 덜 민감하다. 
#                                     대신 정규분포일 때만 사용가능하다.
#                        levene_stat, leven_p = levene(male, female)
#                        print('p값 : ', leven_p)
#                        그때 등분산성을 만족(O)  ->  two_sample = stats.ttest_ind(male, female, equal_var=True)
#                             등분산성을 만족(X)  ->  two_sample = stats.ttest_ind(male, female, equal_var=False)

# 선행조건1) Shapiro 검정으로 각 집단의 정규성 확인
# 귀무가설 : 해당 집단의 자료가 정규분포를 따른다.
# p값 > 0.05이면 정규성 가정을 기각할 근거가 부족하다.
general_normal_p = stats.shapiro(general).pvalue
sales_normal_p = stats.shapiro(sales).pvalue

print('총무부 정규성 p값:', general_normal_p)
print('영업부 정규성 p값:', sales_normal_p)

normal = general_normal_p > alpha and sales_normal_p > alpha

# 선행조건2) Levene 검정으로 등분산성 확인
# 귀무가설 : 두 집단의 분산이 같다.
# p값 > 0.05이면 등분산을 가정한다.
levene_stat, levene_p = stats.levene(general, sales)
print('등분산성 검정 p값:', levene_p)


# [4단계]. 어느 가설을 기각하고 채택할 것인지 결정한다.

if normal:
    # 등분산이면 일반 독립 표본 t검정, 아니면 Welch t검정
    result = stats.ttest_ind(
        general, sales,
        equal_var=(levene_p > alpha)
    )
    print('t검정 결과:', result)

    if result.pvalue < alpha:
        print('귀무가설 기각 : 두 부서의 평균 연봉에 차이가 있다.')
    else:
        print('귀무가설 기각 못함 : 평균 연봉 차이가 있다고 볼 근거가 부족하다.')
else:
    # 정규성 가정이 기각되면 Mann-Whitney U 검정을 사용한다.
    # 이 검정은 평균 차이가 아닌 두 집단의 분포 차이를 검정한다.
    result = stats.mannwhitneyu(
        general, sales,
        alternative='two-sided'
    )
    print('Mann-Whitney U 검정 결과:', result)

    if result.pvalue < alpha:
        print('귀무가설 기각 : 두 부서의 연봉 분포에 차이가 있다.')
    else:
        print('귀무가설 기각 못함 : 연봉 분포 차이가 있다고 볼 근거가 부족하다.')




