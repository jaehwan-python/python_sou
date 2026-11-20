# Graph : Node(vertex)와 Edge의 집합으로 이루어진 자료구조

# Tree : 계층구조, Root있음, 사이클(순환)업승ㅁ, 항상 연결
# Graph : 일반 네트워크 구조, Root없음, 사이클(순환)있음, 연결/비연결 모두 가능

graph = {
    'A' : ('B', 'C'),
    'B' : ('D', 'E'),
    'C' : ('F'),
    'D' : (),
    'E' : (),
    'F' : (),
}

# DFS(깊이우선탐색) vs BFS(너비우선탐색)

# DFS - : 깊이우선탐색방식 
#     - 특징 - 재귀 또는 스택으로 구현
#            - 경로추적, 백트레킹에 적합
def dfsFunc(graph, start, visited):
    visited.append(start)  # 현재노드의 방문 기록 저장
    for next_node in graph[start]:  # 이웃 노드를 탐색 : 현재 node(start)에 인접한 노드를 하나씩 확인한다.
        if next_node not in visited:  # 아직 방문하지 않은 노드라면 ...
            dfsFunc(graph, next_node, visited) # 재귀(현재 길을 끝까지 내려가며 탐색)

visited_dfs = []  # 방문 순서 저장용 list
dfsFunc(graph, 'A', visited_dfs)
print('DFS 방문 순서 : ', visited_dfs)
# DFS 방문 순서 :  ['A', 'B', 'D'(끝), 'E'(끝), 'C', 'F'(끝)]
print()


# BFS - : 너비우선탐색방식
#     - 특징 - Queue로 구현
#            - 최단 거리 탐색에 적합
from collections import deque
def bfsFunc(graph, start):
    visited = [start]
    queue = deque([start])  # 큐(Queue)는 "First In, First Out"구조로 탐색 대기열을 가진다.

    while queue:
        node = queue.popleft()  # 가장 먼저 들어온 node를 꺼낸다.
        for next_node in graph[node]:  # 현재노드와 이웃노드를 확인하는 작업
            if next_node in visited:
                visited.append(next_node) # 방문처리
                queue.append(next_node)  # 다음 탐색의 대상으로 큐(Queue)에 추가
    return visited
print('DFS 방문 순서 : ', visited_dfs)
# BJS 방문 순서 : ['A', 'B', 'C', 'D', 'E']
visited_bfs = bfsFunc(graph, 'A')
# BFS는 직접 그려보기
# A -> B, C -> D, E, F 방문 즉시 큐에 쌓고, 먼저 들어온 것부터 처리한다.
#