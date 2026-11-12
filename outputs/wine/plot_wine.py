import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine

wine = load_wine()
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(figsize=(9, 6), layout='constrained')
for label, color, marker in zip(range(3), ['#2563eb', '#d97706', '#15803d'], ['o', '^', 's']):
    rows = wine.target == label
    ax.scatter(wine.data[rows, 0], wine.data[rows, 6], label=f'클래스 {label} ({rows.sum()}개)',
               c=color, marker=marker, s=45, alpha=0.8, edgecolors='white', linewidths=0.4)
ax.set(title='Wine 데이터셋: 와인 178개의 특성과 정답 클래스',
       xlabel='알코올 (alcohol, 부피 %)', ylabel='플라보노이드 (flavanoids)')
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(title='정답 label: 포도 품종 구분')
fig.savefig('C:/works/projects/outputs/wine/wine-scatter.png', dpi=160, bbox_inches='tight')
