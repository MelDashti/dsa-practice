# Advanced Graphs - Hard Problems

## Overview

This directory contains hard-level advanced graph problems that require sophisticated algorithms and optimizations. These problems often combine multiple graph concepts, require complex state management, and demand deep algorithmic insight to achieve acceptable performance.

## Advanced Algorithms

### 1. Modified Dijkstra with State

Standard Dijkstra tracks only distance. Modified versions track additional state.

**Pattern**:
```python
def dijkstra_with_state(graph, start, end):
    # State: (cost, node, additional_state)
    pq = [(0, start, initial_state)]
    visited = set()

    while pq:
        cost, node, state = heapq.heappop(pq)

        state_key = (node, state)
        if state_key in visited:
            continue

        visited.add(state_key)

        if node == end and satisfies_condition(state):
            return cost

        for neighbor, edge_cost, new_state in get_transitions(node, state, graph):
            if (neighbor, new_state) not in visited:
                heapq.heappush(pq, (cost + edge_cost, neighbor, new_state))

    return -1
```

**State Examples**:
- Keys collected
- Constraints satisfied
- Resources remaining
- Previous node (for path constraints)

### 2. Binary Search on Graph Properties

Sometimes answer can be binary searched, checking feasibility at each value.

**Pattern**:
```python
def binary_search_answer(graph, condition):
    left, right = min_value, max_value

    def is_feasible(mid):
        # Check if solution exists with value <= mid
        # Use BFS/DFS/Dijkstra to verify
        return check_condition(graph, mid)

    while left < right:
        mid = (left + right) // 2

        if is_feasible(mid):
            right = mid  # Try smaller value
        else:
            left = mid + 1  # Need larger value

    return left
```

**When to Use**:
- Answer has monotonic property
- Can verify feasibility efficiently
- Range of answers is known

### 3. Topological Sort with Complex Dependencies

Handle multiple types of dependencies and constraints.

```python
def topological_sort_complex(graph, constraints):
    in_degree = defaultdict(int)
    adj_list = defaultdict(list)

    # Build graph with all constraints
    for u, v in graph:
        adj_list[u].append(v)
        in_degree[v] += 1

    # Apply additional constraints
    for constraint in constraints:
        if not apply_constraint(adj_list, in_degree, constraint):
            return []  # Impossible

    # Kahn's algorithm
    queue = deque([node for node in adj_list if in_degree[node] == 0])
    result = []

    while queue:
        # Can sort queue for lexicographic order
        node = queue.popleft()
        result.append(node)

        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(adj_list) else []
```

### 4. Union-Find with Rollback

Support undoing union operations (useful for offline queries).

```python
class UnionFindWithRollback:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.history = []

    def find(self, x):
        # No path compression (would complicate rollback)
        if self.parent[x] != x:
            return self.find(self.parent[x])
        return x

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)

        if root_x == root_y:
            self.history.append(None)
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.history.append((root_y, self.parent[root_y], self.rank[root_x]))
        self.parent[root_y] = root_x

        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        return True

    def rollback(self):
        if not self.history:
            return

        snapshot = self.history.pop()
        if snapshot is None:
            return

        node, old_parent, old_rank = snapshot
        self.parent[node] = old_parent
        self.rank[self.find(node)] = old_rank
```

## Problems in This Directory

### 1. Swim in Rising Water (778)

**Problem**: N×N grid where each cell has elevation. Start at (0,0), reach (N-1,N-1). At time T, can walk on cells with elevation ≤ T. Find minimum time to reach destination.

**Concept**: Binary search + BFS, or Modified Dijkstra

**Key Insights**:
- Time to reach = max elevation on optimal path
- Want to minimize the maximum elevation encountered
- This is a "minimax" path problem
- Can binary search on time, check reachability with BFS
- Or use modified Dijkstra tracking max elevation

**Approach 1 - Binary Search + BFS**:
```python
def swimInWater(grid):
    n = len(grid)

    def can_reach(time):
        if grid[0][0] > time:
            return False

        visited = {(0, 0)}
        queue = deque([(0, 0)])

        while queue:
            r, c = queue.popleft()

            if r == n - 1 and c == n - 1:
                return True

            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                nr, nc = r + dr, c + dc

                if (0 <= nr < n and 0 <= nc < n and
                    (nr, nc) not in visited and
                    grid[nr][nc] <= time):

                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return False

    left, right = grid[0][0], n * n - 1

    while left < right:
        mid = (left + right) // 2

        if can_reach(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

**Time**: O(N² log(N²)) = O(N² log N)
**Space**: O(N²)

**Approach 2 - Modified Dijkstra**:
```python
def swimInWater(grid):
    n = len(grid)

    # Priority queue: (max_elevation_so_far, row, col)
    pq = [(grid[0][0], 0, 0)]
    visited = set()

    while pq:
        time, r, c = heapq.heappop(pq)

        if (r, c) in visited:
            continue

        visited.add((r, c))

        if r == n - 1 and c == n - 1:
            return time

        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                new_time = max(time, grid[nr][nc])
                heapq.heappush(pq, (new_time, nr, nc))

    return -1
```

**Time**: O(N² log N)
**Space**: O(N²)

**Why Modified Dijkstra**:
- Standard Dijkstra minimizes sum of weights
- Here we minimize maximum weight on path
- Still works because we greedily select minimum "max-so-far"

**Edge Cases**:
- N = 1 (already at destination)
- Start elevation > 0
- Very large elevations

### 2. Alien Dictionary (269)

**Problem**: Given sorted dictionary of alien language, determine lexicographic order of characters. Return empty string if order is invalid.

**Concept**: Topological sort with character ordering

**Key Insights**:
- Sorted dictionary gives ordering constraints
- Compare adjacent words to infer character order
- Build directed graph: edge from c1 to c2 means c1 < c2
- Topological sort gives character order
- Cycle means invalid ordering

**Approach - Topological Sort**:
```python
def alienOrder(words):
    # Build graph
    graph = {c: set() for word in words for c in word}
    in_degree = {c: 0 for c in graph}

    # Compare adjacent words
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))

        # Check for invalid case: "abc" before "ab"
        if word1[:min_len] == word2[:min_len] and len(word1) > len(word2):
            return ""

        # Find first differing character
        for j in range(min_len):
            if word1[j] != word2[j]:
                if word2[j] not in graph[word1[j]]:
                    graph[word1[j]].add(word2[j])
                    in_degree[word2[j]] += 1
                break  # Only first difference matters

    # Topological sort (Kahn's algorithm)
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []

    while queue:
        char = queue.popleft()
        result.append(char)

        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycle (invalid ordering)
    if len(result) != len(graph):
        return ""

    return ''.join(result)
```

**Time**: O(C) where C is total characters in all words
**Space**: O(1) or O(26) since limited alphabet

**Common Mistakes**:
1. Not checking invalid case (longer word before its prefix)
2. Comparing all character pairs instead of just first difference
3. Not detecting cycles
4. Not handling single character words
5. Assuming all characters appear in comparisons

**Edge Cases**:
- Empty input
- Single word
- Words with no ordering info
- Invalid ordering (cycle)
- Longer word before its prefix

### 3. Cheapest Flights Within K Stops (787)

**Problem**: Find cheapest flight from source to destination with at most K stops. Return -1 if impossible.

**Concept**: Shortest path with constraint on path length

**Key Insights**:
- Standard Dijkstra doesn't work (doesn't track stops)
- Need to track (cost, node, stops)
- Can visit same node multiple times with different stop counts
- Bellman-Ford variation or Modified Dijkstra
- BFS with K levels also works

**Approach 1 - Modified Dijkstra**:
```python
def findCheapestPrice(n, flights, src, dst, k):
    # Build graph
    graph = defaultdict(list)
    for u, v, price in flights:
        graph[u].append((v, price))

    # Priority queue: (cost, node, stops)
    pq = [(0, src, 0)]

    # Track minimum cost to reach (node, stops)
    visited = {}

    while pq:
        cost, node, stops = heapq.heappop(pq)

        if node == dst:
            return cost

        if stops > k:
            continue

        # Prevent reprocessing same (node, stops) with higher cost
        if (node, stops) in visited and visited[(node, stops)] <= cost:
            continue

        visited[(node, stops)] = cost

        for neighbor, price in graph[node]:
            new_cost = cost + price
            heapq.heappush(pq, (new_cost, neighbor, stops + 1))

    return -1
```

**Approach 2 - Bellman-Ford (Cleaner)**:
```python
def findCheapestPrice(n, flights, src, dst, k):
    # Distance array
    prices = [float('inf')] * n
    prices[src] = 0

    # Relax edges k+1 times (k stops = k+1 edges)
    for _ in range(k + 1):
        temp_prices = prices[:]

        for u, v, price in flights:
            if prices[u] != float('inf'):
                temp_prices[v] = min(temp_prices[v], prices[u] + price)

        prices = temp_prices

    return prices[dst] if prices[dst] != float('inf') else -1
```

**Approach 3 - BFS with Level Tracking**:
```python
def findCheapestPrice(n, flights, src, dst, k):
    graph = defaultdict(list)
    for u, v, price in flights:
        graph[u].append((v, price))

    queue = deque([(src, 0)])  # (node, cost)
    min_cost = {src: 0}
    stops = 0

    while queue and stops <= k:
        size = len(queue)

        for _ in range(size):
            node, cost = queue.popleft()

            for neighbor, price in graph[node]:
                new_cost = cost + price

                # Only proceed if this is cheaper way to reach neighbor
                if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                    min_cost[neighbor] = new_cost
                    queue.append((neighbor, new_cost))

        stops += 1

    return min_cost.get(dst, -1)
```

**Complexity Comparison**:
| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Modified Dijkstra | O(E × K × log(E × K)) | O(E × K) | Can visit (node, stops) multiple times |
| Bellman-Ford | O(E × K) | O(N) | Simpler, guaranteed correctness |
| BFS | O(E × K) | O(E) | Intuitive, level-based |

**When Each Approach is Best**:
- **Dijkstra**: When you need exact path reconstruction
- **Bellman-Ford**: Clean solution, guaranteed correctness
- **BFS**: When K is small, most intuitive

**Common Pitfalls**:
1. Using standard Dijkstra (doesn't handle stop constraint)
2. Not allowing revisiting nodes (may need to visit with different stops)
3. Wrong stopping condition (stops vs edges)
4. Not handling case where direct flight is cheaper than with stops

**Edge Cases**:
- K = 0 (only direct flights)
- No path exists
- Src = Dst
- Cycles in graph
- Multiple flights between same cities

## Advanced Problem-Solving Patterns

### Pattern 1: Minimax/Maximin Path Problems

Find path that minimizes the maximum (or maximizes the minimum) edge weight.

**Solution**: Modified Dijkstra tracking max/min
```python
def minimax_path(graph, start, end):
    # Track maximum edge weight on path to each node
    pq = [(0, start)]  # (max_weight_so_far, node)
    visited = set()

    while pq:
        max_weight, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if node == end:
            return max_weight

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                new_max = max(max_weight, weight)
                heapq.heappush(pq, (new_max, neighbor))

    return -1
```

### Pattern 2: Constrained Shortest Path

Find shortest path satisfying additional constraints.

**Strategies**:
1. Expand state space to include constraint info
2. Use modified priority (cost, constraint_value)
3. Track multiple dimensions in visited set

### Pattern 3: Binary Search on Graph Properties

Search for threshold value, verify feasibility with graph algorithm.

**Template**:
```python
def binary_search_graph(graph, target):
    def is_feasible(mid):
        # Run graph algorithm with threshold mid
        # Return True if achievable
        pass

    left, right = find_bounds(graph)

    while left < right:
        mid = (left + right) // 2

        if is_feasible(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

### Pattern 4: Multi-Dimensional Dijkstra

Track multiple state dimensions.

```python
def multi_dim_dijkstra(graph, start, end, max_constraint):
    # State: (cost, node, constraint_value)
    pq = [(0, start, 0)]
    visited = set()

    while pq:
        cost, node, constraint = heapq.heappop(pq)

        if (node, constraint) in visited:
            continue

        visited.add((node, constraint))

        if node == end:
            return cost

        for neighbor, edge_cost, edge_constraint in graph[node]:
            new_constraint = constraint + edge_constraint

            if new_constraint <= max_constraint:
                heapq.heappush(pq,
                    (cost + edge_cost, neighbor, new_constraint))

    return -1
```

## Algorithm Selection Guide

### Decision Tree:

1. **What are you minimizing?**
   - Sum of weights → Standard Dijkstra or BFS
   - Max weight on path → Modified Dijkstra (minimax)
   - Path length with constraints → Modified Dijkstra/BFS

2. **Any constraints?**
   - No constraints → Standard algorithms
   - Path length constraint → Track in state
   - Resource constraint → Expand state space

3. **Graph properties?**
   - Unweighted → BFS
   - Non-negative weights → Dijkstra
   - Any weights → Bellman-Ford
   - Need all-pairs → Floyd-Warshall

4. **Optimization possible?**
   - Monotonic property → Binary search
   - Meeting in middle → Bidirectional search
   - Heuristic available → A*

## Complexity Analysis for Hard Problems

### Time Complexity Factors:
- **V**: Number of vertices
- **E**: Number of edges
- **K**: Constraint parameter (stops, keys, etc.)
- **W**: Maximum weight/value
- **Log factors**: From priority queue operations

### Common Complexities:
| Problem Type | Typical Complexity | Why |
|--------------|-------------------|-----|
| Modified Dijkstra | O(E × K × log(V × K)) | K states per vertex |
| Binary Search + BFS | O((V + E) × log W) | Binary search on weights |
| Bellman-Ford variant | O(V × E × K) | K iterations of relaxation |
| Multi-dim state | O(E × K₁ × K₂ × ...) | Cartesian product of constraints |

## Optimization Techniques

### 1. State Space Reduction
Minimize what you track in state:
```python
# Instead of: (cost, node, path, resources, constraints, ...)
# Use: (cost, node, essential_state_only)
```

### 2. Pruning Strategies
Eliminate states that cannot lead to optimal solution:
```python
if lower_bound(state) >= current_best:
    continue  # Prune
```

### 3. Bidirectional Search
For shortest path problems, search from both ends:
```python
# Meet in middle
if node in back_visited:
    return front_cost[node] + back_cost[node]
```

### 4. A* Heuristic
Guide search toward goal:
```python
def heuristic(node, goal):
    # Admissible heuristic (never overestimates)
    return manhattan_distance(node, goal)

pq = [(cost + heuristic(node, goal), cost, node)]
```

### 5. Lazy Deletion
Don't remove from heap, just skip if outdated:
```python
if (node, state) in visited and visited[(node, state)] <= cost:
    continue
```

## Common Pitfalls

1. **State Space Explosion**: Track only essential state
2. **Incorrect Visited Logic**: May need to revisit with different state
3. **Wrong Constraint Handling**: Off-by-one in stop counting
4. **Priority Queue Issues**: Wrong tuple order, not handling ties
5. **Missing Edge Cases**: Source=destination, no path exists
6. **Infinite Loops**: Not marking visited correctly
7. **Memory Limits**: Too much state tracking

## Interview Strategy

### 1. Problem Analysis (5 minutes)
- Identify graph structure
- Recognize if standard algorithm applies
- Identify constraints and how they affect state

### 2. Solution Design (10 minutes)
- Choose appropriate algorithm
- Design state representation
- Consider edge cases
- Estimate complexity

### 3. Implementation (20-25 minutes)
- Write clean, modular code
- Handle edge cases
- Test with examples
- Verify correctness

### 4. Optimization (5-10 minutes)
- Identify bottlenecks
- Apply optimizations
- Discuss tradeoffs

## Time Complexity Summary

| Problem | Time | Space | Key Algorithm |
|---------|------|-------|---------------|
| Swim in Rising Water | O(N² log N) | O(N²) | Modified Dijkstra / Binary Search |
| Alien Dictionary | O(C) | O(1) | Topological Sort |
| Cheapest Flights K Stops | O(E × K) | O(V × K) | Modified Dijkstra / Bellman-Ford |

## Practice Strategy

1. **Master Standard Algorithms**: Dijkstra, Bellman-Ford, Topological Sort
2. **Learn Modifications**: Understand how to adapt for constraints
3. **Practice State Design**: Determine minimal state needed
4. **Study Optimizations**: When binary search, bidirectional, A* apply
5. **Analyze Complexity**: Count state space size accurately
6. **Handle Edge Cases**: Test boundary conditions thoroughly
7. **Time Yourself**: Practice under interview conditions

## Related Concepts

### Graph Problem Categories:
1. **Shortest Path**: Dijkstra, Bellman-Ford, Floyd-Warshall, A*
2. **MST**: Kruskal, Prim, Boruvka
3. **Flow**: Max-flow, Min-cut, Bipartite matching
4. **Connectivity**: SCC, Bridges, Articulation points
5. **Ordering**: Topological sort, Eulerian path
6. **Coloring**: Bipartite check, Graph coloring

### Advanced Topics:
- Strongly Connected Components (Kosaraju, Tarjan)
- Network Flow (Ford-Fulkerson, Dinic)
- Bipartite Matching (Hungarian algorithm)
- Approximation Algorithms for NP-hard graph problems
- Parallel Graph Algorithms

## Next Steps

After mastering hard advanced graph problems:
1. Study network flow algorithms
2. Learn about advanced graph decomposition
3. Explore computational geometry on graphs
4. Practice competitive programming graph problems
5. Study approximation algorithms
6. Learn about graph neural networks (if interested in ML)

## Additional Resources

- **Books**:
  - "Algorithm Design" by Kleinberg & Tardos
  - "Competitive Programming 4" by Halim & Halim
  - "Introduction to Algorithms" (CLRS)

- **Online Courses**:
  - MIT 6.046J (Advanced Algorithms)
  - Stanford CS261 (Optimization and Algorithmic Paradigms)

- **Practice Platforms**:
  - LeetCode Hard graph problems
  - Codeforces graphs tags
  - AtCoder graph problems
  - USACO Gold/Platinum

- **Visualization**:
  - Algorithm Visualizer
  - VisuAlgo
  - Graph Online (graph visualization tool)
