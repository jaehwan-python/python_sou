# BST(Binary Search Tree, 이진 탐색 트리) : 중위 순회로 자료 정렬하기
# 각 노드 기준으로 left < node < right
# 왼쪽 sub-tree : 현재 노드보다 작은 값
# 오른쪽 sub-tree : 현재 노드보다 큰 값
# 입력 순서에 따라서 tree모양이 달라진다.
# 이진트리는 구조만 있으나, BST구조 + 정렬규칙이 있다.
# 중위순회(왼쪽  ->  현재  ->  오른쪽 순서로 방문)를 하면 오름차순 정렬이 된다.

# BST 노드 정의
class Node:
    def __init__(self, key):
        self.key = key # 노드가 저장하는 값
        self.left = None # 왼쪽 자식 노드(더 작은 값이 저장)
        self.right = None # 오른쪽 자식 노드(더 큰 값이 저장)

# BST에 자료 삽입!
def insert(root, key):
    if root is None:  # 현재 위치가 비워져있다면...
        return Node(key) # 새 노드를 생성한다. 그리고 나서 그 자리에 값(key)을 넣고 return탈출함

    if key < root.key: # 넣을 값이 현재 node보다 작다면...
        root.left = insert(root.left, key) # 작은 값이 들어오면 왼쪽 노드에 재귀적으로 삽입한다.
    else:
        root.right = insert(root.right, key) # 큰 값이 들어오면 오른쪽 노드에 재귀적으로 삽입한다.
    return root

# 중위 순회(정렬 결과 생성) : Left  ->  Node  ->  Right 순서로 정렬된다.
def inorder(root, result):
    if root is None:
        return # 더 내려갈 노드가 없으면 함수를 탈출한다.

    inorder(root.left, result) # 왼쪽 노드(작은 값)를 방문
    result.append(root.key)    # 현재 노드값 추가
    inorder(root.right, result) # 오른쪽 노드(큰 값)방문
values = [5, 3, 7, 2, 4, 9]
root = None
for v in values:
    root = insert(root, v) # BST에 삽입하고 root(최상단)을 갱신한다.
# 즉, 5라는 노드를 기준으로 3은 5보다 작기 때문에 왼쪽으로 branch가 생기고 7은 5를 기준으로 오른쪽에 branch가 생긴다.
# 그다음에 3이라는 노드를 기준으로 2는 3보다 작기때문에 3이라는 노드 왼쪽에 4는 3이라는 노드보다 크므로 노드 오른쪽에 배치한다.
# 그리고 9는 5보다 크기 때문에 5노드의 오른쪽에 배치한다.
# 5 - 3 - 2
#       - 4 
#   - 7 - 
#       - 9

# BST 정렬 결과 출력
sorted_result = []
inorder(root, sorted_result)
print('순회결과 : ', sorted_result)

# ** Graph(그래프)란 정점(Vertex, Node)과 정점을 연결하는 간선(Edge)의 집합으로 이루어진 자료구조이다.**