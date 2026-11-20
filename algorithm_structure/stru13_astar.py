# A*알고리즘(에이스타 알고리즘)은 출발 노드에서 목표 노드까지의 최단 경로를 
# 빠르게 찾는 그래프 탐색 알고리즘이다.
# 다익스트라 알고리즘에 목표 지점까지의 추정 비용(휴리스틱)을 더해(사람이 직접 준다) 탐색 범위를 줄인다.

# <핵심 공식>
# 각 노드의 우선순위는 평가 함수 f(n)으로 결정한다.
# "f(n) = g(n) + h(n)"
# 'g(n)' : 출발 노드에서 현재 노드 n까지의 실제 이동 비용
# 'h(n)' : 현재 노드 n에서 목표 노드까지의 추정 비용(휴리스틱, ex : 맨해튼거리, 유클리드 거리)

# 동작 방식
# 1. 출발 노드를 열린 목록(Open List)에 넣고 시작한다. 
# 2. 열린 목록에서 f(n)값이 가장 작은 노드를 선택한다.
# 3. 해당 노드가 목표 노드면 탐색을 종료하고 경로를 반환한다.
# 4. 목표가 아니면 현재 노들르 닫힌 목록(Closed List)으로 옮기고, 인접 이동 가능 노드의 g, h, f값을 계산하여 열린 목록에 추가하거나 갱신한다.
# 5. 목표에 도달하거나 열린 목록이 빌 때까지 2~4단계를 반목한다.

import heapq
def astarFunc(graph, start, goal, h):
    pq = [(h[start], 0, start)]  # (f=g+h, g, 현재노드) 시작노드 초기화
    dist = {start:0}
    parent = {} # 최단 경로 트리 복원을 위한 부모 노드 기록

    while pq:
        f, g, u = heapq.heappop(pq) # f값이 가장 작은 node(비용이 가장 적을 것으로 유망한 노드)를 꺼낸다. 
        # f값 : 전체 예상 비용
        # g값 : 지금까지 온 거리의 비용 = g(n)
        # h값 : 앞으로의 예상 비용
        #   u : 현재 탐색중인 현재 노드
        # f(n) = g + h
        
        if u == goal:
            break

        for v, w in graph[u]: # 현재 노드 u와 연결된 이웃 node인 v탐색
            # 로템에서 주는 프로그램이 Flask서버 연결되는데 그때 우리는 여러 알고리즘을 넣어가면서 작업을 하는데 주로 Astar를 많이 쓴다
            new_g = g + w   # '시작점'  ->  'u'  ->  'v'  까지의 실제 비용 계산
            if v not in dist or new_g < dist[v]:  # 아직 방문 안했거나 더 짧은 경로를 발견한 경우
                dist[v] = new_g  # v까지의 최단 실제 비용을 갱신한다.
                parent[v] = u  # v로 오기 직전 node들을 u로 기록(경로 복원용)
                heapq.heappush(pq, (new_g + h[v], new_g, v))  # f=g+h값으로 큐에 삽입한다.
        
    # 경로 복원(while문 나옴)
    path = [goal]  # 목표node부터 역방향으로 경로 구성을 시작한다.
    while path[-1] != start:
        path.append(parent[path[-1]])  # 부모node르 따라서 거꾸로 집어넣고 있다
    path.reverse()
    return path, dist[goal]  # 최단경로와 총비용 반환

graph = { # 무방향 형태
    'A' : [('B', 1), ('C', 4)], # A에서 B, C로 가는 가중치 간선
    'B' : [('A', 1), ('C', 1), ('D', 2)],
    'C' : [('A', 4), ('B', 1), ('D', 3)],
    'D' : [('B', 2), ('C', 3)],
}

heuristic = {'A':3, 'B':2, 'C':1, 'D':0}  # 휴리스틱(h(n))이다. : 목표 D까지의 예상 비용이다.
path, cost = astarFunc(graph, 'A', 'D', heuristic) # 시작node과 목표 node, A~D까지의 예상 비용을 휴리스틱으로 주었다.
print('A*(Astar)경로 : ', path)
print('총 비용 : ', cost)