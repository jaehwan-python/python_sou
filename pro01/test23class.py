'''
0824(월)

<1교시>
두 점 사이의 거리 : (제곱근){(x1-x2)**2+(y1-y2)**2}

유클리디안 거리 : 두 점 사이의 가장 짦은 직선거리를 구하는 방법으로 2차원 뿐만아니라 여러차원으로 넓힌 개념
'''

'''
두 점사이의 거리를 클래스로 표현하기
'''

'''
지난 시간 정리

클래스 : 어떤 데이터와 그 데이터를 처리하는 기능이 서로 밀접하게 관련되어 있다면 하나로 묶어 처리할 수 있다.
이를 클래스로 구현 가능하다.


1. 두 점 사이의 거리
2. 기울기
3. 로그 처리

< 좌표의 거리와 기울기는 단순한 수학연습이 아니라 나중에 머신러닝 작업 시 등장하게 된다 >
1) 거리는 나중에 KNN, K-Means, Embedding 유사도 등과 연결되고,
2) 기울기는 선형회귀를 거쳐 미분, Gradient Descent, 딥러닝의 학습 원리로 연결된다.
3) 첨도, 왜도가 큰 (편차가 큰 데이터...)데이터를 로그변환하면 분포 개선, 범위 차이 축소 등으로 인해 모델을 안정적으로 수행가능하다.

'''

# 목요일 test : 15문제 / 2시간 / 뒤에 5문제가 10점짜리 문제 / 부분점수 있음 / 


# 1. 두 점 사이의 거리
import math # 수학관련 연산을 해야하기 때문에 math 함수를 불러옴
class CalcTest:
    def __init__(self, x1, y1, x2, y2, offset:float=1.0): # 새로 생성된 객체 속 생성자를 통해 두 점의 좌표를 얻음
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.offset = offset # 로그를 위한 속성 # 로그는 0과 음수를 허용하지않음으로 offset으로 여기에 대치(초기값으로 1을 줌)

    # 두 점 사이의 거리 : 유클리디안 계산 식으로 사용한다. a**2 + b**2 = c**2
    # 피타고라스 정리에 따라 두 점 사이의 직선 거리가 직각 삼삭형의 빗변이 된다.
    def distance(self):
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return (dx**2 + dy**2) ** 0.5
        return math.sqrt(dx**2 + dy**2)
    
# 2. 기울기 
    def slope(self): # 두 점 사이의 기울기(y의 변화량 / x의 변화량)
            dx = self.x2 - self.x1 # d : 변화량을 의미
            dy = self.y2 - self.y2
            if dx == 0 : 
                return None # x좌표가 0이면 기울기를 구할 수 없기 때문 = 분모가 0이라서
            return dy / dx 

# 3. 로그 : 데이터 분석에서의 로그는 큰 수를 작게 압축, 복잡한 연산 단순화, 데이터의 정규성 확보 목적으로 로그를 사용한다.
    def transform(self, x_list:list[float]): # 로그 변환
        return [math.log(x + self.offset) for x in x_list] # 로그 변환값이 등장함. 일반데이터를 로그변환함. 로그는 0과 음수를 허용하지 않는다. 그래서 offset을 주어줌

    def inverse_trans(self, x_list:list[float]): # 역변환 ... exp
        return [math.exp(x_log) - self.offset for x_log in x_list]

    
def main(): 
    ctest = CalcTest(1,2,4,6)
    print('거리 : ', ctest.distance())
    print('기울기 : ', ctest.slope())

    # 로그 처리
    data = [10.0, 100.0, 1000.0, 10000.0] # 이런식으로 편차가 큰 자료들이 있다.

    # 로그 변환 및 역변화
    data_log_scaled = ctest.transform(data)
    print('원본 자료 : ', data)
    print('로그 변환 자료 : ', data_log_scaled)

    reversed_data = ctest.inverse_trans(data_log_scaled) 
    reversed_data_round = [round(val, 1) for val in reversed_data] # 값에 대해서 반올림, 리스트 값을 하나씩 꺼내서 val값을 소숫점 첫째자리까지
    print('역 변환 자료 : ', reversed_data)

# 로그변환 후 다시 역변환하면 원래 값을 찾는다.


if __name__ == "__main__":
    main() # 현재 모듈이 메인 모듈이니? ㅇㅇ 그러면 메인 모듈로 메서드를 불러와!


'''
# 2. 기울기
import math # 수학관련 연산을 해야하기 때문에 math 함수를 불러옴
class CalcTest:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y2
        self.x2 = x2
        self.y2 = y2

    def distance(self):
        dx = self.x2 - self.x1
        dy = self.y2 - self.y2
        return (dx**2 + dy**2) ** 0.5
        return math.sqrt(dx**2 + dy**2)

    # 두 점 사이의 기울기(y의 변화량 / x의 변화량)
    def slope(self):
        dx = self.x2 - self.x1 # d : 변화량을 의미
        dy = self.y2 - self.y2
        if dx == 0 : 
            return None # x좌표가 0이면 기울기를 구할 수 없기 때문 = 분모가 0이라서
        return dy / dx

ctest = CalcTest(1,2,4,6)
print('기울기 : ', ctest.slope())

'''


'''
<2교시>
클래스의 포함과 상속 opp프로그램은 자원의 재활용을 위해 클래스가 또다른 클래스를 불러 쓸 수 있다.
- 포함(has-a) : class a에서 class b를 멤버로 포함시킨다. 
- 상속(is-a) : class a를 자식으로 두고 class b를 부모로 두는 방식. 클래스와 클래스 관계가 강하다.

우리는 상속을 통해서 다형성(polymophism)을 할 수 있다.
다형성 : 하나의 타입이나 메서드가 상황에 따라 여러가지 형태로 변할 수 있는 능력으로 보통 상속 관계를 바탕으로 진행된다.
오버라이딩

예시) 
자동차는 여러 부품으로 구성되어 있다. 그 때 그 자동차의 부품은 자동차의 부품 뿐만아니라 다른 제품의 부품으로 들어갈 수 있다. 
그래서 우리는 자주 쓰이는 부품, 엔진, 타이어, 핸들과 같은 부품을 클래스로 만드는 것이다. 다른 제품을 만들 때 클래스를 불러올 수 있다. 
필요할 때마다 그 클래스를 여러 제품에다 불러 쓸 수 있다 = 자원의 재활용이 가능하다.
그 때 그 클래스를 포함관계or상속관계로 사용할 수 있다.
'''







