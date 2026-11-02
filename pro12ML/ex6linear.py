
print("\n 모델 작성 방법3 : , linregress사용-모델 생성")
# 실습) IQ에 따른 시험 점수 예측

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

score_iq = pd.read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/score_iq.csv")
print(score_iq.head(3))
print(score_iq.info())
x = score_iq.iq
y = score_iq.score
print(x[:3])
print(y[:3])

print('상관 계수 : ', np.corrcoef(x,y)[0,1])
# x,y에 대한 상관계수
# 결과 : 0.88222
# = 매우 강한 양의 상관관계!!

plt.scatter(x, y)
plt.show()
# 위 그래프에는 x에 대한 y의 값들 데이터가 나타나있다.
# 잔차제곱합이 최소가 최는 추세선을 그어줄 것이다 = 선형회귀 방정식을 사용!

# 단순선형회귀분석 모델 생성 - 인과관계가 있다는 가정하에 진행
model = stats.linregress(x, y)
print(model)
# 결과 : LinregressResult( slope(weight : 기울기) = 0.6514309527270086, 
#                           intercept(bias : y절편) = -2.8564471221976078, 
#                           r-value = 0.8822203446134707, 
#                           p-value = 2.8476895206670203e-50, 
#                           stderr = 0.02857793440930537,
#                           intercept_stderr = 3.546211918048529 )
# 단순선형회귀분석만 가능하다.(다중 회귀X)
# 예측함수('predict()')가 없다.

# p값이 나왔으니 위에서 인과관계가 있다고 가정하고 넘어갔지만 한번 두 변수간의 인과관계를 파악해보고 넘어가자.
print("가중치 : ", model.slope)
print("편향 : ", model.intercept)
print("p값 : ", model.pvalue)
# 결과 : 
# - 가중치 :  0.6514309527270086
# - 편향 :  -2.8564471221976078
# - p값 :  2.8476895206670203e-50 > 0.05
# 해석 : 두 변수는 인과관계가 있다.
plt.scatter(x,y)
plt.plot(x, model.slope * x + model.intercept, c = 'r')
plt.show()
# predict()함수는 지원하지 않는다.
# 그래서 점수를 예측할 때는, 선형회귀방정식을 직접 만들어서 사용한다.

newdf = pd.DataFrame({'iq' : [55, 66, 77, 88, 150]})
print('점수예측 : \n', np.polyval([model.slope, model.intercept], newdf))
# 점수예측 : 
#  [ [ 32.97225528 ]
#    [ 40.13799576 ]
#    [ 47.30373624 ]
#    [ 54.46947672 ]
#    [ 94.85819579 ] ]



# 방법 1
# fit_model = LinearRegression().fit(x, y)

# 방법 2
# model2 = smf.ols(formula='y~x', data=df).fit()

# 방법 3
# model = stats.linregress(x, y)