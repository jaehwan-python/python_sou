# SVM 알고리즘은 머신러닝 알고리즘에서 가장 유명하고 많이 사용되고 있었다.
# SVM 알고리즘은 기본적으로 2개의 그룹(데이터)을 분리하는 방법으로 데이터들과 거리가 가장 먼 초평면(hyperplane)을 선택하여 분리하는 방법

# 결정 경계에 가장 가까이 위치하여 마진을 결정하고 초평면을 지탱하는 핵심 데이터 포인트들이다.
# 전체 데이터 중 서포트 벡터를 제외한 나머지는 모델 결정에 영향을 주지 않는다.


# 흑백 이미지 분류
# (이후 딥러닝에서 이미지를 분류하는 방법과 비교해보기)

# 핵심용어 : support vector, margin, kernel, 결정경계


# Support Vector 확인해보기
# support vector :  두 클래스를 나누는 경계선의 위치를 결정하는 핵심 데이터 점
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.datasets import make_blobs

# 변수설정
x, y = make_blobs(n_samples=50, centers=2, cluster_std=0.5, random_state=4)
print(x[:5])
y = 2 * y - 1
print(y[:5])
# 독립변수 :
#  [ [ 4.62196582  2.75549151]
#    [-2.81005093  9.94042522]
#    [-3.17329065  9.11271675]
#    [-2.47543352  8.30191204]
#    [-3.01561318  9.17140979] ]
# 종속변수 : 
#  [ 1 -1 -1 -1 -1 ]

# 변수에 대한 데이터들의 분포 확인
plt.scatter(x[y == -1, 0], x[y == -1, 1], marker = 'o', label = '-1 클래스')
plt.scatter(x[y == +1, 0], x[y == +1, 1], marker = 'x', label = '+1 클래스')
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()
plt.show()
print()

# SVM모델 제작
from sklearn.svm import SVC
model = SVC()

model = SVC(kernel='linear', C=1.0).fit(x, y)
xmin = x[:, 0].min()
xmax = x[:, 0].max()
ymin = x[:, 1].min()
ymax = x[:, 1].max()
xx = np.linspace(xmin, xmax, 10)
yy = np.linspace(ymin, ymax, 10)
x1, x2 = np.meshgrid(xx, yy) # 두 개의 1차원 배열로 2차원 좌표격자(grid)를 생성한다.
# a = np.array([1, 2, 3])
# b = np.array([10, 20])
# a, b = np.meshgrid(a, b)
# print(a)
# print(b)
# 결과 : 
# a :  [[1 2 3]
#       [1 2 3]]
# b :  [[10 10 10]
#       [20 20 20]]

z = np.empty(x1.shape)

for (i, j), val in np.ndenumerate(x1): # 배열좌표와 값쌍을 생성하는 반복기를 반환
    x_value = val
    y_value = x2[i, j]
    p = model.decision_function([[x_value, y_value]])
    z[i, j] = p[0]

plt.scatter(x[y == -1, 0], x[y == -1, 1], marker = 'o', label = '-1 클래스')
plt.scatter(x[y == +1, 0], x[y == +1, 1], marker = 'x', label = '+1 클래스')
plt.contour(x1, x2, z, levels = [-1, 0, 1], colors = 'k', linestyles = ['dashed', 'solid', 'dashed']) # 등고선을 그림 - 결정경계 시각화 목적
plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=300, alpha = 0.5)
x_new = [10, 2]
plt.scatter(x_new[0], x_new[1], marker = '^', s=100)
plt.text(x_new[0] + 0.03, x_new[1] + 0.08, 'test데이터')
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()
plt.title('svm 예측 결과')
plt.show()

print("\n support vector :", model.support_vectors_)
# 결과 : 
# support vector의 좌표  :  [[9.03715314 1.71813465]
#                             [9.17124955 3.52485535]]

# 설명
# support vector : 두 클래스를 나누는 경계선의 위치를 결정하는 핵심 데이터 점
# 그림을 보명 아래쪽 파란 점들과 위쪽 주황 점들을 나누는 선을 그린다. 이때 SVM은 양쪽 데이터와 가능한
# 멀리 떨어진 경계선을 찾는다.
# 경계에 가까운 점들이 "선이 이쪽으로 오면 안돼!"하고 경계선의 위치를 잡아주는 점들이 support vector이다
# <그림>
#     ×    ×    ×     주황 클래스
#          ×          ← 서포트 벡터
# ------------------  마진 경계
# ==================  "결정 경계선"
# ------------------  마진 경계
#        ●            ← 서포트 벡터
#    ●      ●         파란 클래스
# 서포트 벡터를 잡는 이유 : 두 클래스를 나누는 경계선을 어디에 그을지 결정하기 위해 필요하다.
# ex) 파란 점(클래스)과 주황 점(클래스) 사이에는 '선'을 여러 위치에 그을 수 있다 
# SVM은 그 중 양쪽 점들과 최대한 멀리 떨어진 '선'을 선택한다. 
# 이렇게 여유 공간인 마진을 확보하면 새로운 데이터도 안정적으로 구별할 수 있기 때문이다.
# 이때 경계 가까이에 있는 점들이 확보할 수 있는 여유 공간을 결정해요. 그 점들이 '서포트 벡터'이다.
# 비유하면 두 무리 사이에 울타리를 세울 때, 울타리 위치를 결정하는 것은 서로 가장 가까이 있는 사람들이지
# , 뒤쪽에 멀리 있는 사람들이 아닌 것과 같다.
# 즉, 서포트 벡터는 사람이 따로 넣어주는 것이 아니라, SVM이 학습하면서 찾아내는 경계 결정의 기준점이다.