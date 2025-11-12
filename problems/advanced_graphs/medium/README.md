# Advanced Graphs - Medium Problems

## Overview

This directory contains medium-level advanced graph problems that introduce specialized algorithms including Dijkstra's shortest path, Prim's/Kruskal's minimum spanning tree, topological sorting with complex constraints, and greedy graph algorithms.

## Advanced Graph Algorithms

### 1. Dijkstra's Algorithm (Single-Source Shortest Path)

Finds shortest paths from source to all vertices in weighted graph with non-negative weights.

**Core Idea**: Greedily select closest unvisited vertex, update distances to neighbors.

**Implementation**:
```python
import heapq

def dijkstra(graph, start):
    # Distance from start to each node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Priority queue: (distance, node)
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        # Update distances to neighbors
        for neighbor, weight in graph[node]:
            distance = current_dist + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances
```

**Time Complexity**:
- With binary heap: O((V + E) log V)
- With Fibonacci heap: O(E + V log V)

**Space Complexity**: O(V)

**When to Use**:
- Non-negative edge weights
- Single source shortest path
- Need paths to all vertices or specific target

**Key Insight**: Once a vertex is visited (removed from priority queue), its shortest distance is finalized.

### 2. Minimum Spanning Tree (MST)

A tree connecting all vertices with minimum total edge weight.

**Properties**:
- Connects all vertices
- No cycles
- Exactly V-1 edges
- Minimum total weight

#### Kruskal's Algorithm (Union-Find based)

**Idea**: Sort edges by weight, add edge if it doesn't create cycle.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

def kruskal(n, edges):
    # edges: [(weight, u, v), ...]
    edges.sort()  # Sort by weight
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = []

    for weight, u, v in edges:
        if uf.union(u, v):  # No cycle created
            mst_weight += weight
            mst_edges.append((u, v))

            if len(mst_edges) == n - 1:
                break

    return mst_weight, mst_edges
```

**Time Complexity**: O(E log E) for sorting
**Space Complexity**: O(V)

#### Prim's Algorithm (Priority Queue based)

**Idea**: Start from vertex, greedily add minimum weight edge connecting tree to non-tree vertex.

```python
def prim(graph, start):
    # graph: {node: [(neighbor, weight), ...]}
    mst_weight = 0
    mst_edges = []
    visited = set([start])

    # Priority queue: (weight, from_node, to_node)
    edges = [(weight, start, neighbor)
             for neighbor, weight in graph[start]]
    heapq.heapify(edges)

    while edges and len(visited) < len(graph):
        weight, frm, to = heapq.heappop(edges)

        if to in visited:
            continue

        visited.add(to)
        mst_weight += weight
        mst_edges.append((frm, to))

        for neighbor, edge_weight in graph[to]:
            if neighbor not in visited:
                heapq.heappush(edges, (edge_weight, to, neighbor))

    return mst_weight, mst_edges
```

**Time Complexity**: O(E log V) with binary heap
**Space Complexity**: O(V + E)

**Kruskal vs Prim**:
| Aspect | Kruskal | Prim |
|--------|---------|------|
| Approach | Edge-based (global) | Vertex-based (local) |
| Data Structure | Union-Find | Priority Queue |
| Best for | Sparse graphs | Dense graphs |
| Edge sorting | Required | Not needed |
| Parallelizable | Yes | No |

### 3. Topological Sort with Custom Constraints

Order vertices in directed acyclic graph respecting dependencies and additional constraints.

**DFS-based with Validation**:
```python
def topological_sort_with_constraints(graph, constraints):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    result = []
    has_cycle = False

    def dfs(node):
        nonlocal has_cycle
        if color[node] == GRAY:
            has_cycle = True
            return
        if color[node] == BLACK:
            return

        color[node] = GRAY

        for neighbor in graph[node]:
            if validate_constraint(node, neighbor, constraints):
                dfs(neighbor)

        color[node] = BLACK
        result.append(node)

    for node in graph:
        if color[node] == WHITE:
            dfs(node)

    if has_cycle:
        return []

    return result[::-1]
```

### 4. Greedy Graph Algorithms

Make locally optimal choices hoping to find global optimum.

**Pattern**:
```python
def greedy_graph(graph):
    # Sort or prioritize choices
    choices = sorted(get_choices(graph), key=priority_function)

    result = []
    for choice in choices:
        if is_valid(choice, result):
            result.append(choice)

            if is_complete(result):
                return result

    return result
```

## Problems in This Directory

### 1. Reconstruct Itinerary (332)

**Problem**: Given airline tickets, reconstruct itinerary starting from "JFK" using all tickets once. If multiple valid itineraries exist, return the one with smallest lexical order.

**Concept**: Eulerian path in directed graph (visit every edge exactly once)

**Key Insights**:
- Each ticket is an edge
- Need to find Eulerian path starting from JFK
- Lexicographically smallest = visit destinations in sorted order
- Use Hierholzer's algorithm

**Approach - Hierholzer's Algorithm**:
```python
def findItinerary(tickets):
    # Build graph with sorted destinations
    graph = defaultdict(list)
    for src, dst in sorted(tickets)[::-1]:
        graph[src].append(dst)

    route = []

    def dfs(airport):
        while graph[airport]:
            next_dest = graph[airport].pop()
            dfs(next_dest)
        route.append(airport)

    dfs("JFK")
    return route[::-1]
```

**Time**: O(E log E), **Space**: O(E)

**Why It Works**:
- Sort tickets in reverse to pop in correct order
- DFS explores paths until stuck
- When stuck, add to route and backtrack
- Reverse gives correct order

### 2. Min Cost to Connect All Points (1584)

**Problem**: Connect all points where cost is Manhattan distance. Find minimum cost to connect all.

**Concept**: Minimum Spanning Tree with implicit edges

**Key Insights**:
- Every pair of points has an edge (complete graph)
- Edge weight = Manhattan distance
- Need MST of this graph
- Can use Prim's or Kruskal's

**Approach 1 - Prim's Algorithm**:
```python
def minCostConnectPoints(points):
    n = len(points)
    visited = set()
    min_heap = [(0, 0)]  # (cost, point_index)
    total_cost = 0

    while len(visited) < n:
        cost, i = heapq.heappop(min_heap)

        if i in visited:
            continue

        visited.add(i)
        total_cost += cost

        # Add edges to all unvisited points
        for j in range(n):
            if j not in visited:
                dist = abs(points[i][0] - points[j][0]) + \
                       abs(points[i][1] - points[j][1])
                heapq.heappush(min_heap, (dist, j))

    return total_cost
```

**Approach 2 - Kruskal's Algorithm**:
```python
def minCostConnectPoints(points):
    n = len(points)

    # Generate all edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + \
                   abs(points[i][1] - points[j][1])
            edges.append((dist, i, j))

    edges.sort()

    # Union-Find
    uf = UnionFind(n)
    total_cost = 0
    edges_used = 0

    for cost, i, j in edges:
        if uf.union(i, j):
            total_cost += cost
            edges_used += 1

            if edges_used == n - 1:
                break

    return total_cost
```

**Time**:
- Prim's: O(N² log N)
- Kruskal's: O(N² log N)

**Space**: O(N²) for edges (Kruskal), O(N) for heap (Prim)

**Optimization**: Prim's is better for dense graphs (complete graph in this case)

### 3. Network Delay Time (743)

**Problem**: Given directed weighted graph and source node k, find time for all nodes to receive signal. If impossible, return -1.

**Concept**: Single-source shortest path (Dijkstra's)

**Key Insights**:
- Signal propagates like shortest path
- Time = maximum shortest path from source
- Use Dijkstra's algorithm
- Return -1 if any node unreachable

**Approach - Dijkstra's Algorithm**:
```python
def networkDelayTime(times, n, k):
    # Build graph
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # Dijkstra's
    distances = {i: float('inf') for i in range(1, n + 1)}
    distances[k] = 0

    pq = [(0, k)]  # (time, node)
    visited = set()

    while pq:
        time, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph[node]:
            new_time = time + weight

            if new_time < distances[neighbor]:
                distances[neighbor] = new_time
                heapq.heappush(pq, (new_time, neighbor))

    max_time = max(distances.values())
    return max_time if max_time != float('inf') else -1
```

**Time**: O((V + E) log V), **Space**: O(V + E)

**Alternative - Bellman-Ford**: Can handle negative weights, O(VE) time

**Common Mistakes**:
- Forgetting to check if all nodes reached
- Not handling disconnected graphs
- Wrong answer when starting node is not 1

## Algorithm Comparison

### Shortest Path Algorithms:

| Algorithm | Use Case | Time | Negative Weights | Negative Cycles |
|-----------|----------|------|------------------|----------------|
| Dijkstra | Single-source, non-negative | O((V+E) log V) | No | N/A |
| Bellman-Ford | Single-source, any weights | O(VE) | Yes | Detects |
| Floyd-Warshall | All-pairs | O(V³) | Yes | Detects |
| BFS | Unweighted | O(V + E) | N/A | N/A |

### MST Algorithms:

| Algorithm | Approach | Time | Best For |
|-----------|----------|------|----------|
| Kruskal | Edge-based, Union-Find | O(E log E) | Sparse graphs |
| Prim | Vertex-based, Priority Queue | O(E log V) | Dense graphs |
| Boruvka | Parallel-friendly | O(E log V) | Distributed systems |

## Key Concepts

### 1. Priority Queue Usage
- Always store (priority, data)
- Use heapq in Python (min-heap)
- For max-heap, negate priorities
- Check if already processed after popping

### 2. Graph Representation for Weighted Graphs
```python
# Adjacency list with weights
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8)],
    'D': []
}

# Edge list for MST algorithms
edges = [
    (4, 'A', 'B'),
    (2, 'A', 'C'),
    (1, 'B', 'C'),
    (5, 'B', 'D'),
    (8, 'C', 'D')
]
```

### 3. Greedy vs Dynamic Programming
- **Greedy**: Makes locally optimal choice (Dijkstra, MST)
- **DP**: Considers all possibilities (Bellman-Ford, Floyd-Warshall)
- Greedy faster but only works when greedy choice property holds

### 4. Path Reconstruction
```python
def dijkstra_with_path(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {start: None}

    pq = [(0, start)]

    while pq:
        dist, node = heapq.heappop(pq)

        if node == end:
            break

        for neighbor, weight in graph[node]:
            new_dist = dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]

    return distances[end], path[::-1]
```

## Common Patterns

### Pattern 1: Shortest Path Variant
```python
# Standard Dijkstra with modifications
pq = [(0, start, initial_state)]
distances = defaultdict(lambda: float('inf'))
distances[(start, initial_state)] = 0

while pq:
    dist, node, state = heapq.heappop(pq)

    if (node, state) already processed:
        continue

    for neighbor, weight, new_state in get_transitions(node, state):
        new_dist = dist + weight
        if new_dist < distances[(neighbor, new_state)]:
            distances[(neighbor, new_state)] = new_dist
            heapq.heappush(pq, (new_dist, neighbor, new_state))
```

### Pattern 2: MST Construction
```python
# Kruskal pattern
edges.sort()
uf = UnionFind(n)
mst = []

for weight, u, v in edges:
    if uf.union(u, v):
        mst.append((u, v))
        if len(mst) == n - 1:
            break
```

### Pattern 3: Greedy Selection
```python
# Sort by some criterion
items.sort(key=lambda x: x.priority)

result = []
for item in items:
    if is_valid(item, result):
        result.append(item)
```

## Common Pitfalls

1. **Using Dijkstra with Negative Weights**: Produces wrong results
2. **Forgetting Visited Check**: Reprocessing nodes multiple times
3. **Wrong Priority Queue Order**: (node, distance) instead of (distance, node)
4. **Not Checking Reachability**: Assuming all nodes reachable
5. **Off-by-One in Node Indexing**: 0-indexed vs 1-indexed
6. **Modifying While Iterating**: Changing graph during traversal
7. **Memory Issues**: Creating all edges in complete graph

## Optimization Techniques

1. **Early Termination**: Stop when target found (single-target Dijkstra)
2. **Bidirectional Search**: Meet in middle for shortest path
3. **A* Heuristic**: Guide search toward goal
4. **Lazy Deletion**: Mark as deleted instead of removing from heap
5. **Path Compression**: Union-Find optimization
6. **Union by Rank**: Keep trees balanced

## Time Complexity Summary

| Problem | Time | Space | Algorithm |
|---------|------|-------|-----------|
| Reconstruct Itinerary | O(E log E) | O(E) | Hierholzer's |
| Min Cost Connect Points | O(N² log N) | O(N²) or O(N) | MST (Prim/Kruskal) |
| Network Delay Time | O((V+E) log V) | O(V+E) | Dijkstra |

## Practice Strategy

1. **Master Basic Algorithms**: Implement Dijkstra, Prim, Kruskal from scratch
2. **Understand When to Use Each**: Know which algorithm for which problem type
3. **Practice Variations**: Shortest path with constraints, modified MST
4. **Learn to Debug**: Print distances, paths, and intermediate states
5. **Optimize Gradually**: Start with correct solution, then optimize
6. **Study Proofs**: Understand why greedy algorithms work (when they do)

## Next Steps

After mastering these problems:
1. Study hard advanced graph problems (Dijkstra variants, complex MST)
2. Learn Floyd-Warshall for all-pairs shortest path
3. Study Bellman-Ford for negative weights
4. Explore network flow algorithms
5. Learn about strongly connected components
6. Practice graph optimization problems

## Additional Resources

- **Visualizations**: VisuAlgo for Dijkstra and MST animations
- **Books**: "Algorithm Design" by Kleinberg & Tardos
- **Courses**: Princeton Algorithms Part II (Coursera)
- **Practice**: LeetCode graph problems sorted by frequency
- **Theory**: Understanding time complexity proofs for greedy algorithms
