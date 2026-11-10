# RandomForest 분류 알고리즘
# 머신러닝에서 분류와 회귀분석에 널리 사용되는 강력한 앙상블 학습 알고리즘이다.
# 여러 개의 결정트리를 생성하고, 이들의 예측결과를 종합하여 최종적인 분류 결과를 도출한다.

# 앙상블 기법(voting / Bagging / Boosting) 중 Bagging(Bootstrap Aggregation)을 사용한다
# : 복수의 sample data와 DiscisionTree를 학습시키고 결과를 모으는 방식!!
# DecisionTree가 10개라면 sample data도 서로 다른 data로 10개가 있어야한다.

# 참고 : 우수한 성능은 Boosting, 과적합이 걱정된다면 Bagging을 선택해라

# 1. 데이터 전처리
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd. read_csv("https://raw.githubusercontent.com/jaehwan-python/pythonforktest/refs/heads/master/testdata_utf8/titanic_data.csv")
print(df.head(2))
print(df.info())
print(df.shape)
# 결과 : (891, 12)
# 문자열 데이터도 예측하려는 범주라면 종속변수로 사용할 수 있다.
# 범주가 2개면 이진 분류, 3개 이상이면 다중 분류이다.
# 숫자로 변환해야 하는지는 사용하는 모델이나 라이브러리에 따라 다르다.


print(df.isnull().any())
# 결과 : 
#   PassengerId    False
#   Survived       False
#   Pclass         False
#   Name           False
#   Sex            False
#   'Age'           True
#   SibSp          False
#   Parch          False
#   Ticket         False
#   Fare           False
#   'Cabin'         True
#   'Embarked'      True
# False  ->  빈 값이 하나도 없음
# True   ->  null값이 하나라도 있음

df = df.dropna(subset=['Pclass', 'Age', 'Sex'])
print(df.shape)
# 결과 : (714, 12)
# 내가 지정한 열 중 하나라도 null값이 있으면, 지정한 열의 null이 있는 해당 행을 모두 삭제하는 것이다.
print()

# 2. 독립변수, 종속변수 설정
# 독립변수(feature) 설정
df_x = df[['Pclass', 'Age', 'Sex']].copy() # feature
print(df_x.head(3)) 
# 결과 : 
#           Pclass    Age      Sex
#     0       3      22.0      male
#     1       1      38.0     female
#     2       3      26.0     female
# sex열이 모두 문자형이다.
# female, male과 같은 문자형 데이터를 숫자로 바꾸는 약간의 전처리 과정이 필요하다
# 전처리 -- "Sex열(male, female)"  ->  "Laebel Encoding(문자범주형, -> 정수)"

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
df_x['Sex'] = df_x['Sex'].astype('object')
df_x['Sex'] = encoder.fit_transform(df_x['Sex'])
print(df_x.head(3))
#         Pclass    Age     Sex
#    0       3     22.0      1
#    1       1     38.0      0
#    2       3     26.0      0
print()

# 종속변수(label) 설정
df_y = df['Survived']
print(df_y.head(3))

print()

# 3. **Overfitting예방** : 
# [방법1] : train / test split - 과적합 해결 목적
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.3, random_state=1)
print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)
# 결과 : (499, 3) (215, 3) (499,) (215,)

# <Overfitting 해결방법>
# 1. train / test split
# 2. k fold 
# 3. grid search

# 4. RandomForest 모델 생성
model = RandomForestClassifier(criterion='gini', n_estimators=500, random_state=12)
# DecisonTree를 사용하기에 gini imputity나 Entrophy impurity를 사용한다.
# 배깅방식(앙상블)이기때문에 bootstrap = True이다.
# crieterion = entropy도 가능
# n_estimators=500 : RandomForest가 사용하는 DecisionTree model의 갯수가 500개(100이 기본)
# **estimators(parameter) : 데이터를 학습하는 모델(추정기)로 입력값을 보고 정답을 예측하는 모델**
print(model)
# 결과 : RandomForestClassifier(n_estimators=500, random_state=12)
# 방금 생성한 model에 대한 설명

# 5. RandomForest 모델의 학습
model.fit(train_x, train_y)

# 6. 학습한 RandomForest모델의 예측(종속변수값)
pred = model.predict(test_x)
print('예측값 : ', pred[:5])
print('실제값 : ', np.array(test_y[:5]))
print('예측한 값이 실제값과 일치한 데이터의 갯수 : ', sum(test_y == pred))
print('전체 대비 맞춘 비율 : ', sum(test_y == pred) / len(test_y))

# 7. 평가
# 현재 RandomForest모델을 쓰는데 이러한 알고리즘은 500개의 DecisionTree가 각각 임의의 sample data를 받고 결과를 0과 1로 분류하고 있음을 알고 있어야 한다.
# 평가 방법 - ** 모델 학습 및 통계적 적합도 평가 - 가능성(우도) 
#           - ** 분류 정확도 평가 - "accuracy_score"  
#                                - "cross matrix"   ->  Acccuracy, Precision, Recall, F1-score, ROC-AUC
print('분류 정확도 : ', accuracy_score(test_y, pred))


# [방법2] 교차 검증(KFold)
from sklearn.model_selection import cross_val_score
cross_vali = cross_val_score(model, df_x, df_y, cv=5)
print(cross_vali)
print('교차 검증 평균 정확도 : ', np.round(np.mean(cross_vali), 4))


# RandomForestClassifier는 "중요 변수"를 제공한다
print("\n 중요 변수 확인하기 -----")
print("특성(변수,feature)중요도 : ", model.feature_importances_)
# feature_importances_ : 각 특겅이 예측에 기여한 정도(중요도)를 수치로 반환
# 중요도 값의 합은 1.0이다. 수치가 클수록 해당 변수가 불순도 감소에 더 많이 기여했다. 
# = 종속변수의 분류에 기여했다.
# 결과 : 특성(변수,feature)중요도 :  [0.16349895 0.48083309 0.35566796]
# 수치는 독립변수 열 순서와 동일하다 ->  'Pclass'  'Age'  'Sex'
#                                    = 'Age'라는 독립변수가 종속변수 0과1을 구분하는데 가장 많이 영향을 미쳤다.
# 저 3가지 확률을 모두 더하면 0이다.
print(0.16349895 + 0.48083309 + 0.35566796)
# 결과 : 1.0

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
n_features = df_x.shape[1]
plt.barh(range(n_features), model.feature_importances_, align='center')
plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립변수')
plt.yticks(np.arange(n_features), df_x.columns)  # 열 이름 표시
plt.show()
plt.close()

# 정리!!  : 
# 우리가 가진 모든 500개의 DecisionTree가 Pclass, Age Sex 이 3가지의 독립변수(1~500까지는 
# 모두 서로 다른 수치의 sample data)에 대해서 
# 예측(gini)하여 종속변수 0과1을 분류하는 것


print('전체 변수 대상으로 중요도 확인')
# ticket. cabin, Embarked열 : 문자형 -> 바로 사용 불가
# PassengerID, Name : Survived(종속변수)와 상관없음
df_imsi = df[['Pclass', 'Age', 'Sex', 'Fare', 'SibSp', 'Parch']].copy()
df_imsi['Sex'] = encoder.fit_transform(df_imsi['Sex'])
train_x, test_x, train_y, test_y = train_test_split(df_imsi, df_y, test_size=0.3, random_state=12)
# df_y가 survived이고 이를 학습용·평가용으로 나눔
model.fit(train_x, train_y)
# Survived를 정답으로 지정하고 train용 데이터로 학습

importances = model.feature_importances_
# RandomForest 모델에서 중요도를 가져옴

# 컬럼명 + 중요도
feature_df = pd.DataFrame({
    'feature' : df_imsi.columns,
    'importance': importances,
}).sort_values(by='importance', ascending=False)
print(feature_df)
# 결과 : 
#   feature  importance
# 1     Age    0.292984
# 3    Fare    0.276886
# 2     Sex    0.241788
# 0  Pclass    0.090802
# 4   SibSp    0.057529
# 5   Parch    0.040012
# importances에 df_y를 'Survived'라고 지정햇다.
# 이때 survived에 영향을 미치는 모든 독립변수들에 대한 기여도(중요도)를 큰 값부터 나타냄
# 우리는 임의로 독립변수를 지정했기에 Pclass, Age, Sex가 나왔다. 
# 여기서의 확률은 0과1 중 0을 선택할 확률을 뜻하는게 아니라, 
# 종속변수가 0과1을 고를 때 참조한 기여도가 전체 독립변수 중 얼마나 차지하고 있냐를 나타낸다.


# 이것이 RandomForest만이 가지고 있는 장점이다.
# = 어떤 변수가 중요한 변수인지 꺼내서 확인이 가능하다.
# Logistic Regression은 불가능하다. 만약 Logistic Regression에서 쓰고 싶다면
# Randomforest의 컬럼명에 대한 중요도를 조사한 후, 중요한 컬럼명을 골라서 해당 열에 대하여
# Logistic Regression을 하면 된다.

# 전체 변수에 대한 중요도를 시각화
import seaborn as sns

plt.figure(figsize=(8,5))
sns.barplot(x='importance', y='feature', data=feature_df, orient='h')
plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립변수')
plt.show()
plt.close()

# 각 독립변수들이 종속변수에 영향을 미치는 기여도를 나타내는데
# 종속변수가 survived라고 가정했을 때만 이런 기여도를 보이고 
# 다른 변수를 종속변수로 삼으면 독립변수의 중요도가 달라진다.
