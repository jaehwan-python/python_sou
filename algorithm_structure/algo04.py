# 종류 -> 
# (1) O(n²) 시간 복잡도를 갖는 알고리즘 (구현이 쉽지만 데이터가 많아지면 느림)
# • 버블 정렬 (Bubble Sort): 인접한 두 원소를 비교하여 자리를 계속 교환하는 방식.
# • 선택 정렬 (Selection Sort): 전체 데이터 중 가장 작은(또는 큰) 원소를 찾아 맨 앞과 교환하는 방식.
# • 삽입 정렬 (Insertion Sort): 앞에서부터 차례대로 이미 정렬된 부분과 비교하여 자신의 위치를 찾아 삽입하는 방식.

# (2) (O(nlogn)) 시간 복잡도를 갖는 알고리즘 (평균적으로 빠름)
# • 병합 정렬 (Merge Sort): 분할 정복(Divide and Conquer) 방식으로 반으로 쪼갠 뒤 다시 정렬하며 합치는 방식 (안정 정렬).
#                           - 분할 / 정복 / 결합
# • 퀵 정렬 (Quick Sort): 기준점(Pivot)을 설정하고 피벗보다 작은 값과 큰 값으로 나누어 재귀적으로 정렬하는 방식 (평균적으로 가장 많이 쓰임)
# • 힙 정렬 (Heap Sort): 최대 힙이나 최소 힙 자료구조를 구성하여 정렬하는 방식.

# (3) 하이브리드 정렬 (실무 표준 라이브러리에서 사용)
# • 팀 정렬 (Tim sort): 삽입 정렬과 병합 정렬을 결합한 방식으로, 파이썬이나 자바(Collections.sort()) 등의 표준 정렬에 사용됨.
# • 인트로 정렬 (Intro sort): 퀵 정렬을 기본으로 하되 재귀 깊이가 깊어지면 힙 정렬로전환하는 방식이며, C++(std::sort()) 등에서 사용됨.

# (4) 비교를 하지 않는 선형 시간 정렬 (O(n))
# • 기수 정렬 (Radix sort): 데이터의 자릿수를 이용해 비교 연산 없이 분배하고 수집하여 정렬하는 방식.
# • 계수 정렬 (Counting sort): 데이터의 값 범위를 이용해 등장 횟수를 세어 정렬하는 방식
# ----------------------------------------------------------------------------------

# 병합정렬(Merge sort)
# 대표적인 분할 정복(Divide and Conquer) 기반의 정렬 알고리즘입니다.
# 핵심 동작 방식
# 1. 분할(DIvide) : 정렬한 전체 리스트를 원소가 1개 또는 0개가 될 때까지 절반(2개)으로 분할.
# 2. 정복(Donquer) : 쪼개진 부분 리스트를 각각 재귀적으로 정렬.
# 3. 결합(Combine) : 정렬된 두 개의 부분 리스트를 하나의 정렬된 리스트로 병합.

# <방법1> : 이해 위주
# 전체 흐름
# 1) 리스트를 반으로 나눔. 1개씩 남을 때까지 계속
# 2) 각각 다시 merge_sort() 함수로 정렬
# 3) 정렬된 두 리스트를 하나로 합친다.(merge)
#    이 때 합치면서 정렬된 상태를 유지한다.


def merge_sort(a):
    n= len(a)

    if n <= 1:
        return a

    mid = n // 2 # 중간을 기준으로 두 그룹으로 분한

    # 참고 : 함수는 독립적인 공간을 갖음. 아래의 g1, g2는 서로 불간섭 
    g1 = merge_sort(a[:mid]) # 재귀
    print(f'g1 : {id(g1)}, {g1}')
    g2 = merge_sort(a[mid:]) # 재귀
    print(f'g2 : {id(g2)}, {g2}')

    # 두 그룹을 하나로 병합하기 위한 기억장소를 별도 사용
    result = []
    while g1 and g2:
        print(g1[0], ' ', g2[0])
        if g1[0] < g2[0]:
            result.append(g1.pop(0))
        else:
            result.append(g2.pop(0))

    # g1과 g2 중 소진된 것은 skip
    while g1:
        result.append(g1.pop(0))

    while g2:
        result.append(g2.pop(0))


    return result

d = [6,8,3,1,2,4,7,5]
print(merge_sort(d)) # 2개의 그룹으로 나눔

print('----------------------')
# 방법2 : 일반 알고리즘
# 재귀호출이 정렬된 리스트를 반환
# 병합도 새 리스트를 만들어 변환
# 원본 리스트는 그대로이고 정렬된 결과는 새 리스트에 저장
def merge_sort2(a):
    if len(a) <= 1:
        return a

    mid = len(a) // 2
    left = merge_sort2(a[:mid])
    print(f'left : {id(left)}, {left}')
    right = merge_sort2(a[mid:])
    print(f'right : {id(right)}, {right}')

    result = []
    i = j = 0

    # 병합
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 남은 요소 추가
    result += left[i:]
    result += right[j:]
    return result

print()
d = [6,8,3,1,2,4,7,5]
soited_d = merge_sort2(d)
print(soited_d)