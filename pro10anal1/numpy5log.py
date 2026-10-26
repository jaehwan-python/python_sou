# 편차가 큰 데이터에 대한 로그 변환
# 큰 값을 압축해서 데이터 간 격차를 줄이는 변환이 가능!

# ML에서 데이터 분석 시 log를 사용하면?
# 1) 스케일 차이를 축소해 준다. log(10) = 1, log(100) = 2, log(1000) = 3
# 2) 로그 변환하면 치우친 데이터를 정규분포에 가깝게 변경가능
# 3) 모델링에서 지수 관계를 선형 관계로 바꿔준다. ... Logistic Regression : LLM의 기반이다. 그러니 굉장히 중요하다

import numpy as np

np.set_printoptions(suppress=True, precision=6)
# 과학적 표기 형식을 모두 취소하여 유효숫자로 모두 보이게 하였다. = 우리가 쉽게 보기 위해서

print()

def test():
    values = np.array([345, 34.5, 3.45, 0.345, 0.01, 0.1, 10, 100])
    print('values의 2진로그 : ', np.log2(3.45), ' ', 'values의 상용로그 : ', np.log10(3.45), ' ','values의 자연로그 : ', np.log(3.45))
    # 결과:values의 2진로그 :  1.7865963618908067     values의 상용로그 :  0.5378190950732742     values의 자연로그 :  1.2383742310432684
    # 2진 로그 / 상용로그 / 자연로그(e)
    print('\n원본 값 : ', values)

    # 1. 상용로그
    log_values = np.log10(values)
    # values에 있는 각 값들에 대하여 상용로그를 씌움
    print('log_values(상용로그) : ', log_values)
    # values의 각 값들의 상용로그를 취했을 때의 값
    # 결과 : log_values(상용로그) :  [ 2.537819  1.537819  0.537819  -0.462181  -2.  -1.  1.  2. ]

    # 2. 자연로그(e)
    ln_values = np.log(values)
    # values에 있는 각 값들에 대하여 자연로그를 씌움
    print('ln_values(자연로그) : ', ln_values)
    # values의 각 값들의 자연로그를 취했을 때의 값
    # 결과 : [ 5.843544  3.540959  1.238374  -1.064211  -4.60517  -2.302585  2.302585  4.60517 ]


    # ** '정규화'와 '표준화' ** : 데이터 분석과 머신러닝에서 사용되는 서로 다른 크기를 가진 특성(feature)들을 일정한 기준으로 맞춰주는 feature scaleing방법이다.
    # = 데이터의 크기와 범위를 조정하여, 서로 다른 특성을 비교하거나 모델이 학습하기 쉬운 형태로 만드는 과정
    # 1. 정규화(normalization / min-max scaling) : 모든 데이터를 0 ~ 1사이 범위 내에 출력한다.
    #                                             신경망이나 이미지 처리 등 데이터의 범위가 명확해야할 때 주로 사용한다.
    #                                             -> 공식 : (데이터 - 최솟값) / (최댓값 - 최솟값)

    min_val = np.min(values)
    max_val = np.max(values)
    # 두 값에 대해서 '정규화'를 해보자.
    normalized = (values-min_val) / (max_val - min_val)
    print('정규화의 결과 : ', normalized)


    # 2. 표준화(stardardzation / z_score scaling) : 데이터의 평균을 0, 표준편차가 1이 되도록 변환하는 방식이다.
    #                                              -> 공식 : (데이터 - 평균) / 표준편차
    mymean = np.mean(values) 
    mystd = np.std(values)
    standardized = (values - mymean) / mystd
    print('표준화의 결과 : ', standardized)

    # 들쭉날쭉한 원본데이터를 잔잔하게 만드는 것이 중요하다. 그때 사용되는것이
        # 1. log
        # 2. 정규화
        # 3. 표준화
    # 이다. 나중에 scikit-learn에서 수식이 아닌 라이브러리로 불러오는 방법을 배울 것이다.
        
    # 모델학습시 모델에게 원본데이터를 주기보다 '정규화'와 '표준화'를 거친 데이터를 주어아 모델이 처리하기가 쉽다.


class LogTrans:
    # 편차가 큰 데이터를 로그 스케일 변환하고 그 역변환을 제공하는 클래스

    def __init__(self, offset:float=1.0):
        self.offset = offset
        # offset : 기준 위치에서 얼마나 떨어져 있는지 나타내는 값이다.
        # log를 취하기 전에 offset으로 고정값이 나온다.

    # 로그 변환 메서드 -> log를 써준다.
    def transform(self, x:np.ndarray) -> np.ndarray:
        return np.log(x + self.offset)

    # 역 변환 메서드  -> exp를 써준다.
    def inverse_transform(self, x_log:np.ndarray) -> np.ndarray:
        return np.exp(x_log) - self.offset

test()

print('\n-----------------------')

data = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000], dtype =float)
logObj = LogTrans()
# 이 코드를 통해서 LogTrnas를 수행할 객체가 생성됨


# 이건 '로그변환' :  수 -> 로그값
data_log_scaled = logObj.transform(data)
#logTrans 클래스에 data라는 값을 넣었을 때 로그값으로 바뀌어서 출력된다.


# 이거는 '역변환' :  로그값 -> 수
reversed_data = logObj.inverse_transform(data_log_scaled)

# 원본을 로그변환으로 바꾸었으면 다시 원래대로 돌아오는 역변환 과정을 해주어야 한다.

print('\n원본자료 : ', data)
print('로그변환을 하면 ~ : ', data_log_scaled)
print('역변환을 하면 ~ : ', reversed_data)

