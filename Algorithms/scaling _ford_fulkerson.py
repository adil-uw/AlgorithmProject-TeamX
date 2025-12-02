# Algorithms/scaling_ford_fulkerson.py
# Author: Aayush Modi 

import math
from collections import defaultdict, deque

def max_flow_scaling(n, edges, s, t):
    # ==================== STEP 1: Build Graph Structure ====================
    # Create adjacency list representation for efficient neighbor lookup
    # graph[u] = [(v1, cap1), (v2, cap2), ...] means edges u->v1, u->v2, etc.
    graph = defaultdict(list)
    
    for u, v, cap in edges:
        graph[u].append((v, cap))
    
    # ==================== STEP 2: Initialize Flow ====================
    # Flow dictionary: flow[(u, v)] = current flow on edge (u, v)
    # Initially all flows are 0
    flow = defaultdict(int)
    
    # ==================== STEP 3: Find Maximum Capacity & Initialize Delta ====================
    # To initialize Δ, we need the maximum capacity of any edge leaving source
    max_capacity = 0
    for u, v, cap in edges:
        if u == s:
            max_capacity = max(max_capacity, cap)
    
    # Edge case: if no edges leave source, max flow is 0
    if max_capacity == 0:
        return 0
    
    # Initialize Δ (delta) as the largest power of 2 that is ≤ max_capacity
    # Example: if max_capacity = 100, then delta = 64 (2^6)
    delta = 2 ** int(math.log2(max_capacity))  
    
    # ==================== HELPER FUNCTIONS ====================
    
    def build_residual_graph(delta_threshold):
        residual = defaultdict(list)
        
        # Add forward edges: original edges with sufficient unused capacity
        for u, v, cap in edges:
            # Residual capacity = original capacity - current flow
            residual_cap = cap - flow[(u, v)]
            
            # Only include if residual capacity ≥ delta
            if residual_cap >= delta_threshold:
                residual[u].append((v, residual_cap, True))
        
        # Add backward edges: reverse of edges with sufficient current flow
        # These allow us to "undo" previously sent flow
        for u, v, cap in edges:
            current_flow = flow[(u, v)]
            
            # Only include if current flow ≥ delta
            if current_flow >= delta_threshold:
                # Note: backward edge goes from v to u (reverse direction)
                residual[v].append((u, current_flow, False))
        
        return residual
    
    def bfs_find_path(residual):
        # BFS initialization
        visited = {s}  # Set of visited nodes
        parent = {s: None}  # parent[node] = previous node in path
        parent_edge_info = {}  # Stores edge type (forward/backward) for reconstruction
        queue = deque([s])  # Queue for BFS
        
        # BFS main loop
        while queue:
            node = queue.popleft()
            
            # Check if we reached the sink
            if node == t:
                # Reconstruct the path from s to t
                path = []
                current = t
                
                # Walk backwards from t to s using parent pointers
                while current != s:
                    prev, is_forward = parent_edge_info[current]
                    path.append((prev, current, is_forward))
                    current = prev
                
                # Reverse to get path in s->t order
                return path[::-1]
            
            # Explore all neighbors in residual graph
            for neighbor, res_cap, is_forward in residual[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    parent_edge_info[neighbor] = (node, is_forward)
                    queue.append(neighbor)
        
        # No path found from s to t
        return None
    
    def compute_bottleneck(path, residual):
        min_cap = float('inf')
        
        # Check each edge in the path
        for u, v, is_forward in path:
            # Find the residual capacity of edge (u, v)
            for neighbor, res_cap, fwd in residual[u]:
                if neighbor == v and fwd == is_forward:
                    min_cap = min(min_cap, res_cap)
                    break
        
        return min_cap
    
    def augment_flow(path, bottleneck):
        for u, v, is_forward in path:
            if is_forward:
                # Forward edge: increase flow from u to v
                flow[(u, v)] += bottleneck
            else:
                # Backward edge: we're using the reverse edge (v, u)
                # This means we're decreasing flow from v to u
                flow[(v, u)] -= bottleneck
    
    # ==================== STEP 4: MAIN SCALING ALGORITHM ====================
    while delta >= 1:
        # === Scaling Phase: Process all paths with bottleneck ≥ delta ===
        
        while True:
            # Build the restricted residual graph G_f^Δ
            # Only includes edges with residual capacity ≥ delta
            residual = build_residual_graph(delta)
            
            # Find an augmenting path from s to t using BFS
            path = bfs_find_path(residual)
            
            # If no path exists, this scaling phase is complete
            if path is None:
                break
            
            # Compute the bottleneck capacity of the path
            bottleneck = compute_bottleneck(path, residual)
            
            # Push flow along the path
            augment_flow(path, bottleneck)
        
        # Move to next scaling phase: reduce delta by half
        delta = delta // 2
    
    # ==================== STEP 5: Compute Final Flow Value ====================
    # The flow value is the total flow leaving the source
    max_flow_value = 0
    for u, v, cap in edges:
        if u == s:
            max_flow_value += flow[(u, v)]
    
    return max_flow_value
  
# ==================== OPTIONAL: STANDALONE TESTING ====================
if __name__ == "__main__":

    print("="*60)
    print("TESTING SCALING FORD-FULKERSON ALGORITHM")
    print("="*60)
    
    # -------------------- Test Case 1: Simple Graph --------------------
    print("\n[TEST 1] Simple 4-node graph")
    print("-" * 40)
    
    n1 = 4
    edges1 = [
        (0, 1, 10),  # s -> 1
        (0, 2, 5),   # s -> 2
        (1, 3, 10),  # 1 -> t
        (1, 2, 5),   # 1 -> 2
        (2, 3, 20),  # 2 -> t
    ]
    s1, t1 = 0, 3
    
    result1 = max_flow_scaling(n1, edges1, s1, t1)
    expected1 = 15
    
    print(f"Nodes: {n1}")
    print(f"Edges: {len(edges1)}")
    print(f"Source: {s1}, Sink: {t1}")
    print(f"\nResult: {result1}")
    print(f"Expected: {expected1}")
    print(f"Status: {'✓ PASSED' if result1 == expected1 else '✗ FAILED'}")
     
    # -------------------- Test Case 2: Larger Capacities --------------------
    print("\n[TEST 2] Graph with large capacities")
    print("-" * 40)
    """
    This test demonstrates the advantage of scaling:
    - Large capacities (1000s) would cause many iterations in basic FF
    - Scaling FF handles this efficiently
    """
    
    n2 = 4
    edges2 = [
        (0, 1, 1000),  # s -> 1
        (0, 2, 500),   # s -> 2
        (1, 3, 1000),  # 1 -> t
        (2, 3, 500),   # 2 -> t
    ]
    s2, t2 = 0, 3
    
    result2 = max_flow_scaling(n2, edges2, s2, t2)
    expected2 = 1500
    
    print(f"Nodes: {n2}")
    print(f"Edges: {len(edges2)}")
    print(f"Source: {s2}, Sink: {t2}")
    print(f"\nResult: {result2}")
    print(f"Expected: {expected2}")
    print(f"Status: {'✓ PASSED' if result2 == expected2 else '✗ FAILED'}")
    
    # -------------------- Test Case 3: Bottleneck Edge --------------------
    print("\n[TEST 3] Graph with bottleneck edge")
    print("-" * 40)
    """
    Graph with one small capacity edge that limits flow:
        s(0) --100--> (1) --1--> (2) --100--> t(3)
    
    Max flow is limited by the middle edge with capacity 1
    """
    
    n3 = 4
    edges3 = [
        (0, 1, 100),  # s -> 1
        (1, 2, 1),    # 1 -> 2 (bottleneck!)
        (2, 3, 100),  # 2 -> t
    ]
    s3, t3 = 0, 3
    
    result3 = max_flow_scaling(n3, edges3, s3, t3)
    expected3 = 1
    
    print(f"Nodes: {n3}")
    print(f"Edges: {len(edges3)}")
    print(f"Source: {s3}, Sink: {t3}")
    print(f"\nResult: {result3}")
    print(f"Expected: {expected3}")
    print(f"Status: {'✓ PASSED' if result3 == expected3 else '✗ FAILED'}")
    
    # -------------------- Test Case 4: No Path --------------------
    print("\n[TEST 4] Disconnected graph (no path from s to t)")
    print("-" * 40)
    
    n4 = 4
    edges4 = [
        (0, 1, 10),  # s -> 1
        (2, 3, 10),  # 2 -> t (disconnected)
    ]
    s4, t4 = 0, 3
    
    result4 = max_flow_scaling(n4, edges4, s4, t4)
    expected4 = 0
    
    print(f"Nodes: {n4}")
    print(f"Edges: {len(edges4)}")
    print(f"Source: {s4}, Sink: {t4}")
    print(f"\nResult: {result4}")
    print(f"Expected: {expected4}")
    print(f"Status: {'✓ PASSED' if result4 == expected4 else '✗ FAILED'}")

    # -------------------- Summary --------------------
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = (
        result1 == expected1 and
        result2 == expected2 and
        result3 == expected3 and
        result4 == expected4
    )
    
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYour implementation is ready to use with main.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please review the failed test cases above")
    
    print("="*60)