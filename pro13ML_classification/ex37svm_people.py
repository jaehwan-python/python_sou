# fetch_lfw_people : 얼굴 인식용 이미지 데이터셋을 불러오는 함수

# SVM모델로 이미지 분류
# 세계 정치인들 일부 사진 데이터를 이용
# 전체 규모 : 총 5,749명의 인물에 대한 13,232개의 얼굴 이미지로 구성되어 있다.
# 주요 용도 : 얼굴인식, 이미지분류, 주성분분석(PCA) 등 머신러닝 학습에 쓰인다.
from sklearn.datasets import fetch_lfw_people
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline # 여러 작업을 하나의 처리 과정으로 만든다.

# PCA라는 비지도학습을 진행하고 나서 후에 지도학습 모델인 svm모델을 사용한다.

# 데이터 불러오기
faces = fetch_lfw_people(min_faces_per_person=60, color=False, resize=0.5)
# 60 : 한 사람당 60장 이상의 사진이 있는 자료만 사용. 
# 즉, 한 사람에 대한 이미지가 60장 이상이 안되는 사람은 제외.
# 흑백 크기는 절반
# "이런 62x47형태(픽셀)의 이미지 데이터는 총 2914개의 픽셀을 가지고 있고 이 픽셀을 모두 가로로 나열하여 1차원으로 만들어야 하는데
# faces.data는 해당 이미지를 이미 1차원으로 만든 것이다. 그리고 모든 이미지(1348장)에 대해서 표현한 것이기에 
# 현재 2차원 데이터로 표현되는 것이다." = 1348장에 대한 모든 이미지를 2914개의 열로 만들었다. 1차원 배열 1,348개를 행으로 모은 것이라서 2차원
# print(faces.DESCR)
print(faces.data)
# 결과 : 
#   [[0.53464055 0.5254902  0.49673203 ... 0.00653595 0.00653595 0.00261438]
#    [0.28627452 0.20784314 0.2522876  ... 0.96993464 0.9490196  0.9346406 ]
#    [0.31895426 0.39215687 0.275817   ... 0.4261438  0.7908497  0.9555555 ]
#    ...
#    [0.11633987 0.11111111 0.10196079 ... 0.5686274  0.5803922  0.5542484 ]
#    [0.19346406 0.21176471 0.2901961  ... 0.6862745  0.654902   0.5908497 ]
#    [0.12287582 0.09803922 0.10980392 ... 0.12941177 0.1633987  0.29150328]]
print(faces.data.shape)
# 결과 : 1348행, 2914열 = 2차원 배열
# 이미지 1348장, 이미지 한 장당 픽셀 특성 '2914개'
# 각 이미지는 세로 62 × 가로 47이며,
# 이를 길이 '2914'인 1차원 벡터로 펼친 것이다.
# faces.data는 이 벡터들을 행으로 쌓은 2차원 배열이다.
print(faces.target)
print(faces.target_names)
print(faces.target.shape)
print()
print(faces.images[1])
print(faces.target_names[faces.target[1]])

plt.imshow(faces.images[1], cmap='bone') # 원본 이미지 한 개를 시각화
plt.show()

# 원본이미지 15개 시각화
fig, ax = plt.subplots(3, 5)
for i, axi in enumerate(ax.flat):
    axi.imshow(faces.images[i], cmap='bone')
    axi.set(xticks=[], yticks=[], # x,y축 숨기기
            xlabel=faces.target_names[faces.target[i]])
plt.show()

# 이미지 한 장은 2914개의 1차원 배열이다. 이미지 한 장: [픽셀1, …, 픽셀2914]  → 2914차원 공간의 점 하나
# 그리고 특정 동일한 대상을 나타내는 이미지에 대해서는 2914개의 픽셀 특정 부분에서 공통적인 밝기를 나타내는 규칙이 있을 것이다. 그 패턴을 
# 여러 장의 사진을 통해서 학습한다.
# 이 때 이렇게 1차원으로 나열된 배열에 빛을 쏠 것이다. 빛을 쏠 때 분산이 가장 넓게 되는 방향으로 빛을 쏘아서 분산이 가장 크게 되는 직교를 찾는 좌표축을 찾느다.= pc1
# pc1과 수직인 방향 중 다음으로 많이 퍼진 방향을 pc2로 찾는다.

# [픽셀 밝기 2914개] → [PC1 좌표, PC2 좌표, …, PC100 좌표]
# 이후 svm모델은 그 100개의 입력받은 주성분 분석에 대한 좌표를 받아서 사람을 분류한다.


# 주성분 분석으로 이미지 차원을 축소시켜 분류 작업을 진행 ------------
pca = PCA(n_components=0.95) # 설명력 95%을 설명할 수 있는 주성분 갯수를 선택
x_pca = pca.fit_transform(faces.data)
print(pca.n_components_)
# 결과 : 
#  George W Bush
#  184

# PCA에서의 차원은 배열의 차원이 아니라, 사진 한 장을 표현하는 특성의 갯수이다. 현재는 사진 한 장당 2914개의 특성을 가지고 있다.
# 그런데 여기서 PCA적용을 하게 되면 픽셀 밝기 2914개 → 주성분 값 100개, 사진을 표현하는 특성 개수가 줄어듦
# PCA가 항상 2차원을 1차원으로 줄이는 것은 아니에요. 앞의 iris 예제는 특성이 길이·너비 2개여서 2개 → 1개로 줄였고, 얼굴에서는 2914개 → 100개처럼 줄이는 거예요.
# PCA 적용 후에도 전체 데이터는 (1348, 100)이라는 2차원 배열이에요. 사진 수는 같고, 각 사진을 표현하는 숫자 개수만 줄어든 것

n = 150 # 차원수는 분석가사 결과를 보고 판단함.
m_pca = PCA(n_components=n, whiten=True, random_state=0)
# whiten=True : 주성분의 스케일이 작아지도록 조정
x_low = m_pca.fit_transform(faces.data)
print('x_low : ', x_low, ' ', x_low.shape) #

# 주성분 처리된 이미지 15개를 시각화
fig, ax = plt.subplots(3, 5, figsize=(10, 6))
for i, axi in enumerate(ax.flat):
    axi.imshow(m_pca.components_[i].reshape(faces.images[0].shape), cmap='bone')
    # reshape(faces.images[0].shape) : [2914] -> [62, 47]
    axi.axis('off')
    axi.set_title(f'pc {i + 1}')
plt.suptitle('주성분 얼굴(EigenFaces)', fontsize=12)
plt.tight_layout()
plt.show() # 출력 이미지는 실제가 아니라 특징 패턴(얼굴 윤곽, 코그림자, 눈위치...)을 보여준다.
# svm 알고리즘은 실제 얼굴이 아니라 특징패턴으로 학습한다. 그래서 원본 이미지와 차이가 난다.
# 이런 식으로 svm알고리즘이 학습하게 한다.

# 이미지 분류에서 PCA와 SVM이 연결되는 과정(이미지 펼치기 → PCA로 특성 축소 → SVM 학습 → 새 사진 분류)
# 1. 이미지 한 장(세로 62 × 가로 47)을 펼치면 픽셀 밝기값 2914개가 된다.
#    faces.data에는 이미 각 이미지를 펼친 값이 들어 있으므로 직접 펼칠 필요가 없다.
#    한 장은 (2914,) 모양의 1차원 배열이지만, 특성이 2914개이므로 2914차원 공간의 점 하나이다.
#    여러 장을 모은 faces.data는 (사진 수, 2914) 모양의 2차원 배열이다.

# 2. 펼치기는 배열 모양만 바꾸며, 사진을 표현하는 숫자의 개수를 줄이지는 않는다.
#    PCA는 여러 학습 사진에서 픽셀 밝기가 함께 변하는 패턴을 찾아 특성의 개수를 줄인다.
#    PC1은 사진들을 투영했을 때 분산이 가장 큰 방향이다.
#    PC2는 PC1과 수직인 방향 중 투영된 값의 분산이 가장 큰 방향이다.
#    이후 주성분들도 앞서 구한 축들과 수직이면서 남은 분산을 가장 많이 담는 방향으로 구한다.

# 3. 위의 m_pca는 주성분 150개를 사용하므로 사진 한 장을 2914개 값에서 150개 좌표로 변환한다.
#    이 좌표는 픽셀 150개를 선택한 값이 아니라, 원래 픽셀값들을 조합한 새로운 특성값이다.
#    변환 결과 x_low는 (사진 수, 150) 모양이며, 일부 정보는 줄어들지만 주요 변동을 보존한다.

# 4. 이후 SVM에는 사진별 주성분 좌표 150개와 정답인 사람 번호(faces.target)를 함께 입력한다.
#    SVM은 같은 사람의 사진들을 같은 클래스로 분류하도록 클래스 사이의 경계를 학습한다.
#    이때 경계와 가까운 학습 데이터 사이의 간격(마진)을 크게 확보하도록 경계를 찾는다.

# 5. 새 사진도 픽셀을 펼친 뒤 학습된 PCA로 변환하고, 학습된 SVM으로 누구인지 예측한다.
#    PCA는 정답 없이 특성을 요약하고, SVM은 정답을 이용해 사람을 구분하는 기준을 배운다.
#    실제 성능 평가에서는 먼저 학습용과 평가용 사진을 나누고, PCA와 SVM은 학습용으로만 학습한다.
#    위에서 시각화한 주성분 얼굴은 PCA 축의 픽셀별 가중치이며, SVM의 입력은 각 사진의 주성분 좌표이다.

print('주성분 설명력 : \n', m_pca.explained_variance_ratio_[:10])
print('누적 설명력 : \n', m_pca.explained_variance_ratio_.sum())
# 0.935900 : n=100개로 얼마나 원본 정보를 유지했는지 확인한다

# 원본 vs 복원 이미지 비교
x_reconst = m_pca.inverse_transform(x_low)
fig, ax = plt.subplots(2, 5, figsize=(10, 4))
for i in range(5):
    # <원본 image>
    ax[0, i].imshow(faces.images[i], cmap='bone')
    ax[0, i].set_title('원본')
    ax[0, i].axis('off')

    # <복원 image>
    ax[1, i].imshow(x_reconst[i].reshape(faces.images[0].shape), cmap='bone')
    ax[1, i].set_title('복원')
    ax[1, i].axis('off')
plt.suptitle('PCA 복원 비교', fontsize=12)
plt.tight_layout()
plt.show() # 원본과 복원 이미지의 기본 특징은 크게 차이가 없다. = 패턴이 계속 유지가 된다.
print()

# svm모델 생성
svcmodel = SVC(C=1.0, random_state=1)
mymodel = make_pipeline(m_pca, svcmodel) # pca와 분류기를 하나의 작업으로 묶어
print('mymodel : ', mymodel)
# 결과 : Pipeline(steps=[('pca', PCA(n_components=150, random_state=0, whiten=True)), ('svc', SVC(random_state=1))])
# pca를 하고 svc를 하였다. (PCA를 사용한 mymodel과 SVM모델인 svcmodel을 연결하기 위해서 pipeline을 사용함)

# train/test split
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(faces.data, faces.target, random_state=1, stratify=faces.target)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
print(x_train[0])
print(y_train[0])

# svm모델 학습(train용 데이터로 학습한다)
mymodel.fit(x_train, y_train)
pred = mymodel.predict(x_test)
print('예측값 : ', pred[:10])
print('실제값 : ', y_test[:10])

# 평가
# 분류 정확도 평가(5가지) -> accuracy_score / confusion_matrix / classification_report # 이렇게 3가지를 통해서 평가가 가능하다.
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
confmat = confusion_matrix(y_test, pred)
print('confusion_matrix : \n', confmat)
# 결과 :  [[ 11   1   0   7   0   0   0   0]
#          [  0  50   0   9   0   0   0   0]
#          [  0   1  15  14   0   0   0   0]
#          [  0   0   0 133   0   0   0   0]
#          [  0   0   0  16  11   0   0   0]
#          [  0   1   0  11   0   6   0   0]
#          [  0   0   1   3   0   0  11   0]
#          [  0   0   0  12   0   0   0  24]]

print('accuracy : ', accuracy_score(y_test, pred))
# accuracy : 0.7744807121661721

print('classification_report : \n', classification_report(y_test, pred, target_names = faces.target_names))
# 결과 : 
#                     precision    recall  f1-score   support

#      Ariel Sharon       1.00      0.58      0.73        19
#      Colin Powell       0.94      0.85      0.89        59
#   Donald Rumsfeld       0.94      0.50      0.65        30
#     George W Bush       0.65      1.00      0.79       133
# Gerhard Schroeder       1.00      0.41      0.58        27
#       Hugo Chavez       1.00      0.33      0.50        18
# Junichiro Koizumi       1.00      0.73      0.85        15
#        Tony Blair       1.00      0.67      0.80        36

#        "accuracy"                           0.77       337
#         macro avg       0.94      0.63      0.72       337
#      weighted avg       0.85      0.77      0.76       337


# 분류 결과 시각화
print('분류 결과 시각화') 
fig, axes = plt.subplots(4, 6)
for i, ax in enumerate(axes.flat):
    ax.imshow(x_test[i].reshape(62, 47), cmap='bone')
    ax.set(xticks=[], yticks=[])
    ax.set_ylabel(faces.target_names[pred[i]].split()[-1], color='blue' if pred[i] == y_test[i] else 'red', fontweight='bold')
fig.suptitle('예측결과 : ', fontsize=12)
plt.tight_layout()
plt.show()
# 해석 : 맞으면 파란색, 틀리면 빨간색으로 보여주었다.

# Confusion_Matrix(오차 행렬)시각화(heatmap)
import seaborn as sns
sns.heatmap(confmat, annot=True, fmt='d', cmap='Blues', xticklabels=faces.target_names, yticklabels=faces.target_names)
plt.xlabel('예측')
plt.ylabel('실제')
plt.title('혼동행렬(confusion_matrix)')
plt.show()
# 해석 : 맞고 틀림을 표 형태로 확인이 가능하다.
#       'bush'가 틀리게 예측한 값이 제일 많다.

# ---------------------------------------------------------------------------------------------------------
print('\n 새로운 이미지를 입력하여 분류하기(중요!!) -----')

# 실습1 : "기존 이미지"로 분류 예측
test_img = faces.data[0].reshape(1, -1) # (1, 2914)형태로 변환 - 모델은 이 형태로 학습한다.
print('test_img : ', test_img)
test_pred = mymodel.predict(test_img)
print("실습1 예측결과 : ", faces.target_names[test_pred[0]], ', index : ', test_pred[0])
print("실습1 실제값 :  ", faces.target_names[faces.target[0]], ', index : ', faces.target[0])
# 결과 : 
# 실습1 예측결과 :  Colin Powell index :  1
# 실습1 실제값 :   Colin Powell index :  1

# 실습2 : **"완전히 새로운 이미지"로 분류 예측**
# bush.jpeg로 svm모델이 학습하지 않은 bush대통령의 다른 사진을 넣어주고 맞출 수 있는지 알아보자.
# 단계 : 이미지 읽기  ->  흑백변화  ->  크기 맞추기(62x47)  ->  1차원으로 변환  ->  예측하기 .. 추후에 CNN도 이와 동일한 과정을 거친다
from PIL import Image


# [1단계] : 이미지 읽기
img = Image.open('bush.jpeg')


# [2단계] : 흑백 전환
img = img.convert("L")


# [3단계] : 크기 맞추기(width x height)
img = img.resize((47, 62))


# [4단계] : 1차원으로 변환
# numpy 이미지는 (height x width)으로 세로, 가로 순서이다. 하지만 PIL 이미지는 반대로 (width x height)로 가로, 세로로 구성되어 있다.
# 이미지는 라이브러리(numpy vs PIL)마다 축의 순서가 다를 수 있다.
import numpy as np

# 이미지의 Lib확인하기
img_np = np.array(img) # img파일을 numpy배열로 변환하였다. 그래야 차원을 바꿀 수 있기 때문이다.
print('img_np : ', img_np)
# 결과 : 
# [[ 9  8  7 ... 63 63 63]
#  [ 9  8  7 ... 63 63 63]
#  [ 9  8  7 ... 63 63 63]
#  ...
#  [12  6 58 ...  9 10 10]
#  [12 10 10 ... 13 14 13]
#  [14 10  7 ... 15 17 17]]

# 정규화 하기
img_np = img_np / 255.0
print(img_np)
# 꼭하기!! : 정규화(학습데이터도 이렇게 되어 있다)
# 결과 : 

# 1차원으로 변환하기
img_flat = img_np.reshape(1, -1)
print(img_flat)
# 결과 : 
# 내가 넣어준 bush.jpeg 사진이 1차원 배열로 표현


# [5단계] : 예측하기
# 내가 넣어준 사진을 svm모델이 받게되면 자신의 학습데이터에 기반해서 이를 조지부시라고 찾을 수 있을지 확인해본다.
new_pred = mymodel.predict(img_flat)
print('실습2 예측결과 : ', faces.target_names[new_pred[0]], ', index : ', new_pred[0])
# 예측 성공!!...내가 입력한 사진(bush.jpeg)를 내가 만든 정확도 77%인 svm모델이 보고 이가 조지부시임을 알아차림!!

# 시각화 + 예측
plt.imshow(img_np, cmap='bone')
plt.title(f'예측 : {faces.target_names[new_pred[0]]}')
plt.axis('off')
plt.show()
# 참고 : 정확도를 높이려면 밝기/위치 정렬등의 작업이 필요하다!