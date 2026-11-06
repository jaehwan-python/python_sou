# DecisionTree 분류 모델
# 키, 머리카락 길이로 남녀를 구분

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.tree import DecisionTreeClassifier,plot_tree

x = [[180, 15], [177, 42], [156, 35], [174, 65], [161, 25], [160, 45], [170, 65], [155, 55], [163, 5], [180, 15]]
y = [  'man',    'woman',   'woman',    'man',    'woman',   'woman',   'woman',   'woman',    'man',    'man']
# 내가 임의로 만든 x,y값
# 독립변수 : 키(x1), 머리카락 길이(x2)
# 종속변수 : 남녀(y) -> 0과 1로 주지 않고 대립되는 두 개의 값('man'과 'woman')으로 주어졌다.

feature_names = ['height', 'hair_length'] # 독립변수 명
class_names = ['man', 'woman']            # 종속변수 명

# 모델 생성
model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0).fit(x,y)
# criterion='gini'를 써도 된다.
# 노드에서 질문을 생성하여 그 질문에 대한 답을 가진 하위 노드로 이동하면서 점차 값에 가까워진다.

# 모델 성능 점수
print("예측값 : ", model.predict(x))
print("실제값 : ", y)
# 결과 : 
# 예측값 :  ['man' 'woman' 'woman' 'man' 'woman' 'woman' 'woman' 'woman' 'man' 'man']
# 실제값 :  ['man', 'woman', 'woman', 'man', 'woman', 'woman', 'woman', 'woman', 'man', 'man']
print(f"정확도 : {model.score(x, y)}")
# 결과 : 1.0
print()

# 새로운 데이터로 예측하기 -------------------------
new_data = [[177, 78]] # 이것이 새 x값 .. 기존의 데이터에는 없는 독립변수 값
print('새로 넣은 데이터로 예측한 값 : ', model.predict(new_data)) 
# 결과 : ['woman']

# 시각화
plt.figure(figsize=(10, 6))
plot_tree(model, 
        feature_names=feature_names,
        class_names = model.classes_, 
        filled=True,
        rounded=True, 
        fontsize=12
        )
plt.title("Decision Tree")
plt.show()