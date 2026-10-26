# license : 정보처리기사 / SQLD / ADsP / ADP / aws(aws는 네트워크 자격증) ... (Database자격증으로는 oracle것만 취급. 근데 비쌈 한 200정도)

# 1021 수업

# 자전거 공유 시스템 분석용
#    : kaggle 사이트의 Bike Sharing in Washington D.C. Dataset를 편의상 조금 변경한 dataset을 사용함

# columns : 
#        'datetime', 
#        'season'(사계절:1,2,3,4), 
#        'holiday'(공휴일(1)과 평일(0)), 
#        'workingday'(근무일(1)과 비근무일(0)), 
#        'weather'(4종류:Clear(1), Mist(2), Snow or Rain(3), Heavy Rain(4)), 
#        'temp'(섭씨온도), 'atemp'(체감온도), 
#        'humidity'(습도), 'windspeed'(풍속), 
#        'casual'(비회원 대여량), 'registered'(회원 대여량), 
#        'count'(총대여량)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
# 위 5개 lib는 앞으로 계속 사용한다.

from scipy import stats
# scipy를 사용할 것이다.

plt.style.use('ggplot')
# 파이썬에서 R을 불러다 쓸 수 있다.
# R의 기능 중 하나 : ggplot style(lib)을 사용한다.

train = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv", parse_dates=['datetime'])
# datetime을 보기 쉽게 바꿔주기 위해서 parse를 써줌
# datetime, season, holiday, workingday, weather, temp, atemp, humidity, windspeed, casual, registered, count

# < EDA(Exploratory Data Analysis) : 탐색적 데이터 분석 >
pd.set_option('display.width', None)
# 위에서 가져온 train.csv 열이 너무 많아도 그냥 다 보여줘

print(train.info())
print(train.dtypes)
print(train.shape)  # (10886, 12)
print(train.columns)

print(train.head(3))
#                  datetime  season  holiday  workingday  weather  temp   atemp  humidity  windspeed  casual  registered  count
#     0 2011-01-01 00:00:00       1        0           0        1  9.84  14.395        81        0.0       3          13     16
#     1 2011-01-01 01:00:00       1        0           0        1  9.02  13.635        80        0.0       8          32     40
#     2 2011-01-01 02:00:00       1        0           0        1  9.02  13.635        80        0.0       5          27     32

print(train.temp.describe())
# count    10886.00000
# mean        20.23086
# std          7.79159
# min          0.82000
# 25%         13.94000
# 50%         20.50000
# 75%         26.24000
# max         41.00000
# Name: temp, dtype: float64

print(train.isnull(). sum()) # ... null인 데이터가 하나도 없다.
# 이렇게 train.csv의 데이터를 확인한다.

# 저 DataFrame에서 년월일시분초를 기준으로 분리하여 칼럼을 추가할 수 있다.
#.dt는 시간 계산 연산자. 이를 사용하여 여러 기준으로 시간을 구분할 수 있다. 
train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['date'] = train['datetime'].dt.date
train['hour'] = train['datetime'].dt.hour
train['minure'] = train['datetime'].dt.minute
train['second'] = train['datetime'].dt.second
# train이라는 df에 열을 추가해라. 그 열은 datetime이라는 기존 열의 year / month ...만 계산하여 만든 새로운 열이다.
# 즉, 6개의 열이 생겼다.

print(train.head(2))
print(train.columns)


# 대여량 시각화 : 년, 월, 일, 시간 대별 시각화를 해보자 ~ 
figure, (ax1, ax2, ax3, ax4) = plt.subplots(nrows = 1, ncols=4)
# 1행 4열짜리 figure가 만들어짐
figure.set_size_inches(15, 5)
sns.barplot(data=train, x='year', y='count', ax=ax1)
sns.barplot(data=train, x='month', y='count', ax=ax2)
sns.barplot(data=train, x='date', y='count', ax=ax3)
sns.barplot(data=train, x='hour', y='count', ax=ax4)
ax1.set(ylabel='대여수', title='년도별 대여')
ax1.set(ylabel='월', title='월별 대여')
ax1.set(ylabel='일', title='일별 대여')
ax1.set(ylabel='시간', title='시간별 대여')
plt.show()

# boxplot : 기본 방향은 세로이다. 그래서 orient='v'를 적어줌
fig, axes = plt.subplots(nrows=2, ncols=2)
# 2행 2열짜리 figure가 만들어짐
fig.set_size_inches(14, 12)
sns.boxplot(data=train, y='count', orient='v', ax=axes[0][0])
sns.boxplot(data=train, y='count', x='season', orient='v', ax=axes[0][1])
sns.boxplot(data=train, y='count', x='hour', orient='v', ax=axes[1][0])
sns.boxplot(data=train, y='count', x='workingday', orient='v', ax=axes[1][1])
axes[0][0].set(ylabel='대여수', title='대여')
axes[0][1].set(xlabel='계절', ylabel='대여수', title = '계절별 대여량')
axes[1][0].set(xlabel='시간', ylabel='대여수', title = '시간별 대여량')
axes[1][1].set(xlabel='대여수', ylabel='대여수', title = '근무일에 따른 대여량')
# axes의 xlabe과 ylabel을 찾아서 이름을 지칭해줌
plt.show()


# 산점도 : regplot - 산점도와 회귀선 그리기 - 온도 / 습도 / 풍속
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(12, 5))
sns.regplot(x='temp', y = 'count', data=train, ax=ax1)
sns.regplot(x='humidity', y = 'count', data=train, ax=ax2)
sns.regplot(x='windspeed', y = 'count', data=train, ax=ax3)
plt.show()

# maria db의 자료를 꺼내서 flask서버에 보내는 방법 배우기!!
# 왜? 우리는 python으로 만든 dataframe을 flask서버에서 보이게 할 것이기 때문이다!!
# fprodb로 이동!!