# matplotlib : 플로팅 라이브리로 그래프 작성을 위해서 다양한 함수를 제공해 주었다.
# 데이터 시각화는 복잡하고 방대한 양의 데이터를 char, graph, map등의
# 시각적 형태로 표현하여 정보를ㄹ 직관적으로 이해하고 빠른 의사결정을 돕는다.mlㄷ 

# 시각화하기!! = 어떤 그래플를 쓸 때 사용한다. 
# Seaborn이란? - 자신의 구실과 파이썬을 드래닌다.

# 시각화의 중요성
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family="malgun gothic")  # AppleGothic 한글깨짐 방지
plt.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지 
import koreanize_matplotlib   # 얘를 이용하면 위 두 줄을 대체할 수 있다.

x = ['서울', '인천', '수원']   # 그래프의 x축에 값은 인덱스(수치) : 문자열은 올 수 없다. 지금 여기 있는 문자들은 문자열이 아니라 인덱스의 번호이다(list vs array생각!!)
y = [4, 3, 8] # 여기 각 값을 tuple, list으로 줄 수 있고 dict과 set은 안된다.

plt.xlabel("지역명")
plt.ylabel("투자액")

plt.xlim([-1, 3])
plt.ylim([0, 10])

plt.yticks(list(range(0, 11, 3))) # y축의 라벨을 인위적으로 변경한다. (위치표시지점 = tick)
plt.plot(x,y)
plt.show()

# 모든 차트가 그려지는 영역 : figure
# 그리고 한 figure는 여러개의 도표 그림인 plot으로 표현된다.
# plot은 y-axis와 x-axis로 구성이 된다. 
# axes은 x-axis와 y-axis가 모인 하나의 그래프인 plot을 의미한다
# 차트에서는 숫자만 표현가능하고 문자는 표현할 수 없다.

data = np.arange(1, 11, 2)
plt.plot(data) # x축의 구간은 자동 설정된다.
x = [0, 1, 2, 3, 4]
for a, b in zip(x, data):
    plt.text(x=a, y=b, s=str(b))
# 1  3  5  7  9라는 구간이 그래프 위에 보인다.
plt.show()


x=np.arange(10)
y=np.sin(x)
print(x, y)
# 1. plt.plot(x, y)
# 2. plt.plot(x, y, 'bo') # color와 마커를 주었다.
# 3. plt.plot(x, y, 'go--', linewidth=2, markersize=12) # 이렇게 옵션을 줄수록 그래프가 다양해진다
plt.show()
# sin 삼각함수 그래프의 모양이 나타난다. 그때의 각 값들은 라디안이다.


# hold : 복수의 plot으로 여러 개의 차트를 겹쳐 그림 = 한번에 여러개의 차트를 같이 그림 = 겹친것 처럼 보임
x=np.arange(0, np.pi * 3, 0.1)
print(x)
y_cos = np.cos(x)
y_sin = np.sin(x)
plt.figure(figsize=(10, 5)) # figure : 그림을 그리는 공간 ... 그래프 전체 크기 지정(w, h)

plt.plot(x, y_sin, 'r') # 선으로 그림
plt.plot(x, y_cos)      # 산접도로 그림
plt.legend(['사인', '코사인']) # 범례
plt.show()


# subplot :  : 하나의 Figure를 여러 개의 Axes(plot)으로 나누기
plt.subplot(2, 1, 1)  # 1행
plt.plot(x, y_sin)
plt.title('sine')
plt.subplot(2, 1, 2)  # 2행
plt.plot(x, y_cos)
plt.title('cosine')
plt.show()


print()
irum = ['a','b','c','d','e']
kor = [80, 50, 70, 70, 90]
eng = [60, 70, 80, 90, 100]
plt.plot(irum, kor, 'ro-')
plt.plot(irum, eng, 'bo--')
plt.ylim([50, 100])
plt.title('시험 점수')
plt.legend(['국어', '영어'], loc='best')  # loc=1 ~ 4
plt.grid(True)


# 그래프를 이미지 파일로 저장
fig = plt.gcf()
plt.show()
fig.savefig('mplot1.png')


# 이미지 읽기
from matplotlib.pyplot import imread
img = imread('mplot1.png')
plt.imshow(img)
plt.show()