# 계층적 군집분석 : 데이터를 단계적으로 묶어 군집을 형성하는 알고리즘
# 거리가 가까운 데이터부터 계속 묶어가는 방식
# 군집 수를 미리 정하지 않아도 된다. 구조는 덴드로그램으로 확인한다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster # clustering을 사용하고 그 구조를 뎅드로그램으로 확인해보자.
from sklearn.datasets import load_iris # 이번에는 붓꽃 데이터셋에서 label이 없다고 가정하고 보자.
from sklearn.preprocessing import StandardScaler

iris = load_iris()
x = iris.data
y = iris.target  # y값은 추후 참고를 위해서 그냥 꺼낸둔 것일 뿐, clustering에서 사용X
labels = iris.target_names

df=pd.DataFrame(x, columns=iris.feature_names)
print(df.head(2))
# 결과 : 
#    sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)
# 0                5.1               3.5                1.4               0.2
# 1                4.9               3.0                1.4               0.2
print()

# Scaling(표준화/정규화)
scalar = StandardScaler()
x_scaled = scalar.fit_transform(x)
# 입력데이터(x)를 표준화/정규화 함

# 계층적 군집분석
z = linkage(x_scaled, method='ward')

# 덴드로그램
plt.figure(figsize=(12, 5))
dendrogram(Z=z)
plt.title('iris데이터로 계층적 군집분석(응집형)')
plt.xlabel('샘플')
plt.ylabel('거리(유클리드)')
plt.show()

# 덴드로그램을 분리하여 최대 3개의 군집을 만들어보자
clusters = fcluster(Z=z, t=3, criterion='maxclust')
df['cluster'] = clusters
print(df.head(3))

# 시각화(산점도)
plt.figure(figsize=(6, 5))
sns.scatterplot(x=x_scaled[:,0], y=x_scaled[:,1], hue=clusters, palette='Set1')
# hue=clusters : clusters를 기준으로 색을 달리 표시
# palette='Set1' : 색상과 스타일을 지정
plt.title('군집결과')
plt.xlabel('feature1')
plt.ylabel('feature2')
plt.show() # 꽤 비슷하게 나눠짐. 군집은 label이 없다.

print('실제 label : ', y[:10])
print('군집 결과 : ', clusters[:10])
# 결과 :
# 실제 label :  [0 0 0 0 0 0 0 0 0 0]
# 군집 결과 :  [1 1 1 1 1 1 1 1 1 1]  # 실제 0이 군집1로 군집화 되었다.
# : 데이터의 앞 쪽에 있는 10개의 데이터는 label이 '0'인 setosa데이터이다. 그리고 그 군집은 1번 군집에 속한다

print('\n 군집 결과 검증 ---')
print('교차표 - 실제label vs 군집결과')
ct = pd.crosstab(y, clusters)
print(ct)
# 결과 : 
#            col_0     cluster1   cluster2   cluster3
#            row_0            
#   0(setosa)            49          1          0
#   1(versicolor)         0         27         23
#   2(verginica)          0          2         48
# row_0(실제 label) :  0 - setosa, 1 - versicolor, 2 - verginica
# col_0(군집 결과)  : cluster1, cluster2, cluster3
# setosa는 완벽히 분리된다.
# 반면 versicolor와 verginica는 일부 데이터가 서로의 군집에 속해 있다.

print('\n 교차표 보조 설명 : 각 클래스가 가장 많이 속한 군집')
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f'-실제 클래스 {i} -> 군집{max_cluster} (갯수 : {ct.iloc[i].max()})')
print()
# 교차표 보조 설명 : 각 클래스가 가장 많이 속한 군집
#   -실제 클래스 0 -> 군집1 (갯수 : 49)
#   -실제 클래스 1 -> 군집2 (갯수 : 27)
#   =실제 클래스 2 -> 군집3 (갯수 : 48)

# 정량적 평가 : 군집 결과가 실제 정답과 얼마나 유사한지를 수치로 표현
from sklearn.metrics import adjusted_mutual_info_score, normalized_mutual_info_score
# [평가지표1] : adjusted_mutual_info_score : ARI(Adjusted Rand Index) - 같은 그룹끼리 잘 묶였는지 평가
ari = adjusted_mutual_info_score(y, clusters)
print(f'평가지표ARI ==>  {ari:.4f}')
# <해석기준>
# 0.7이상 : 매우 잘된 군집
# 0.5 ~ 0.7 : 잘된 군집
# 0.5미만 : 약간의 문제가 있는 군집
# 결과 : 0.6713 ... 잘된 군집이다!!

# [평가지표2] : normalized_mutual_info_score : NMI(Normalized Mutual Info) 
# - 정보량을 기준으로 얼마나 유사한 지를 확인(군집간 얼마나 같은 정보를 공유하고 
#   있는가를 수치로 표현)
nmi = normalized_mutual_info_score(y, clusters)
print(f'평가지표NMI ==>  {nmi:.4f}')
# <해석기준>
# 0~1사이 - 1에 가까움 : 완벽
#         - 0에 가까움 : 매우 다름
# 결과 : 0.6755 ... 다소 같음!

