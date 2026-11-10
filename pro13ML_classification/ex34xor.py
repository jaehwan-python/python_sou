# xor분류 : LogisticRegression과 SVM으로 분류

x_data = [
    [0, 0, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn import svm, metrics
x_df = pd.DataFrame(x_data)
print(x_df)
feature = np.array(x_df.iloc[:, 0:2])
label = np.array(x_df.iloc[:, 2])
print(feature)
print(label)
# 독립변수 : 
# [[0 0]
#  [0 1]
#  [1 0]
#  [1 1]]
# 종속변수 : 
# [0 1 1 0]


# 모델 생성 -> LogisticRegression  vs  SVM
lmodel = LogisticRegression()
# 선형 분류 모델

smodel = svm.SVC(kernel='rbf')
# RBF 커널을 사용하는 비선형 분류 모델
# kernel='rdf'인 경우  vs  kernel='linear'인 경우
lmodel.fit(feature, label)
smodel.fit(feature, label)

pred1 = lmodel.predict(feature)
print('lmodel pred : ', pred1)
pred2 = smodel.predict(feature)
print('smodel pred : ', pred2)
# 결과 : 
# lmodel pred :  [0 0 0 0]
# smodel pred :  [0 1 1 0]

acc1 = metrics.accuracy_score(label, pred1)
print('lmodel accuracy : ', acc1)
acc2 = metrics.accuracy_score(label, pred2)
print('smodel accuracy : ', acc2)
# 결과 : 
# lmodel accuracy :  0.5
# smodel accuracy :  1.0

