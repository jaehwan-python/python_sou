# < 선호도 분석 실습 >
# 일원카이제곱 분석 ㅏ방식이다.
# 5개의 스포츠 음료에 대한 선호도에 차이가 있는지 검정하기

# 귀무가설 : 스포츠 음료에 대한 선호도에도 차이가 없다. # 
# 대립가설 : 스포츠 음료에 대한 선호도에 차이가 존재한다.

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinkdata.csv")
print(data)
print(stats.chisquare(data['관측도수']))
# 결과 :       음료종류  관측도수
#         0      s1        41
#         1      s2        30
#         2      s3        51
#         3      s4        71
#         4      s5        61

# 판정 : 유의수준 0.05 > pavlue 0.00039이므로 귀무 가설을 채택한다.
# 스포츠 음료에 대한 선호도에 차이가 있다. 라는 의견이 받아들여짐

exp = [data['관측도수'].sum() / 5] * 5
print("기대 도수(exp) : ", exp)
stat, pv = stats.chisquare(f_obs=data["관측도수"], f_exp=exp)
print(f"검정 통계량(chi2) : {stat:.7f}")
print(f"유의 확률(p) : {pv:7f}")

# 시각화 
import matplotlib.pylab as plt
import koreanize_matplotlib
import numpy as np

# 기대도수
total = data['관측도수'].sum()
expected = [total / len(data)] * len(data)
x = np.arange(len(data))   # 음로 수만큼 x축 좌표
width = 0.35  # 막대 너비

plt.figure(figsize=(10, 5))
plt.bar(x - width / 2, data['관측도수'], width=width, label='관측도수')
plt.bar(x + width / 2, expected, width=width, label='기대도수', alpha=0.6)
plt.xticks(x, data['음료종류'])
plt.xlabel('음료종류')
plt.ylabel('도수')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 카이제곱 검정결과와 그래프를 근거로 어떤 음료가 더 인기 있는지 분석
data['기대도수'] = expected
data['차이(관측-기대)'] = data['관측도수'] - data['기대도수']
data['차이비율(%)'] = round(data['차이(관측-기대)'] / expected * 100, 2)
pd.set_option('display.max_columns', None)
# print(data)
data.sort_values(by='차이(관측-기대)', ascending=False, inplace=True)
data.reset_index(drop=True, inplace=True)
print(data)
# 결과 : 
#            음료종류  관측도수  기대도수  차이(관측-기대)  차이비율(%)
#        0     s4        71      50.8         20.2         39.76
#        1     s5        61      50.8         10.2         20.08
#        2     s3        51      50.8          0.2          0.39
#        3     s1        41      50.8         -9.8        -19.29
#        4     s2        30      50.8        -20.8        -40.94