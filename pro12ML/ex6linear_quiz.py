
# 회귀분석 문제 1) scipy.stats.linregress() <= 꼭 하기 : 심심하면 해보기 => statsmodels ols(), LinearRegression 사용
# 나이에 따라서 지상파와 종편 프로를 좋아하는 사람들의 하루 평균 시청 시간과 운동량에 대한 데이터는 아래와 같다.
#  - 지상파 시청 시간(x)을 입력하면 어느 정도의 운동 시간(y1)을 갖게 되는지 회귀분석 모델을 작성한 후에 예측하시오.
#  - 지상파 시청 시간(x)을 입력하면 어느 정도의 종편 시청 시간(y2)을 갖게 되는지 회귀분석 모델을 작성한 후에 예측하시오.
#     참고로 결측치는 해당 칼럼의 평균 값을 사용하기로 한다. 이상치가 있는 행은 제거. 운동 10시간 초과는 이상치로 한다.  

# 구분,지상파(x),종편(y2),운동(y1)
# 1, 0.9, 0.7, 4.2
# 2, 1.2, 1.0, 3.8
# 3, 1.2, 1.3, 3.5
# 4, 1.9, 2.0, 4.0
# 5, 3.3, 3.9, 2.5
# 6, 4.1, 3.9, 2.0
# 7, 5.8, 4.1, 1.3
# 8, 2.8, 2.1, 2.4
# 9, 3.8, 3.1, 1.3
# 10, 4.8, 3.1, 35.0
# 11, NaN, 3.5, 4.0
# 12, 0.9, 0.7, 4.2
# 13, 3.0, 2.0, 1.8
# 14, 2.2, 1.5, 3.5
# 15, 2.0, 2.0, 3.5

# 방법1 : LinearRegression 사용

import numpy as np
import pandas as pd
from io import StringIO
from scipy import stats # 세번째 방법으로 선형회귀 모델 생성 : linegress 
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf # 두번째 방법으로 선형회귀 모델 생성: ols
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression # 첫번째 방법으로 선형회귀 모델 생성 : LinearRegression 

# [데이터]
data = """구분,지상파,종편,운동
1,0.9,0.7,4.2
2,1.2,1.0,3.8
3,1.2,1.3,3.5
4,1.9,2.0,4.0
5,3.3,3.9,2.5
6,4.1,3.9,2.0
7,5.8,4.1,1.3
8,2.8,2.1,2.4
9,3.8,3.1,1.3
10,4.8,3.1,35.0
11,NaN,3.5,4.0
12,0.9,0.7,4.2
13,3.0,2.0,1.8
14,2.2,1.5,3.5
15,2.0,2.0,3.5
"""

# [데이터] 수정1.
# 결측치를 해당 열의 평균으로 채운 뒤 운동 10시간 초과 행 제거
df = pd.read_csv(StringIO(data), index_col='구분')
df = df.fillna(df.mean())
df = df[df['운동'] <= 10].copy()

# [데이터] 수정2.
# 지상파 시청 시간(x)으로 운동 시간(y1) 예측
# 지상파 시청 시간(x)으로 종편 시청 시간(y2) 예측
x = df[['지상파']].to_numpy()  # 2차원
y1 = df['운동'].to_numpy()
y2 = df['종편'].to_numpy() # 1차원
# 이후에 뒤에서 계산할 때 ravel()을 사용하여 x의 차원을 떨어트려야 한다.



# [데이터1], [데이터2]에 대하여 -> 지상파 시청 시간(x)을 입력하면 어느 정도의 운동 시간(y1)을 갖게 되는지 회귀분석 모델을 작성한 후에 예측하시오.
y = y1

model = LinearRegression()
fit_model = model.fit(x, y)
# fit()함수의 역할
#  1) 독립변수(x)와 종속변수(y)를 입력 받음
#  2) 예측값과 실제값 사이의 오차제곱합이 최소가 되도록 계산
#  3) 최적의 회귀계수(기울기, 절편)를 구함
#  4) 계산된 계수를 모델에 저장

# **주의/참고** : LinearRegression은 신경망처럼 반복학습을 통해 가중치를 갱신하는 것이 아니고, 
# 최소 제곱법이라는 계산을 통해 작성된 것이다.
# 그러니까 기울기와 절편을 확인해야한다.
print('기울기(가중치, weight, slope) : ', fit_model.coef_)
print('절편(편향, bias) : ', fit_model.intercept_)
# 기울기(가중치, weight, slope) :  -0.66845502
# 절편(편향, bias)              :  4.709676019780581
# yhat = -0.66845502 * x + 4.709676019780581

# 예측값을 확인!
# 1. 기존의 값을 넣었을 때의 예측값
y1_newpred1 = fit_model.predict(x[[0]])
# 기존데이터 [0]번째의 데이터를 입력값으로 주었다.
# 대부분의 경우 scikiy-learn에서 독립변수는 2차원, 종속변수는 1차원이다.
print('예측값1 : ', y1_newpred1)
# 예측값1 : 4.1080665  
# 실제값 : 4.0

# 2. 새로운 값(지상파 시청시간)을 넣었을 때의 예측값 
y1_newpred2 = fit_model.predict(np.array([[2.3], [8.7], [23.3]]))
print('예측값2(운동시간) : ', y1_newpred2)
# = 지상파 시청 시간이 2.3, 8.7, 23.2시간(실제 없는 데이터)일 때 운동시간(예측)은?
# 예측값2 :  3.17222948  -1.10588263 -10.86532587
# 경험하지 못한 x값(지상파 시청시간)에 대해서도 결과인 y1값을 줄 수 있다.
print("\n---------------------------------------------------------------------------------")


# 방법2 : ols 사용
# [데이터1], [데이터2]에 대하여 -> 지상파 시청 시간(x)을 입력하면 어느 정도의 종편 종영 시간(y2)을 갖게 되는지 회귀분석 모델을 작성한 후에 예측하시오.
y = y2

data = np.array([x.ravel(), y2])
df = pd.DataFrame(data.T)
df.columns = ['x', 'y2']
print(df.head(3))

model = smf.ols(formula='y2~x', data=df).fit()
print(model.summary())
# summary 표가 모든 검정통계량을 포함한 특성을 설명한다.(단 선형회귀 방정식은 나타나지 않는다.)
# = ols Regression Result를 제공
print('가중치 : ', model.params['x'])
print('편향 : ', model.params['Intercept'])
# 결과 :
# 가중치 :  0.7726869861042749
# 편향 :  0.29516333605064715
# 선형회귀 방정식 : 예측값2(종편종영시간) = 0.7726869861042749 * x + 0.29516333605064715 

# 예측값 확인!
new_df = pd.DataFrame({'x': [2.3, 8.7, 23.3]})
print('예측값2(종편 종영 시간-ols) : ', model.predict(new_df))
# = 지상파 시청 시간이 2.3, 8.7, 23.2시간(실제 없는 데이터)일 때 종평종영시간(예측)은?
# 결과 : 
#       0     2.072343
#       1     7.017540
#       2    18.298770
print("\n---------------------------------------------------------------------------------")


# 방법3 : Linegress 사용
# y2를 이번에는 Linegress를 사용하여 선형회귀모델을 만들어 보겠다.
y = y2
print('상관 계수 : ', np.corrcoef(x.ravel(), y2)[0,1])
# 결과 : 0.8875299693193012
# 매우 가한 상관관계....

model = stats.linregress(x.ravel(), y2)
print(model)
# 결과 : 
# LinregressResult( slope = np.float64(0.7726869861042756), 
#                   intercept = np.float64(0.29516333605064626), 
#                   rvalue = np.float64(0.8875299693193012), 
#                   pvalue = np.float64(2.2838747299772618e-05), 
#                   stderr = np.float64(0.11579645994688036), 
#                   intercept_stderr = np.float64(0.3346077236952637))

print("가중치 : ", model.slope)
print("편향 : ", model.intercept)
print("p값 : ", model.pvalue)

newdf = pd.DataFrame({'지상파' : [2.3, 8.7, 23.3]})
print('예측값2(종평 종영 시간-lingregress) : \n', np.polyval([model.slope, model.intercept], newdf))
# 결과 :
#  2.0723434 
#  7.01754012
#  18.29877011