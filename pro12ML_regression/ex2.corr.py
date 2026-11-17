
# 공분산과 상관계수

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns



# 자, 데이터를 불러오자~ 
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv")
print(data.head())
print(data.describe())
# 결과 : 
#       친밀도  적절성   만족도
#    0    3       4       3
#    1    3       3       2
#    2    4       4       4
#    3    2       2       2
#    4    2       2       2


# 평균과 표준편차는?
print("평균과 표준편차는 : " , np.mean(data.친밀도), ' ', np.std(data.친밀도))
print("평균과 표준편차는 : " , np.mean(data.적절성), ' ', np.std(data.적절성))
print("평균과 표준편차는 : " , np.mean(data.만족도), ' ', np.std(data.만족도))
print()


# 히스토그램은?
plt.hist([np.std(data.친밀도), np.std(data.적절성), np.std(data.만족도)])
plt.show()
# 아직 하나도 가공이 되지 않은 원본데이터의 시각화!


# 공분산은?
# 공분산 표현방법1. numpy함수
print("공분산은?")
print(np.cov(data.친밀도, data.적절성))
print(np.cov(data.친밀도, data.만족도))
# 공분산은 2개의 변수를 기준만 잡을 수 있다. ... 3개 불가능!
# 결과 : 
# [ [ 0.94156873    0.41642182 ]
#   [0.41642182     0.73901083 ] ]
# [ [ 0.94156873    0.37566252 ]
#   [ 0.37566252    0.68681588 ] ]
print()

# 공분산 표현방법2. pandas함수
print(data.cov())
# 위의 공분산은 numpy 유니버셜함수를 이용했고
# 이번에는 pandas의 DataFrame 함수를 사용했다.
# 결과 : 
#           친밀도       적절성       만족도
# 친밀도   0.941569     0.416422     0.375663
# 적절성   0.416422     0.739011     0.546333
# 만족도   0.375663     0.546333     0.686816
# 동일한 변수에 대한 공분산 = 해당 변수의 분산
print()

# 각 변수간의 관계(정비례인지 반비례인지)를 공분산으로 알아보았다.
# 그러면 해당 변수들의 데이터가 얼마나 골고루 퍼져있을까?


# 공분산을 표준화하면? = 상관계수!!
print("상관계수")
# 상관계수 표현방법1 : numpy함수
print(np.corrcoef(data.친밀도, data.적절성)) # 결과 : 0.4922
#                                             해석 : 친밀도와 적절성은 양의 상관관계가 존재한다
print(np.corrcoef(data.친밀도, data.만족도)) # 결과 : 0.4671
#                                             해석 : 친밀도와 만족도는 양의 상관관계가 존재한다.
# 결과 : 
# [ [ 1.            0.49920861 ]
#   [ 0.49920861    1.         ] ]
# [ [ 1.            0.46714498 ]
#   [ 0.46714498    1.         ] ]
print()

# 상관계수 표현방법2 : pandas함수(df)
print(data.corr())
print(data.corr(method='pearson')) # pearson대신에 spearman이나 kendall을 쓸 수도 있다.
# 변수는 연속형이기 때문에 정규성을 따른다.
# 결과 : 
#             친밀도       적절성        만족도
#    친밀도  1.000000     0.499209     0.467145
#    적절성  0.499209     1.000000     0.766853
#    만족도  0.467145     0.766853     1.000000


# 변수 간 관계파악 
print("\n 만족도에 따른 다른 특성 사이의 관계")
co_re = data.corr()
print(co_re['만족도'].sort_values(ascending=False))


# 시각화1
data.plot(kind='scatter', x='만족도', y='적절성')
plt.show()
plt.close()
# 만족도와 적절성의 관계를 그래프로 표현

# 시각화2
from pandas.plotting import scatter_matrix
attr = ['친밀도', '적절성', '만족도']
scatter_matrix(data[attr], figsize=(10, 6))
plt.show()
plt.close()
# 각 (모든) 변수 간의 관계를 여러 개의 그래프로 표현


# 전체화면에서 고장나서 아무 터치도 안먹을때
# 컨트롤 + alt + del눌러서 '작업관리자'로 들어간다. 그리고 해당 프로그램 작업닫기를 누른다.

# 시각화3
sns.heatmap(data.corr(), annot=True)
plt.show()
# heatmap을 사용하면 상관계수들을 조금 더 시각적으로 보기 좋게 표현된다.

# 시각화4
# "다음카페에서 가져온 코드"
# heatmap에 텍스트 표시 추가사항 적용해 보기  ---------------
corr = data.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)  # 상관계수값 표시
mask[np.triu_indices_from(mask)] = True
# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
fig, ax = plt.subplots()     # Set up the matplotlib figure

sns.heatmap(corr, mask=mask, vmin=-vmax, vmax=vmax, square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    ax.text(i + 0.5, len(corr) - (i + 0.5), corr.columns[i], ha="center", va="center", rotation=45)
    for j in range(i + 1, len(corr)):
        s = "{:.3f}".format(corr.values[i, j])
        ax.text(j + 0.5, len(corr) - (i + 0.5), s, ha="center", va="center")
ax.axis("off")
plt.show()

# 표준편차  ->  공분산  ->  상관계수
# 표준편차 : 한 변수가 얼마나 흩어져 있는가를 찾음. 값들이 평균에서 얼마나 떨어져 있는지를 나타냄.
# 공분산 : 두 변수가 함께 어떻게 변하는지 표현. 두 변수의 평균으로부터의 편차를 곱한 값의 평균
# 상관계수 : 공분산을 두 변수의 표준편차의 곱으로 나누어 단위와 척도의 영향을 제거한 값

# 실제 미국인, 일본인, 중국인 방문객의 파일을 통해 상관계수를 이해해보자.