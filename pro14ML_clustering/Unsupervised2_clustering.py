#  군집(Clustering)분석의 구분
# 1. 계층적 군집 : 군집을 단계적으로 합치거나 나누어 계층 구조를 만든다.
#    - 응집형(상향식) : 각 데이터를 개별 군집으로 시작하여 비슷한 군집끼리 합친다.
#                      → 연결 방법 : 최단연결법 / 최장연결법 / 중심연결법 / 평균연결법 / "와드연결법"
#    - 분리형(하향식) : 모든 데이터를 하나의 군집으로 시작하여 점차 작은 군집으로 나눈다.
#
# 2. 비계층적 군집 : 계층 구조를 만들지 않고 데이터를 군집으로 묶는다.
#    - 방법 : K-means clustering / 동시 군집 분석법 / 최적할당 군집 분석법
#    - 일반적으로 응집형과 분리형으로 구분하지 않는다.

# -----------------------------------------------------------------------
# 실습) 학생 11명의 시험점수 사용

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster 
# **linkage** : 학생들을 비슷한 점수끼리 차례로 합치고, 어떤 군집끼리 합쳐졌는지 기록한 배열을 반환한다.
# **fcluster** : linkage의 합친 기록을 원하는 기준(예: 최대 3개 군집)으로 잘라, 각 학생의 군집 번호를 반환한다.
students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
scores = np.array([76, 95, 67, 88, 67, 100, 53, 46, 89, 93]) # 1차원 배열
print('점수 : ', scores)

linked = linkage(scores.reshape(-1, 1), method='ward')
# (11,)(1차원)을 (11, 1)(2차원)로 변환: 각 행은 학생 1명, 열은 시험점수라는 특성 1개이다.
# 1차원 배열을 그대로 넣으면 linkage는 원래의 자료가 아닌 점 사이의 거리 배열로 해석한다.
# : 점수 차이를 사용해서 서로 점수 차이가 작은 학생들끼리 합친다. 
#   그리고 군집 내부 점수의 흩어짐이 가장 적게 증가하는 두 군집을 또 합친다.

# 시각화
plt.figure(figsize=(10, 6))
dendrogram(linked, labels=students)
plt.title('학생들 점수 군집')
plt.xlabel('학생이름')
plt.ylabel('거리')
plt.axhline(y=25, color='red', linestyle='--', label='cut at 25')
plt.legend()
plt.grid(True)
plt.show()
plt.close()
print()

# 계층정 군집분석 결과를 3개의 군집으로 나누기
clusters = fcluster(linked, t=3, criterion='maxclust')
print('학생 군집 결과')
for stu, cluster in zip(students, clusters):
    print(f"{stu} : cluster {cluster}")
# 결과 : 
# 학생 군집 결과
# s1 : cluster 3
# s2 : cluster 1
# s3 : cluster 3
# s4 : cluster 1
# s5 : cluster 3
# s6 : cluster 1
# s7 : cluster 2
# s8 : cluster 2
# s9 : cluster 1
# s10 : cluster 1
# 어떤 학생이 어떤 학생과 점수가 비슷한 군집을 이루고 있는지 알 수 있다.
print()

# 군집별 점수와 이름 확인
cluster_info = {}
for student, cluster, score in zip(students, clusters, scores.flatten()):
    if cluster not in cluster_info:
        cluster_info[cluster] = {"students":[], "scores":[]}

    # students군집 -> 
    cluster_info[cluster]["students"].append(student)

    # scores군집 -> 
    cluster_info[cluster]["scores"].append(score)
print(cluster_info)
# 결과 : {np.int32(3): {'students': ['s1', 's3', 's5'],   'scores': [np.int64(76), np.int64(67), np.int64(67)]}, 
#        np.int32(1): {'students': ['s2', 's4', 's6', 's9', 's10'],   'scores': [np.int64(95), np.int64(88), np.int64(100), np.int64(89), np.int64(93)]},
#        np.int32(2): {'students': ['s7', 's8'],   'scores': [np.int64(53), np.int64(46)]}}
print()

# 군집별로 평균점수와 이름 출력
for cluster_id, info in sorted(cluster_info.items()):
    avg_score = np.mean(info["scores"])
    student_list = ",".join(info["students"])
    print(f'군집{cluster_id} : 평균점수={avg_score:.2f},  학생들={student_list}')
# 결과 :
# 군집1 : 평균점수=93.00,  학생들=s2,s4,s6,s9,s10
# 군집2 : 평균점수=49.50,  학생들=s7,s8
# 군집3 : 평균점수=70.00,  학생들=s1,s3,s5

# LLM이 프로그램에 직접 들어가서 api를 사용해서는 안돼. 
# 지금까지 배운 Flask서버와 ML모델들을 사용할거야. 그리고 시각화를 사용할거야

# 군집별 시각화
x_position = np.arange(len(students))
y_scores = scores.ravel()  # 2차원인 데이터를 1차원으로 떨어트림
colors = {1:'red', 2:'blue', 3:'green'}
plt.figure(figsize=(10,6))
for i, (x, y, cluster) in enumerate(zip(x_position, y_scores, clusters)): # 차례대로 꺼내서 index를 붙임
    plt.scatter(x, y, color=colors[cluster], s=100)
    plt.text(x, y + 1.5, students[i], fontsize=12, ha='center')

plt.xticks(x_position, students)
plt.xlabel('Students')
plt.ylabel('Score')
plt.title('Score cluster')
plt.grid(True)
plt.show()

# 성적 그룹 분석, 고객 등급 분석, 사용자 패턴 분석 등을 군집화

