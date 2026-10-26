# https://m.blog.naver.com/waterhyacinth10/222696336271 
# iris dataset 사용하기 : 150행 4열
# 꽃의 종류 - 3가지, 4개의 특성(꽃받침과 꽃잎의 너비, 꽃잎의 길이)
# regression과 classification을 연습하기에 iris data가 그 표본으로 제일 좋다.

import pandas as pd
import matplotlib.pyplot as plt

iris_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/iris.csv")
print(iris_data.info())
print(iris_data.head(3))
# 결과 :       Sepal.Length  Sepal.Width  Petal.Length  Petal.Width   Species
#       0           5.1          3.5           1.4          0.2       setosa
#       1           4.9          3.0           1.4          0.2       setosa
#       2           4.7          3.2           1.3          0.2       setosa
print(iris_data.tail(3))
# 결과 :      Sepal.Length  Sepal.Width  Petal.Length  Petal.Width    Species
#   147           6.5          3.0           5.2          2.0        virginica
#   148           6.2          3.4           5.4          2.3        virginica
#   149           5.9          3.0           5.1          1.8        virginica

# 산점도 차트
plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'])
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃 잎 길이')
plt.title('붓 꽃 자료')
plt.show()

# 꽃의 종류에 따라 다른색(3가지)으로 출력
print()
print(iris_data['Species'].unique())
# 결과 : ['setosa', 'versicolor', 'virginica']

cols = []
for s in iris_data['Species']:
    choice = 0
    if s == 'setosa' : choice = 1
    elif s == 'versicolor' : choice = 2
    elif s == 'virginica' : choice = 3
    cols.append(choice)

# 산점도 차트
plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'], c=cols)
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃 잎 길이')
plt.title('붓 꽃 자료')
plt.legend()
plt.show()

# pandas의 시각화 기능
from pandas.plotting import scatter_matrix
iris_col = iris_data.loc[:, 'Sepal.Length' : 'Petal.Length']
scatter_matrix(iris_col, diagonal='kde')
# 커널 밀도 추정값(kde) : 데이터의 분포를 부드러운 곡선으로 표현함
plt.show()

# seaborn : Python에서 데이터를 그래프로 시각화하는 라이브러리
import seaborn as sns
sns.pairplot(iris_data, hue='Species', height=2)
plt.show()

# git을 중심으로 배포하는 클라우드 : '도커'  ->  동일한 환경을 맞추어서 작업하는 것(linux기반) ... 도커는 리눅스 환경에서만 운영된다. 
# 'CICD' 
# '도커'를 이용하여 프로젝트 해보기!
# 도커 : 작업환경을 자동화 하는 것

# 지금 우리가 배우는 모든 것은 linx환경에서 가상환경으로 anaconda를 깔고 vscode를 설치한다. 그리고 지금까지 한 모든 작업을 할 수 있어야 한다.
# 우리가 수업 시간에 한 환경을 linux 운영체제에서 만든 가상환경(anaconda)를 이용한다
# 거기서 github 공부해보기
# 아마존의 ec2서버와 rds

# 핵심 : 
# github공부
# 도커공부
# 운영체제와 가상환경 구분


# 1021 수업!
