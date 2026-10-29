# 광고비(tv, radio, newspaper)와 판매량(sales)의 상관관계
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head())
print(data.describe())

attr = ['tv', 'radio', 'newspaper', 'sales']
data = data[attr]

print('\n광고 매체 간 상관관계')
print(data[['tv', 'radio', 'newspaper']].corr())

print('\nsales와 다른 특성 사이의 상관관계 (내림차순)')
co_re = data.corr()
print(co_re['sales'].sort_values(ascending=False))

sns.heatmap(co_re, annot=True)
plt.title('광고비와 판매량의 상관관계')
plt.show()
plt.close()