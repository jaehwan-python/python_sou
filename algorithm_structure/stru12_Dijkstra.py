# 다익스트라 알고리즘 두번째 실습~
# 그래프는 dict로 표현
# 우선순위 큐(heapq)를 이용하여 이동 비용이 적은 도시부터 탐색
# 기존 경로보다 짧은 경로를 발견하면 거리 갱신

import heapq

INF = float('inf') # 아직 도달하지 못한 도시의 거리

graph = { # 각 지역 기준으로 다른 노드(지역)들까지의 가중치
    '서울' : [('대전', 2), ('대구', 5), ('인천', 1)],
    '대전' : [('서울', 2), ('대구', 3), ('인천', 2)],
    '대구' : [('서울', 5), ('대전', 3), ('인천', 3), ('광주', 1), ('부산', 5)], # 새로운 노드(지역)이 추가됨!
    '인천' : [('서울', 1), ('대전', 2), ('대구', 3), ('광주', 1)],
    '광주' : [('대구', 1), ('인천', 1), ('부산', 2), ('광주', 1)],
    '부산' : [('대구', 5), ('광주', 2)]
}

# 목적 : 하나의 출발도시에서 다른 도시(모든) 최단경로와 이동거리를 찾는다. 

# 다익스트라 알고리즘을 적용해보자
# 다익스트라 알고리즘 함수
def dijkstraFunc(start):
    # 모든 도시까지의 최단 거리를 초기화(inf)
    distance = {city:INF for city in graph}
    # print(distance)

    # 최단 거리 추적용 : 각 도시로 이동하기 직전에 방문한 도시 저장
    # 예) previous['광주] = '인천'  <= 광주까지 최단거리에서 바로 이전 도시는 인천 
    previous = {city:None for city in graph}

    # 우선순위 큐 생성
    pq = []
    distance[start] = 0

    heapq.heappush(pq, (0, start)) # (0, '서울')

    while pq:
        # 이동 비용이 적은 도시 꺼내기
        # dist : 출발도시(현재는 서울)에서 현재도시까지의 누적비용, now : 현재 탐색할 도시
        dist, now = heapq.heappop(pq)    

        # 예) 큐에서 꺼낸 거리:5인데 distance[now] = 3이라면 더 이상 탐색하지 않는다.
        if distance[now] < dist:
            continue

        for next_city, cost in graph[now]:
            # 현재 도시를 거쳐 다음 도시까지 가는 총 비용(총 가중치)
            new_cost = dist+ cost

            if new_cost < distance[next_city]: # 새로운 경로가 기존 경로보다 더 짧다면 최단거리를 갱신해야한다.
                distance[next_city] = new_cost # 최단 거리 갱신

                # 최단 경로 추적을 위해서 이전 도시를 저장해둠. ex) 서울  ->  인천  ->  광주
                previous[next_city] = now  # previous['광주'] = '인천'

                # 갱신된 거리와 도시를 우선순위큐에 삽입한다.
                # 이후 이 도시도 다른 도시를 탐색하는 출발점으로 사용된다.
                heapq.heappush(pq, (new_cost, next_city))

    return distance, previous # 모든 도시의 최단 거리와 이전도시 정보 반환

# 최단 경로 추적
def get_path(previous, start, end):
    path = []
    current = end # 도착 도시부터 역순으로 이전 도시를 추적

    while current is not None:
        path.append(current)
        current = previous[current] # 현재 도시의 바로 이전 도시로 옮겨간다.

    path.reverse()  # 도착지  ->  출발지 순서로 저장되어 있으므로 뒤집기를 해야 한다.

    # 출발 도시에서 도착 도시로 연결되지 않은 경우 이전 도시가 전부 None이면 도착도시만 남는다.
    if not path or path[0] != start:
        return []
    return path


# 실행 시작은 여기서부터 !! -------------------    
start_city = '서울' # 알고리즘의 시작!!
distance, previous = dijkstraFunc(start_city)

# 각 도시까지의 최단거리 및 경로 출력
print(f"\n{start_city} 출발 최단 경로")
for city in graph:
    path = get_path(previous, start_city, city)

    if distance[city] == INF:
        print(f"{start_city} -> {city} : 이동불가")
        continue

    route = ' -> '.join(path)
    print(f'도착지 : {city}, 최단비용 : {distance[city]}')
    print(f"이동경로 : {route}")
    print('-' * 30)

    # 출발지인 '서울'에서 출발하여 설정된 도착 도시까지 도착하는데 최단 경로를 선택하는 것 = 최단비용 = 가중치가 제일 작은 경로
    
# 다익스트라에 휴리스틱을 넣은 것 = astar