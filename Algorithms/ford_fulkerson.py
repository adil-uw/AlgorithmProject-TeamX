# ford_fulkerson.py
from typing import List, Tuple

EdgeTuple = Tuple[int, int, int]   # (u, v, capacity)

class Edge:
    #Residual edge structure: to = neighbor node, capacity = current residual capacity,
    #rev = index of the reverse edge in res[to].
    def __init__(self, to: int, capacity: int, rev: int) -> None:
        self.to = to
        self.capacity = capacity
        self.rev = rev

def fordFulkMaxFlow(n: int,
                    edges: List[EdgeTuple],
                    s: int,
                    t: int) -> int:  
    res = buildResidualGraph(n, edges)
    max_flow = 0

    while True:
        visited = [False] * n

        pushed = dfs(s, t, float("inf"), res, visited)

        if pushed == 0:
            break  # No more augmenting paths

        max_flow += pushed

    return max_flow

def addEdge(res: List[List[Edge]], u: int, v: int, capacity: int) -> None:
    #addon an forward and backward edge to the residual graph
    forward = Edge(to=v, capacity=capacity, rev=len(res[v]))
    backward = Edge(to=u, capacity=0, rev=len(res[u]))
    res[u].append(forward)
    res[v].append(backward)

def buildResidualGraph(n: int, edges: List[EdgeTuple]) -> List[List[Edge]]:
    
    #making the initial residual graph from the given list of edges.
    res: List[List[Edge]] = [[] for _ in range(n)]
    for u, v, c in edges:
        addEdge(res, u, v, c)
    return res

def dfs(u: int,
        t: int,
        flow_limit: int,
        res: List[List[Edge]],
        visited: List[bool]) -> int:
    
    #DFS to find an augmenting path
    if u == t:
        return flow_limit

    visited[u] = True

    for edge in res[u]:
        if edge.capacity <= 0:
            continue

        v = edge.to
        if visited[v]:
            continue

        new_limit = min(flow_limit, edge.capacity)
        pushed = dfs(v, t, new_limit, res, visited)

        if pushed > 0:
            # Reduce forward capacity
            edge.capacity -= pushed
            # Increase backward capacity
            rev_edge = res[v][edge.rev]
            rev_edge.capacity += pushed
            return pushed

    return 0