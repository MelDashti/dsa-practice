# Graphs - Medium Problems

## Overview

This directory contains medium-level graph problems that build upon basic traversal techniques. These problems introduce multi-source BFS, cycle detection, topological sorting, union-find, and more complex graph manipulation patterns.

## Advanced Graph Concepts

### 1. Multi-Source BFS

Start BFS from multiple sources simultaneously, processing them level by level.

```python
def multi_source_bfs(sources):
    visited = set(sources)
    queue = deque(sources)
    level = 0

    while queue:
        size = len(queue)
        for _ in range(size):
            node = queue.popleft()
            # Process node at current level

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        level += 1
```

**Use Cases**:
- Rotting Oranges (multiple starting points)
- Walls and Gates (distance from multiple gates)
- Multiple starting positions

### 2. Cycle Detection

**Undirected Graph (DFS)**:
```python
def has_cycle(node, parent, visited):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            if has_cycle(neighbor, node, visited):
                return True
        elif neighbor != parent:
            # Found cycle: visited neighbor that's not parent
            return True

    return False
```

**Directed Graph (DFS with states)**:
```python
def has_cycle():
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        if color[node] == GRAY:
            return True  # Back edge found (cycle)
        if color[node] == BLACK:
            return False  # Already processed

        color[node] = GRAY  # Mark as being processed

        for neighbor in graph[node]:
            if dfs(neighbor):
                return True

        color[node] = BLACK  # Mark as completed
        return False

    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False
```

### 3. Topological Sort

Order vertices such that for every directed edge (u, v), u comes before v.

**DFS-based (Reverse Post-order)**:
```python
def topological_sort():
    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        result.append(node)  # Add after processing all neighbors

    for node in graph:
        if node not in visited:
            dfs(node)

    return result[::-1]  # Reverse to get topological order
```

**Kahn's Algorithm (BFS-based)**:
```python
def topological_sort():
    in_degree = {node: 0 for node in graph}

    # Calculate in-degrees
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Start with nodes having in-degree 0
    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If result has all nodes, graph is a DAG
    return result if len(result) == len(graph) else []
```

### 4. Union-Find (Disjoint Set Union)

Efficiently tracks and merges disjoint sets.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Union by rank
        root_x, root_y = self.find(x), self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True  # Successfully merged

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Time Complexity**: Nearly O(1) per operation with path compression and union by rank (actually O(α(n)) where α is inverse Ackermann function)

### 5. Graph Cloning

Deep copy a graph preserving structure and values.

```python
def clone_graph(node):
    if not node:
        return None

    old_to_new = {}

    def dfs(node):
        if node in old_to_new:
            return old_to_new[node]

        copy = Node(node.val)
        old_to_new[node] = copy

        for neighbor in node.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)
```

## Problems in This Directory

### 1. Clone Graph (133)
**Concept**: Deep copy a graph
**Pattern**: DFS/BFS with hashmap to track old→new mapping
**Key Insight**: Create new node when first encountered, use map for subsequent references
**Edge Cases**: None/empty graph, single node, cycles

### 2. Max Area of Island (695)
**Concept**: Find the largest island in a grid
**Pattern**: DFS/BFS to calculate area of each component
**Key Insight**: Track maximum area while exploring each island
**Time**: O(m × n), **Space**: O(m × n)

### 3. Pacific Atlantic Water Flow (417)
**Concept**: Find cells where water can flow to both oceans
**Pattern**: Reverse thinking - start from oceans and work inward
**Key Insight**: Run DFS/BFS from ocean borders, find intersection
**Approach**:
```python
def pacificAtlantic(heights):
    if not heights:
        return []

    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()

    def dfs(r, c, visited):
        visited.add((r, c))
        directions = [(0,1), (0,-1), (1,0), (-1,0)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and
                heights[nr][nc] >= heights[r][c]):
                dfs(nr, nc, visited)

    # DFS from Pacific borders (top and left)
    for c in range(cols):
        dfs(0, c, pacific)
    for r in range(rows):
        dfs(r, 0, pacific)

    # DFS from Atlantic borders (bottom and right)
    for c in range(cols):
        dfs(rows-1, c, atlantic)
    for r in range(rows):
        dfs(r, cols-1, atlantic)

    return list(pacific & atlantic)
```

### 4. Surrounded Regions (130)
**Concept**: Capture regions surrounded by 'X'
**Pattern**: Find non-captured regions (connected to border) then flip others
**Key Insight**: Start from border 'O's, mark them safe, flip remaining 'O's
**Approach**: Border DFS/BFS + in-place modification

### 5. Rotting Oranges (994)
**Concept**: Calculate time for all oranges to rot (multi-source spread)
**Pattern**: Multi-source BFS with level tracking
**Key Insight**: Start BFS from all rotten oranges simultaneously
**Time**: O(m × n), **Space**: O(m × n)
**Return**: -1 if fresh oranges remain unreachable

### 6. Walls and Gates (286)
**Concept**: Fill distances to nearest gate
**Pattern**: Multi-source BFS from all gates
**Key Insight**: Process all gates simultaneously, closer gates fill first
**Time**: O(m × n), **Space**: O(m × n)

### 7. Course Schedule (207)
**Concept**: Detect if course schedule is possible (cycle detection)
**Pattern**: Detect cycle in directed graph
**Approaches**:
- DFS with three colors (white, gray, black)
- Kahn's algorithm (topological sort with in-degrees)
**Key Insight**: Cycle means impossible to complete courses
**Time**: O(V + E), **Space**: O(V + E)

### 8. Course Schedule II (210)
**Concept**: Return a valid course order
**Pattern**: Topological sort
**Approaches**:
- DFS with reverse post-order
- Kahn's algorithm (BFS-based)
**Key Insight**: Topological order exists iff no cycles
**Return**: Empty array if cycle detected

### 9. Redundant Connection (684)
**Concept**: Find edge that creates cycle in undirected graph
**Pattern**: Union-Find to detect cycle
**Key Insight**: Edge connecting already-connected nodes creates cycle
**Approach**:
```python
def findRedundantConnection(edges):
    uf = UnionFind(len(edges))

    for u, v in edges:
        if not uf.union(u-1, v-1):  # Already connected
            return [u, v]

    return []
```
**Time**: O(n × α(n)) ≈ O(n), **Space**: O(n)

### 10. Number of Connected Components (323)
**Concept**: Count connected components in undirected graph
**Pattern**: DFS/BFS count or Union-Find
**Approaches**:
- DFS/BFS: Count times we start new traversal
- Union-Find: Count distinct roots
**Time**: O(V + E) or O(E × α(V)), **Space**: O(V)

### 11. Graph Valid Tree (261)
**Concept**: Check if graph is a valid tree
**Pattern**: Tree properties verification
**Key Insight**: Tree iff:
  - Exactly n-1 edges for n nodes
  - Connected (one component)
  - No cycles
**Approaches**:
- DFS with cycle detection + connectivity check
- Union-Find to detect cycle + count components
**Time**: O(V + E), **Space**: O(V)

## Problem-Solving Strategies

### When to Use DFS:
- Need to explore all paths
- Cycle detection
- Topological sort
- Path finding with all possibilities
- Backtracking needed

### When to Use BFS:
- Shortest path in unweighted graph
- Level-order traversal
- Multi-source propagation
- Minimum steps/time problems

### When to Use Union-Find:
- Dynamic connectivity queries
- Detecting cycles in undirected graphs
- Counting connected components
- Minimum spanning tree

### Pattern Recognition:

| Problem Type | Algorithm | Example |
|--------------|-----------|---------|
| Multi-source spread | Multi-source BFS | Rotting Oranges |
| Reverse thinking | Border DFS/BFS | Surrounded Regions |
| Course dependencies | Topological Sort | Course Schedule |
| Cycle detection | DFS or Union-Find | Redundant Connection |
| Component counting | DFS/BFS or Union-Find | Connected Components |
| Graph copying | DFS/BFS with hashmap | Clone Graph |

## Advanced Techniques

### 1. Bidirectional Search
Search from both start and end, meet in middle.
```python
def bidirectional_search(start, end):
    if start == end:
        return 0

    front = {start}
    back = {end}
    visited_front = {start}
    visited_back = {end}
    level = 0

    while front and back:
        if len(front) > len(back):
            front, back = back, front
            visited_front, visited_back = visited_back, visited_front

        level += 1
        next_level = set()

        for node in front:
            for neighbor in graph[node]:
                if neighbor in back:
                    return level
                if neighbor not in visited_front:
                    visited_front.add(neighbor)
                    next_level.add(neighbor)

        front = next_level

    return -1  # No path found
```

### 2. State-based BFS
Track state beyond just position (e.g., keys collected, walls broken).
```python
def state_bfs(start):
    # state = (position, additional_info)
    queue = deque([(start, initial_state, 0)])
    visited = {(start, initial_state)}

    while queue:
        pos, state, steps = queue.popleft()

        if is_goal(pos, state):
            return steps

        for next_pos, next_state in get_next_states(pos, state):
            if (next_pos, next_state) not in visited:
                visited.add((next_pos, next_state))
                queue.append((next_pos, next_state, steps + 1))

    return -1
```

### 3. Modified DFS for Ordering
Track ordering information during traversal.
```python
def dfs_with_timing():
    time = 0
    discovery = {}
    finish = {}

    def dfs(node):
        nonlocal time
        time += 1
        discovery[node] = time

        for neighbor in graph[node]:
            if neighbor not in discovery:
                dfs(neighbor)

        time += 1
        finish[node] = time

    for node in graph:
        if node not in discovery:
            dfs(node)

    return discovery, finish
```

## Common Pitfalls

1. **Not Handling Disconnected Graphs**: Loop through all vertices for DFS/BFS
2. **Marking Visited Too Late**: Mark when adding to queue (BFS), not when popping
3. **Wrong Cycle Detection**: Undirected graphs need parent tracking
4. **Forgetting Reverse**: Topological sort with DFS needs reversal
5. **In-degree Errors**: Careful calculation for Kahn's algorithm
6. **Union-Find Without Optimization**: Use path compression and union by rank
7. **Modifying While Iterating**: Create copy if modifying graph during traversal

## Optimization Techniques

1. **Path Compression** (Union-Find): Make tree flatter
2. **Union by Rank** (Union-Find): Attach smaller tree to larger
3. **Early Termination**: Return as soon as answer found
4. **In-place Modification**: Save space by modifying input
5. **Bidirectional Search**: Meet in middle for shorter search
6. **Visited Set**: Use set instead of list for O(1) lookup
7. **Deque**: Use collections.deque for O(1) queue operations

## Time Complexity Summary

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Clone Graph | O(V + E) | O(V) | Visit each vertex and edge once |
| Max Area Island | O(m × n) | O(m × n) | Grid traversal |
| Pacific Atlantic | O(m × n) | O(m × n) | DFS from borders |
| Surrounded Regions | O(m × n) | O(m × n) | Border DFS |
| Rotting Oranges | O(m × n) | O(m × n) | Multi-source BFS |
| Walls and Gates | O(m × n) | O(m × n) | Multi-source BFS |
| Course Schedule | O(V + E) | O(V + E) | DFS/BFS for cycle |
| Course Schedule II | O(V + E) | O(V + E) | Topological sort |
| Redundant Connection | O(n × α(n)) | O(n) | Union-Find |
| Connected Components | O(V + E) | O(V) | DFS/BFS or Union-Find |
| Graph Valid Tree | O(V + E) | O(V) | DFS/BFS or Union-Find |

## Practice Strategy

1. **Master Basic Traversals**: Ensure solid understanding of DFS/BFS
2. **Learn Pattern Variations**: Multi-source, reverse thinking, state-based
3. **Study Union-Find**: Essential for connectivity problems
4. **Practice Topological Sort**: Both DFS and BFS approaches
5. **Understand Cycle Detection**: Different for directed vs undirected
6. **Work on Grid Problems**: Bridge between arrays and graphs
7. **Draw Examples**: Visualize graph structure and algorithm steps

## Related Concepts

### Graph Properties:
- **Tree**: Connected acyclic graph with V-1 edges
- **DAG**: Directed Acyclic Graph (topological order exists)
- **Bipartite**: Can color with 2 colors (no odd cycles)
- **Complete**: Edge between every pair of vertices
- **Sparse**: E ≈ V (adjacency list preferred)
- **Dense**: E ≈ V² (adjacency matrix preferred)

### Advanced Topics to Study:
- Shortest path algorithms (Dijkstra, Bellman-Ford)
- Minimum spanning tree (Kruskal, Prim)
- Strongly connected components (Kosaraju, Tarjan)
- Bipartite matching
- Network flow

## Debugging Tips

1. **Draw Small Examples**: Visualize on paper
2. **Check Visited Logic**: Ensure correct timing of marking
3. **Verify Directions**: Confirm directed vs undirected handling
4. **Test Edge Cases**: Empty graph, single node, disconnected components
5. **Print State**: Log current node and neighbors during traversal
6. **Check Indices**: Off-by-one errors in grid problems
7. **Validate Input**: Ensure graph is properly constructed

## Next Steps

After mastering medium graph problems:
1. Study weighted graph algorithms (Dijkstra, Bellman-Ford)
2. Learn about minimum spanning trees
3. Explore advanced graph problems (strongly connected components)
4. Practice network flow problems
5. Study graph optimization algorithms
6. Learn about specialized graph structures (tries, segment trees)

## Additional Resources

- **Visualizations**: VisuAlgo, Algorithm Visualizer
- **Books**: Introduction to Algorithms (CLRS), Algorithm Design Manual
- **Online Judges**: LeetCode, Codeforces, HackerRank
- **Courses**: MIT 6.006, Princeton Algorithms Part II
