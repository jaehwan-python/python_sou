# 실습2) 학생 11명의 시험점수 사용-Unsupervised2_clustering.py에서는 계층적 군집분석을 사용했지만 이번에는 비계층적 군집분석을 사용해본다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans 
# **linkage** : 학생들을 비슷한 점수끼리 차례로 합치고, 어떤 군집끼리 합쳐졌는지 기록한 배열을 반환한다.
# **fcluster** : linkage의 합친 기록을 원하는 기준(예: 최대 3개 군집)으로 잘라, 각 학생의 군집 번호를 반환한다.
students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
scores = np.array([76, 95, 67, 88, 67, 100, 53, 46, 89, 93]).reshape(-1, 1) # 1차원 배열
print('점수 : ', scores)

# k = 3
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
km_clusters = kmeans.fit_predict(scores)
print(km_clusters)
df = pd.DataFrame({
    'student' : students,
    'score' : scores.ravel(),
    'cluster' : km_clusters
})
print(df)
# 결과 : 
#          student  score  cluster
#      0      s1     76        2
#      1      s2     95        0
#      2      s3     67        2
#      3      s4     88        0
#      4      s5     67        2
#      5      s6    100        0
#      6      s7     53        1
#      7      s8     46        1
#      8      s9     89        0
#      9     s10     93        0
print()

print('군집별 평균 점수')
groupd = df.groupby('cluster')['score'].mean()
print('군집별 평균 : ', groupd)

# 시각화
x_position = np.arange(len(students))
y_scores = scores.ravel()
colors = {0:'red', 1:'blue', 2:'green'}
plt.figure(figsize=(10, 6))

# 학생별 군집을 색으로 구분하는 산점도
for i, (x, y, cluster) in enumerate(zip(x_position, y_scores, km_clusters)):
    plt.scatter(x, y, color=colors[cluster], s=100)
    plt.text(x, y+1.5, students[i], fontsize=10, ha='center')

# 중심점
centers = kmeans.cluster_centers_
for center in centers:
    plt.scatter(len(students) // 2, center[0], marker='X', c='black', s=200)

plt.xticks(x_position, students)
plt.xlabel('학생명')
plt.ylabel('점수')
plt.grid()
plt.show()