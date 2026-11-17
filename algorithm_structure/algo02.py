# 순차 탐색으로 특정 값의 위치 확인

def searchFunc(aa, x):
    n = len(aa)
    for i in range(0, n):
        if x == aa[i]:
            return i # 같다면 index=i를 반환한다.
    return -1 # 만약 해당 값이 없다면 '-1'을 반환한다.

values = [17, 92, 18, 33, 55, 7, 32, 44]
# 학습목표 : 해당 리스트에서 특정 숫자가 몇번째에 있는지 위치를 찾아보자!!
print(searchFunc(values, 18))
# values에서 18이라는 값을 찾아줘~
print(searchFunc(values, 17))
print(searchFunc(values, 44))
print(searchFunc(values, 44))
print(searchFunc(values, 0))
# 항상 최악의 경우를 생각해야하기에 빅오표기법 : o(n)으로 설정한다.

print('\n**정렬 알고리즘** ------------')
# 정렬 알고리즘(Sorting Algorithm) : 컴퓨터 과학에서 리스트나 배열에 담긴 원소들을 특정한 순서(오름차순, 내림차순, 사전순 등)에 따라 
#                                   새로 배열하는 알고리즘

# 사용 목적 : 데이터를 원하는 기준에 따라 순서대로 배치하기 위해 사용한다.

# 종류 -> 
# (1) O(n²) 시간 복잡도를 갖는 알고리즘 (구현이 쉽지만 데이터가 많아지면 느림)
# • 버블 정렬 (Bubble Sort): 인접한 두 원소를 비교하여 자리를 계속 교환하는 방식.
# • 선택 정렬 (Selection Sort): 전체 데이터 중 가장 작은(또는 큰) 원소를 찾아 맨 앞과 교환하는 방식.
# • 삽입 정렬 (Insertion Sort): 앞에서부터 차례대로 이미 정렬된 부분과 비교하여 자신의 위치를 찾아 삽입하는 방식.

# (2) (O(nlogn)) 시간 복잡도를 갖는 알고리즘 (평균적으로 빠름)
# • 병합 정렬 (Merge Sort): 분할 정복(Divide and Conquer) 방식으로 반으로 쪼갠 뒤 다시 정렬하며 합치는 방식 (안정 정렬).
# • 퀵 정렬 (Quick Sort): 기준점(Pivot)을 설정하고 피벗보다 작은 값과 큰 값으로 나누어 재귀적으로 정렬하는 방식 (평균적으로 가장 많이 쓰임).
# • 힙 정렬 (Heap Sort): 최대 힙이나 최소 힙 자료구조를 구성하여 정렬하는 방식.

# (3) 하이브리드 정렬 (실무 표준 라이브러리에서 사용)
# • 팀 정렬 (Tim sort): 삽입 정렬과 병합 정렬을 결합한 방식으로, 파이썬이나 자바(Collections.sort()) 등의 표준 정렬에 사용됨.
# • 인트로 정렬 (Intro sort): 퀵 정렬을 기본으로 하되 재귀 깊이가 깊어지면 힙 정렬로전환하는 방식이며, C++(std::sort()) 등에서 사용됨.

# (4) 비교를 하지 않는 선형 시간 정렬 (O(n))
# • 기수 정렬 (Radix sort): 데이터의 자릿수를 이용해 비교 연산 없이 분배하고 수집하여 정렬하는 방식.
# • 계수 정렬 (Counting sort): 데이터의 값 범위를 이용해 등장 횟수를 세어 정렬하는 방식
# ----------------------------------------------------------------------------------

# 1. "선택정렬"(selection sort) : "전체 데이터 중 가장 작은(또는 큰) 원소를 찾아 맨 앞과 교환하는 방식"
# <방법 1> : 이해 위주
def find_min_idx(a):
    n=len(a)
    min_idx=0
    for i in range(1, n):
        if a[i] < a[min_idx]:
            min_idx=i
    return min_idx
# : 최솟값의 인덱스를 출력하는 함수

def sel_sort(a):
    result = [] # d의 자료가 정렬되어 저장될 기억장소
    while a:
        min_idx = find_min_idx(a) # min_idx는 해당 인덱스번째의 값을 받음
        value = a.pop(min_idx)
        result.append(value)
    return result
# : 해당 리스트를 최솟값부터 차례대로 정렬하는 함수

d = [2 ,4, 5, 1, 3]
print(find_min_idx(d))
# ram에 저장되어 있는 [2 ,4, 5, 1, 3]의 주소를 d도 가지고 있고 a도 가지고 있다.
# 해당 d중 제일 작은 숫자를 찾아서 ram에 넣고 다시 남은 4개의 숫자들 중에서 제일 작은 숫자를
# ram에 넣는다. 이렇게 순서대로 넣고 해당 값들의 위치를 return한다.
print(sel_sort(d))
# 이러한 방법은 데이터가 커지면 속도가 떨어진다.


# <방법 2> : 일반적인 방법(알고리즘) - 정렬결과를 result와 같은 기억장소없이 자체 해결한다.
def sel_sort2(a):
    n=len(a)
    for i in range(0, n-1): # 0부터 n-2회 반복
        min_idx = i
        for j in range(i+1, n):
            if a[j] < a[min_idx]:
                min_idx = j

        a[i], a[min_idx] = a[min_idx], a[i] # 찾은 가장 작은 값을 i번 위치로 이동

d = [2 ,4, 5, 1, 3]
sel_sort2(d)
print(d)
