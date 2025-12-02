
import random
import time
import copy


class PreflowPush:
    def __init__(self, graph):
        """
        graph: adjacency matrix where graph[u][v] is capacity.
        """
        self.graph = graph
        self.V = len(graph)
        self.flow = [[0 for _ in range(self.V)] for _ in range(self.V)]
        self.height = [0] * self.V
        self.excess = [0] * self.V
        self.active_nodes = []

    def residual_capacity(self, u, v):
        return self.graph[u][v] - self.flow[u][v]

    def push(self, u, v):
        """
        Push up to min(excess[u], residual(u,v)).
        Returns amount pushed.
        """
        cap = self.residual_capacity(u, v)
        if cap <= 0 or self.excess[u] <= 0:
            return 0
        delta = min(self.excess[u], cap)
        self.flow[u][v] += delta
        self.flow[v][u] -= delta
        self.excess[u] -= delta
        self.excess[v] += delta
        return delta

    def relabel(self, u):
        """
        Set height[u] = 1 + min{ height[v] | residual(u,v) > 0 }.
        """
        min_h = float('inf')
        for v in range(self.V):
            if self.residual_capacity(u, v) > 0:
                min_h = min(min_h, self.height[v])
        if min_h < float('inf'):
            self.height[u] = min_h + 1

    def discharge(self, u, source, sink):
        """
        Discharge node u until excess[u] == 0 (or u is source/sink).
        """
        while self.excess[u] > 0 and u != source and u != sink:
            pushed_any = False
            for v in range(self.V):
                if self.residual_capacity(u, v) > 0 and self.height[u] == self.height[v] + 1:
                    pushed = self.push(u, v)
                    if pushed:
                        pushed_any = True
                        # activate v if it's an internal node
                        if v != source and v != sink and v not in self.active_nodes:
                            self.active_nodes.append(v)
                        if self.excess[u] == 0:
                            break
            if not pushed_any:
                self.relabel(u)

    def solve(self, source, sink):
        """
        Run Preflow-Push and return max flow (int).
        """
        if source == sink:
            return 0

        # init
        self.height = [0] * self.V
        self.excess = [0] * self.V
        self.flow = [[0 for _ in range(self.V)] for _ in range(self.V)]
        self.active_nodes = []

        self.height[source] = self.V
        for v in range(self.V):
            if self.graph[source][v] > 0:
                cap = self.graph[source][v]
                self.flow[source][v] = cap
                self.flow[v][source] = -cap
                self.excess[v] += cap
                self.excess[source] -= cap
                if v != source and v != sink and v not in self.active_nodes:
                    self.active_nodes.append(v)

      
        while self.active_nodes:
            u = self.active_nodes.pop(0)
            old_excess = self.excess[u]
            self.discharge(u, source, sink)
            if self.excess[u] > 0 and u not in self.active_nodes and u != source and u != sink:
                self.active_nodes.append(u)

        
        maxflow = sum(self.flow[source][v] for v in range(self.V))
        return maxflow


class GraphGenerator:
    def generate_random_graph(self, num_nodes, probability, max_capacity):
        graph = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        for u in range(num_nodes):
            for v in range(num_nodes):
                if u != v and random.random() < probability:
                    graph[u][v] = random.randint(1, max_capacity)

        if sum(graph[0]) == 0:
            graph[0][random.randint(1, num_nodes - 1)] = max_capacity
        return graph

    def generate_mesh_graph(self, rows, cols, max_capacity):
        num_nodes = rows * cols
        graph = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        for r in range(rows):
            for c in range(cols):
                u = r * cols + c
                if c + 1 < cols:
                    v = r * cols + (c + 1)
                    graph[u][v] = random.randint(1, max_capacity)
                if r + 1 < rows:
                    v = (r + 1) * cols + c
                    graph[u][v] = random.randint(1, max_capacity)
        return graph

    def generate_bipartite_graph(self, u_size, v_size, probability, max_capacity):
        source = 0
        sink = u_size + v_size + 1
        total = sink + 1
        graph = [[0 for _ in range(total)] for _ in range(total)]
        for i in range(1, u_size + 1):
            graph[source][i] = random.randint(1, max_capacity)
        for i in range(1, u_size + 1):
            for j in range(u_size + 1, u_size + v_size + 1):
                if random.random() < probability:
                    graph[i][j] = random.randint(1, max_capacity)
        for j in range(u_size + 1, u_size + v_size + 1):
            graph[j][sink] = random.randint(1, max_capacity)
        return graph


def max_flow_preflow(n, edges, source, sink):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for e in edges:
        try:
            u, v, c = e
        except Exception:
            continue
        
        if isinstance(u, int) and isinstance(v, int) and isinstance(c, (int, float)):
            if 0 <= u < n and 0 <= v < n:
                graph[u][v] += int(c)

    solver = PreflowPush(graph)
    return solver.solve(source, sink)
