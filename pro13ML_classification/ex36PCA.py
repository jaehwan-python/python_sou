# 이제부터 이미지 분류에 대해서 알아보자.
# "이미지 분류"를 알기 위해서는 "차원 축소"에 대해서 이해해야만 한다.

# 디지털 이미지는 작은 점인 픽셀(pixel)들이 모여 만들어진다.
# 일반적인 8비트 컬러 이미지에서는 각 픽셀의 색을 R(빨강), G(초록), B(파랑) 값으로 표현한다.
# 각 색상 값은 "0~255"범위이며, 세 값을 조합하여 하나의 색을 만든다.
# 흑백 이미지에서는 보통 픽셀마다 0~255의 밝기 값 하나를 사용한다.
#
# 컴퓨터는 이미지를 이러한 숫자들의 배열로 처리한다.
# 모델에 따라 픽셀 값을 한 줄로 펼친 벡터로 입력하거나,
# 이미지의 가로·세로 구조를 유지한 배열로 입력한다.
# 이 숫자들을 바탕으로 모델은 선, 모양, 색 등의 패턴을 학습하여 대상을 분류한다.
#
# 다양한 이미지를 충분히 학습하면 위치, 크기, 배경 등이 달라도 대상을 구별하는 데 도움이 된다.
# 소리와 동영상 역시 숫자 데이터로 표현하여 패턴을 학습하지만,
# 데이터의 구조와 처리 방식은 이미지와 다르다.

# 이제 우리는 이러한 이미지를 SVM을 통해서 패턴을 알아차린다.

# 컴퓨터에게 고차원(고화질)의 데이터를 주면 픽셀칸을 많이 쓰게 되어 하나의 사진을 처리하는데도 오래 걸린다.
# 이는 많은 사진을 처리해야하는 svm에게 비효율적이다.
# 그래서 고차원의 사진을 저차원의 데이터로 떨어트려 해당 사진의 특징을 파악하도록 한다.
# 직렬로 나열된 픽셀들이 짧을 수록(저차원의 데이터일수록) 메모리를 아낄 수 있다. 그때 원본데이터의 특징을 유지하면서 차원을 떨어트려야한다. 이를 주성분 분석(PCA)라고 한다.
# 주성분 분석 : 원본데이터의 성질을 최대한 유지하면서 차원을 떨어트리는 것
# 이는 비지도학습으로 feature만 가지고 차원을 낮추는 것이다.

# Overfitting은 과적합 문제 : feature에 대한 label값을 예측하여 해당 패턴에 익숙해지는 것
# 이는 지도학습에서만 나타날 수 있는 특징아닌가?
# 근데 svm도 해당 사진을 너무 과하게 학습하는 overfitting이 발생할 수 있는가?


# 주성분 분석 vs 요인 분석
# 둘 다 여러 변수의 정보를 더 적은 차원으로 요약하지만 목적과 가정이 다르다.

# 1. 주성분 분석(PCA)
# 원래 변수들을 조합하여 데이터의 전체 분산을 최대한 보존하는 새로운 축(주성분)을 찾는다.
# 예) 이미지의 수많은 픽셀 값을 적은 수의 주성분 점수로 요약하여 모델의 입력으로 사용한다.
# 주로 차원 축소와 데이터 압축에 사용하며, label 없이 feature만으로 학습한다.
# 분산이 큰 방향을 보존하므로, 분류에 중요한 정보가 반드시 보존되는 것은 아니다.

# 2. 요인 분석(Factor Analysis)
# 여러 변수 사이의 상관관계를 설명하는, 직접 관측되지 않는 공통 요인을 추정한다.
# 각 변수는 공통 요인의 영향과 변수 고유의 영향 및 오차로 구성된다고 가정한다.
# 예) 여러 설문 문항의 응답이 함께 변하는 이유를 '만족도', '불안' 등의 요인으로 설명한다.
# 요인의 이름과 의미는 분석 결과와 문항 내용을 바탕으로 사람이 해석한다.

# 핵심 차이: PCA는 전체 변동을 적은 축으로 요약하고,
# 요인 분석은 변수들이 함께 변하는 이유를 공통 요인으로 설명한다.

# 그리고 우리는 이런 차원축소를 위해서 주성분 분석에 대해서 알아야 한다!

# ----------------------------------------------------------------------------------------
# 주성분분석(PCA) : 선형대수 관점에서, 입력데이터의 공분산 행렬을 고윳값 분해하고 이렇게 구한 
# 고유벡터에 입력 데이터를 선형변환하는 것이다.
# 이 고유벡터가 PCA의 주성분 벡터로서 입력 데이터의 분산이 큰 방향을 나타낸다.
# 입력 데이터의 성질을 최대한 유지한 상태로 고차원을 저차원 데이터로 변환하는 기법이다.

# "차원 축소"의 3가지 순기능
# 1) 차원이 낮아지면 대상에 대한 이해가 보다 쉬워지게 된다. 공간보다는 면, 면보다는 선, 선보다는 점
# 2) 연산속도가 개선된다.
# 3) 차원의 저주를 해결하는 열쇠가 된다. 차원이 커지면 메모리를 많이 사용하게 되는 문제를 해결해준다.

# 주요 개념 : 차원축소 / 주성분분석 / 이미지분류
# 이미지를 분류할 때 입력값이 너무 많으면, 주성분분석(PCA)으로 차원을 줄인(차원축소) 다음 분류 모델에 넣을 수 있다.
# "이미지 분류" : 사진이 무엇인지 맞히는 목적
# "차원 축소" : 입력 변수의 개수를 줄이는 과정
# "주성분분석(PCA)" ": 차원 축소를 수행하는 방법 중 하나

# ---------------------------------------------------------
# 1110(화)수업

# 데이터의 산점도에서 해당 2차원 데이터를 1차원으로 표현했을 때,
# 분산이 더 큰 방향으로 빛을 투영해주어야 한다.
# 왜냐하면 분산이 작고 밀집되어 있는 경우로 빛을 투영해주면,
# 원본 data의 성질을 많이 잃어버리기 때문이다.
# 이때 2차원을 1차원으로 떨어트릴때 원본 데이터를 최대한 유지하는 것을
# 주성분분석(pca)라고 한다.

# 특성공학 - : 좋은 model을 위해 입력 data를 가공하는 것
#         - 방법 - 차원축소 - 변수 제거
#                          - 주성분 분석
#                - scaling
#                - 변형 - binning : 연속된 자료를 구간화
#                       - dummy 

# 이미지 분류 과정
# 1) 원본 이미지  ->  픽셀숫자화  -> [[124, 85, ...], [97, 52, ...]] ->  배열로 표현
# 2) 모델학습(배열+정답)  ->  모델 생성

# ** 비지도 학습 - clustering / pca

# 실습) iris데이터를 그림으로 표현해보기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# 이미지 data 준비
img = np.random.randint(0, 256, (28, 28)) # 28x28 크기의 가상 흑백 이미지
print(img.shape) 
# 결과 : (28, 28)
vector = img.flatten()  # 1차원 벡터로 변환
print(vector.shape)
# 결과 : (784,) 
# 즉, 28 x 28개의 픽셀을 가진 이미지는 784개 벡터로 변환된다.

# iris 데이터 준비
iris = load_iris()
n=10
x=iris.data[:n, :2] # 'sepal length열', 'sepal width열'만 선택한다.
print('차원 축소 전 x : ', x, x.shape, type(x))
print(x.T)
# 결과 : 
# [[5.1 4.9 4.7 4.6 5.  5.4 4.6 5.  4.4 4.9]
#  [3.5 3.  3.2 3.1 3.6 3.9 3.4 3.4 2.9 3.1]]
print()

# 시각화1 : 각 sample의 두 특성 값을 선으로 연결하여 비교
plt.plot(x.T, 'o:')
plt.xticks(range(2), ['꽃받침 길이', '꽃받침너비'])
plt.grid(True)
plt.title('iris크기 특성')
plt.xlabel('특성의 종류')
plt.ylabel('특성값')
plt.legend(['표본 {}'.format(i+1) for i in range(n)])
plt.show()
plt.close()

# 시각화2 : 산점도
df = pd.DataFrame(x)
print(df)

ax = sns.scatterplot(x=0, y=1, data=df, markers='s', s=100, color='b')
for i in range(n):
    ax.text(x[i, 0] - 0.05, x[i, 1] + 0.05, '표본{}'.format(i+1)) 
plt.title('iris크기 특성')
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃받침 너비')
plt.show()
plt.close()
# 이제 분산이 큰 방향으로 직교하는 형태로 pca가 이루어지면 된다.

# 위 두 개의 그래프 결과 두 변수(꽃받침길이, 꽃받침너비)는 공통적인 특징이 있으므로 차원축소의 근거가 있다고 판단.
# PCA를 진행 - 선형변환을 통해 차원을 축소
# 순서1 : 입력 데이터의 공분산 행렬을 생성한다.
# 순서2 : 공분산 행렬의 고유벡터와 고윳값(고유벡터 크기)을 계산한다.
# 순서3 : 고윳값이 큰 순서대로 k개(PCA변환차수)만큼 고유벡터를 추출한다.
# 순서4 : 고윳값이 가장 큰 순서로 추출도니 고유벡터를 이용하여 새롭게 입력데이터를 변환한다.
# sklearn의 PCA를 이용하면 순서대로 진행을 한다.

# [제 1주성분] : 원본 데이터의 분산이 가장 큰 방향
pca1 = PCA(n_components=1) # 변환할 차원 수
x_low = pca1.fit_transform(x) # 특징 행렬을 낮은 차원의 근사행렬로 변환
print('x_low : ', x_low, ' ', x_low.shape)

# 값 비교
x2 = pca1.inverse_transform(x_low) # 주성분값 원복
print('원복 후 x2 : ', x2, x2.shape) # 2차원 : [[5.06676112 3.53108532]]
print('원본 : ', x[0, :])            # 1차원 :  [5.1 3.5]
print('주성분 : ', x_low[0])         # [0.30270263]
print('원복 : ',x2[0, :])            # 2차원 :  [5.06676112 3.53108532]


# [제 2주성분] : 제1주성분과 수직인 방향 중에서 분산이 가장 큰 방향 = 분산을 가장 많이 담는 방향
# pca1 = PCA(n_components=1) # 변환할 차원 수(제1주성분)
pca1 = PCA(n_components=2) # 제 1주성분(데이터 분산이 가장 큰 방향), 제 2주성분(제 1주성분과 직교하면서 분산이 두번째로 큰 방향)
x_low = pca1.fit_transform(x) # 특징 행렬을 낮은 차원의 근사행렬로 변환
print('x_low : ', x_low, ' ', x_low.shape)

# 값 비교
x2 = pca1.inverse_transform(x_low) # 주성분값 원복
print('원복 후 x2 : ', x2, x2.shape) 
print('원본 : ', x[0, :])          # 1차원 :  [5.1 3.5]
print('주성분 : ', x_low[0])       # 1차원 :  [0.30270263 0.04550957]
print('원복 : ',x2[0, :])          # 1차원 :  [5.1 3.5]

# 주성분 분석값을 기반으로 시각화 : PCA방향벡터
pc1 = pca1.components_[0] # components_ : 주성분 벡터
mean = x.mean(axis=0) # 데이터 평균(중심점)

df = pd.DataFrame(x)
ax = sns.scatterplot(x=0, y=1, data=df, markers='s', s=100, color='b')
for i in range(n):
    ax.text(x[i, 0] - 0.05, x[i, 1] + 0.05, '표본{}'.format(i+1)) 

# PCA축(화살표)
plt.quiver(
    mean[0], mean[1],  # 시작점(평균
    pc1[0], pc1[1],    # 방향
    scale=3, color='r', width=0.01
)
plt.title('iris크기 특성 + 제1주성분')
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃받침 너비')
plt.axis('equal') # x, y의 눈금 간격을 동일한 비율로 표시
plt.grid(True)
plt.show()
plt.close()

# ** pc1 : 데이터를 그 축에 투영했을 때, 투영된 좌표들의 분산이 가장 커지는 방향의 좌표축, PC1 좌표는 각 점을 그 축에 투영했을 때의 위치 값
# ** pc2 : PC1과 수직인 방향 중에서, 데이터를 투영했을 때 분산이 가장 커지는 좌표축, 각 데이터 점을 PC2 축에 투영했을 때의 위치 값
# ---------------------------------------------------------------------------------
print('***' * 10)
# 원본 열 4개를 차원 축소하여 2개의 열로 변환한 후 svm 분류 모델을 작성
x = iris.data
print(x[0, : ]) # 0행, 4열이 나온다.
pca2 = PCA(n_components=2) # 제 2주성분 분석 : 제 1주성분 분석으로 데이터가 가장 많이 퍼진 방향의 좌표(제 1주성분 분석)에 대해서 수직이면서 분산을 가장 많이 담는 좌표
x_low2 = pca2.fit_transform(x)
print('x_low2 : ', x_low2[0, :], ' ', x_low2.shape)

# "변동성 비율" 확인 : 각 주성분이 전체 데이터의 분산을 얼마나 잘 설명하는지에 대한 비율
print(pca2.explained_variance_ratio_) # [0.92461872 0.05306648] : 제1주성분에서 원본데이터가 92% 가까이 설명하고 있다.
x4 = pca2.inverse_transform(x_low2)   
print('최초자료 : ', x[0])           # [5.1 3.5 1.4 0.2]
print('차원축소 : ', x_low2[0])      # [-2.68412563  0.31939725]
print('차원복귀 : ', x4[0, :])       # [5.08303897  3.51741393  1.40321372  0.21353169]
print() 

iris1 = pd.DataFrame(x, columns=['sepal length', 'sepal width', 'petal length', 'petal width'])
print(iris1.head(3))
iris2 = pd.DataFrame(x_low2, columns=['var1', 'var2'])
print(iris2.head(3))
print()

# 원본데이터와 pca데이터로 만든 svm모델
from sklearn import svm, metrics
feature1 = iris1.values # 원본데이터
print(feature1[:3])
label = iris.target    
print(label[:3])


# <원본 데이터>
print('원본데이터로 svm분류 모델 작성')
# 1. svm모델 생성 및 학습
model1 = svm.SVC(C = 0.1, random_state=0).fit(feature1, label)
# 2. 예측 및 평가
pred1 = model1.predict(feature1)
print('model1 accuracy : ', metrics.accuracy_score(label, pred1))
# 결과 : 0.94

# <pca데이터>
print('pca데이터로 svm분류 모델 작성')
feature2 = iris2.values # pca데이터
print(feature2[:3])
# 1. svm모델 생성 및 학습
model2 = svm.SVC(C = 0.1, random_state=0).fit(feature2, label)
# 2. 예측 및 평가
pred2 = model2.predict(feature2)
print('model2 accuracy : ', metrics.accuracy_score(label, pred2))
# 결과 : 0.9466

# pca를 사용해도 결과는 비슷하게 나온다.