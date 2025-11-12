# Graphs - Easy Problems

## Overview

This directory contains easy-level graph problems that introduce fundamental graph concepts, traversal algorithms, and basic problem-solving patterns. These problems form the foundation for more complex graph algorithms.

## What is a Graph?

A graph is a data structure consisting of:
- **Vertices (Nodes)**: The points in the graph
- **Edges**: Connections between vertices

### Graph Types:

1. **Directed vs. Undirected**:
   - Directed: Edges have direction (A → B)
   - Undirected: Edges are bidirectional (A ↔ B)

2. **Weighted vs. Unweighted**:
   - Weighted: Edges have associated costs/weights
   - Unweighted: All edges are equal

3. **Connected vs. Disconnected**:
   - Connected: Path exists between any two vertices
   - Disconnected: Some vertices are unreachable from others

### Graph Representations:

**1. Adjacency Matrix**:
```python
# n x n matrix where matrix[i][j] = 1 if edge exists
graph = [[0, 1, 1],
         [1, 0, 0],
         [1, 0, 0]]
```
- Space: O(V²)
- Edge lookup: O(1)
- Finding neighbors: O(V)

**2. Adjacency List**:
```python
# Dictionary mapping vertex to list of neighbors
graph = {
    0: [1, 2],
    1: [0],
    2: [0]
}
```
- Space: O(V + E)
- Edge lookup: O(degree)
- Finding neighbors: O(degree)

**3. Edge List**:
```python
# List of all edges
edges = [(0, 1), (0, 2), (1, 3)]
```
- Space: O(E)
- Best for union-find problems

## Core Traversal Algorithms

### 1. Depth-First Search (DFS)

Explores as far as possible along each branch before backtracking.

**Recursive Implementation**:
```python
def dfs(node, visited):
    if node in visited:
        return

    visited.add(node)
    # Process node

    for neighbor in graph[node]:
        dfs(neighbor, visited)
```

**Iterative Implementation (using stack)**:
```python
def dfs_iterative(start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        # Process node

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

**Characteristics**:
- Uses stack (or recursion)
- Time: O(V + E)
- Space: O(V) for visited set + O(V) for recursion/stack
- Good for: Detecting cycles, topological sort, finding connected components

### 2. Breadth-First Search (BFS)

Explores all neighbors at current depth before moving to next depth.

**Implementation (using queue)**:
```python
from collections import deque

def bfs(start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        # Process node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Characteristics**:
- Uses queue
- Time: O(V + E)
- Space: O(V) for visited set + O(V) for queue
- Good for: Shortest path in unweighted graphs, level-order traversal

### DFS vs BFS Comparison:

| Aspect | DFS | BFS |
|--------|-----|-----|
| Data Structure | Stack (recursion) | Queue |
| Exploration | Deep then backtrack | Level by level |
| Path | Not guaranteed shortest | Shortest in unweighted |
| Memory | Less (just path) | More (all nodes at level) |
| Use Cases | Cycle detection, topological sort | Shortest path, level traversal |

## Grid Problems

Many graph problems are represented as 2D grids where each cell is a node.

### Grid as Graph:
```python
# Each cell has up to 4 neighbors (up, down, left, right)
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def get_neighbors(row, col, rows, cols):
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    return neighbors
```

### Grid DFS Pattern:
```python
def dfs(row, col):
    # Base cases
    if (row < 0 or row >= rows or col < 0 or col >= cols or
        (row, col) in visited or grid[row][col] == 0):
        return

    visited.add((row, col))

    # Explore all 4 directions
    dfs(row + 1, col)
    dfs(row - 1, col)
    dfs(row, col + 1)
    dfs(row, col - 1)
```

### Grid BFS Pattern:
```python
def bfs(start_row, start_col):
    visited = {(start_row, start_col)}
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < rows and 0 <= new_col < cols and
                (new_row, new_col) not in visited and
                grid[new_row][new_col] == 1):

                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
```

## Problems in This Directory

### Number of Islands (200)
**LeetCode**: https://leetcode.com/problems/number-of-islands/

**Problem**: Count the number of islands in a 2D grid where '1' is land and '0' is water. Islands are formed by connecting adjacent lands horizontally or vertically.

**Concept**: Connected components in a grid graph

**Approach 1 - DFS**:
```python
def numIslands(grid):
    if not grid:
        return 0

    islands = 0
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] == '0'):
            return

        visited.add((r, c))

        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                islands += 1

    return islands
```

**Approach 2 - BFS**:
```python
def numIslands(grid):
    if not grid:
        return 0

    islands = 0
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def bfs(r, c):
        queue = deque([(r, c)])
        visited.add((r, c))

        while queue:
            row, col = queue.popleft()

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                new_r, new_c = row + dr, col + dc

                if (0 <= new_r < rows and 0 <= new_c < cols and
                    (new_r, new_c) not in visited and
                    grid[new_r][new_c] == '1'):

                    visited.add((new_r, new_c))
                    queue.append((new_r, new_c))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                bfs(r, c)
                islands += 1

    return islands
```

**Approach 3 - In-place Modification** (Space Optimized):
```python
def numIslands(grid):
    if not grid:
        return 0

    islands = 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != '1'):
            return

        grid[r][c] = '0'  # Mark as visited

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                islands += 1

    return islands
```

**Key Insights**:
- Each island is a connected component
- Start DFS/BFS from each unvisited land cell
- Mark cells as visited to avoid recounting
- Can modify grid in-place to save space

**Time Complexity**: O(m × n) where m, n are dimensions
**Space Complexity**:
- O(m × n) with visited set
- O(1) with in-place modification (excluding recursion stack)
- O(min(m, n)) for recursion depth in worst case

**Edge Cases**:
- Empty grid
- All water (return 0)
- All land (return 1)
- Single cell
- Diagonal connections (not counted as adjacent)

**Variations**:
- Number of Islands II (with adding islands dynamically)
- Max Area of Island (find largest island)
- Number of Distinct Islands (count unique shapes)

**Common Mistakes**:
- Forgetting to mark cells as visited
- Incorrect boundary checks
- Counting diagonal neighbors
- Not handling empty grid
- Modifying grid when problem requires original to be preserved

## Key Concepts for Easy Graph Problems

### 1. Connected Components
- Group of vertices where each vertex is reachable from others
- Count by doing DFS/BFS from each unvisited vertex

### 2. Graph Traversal
- Systematic way to visit all vertices
- DFS for deep exploration
- BFS for level-by-level exploration

### 3. Visited Tracking
- Essential to avoid infinite loops
- Can use set, array, or in-place modification
- Must mark before adding to queue/stack (BFS) or at start of function (DFS)

### 4. Grid Navigation
- 4 directions: up, down, left, right
- 8 directions: add diagonals
- Boundary checking is crucial

## Common Patterns

### Pattern 1: Count Components
```python
count = 0
for each unvisited node:
    traverse_component(node)  # DFS or BFS
    count += 1
```

### Pattern 2: Mark and Explore
```python
visited = set()
for each cell in grid:
    if cell is valid and not visited:
        explore(cell)
```

### Pattern 3: Grid Traversal
```python
for row in range(rows):
    for col in range(cols):
        if grid[row][col] meets condition:
            dfs(row, col)
```

## Practice Strategy

1. **Understand Graph Representation**: Know how to convert between different representations
2. **Master DFS and BFS**: Practice both recursive and iterative versions
3. **Grid Problems**: Treat grids as graphs with directional edges
4. **Visited Tracking**: Understand when and how to mark vertices as visited
5. **Edge Cases**: Always consider empty graphs, single nodes, disconnected components

## Common Pitfalls

1. **Forgetting Boundary Checks**: Always validate indices for grids
2. **Infinite Loops**: Must track visited nodes
3. **Wrong Data Structure**: Using stack for BFS or queue for DFS
4. **Marking Visited Too Late**: Mark before adding to queue (BFS)
5. **Modifying Input**: Be careful if input should be preserved

## Optimization Tips

1. **In-place Modification**: Save space by modifying grid directly
2. **Early Termination**: Return early when answer is found
3. **Direction Arrays**: Use arrays for cleaner directional movement
4. **Union-Find**: Consider for dynamic connectivity problems

## Next Steps

After mastering easy graph problems:
1. Move to medium graph problems with more complex traversals
2. Study weighted graphs and Dijkstra's algorithm
3. Learn about topological sorting
4. Practice cycle detection
5. Study bipartite graphs and graph coloring

## Time Complexity Reference

| Operation | Adjacency List | Adjacency Matrix |
|-----------|----------------|------------------|
| Add vertex | O(1) | O(V²) |
| Add edge | O(1) | O(1) |
| Remove vertex | O(V + E) | O(V²) |
| Remove edge | O(E) | O(1) |
| Query edge | O(V) | O(1) |
| Traverse | O(V + E) | O(V²) |
| Space | O(V + E) | O(V²) |

## Additional Resources

- **Visualizations**: Use tools like VisuAlgo to visualize DFS/BFS
- **Graph Theory Basics**: Study basic graph theory terminology
- **Practice**: Solve similar problems on LeetCode, HackerRank
- **Debug**: Draw out small examples on paper
