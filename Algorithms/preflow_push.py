import random
import time
import copy


class PreflowPush:
    def __init__(self, graph):
        """
        graph: Adjacency matrix where graph[u][v] is capacity.
        """
        self.graph = graph 
        self.V = len(graph)
        
       
        self.flow = [[0 for _ in range(self.V)] for _ in range(self.V)]
        
    
        self.height = [0] * self.V
        
        
        self.excess = [0] * self.V
        
       
        self.active_nodes = []

    def push(self, u, v):
        """
        Push flow from u to v.
        Only allowed if u has excess and height(u) == height(v) + 1
        """
       
        residual_capacity = self.graph[u][v] - self.flow[u][v]
        
        
        delta = min(self.excess[u], residual_capacity)
        
       
        self.flow[u][v] += delta
        self.flow[v][u] -= delta 
        
        
        self.excess[u] -= delta
        self.excess[v] += delta
        
    def relabel(self, u):
        """
        Increase the height of u to be 1 greater than its lowest neighbor
        in the residual graph.
        """
        min_height = float('inf')
        for v in range(self.V):
            
            if self.graph[u][v] - self.flow[u][v] > 0:
                min_height = min(min_height, self.height[v])
                
        
        if min_height != float('inf'):
            self.height[u] = min_height + 1

    def discharge(self, u, source, sink):
        """
        Keep pushing/relabeling u until it has no excess flow.
        """
        while self.excess[u] > 0:
            pushed = False
            for v in range(self.V):
                
                if (self.graph[u][v] - self.flow[u][v] > 0) and (self.height[u] == self.height[v] + 1):
                    self.push(u, v)
                    
                   
                    if v != source and v != sink and self.excess[v] > 0 and v not in self.active_nodes:
                        self.active_nodes.append(v)
                        
                    pushed = True
                 
                    if self.excess[u] == 0:
                        break
            
            if not pushed and self.excess[u] > 0:
                self.relabel(u)

    def solve(self, source, sink):
       
        self.height[source] = self.V
        self.active_nodes = []
        
        
        for v in range(self.V):
            if self.graph[source][v] > 0:
                cap = self.graph[source][v]
                self.flow[source][v] = cap
                self.flow[v][source] = -cap
                self.excess[v] = cap
                self.excess[source] -= cap
                
        
                if v != sink and v != source:
                    self.active_nodes.append(v)

   
        while self.active_nodes:
          
            u = self.active_nodes.pop(0)
            self.discharge(u, source, sink)
            
        return self.excess[sink]


class GraphGenerator:
    def generate_random_graph(self, num_nodes, probability, max_capacity):
       
        graph = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        for u in range(num_nodes):
            for v in range(num_nodes):
                if u != v and random.random() < probability:
                    graph[u][v] = random.randint(1, max_capacity)
        
        if sum(graph[0]) == 0: graph[0][random.randint(1, num_nodes-1)] = max_capacity
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



if __name__ == "__main__":
    
    
   
    print("--- 1. Sanity Check (Hardcoded Graph) ---")
    simple_graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    pp_simple = PreflowPush(simple_graph)
    print(f"Max Flow (Expected 23): {pp_simple.solve(0, 5)}")
    print()

    
    print("--- 2. Project Experiments (Generated Graphs) ---")
    gen = GraphGenerator()
    
    
    experiments = [
        ("Random (Small)", lambda: gen.generate_random_graph(20, 0.5, 50), 0, 19),
        ("Random (Large)", lambda: gen.generate_random_graph(50, 0.3, 50), 0, 49),
        ("Mesh (5x5)",     lambda: gen.generate_mesh_graph(5, 5, 20), 0, 24),
        ("Bipartite",      lambda: gen.generate_bipartite_graph(10, 10, 0.5, 20), 0, 21),
    ]
    
    print(f"{'Graph Type':<20} | {'Nodes':<5} | {'Max Flow':<10} | {'Time (s)':<10}")
    print("-" * 55)

    for name, func, src, snk in experiments:
        graph_instance = func()
        num_nodes = len(graph_instance)
        
        
        solver = PreflowPush(graph_instance)
        
        start_time = time.time()
        max_flow = solver.solve(src, snk)
        end_time = time.time()
        
        print(f"{name:<20} | {num_nodes:<5} | {max_flow:<10} | {(end_time - start_time):.5f}")
    