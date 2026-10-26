# 통계량 : 데이터의 특징을 하나의 숫자로 요약한 것
# 표본 데이터를 추출하여 표본 통계량을 구한 후 이를 근거로 전체(모집단)의, 미지의, 미래의 경험하지 못한 데이터를 짐작가능하다.
# = 모집단으로 부터 표본 데이터를 추출하여 표본 통계량을 구한다.
# 평균 / 분산 / 표준편차 등을 사용
# 데이터의 대푯값 : '평균'(산술/기하/조화평균) / '중앙값' / '최빈값'
# 우리는 저 3가지 대푯값 중 평균을 중요하다


grades = [1, 3, -2, 4]
# 표본데이터 = 변량
# 리스트로 저장해두어야 한다.

def show_grades(grades):
    for g in grades:
        print(g, end = " ") # end = " " 옆으로 한칸 띄우기
show_grades(grades) # 클래스를 호출
print()

# 1. <분산>
# R을 이용하면 n(자유도)-1로 나누지만 파이썬에서는 n으로 나눈다.
# numpy를 이용하지 않고 순수 클래스를 이용하여 분산 구해보기 

# 1-1. "합" 구하기
def grades_sum(grades):
    tot = 0
    for g in grades:
        tot = tot + g
    return tot
print('합은', grades_sum(grades))


# 1-2. "평균 구하기"
def grades_ave(grades):
    ave = grades_sum(grades) / len(grades)
    return ave
print('평균은', grades_ave(grades))


# 1-3. "분산 구하기" -> 분산 : 편차 제곱의 평균 = 평균값 기준으로 다른 값들의 흩어진 정도
# 분산을 그래프로 나타낸 것 = 산포도
def grades_variance(grades):
    ave = grades_ave(grades)
    vari = 0
    for su in grades: # su는 변량
        vari = vari + (su - ave)**2
    return vari / len(grades) #     -> 파이썬 방식
    # return vari / len(grades)-1   -> R방식
print('분산은 ', grades_variance(grades))


# "1-4. 표준편차 구하기" -> 분산에 루트를 씌운것
def grades_std(grades):
    return grades_variance(grades) ** 0.5
print('표준편차는', grades_std(grades))

print("----------------------------------------------------------------------------------------------------------------------------------------------------")

# numpy를 이용하여 구하면 편하게 쓸 수 있다.
# 앞으로 우린 이런 방식으로 사용한다.
print('numpy 모듈이 지원하는 함수 사용')

import numpy
# 이 모듈에서는 numpy 라이브러리를 사용할 수 있다.

print("합은", numpy.sum(grades))
print("평균은", numpy.mean(grades))
print("분산은", numpy.var(grades))
print("표준편차는", numpy.std(grades))

# 수식은 몰라도 된다. 하지만 numpy모델을 불러서 쓰는 함수만 알고 있으면 된다.
# "W3C school 앱" / "데이터 사이언스 스쿨"에 들어가면 모든 numpy lib가 나온다.

# numpy에서 가장 중요한 점은 ndarray를 써서 벡터를 계산할 수 있다는 점이다.
# 지금은 단순히 리스트 형 자료를 계산했지만 numpy의 가장 큰 장점은 벡터값인 array을 계산할 수 있다는 것이다
