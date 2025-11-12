# Graphs - Hard Problems

## Overview

This directory contains hard-level graph problems that require advanced algorithms, complex state management, and sophisticated optimization techniques. These problems often combine multiple graph concepts and require deep algorithmic insight.

## Advanced Graph Algorithms

### 1. Bidirectional BFS

Search from both source and destination simultaneously, meeting in the middle. This can significantly reduce search space.

**Why It's Faster**:
- Regular BFS: O(b^d) where b is branching factor, d is depth
- Bidirectional: O(b^(d/2) + b^(d/2)) = O(2 × b^(d/2))
- Huge savings when b is large

**Implementation**:
```python
def bidirectional_bfs(start, end, graph):
    if start == end:
        return 0

    # Two frontiers
    front_set = {start}
    back_set = {end}

    # Visited from each direction
    front_visited = {start: 0}
    back_visited = {end: 0}

    level = 0

    while front_set and back_set:
        # Always expand smaller frontier
        if len(front_set) > len(back_set):
            front_set, back_set = back_set, front_set
            front_visited, back_visited = back_visited, front_visited

        level += 1
        next_front = set()

        for node in front_set:
            for neighbor in graph[node]:
                # Found connection between frontiers
                if neighbor in back_visited:
                    return level + back_visited[neighbor]

                if neighbor not in front_visited:
                    front_visited[neighbor] = level
                    next_front.add(neighbor)

        front_set = next_front

    return -1  # No path exists
```

### 2. Word Transformation with BFS

Transform one word to another, changing one letter at a time, using only dictionary words.

**Key Insights**:
- Each word is a node
- Edge exists if words differ by one letter
- BFS finds shortest transformation sequence
- Can optimize by building graph or using bidirectional BFS

**Optimization Strategies**:

**A. Build Full Graph (if used multiple times)**:
```python
def build_graph(word_list):
    graph = defaultdict(list)

    for word in word_list:
        for i in range(len(word)):
            # Create pattern with wildcard
            pattern = word[:i] + '*' + word[i+1:]
            graph[pattern].append(word)

    return graph
```

**B. On-the-fly Generation**:
```python
def get_neighbors(word, word_set):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set:
                    neighbors.append(new_word)
    return neighbors
```

**C. Bidirectional BFS** (Optimal):
```python
def ladderLength(beginWord, endWord, wordList):
    if endWord not in wordList:
        return 0

    word_set = set(wordList)
    front = {beginWord}
    back = {endWord}
    length = 1

    while front:
        if len(front) > len(back):
            front, back = back, front

        next_front = set()
        for word in front:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i+1:]

                    if new_word in back:
                        return length + 1

                    if new_word in word_set:
                        next_front.add(new_word)
                        word_set.remove(new_word)

        front = next_front
        length += 1

    return 0
```

### 3. State-Space Search

Problems where state is more than just position - includes additional context.

**State Components**:
- Position/location
- Items collected
- Constraints satisfied
- Resources available
- Time/steps taken

**Pattern**:
```python
def state_space_bfs(initial_state):
    # State tuple: (position, context)
    queue = deque([(initial_state, 0)])
    visited = {initial_state}

    while queue:
        state, cost = queue.popleft()

        if is_goal(state):
            return cost

        for next_state, move_cost in get_next_states(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, cost + move_cost))

    return -1
```

## Problems in This Directory

### Word Ladder (127)

**Problem**: Transform `beginWord` to `endWord` by changing one letter at a time. Each transformed word must exist in word list. Return the length of shortest transformation sequence, or 0 if impossible.

**Example**:
```
Input: beginWord = "hit", endWord = "cog"
       wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: "hit" -> "hot" -> "dot" -> "dog" -> "cog"
```

**Approach 1: Standard BFS** (O(N × M² × 26)):
```python
def ladderLength(beginWord, endWord, wordList):
    if endWord not in wordList:
        return 0

    word_set = set(wordList)
    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        if word == endWord:
            return length

        # Try changing each position
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]

                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))

    return 0
```

**Approach 2: Pattern-based Graph** (O(N × M²)):
```python
def ladderLength(beginWord, endWord, wordList):
    if endWord not in wordList:
        return 0

    # Build graph with patterns
    graph = defaultdict(list)
    wordList.append(beginWord)

    for word in wordList:
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i+1:]
            graph[pattern].append(word)

    # BFS
    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        if word == endWord:
            return length

        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i+1:]
            for next_word in graph[pattern]:
                if next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))

    return 0
```

**Approach 3: Bidirectional BFS** (Optimal - O(N × M²)):
```python
def ladderLength(beginWord, endWord, wordList):
    if endWord not in wordList:
        return 0

    word_set = set(wordList)
    word_set.discard(beginWord)

    front = {beginWord}
    back = {endWord}
    length = 1

    while front and back:
        # Always expand smaller frontier
        if len(front) > len(back):
            front, back = back, front

        next_front = set()

        for word in front:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]

                    if next_word in back:
                        return length + 1

                    if next_word in word_set:
                        next_front.add(next_word)
                        word_set.discard(next_word)

        front = next_front
        length += 1

    return 0
```

**Complexity Analysis**:
- N = number of words, M = word length
- Standard BFS: O(N × M² × 26) time, O(N) space
- Pattern-based: O(N × M²) time, O(N × M) space
- Bidirectional BFS: O(N × M²) time, O(N) space (but ~2x faster in practice)

**Key Insights**:
1. **Graph Construction**: Each word is a node, edges connect words differing by one letter
2. **BFS for Shortest Path**: Unweighted graph, BFS guarantees shortest path
3. **Optimization**: Bidirectional BFS significantly reduces search space
4. **State Space**: Can think of as navigating M-dimensional space with 26 choices per dimension
5. **Pruning**: Remove words from word_set after visiting to avoid cycles

**Edge Cases**:
- endWord not in wordList (return 0)
- beginWord equals endWord (return 1 or handle specially)
- No transformation possible (return 0)
- Word list is empty
- Single letter words
- Very long transformation chains

**Common Mistakes**:
1. Not removing visited words from word_set (wastes time rechecking)
2. Building full neighbor graph upfront (too slow for large inputs)
3. Not using bidirectional BFS when possible
4. Forgetting to include beginWord in transformations
5. Off-by-one errors in counting sequence length
6. Not handling endWord not in wordList

**Optimization Techniques**:
1. **Bidirectional BFS**: Essential for large graphs
2. **Always expand smaller frontier**: Minimizes work
3. **Remove from word_set**: Avoid revisiting words
4. **Early termination**: Return immediately when paths meet
5. **Pattern preprocessing**: Can help if solving multiple queries

**Related Problems**:
- Word Ladder II (find all shortest paths)
- Minimum Genetic Mutation
- Word Squares
- Shortest Path in Unweighted Graph

**Interview Tips**:
1. Start with clear explanation of graph structure
2. Mention BFS is optimal for shortest path in unweighted graph
3. Discuss optimization options (bidirectional BFS)
4. Analyze time complexity carefully (M, N, alphabet size)
5. Handle edge cases explicitly
6. Consider space-time tradeoffs

## Hard Problem Characteristics

### 1. Multiple Optimization Layers
- Need several optimizations to pass time limits
- Naive solution times out
- Requires algorithmic insight, not just implementation

### 2. Complex State Management
- State is multi-dimensional
- Must track various conditions simultaneously
- Careful state representation is crucial

### 3. Large Search Spaces
- Exponential or large polynomial spaces
- Must prune aggressively
- Bidirectional search often helps

### 4. Combination of Techniques
- Often combines multiple algorithms
- May need graph + dynamic programming
- Requires recognizing multiple patterns

## Problem-Solving Strategies

### Strategy 1: Optimize Search Space
```python
# Instead of exploring all possibilities:
- Use bidirectional search
- Prune invalid states early
- Use heuristics to guide search
- Cache/memoize repeated computations
```

### Strategy 2: Clever State Representation
```python
# Compact state representation:
- Use bit manipulation for sets
- Hash states efficiently
- Minimize state tuple size
- Avoid redundant information
```

### Strategy 3: Mathematical Insight
```python
# Sometimes mathematical observation helps:
- Recognize patterns
- Use properties of the problem
- Find closed-form solutions
- Eliminate impossible cases early
```

### Strategy 4: Hybrid Approaches
```python
# Combine multiple techniques:
- BFS + DP
- DFS + memoization
- Graph + greedy
- Preprocessing + online queries
```

## Advanced Optimization Techniques

### 1. Meet in the Middle
Divide search space in half, search both halves, combine results.
```python
def meet_in_middle(items, target):
    mid = len(items) // 2
    left_half = items[:mid]
    right_half = items[mid:]

    # Generate all subset sums for each half
    left_sums = generate_all_sums(left_half)
    right_sums = generate_all_sums(right_half)

    # Find complementary sums
    for left_sum in left_sums:
        if target - left_sum in right_sums:
            return True
    return False
```

### 2. A* Search
BFS with heuristic to guide search toward goal.
```python
def a_star(start, goal, heuristic):
    # Priority queue: (f_score, node) where f = g + h
    pq = [(heuristic(start, goal), 0, start)]
    g_score = {start: 0}

    while pq:
        _, current_g, node = heappop(pq)

        if node == goal:
            return current_g

        for neighbor, cost in get_neighbors(node):
            new_g = current_g + cost

            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f_score = new_g + heuristic(neighbor, goal)
                heappush(pq, (f_score, new_g, neighbor))

    return -1
```

### 3. Iterative Deepening
Combine space efficiency of DFS with shortest path of BFS.
```python
def iterative_deepening(start, goal, max_depth):
    for depth in range(max_depth):
        result = dfs_limited(start, goal, depth)
        if result is not None:
            return result
    return None

def dfs_limited(node, goal, depth):
    if depth == 0:
        return node if node == goal else None
    if depth > 0:
        for neighbor in get_neighbors(node):
            result = dfs_limited(neighbor, goal, depth - 1)
            if result is not None:
                return result
    return None
```

## Common Patterns in Hard Problems

### Pattern 1: State Compression
Use bits or tuples to represent complex state efficiently.
```python
# Instead of: visited = set of (pos, keys, doors_opened, ...)
# Use: state = (pos, keys_bitmask, doors_bitmask)
state = (position, 0b10110)  # Bits represent boolean flags
```

### Pattern 2: Bidirectional Exploration
Search from both ends to reduce complexity.
```python
# Instead of: BFS from start to end (O(b^d))
# Use: BFS from both start and end (O(b^(d/2)))
```

### Pattern 3: Preprocessing + Query
Precompute information to answer queries quickly.
```python
# Preprocess graph structure
preprocessed = precompute_relationships(graph)

# Answer queries in O(1) or O(log n)
for query in queries:
    result = fast_lookup(preprocessed, query)
```

### Pattern 4: Constraint Relaxation
Solve relaxed version first, use to guide full solution.
```python
# Solve without some constraints
relaxed_solution = solve_relaxed(problem)

# Use relaxed solution as heuristic
if not validate_all_constraints(relaxed_solution):
    refined_solution = refine(relaxed_solution)
```

## Complexity Analysis for Hard Problems

### Time Complexity Considerations:
- **Branching Factor**: How many choices at each step?
- **Depth**: How many steps to solution?
- **State Space**: How many unique states?
- **Pruning Effectiveness**: How many states can we eliminate?

### Space Complexity Considerations:
- **State Representation**: How compact is each state?
- **Visited Set**: How many states must we track?
- **Queue/Stack Size**: Maximum size during execution?
- **Auxiliary Structures**: What extra data do we need?

### Optimization Impact:
| Optimization | Time Reduction | Space Cost |
|--------------|----------------|------------|
| Bidirectional BFS | O(b^d) → O(b^(d/2)) | 2× visited set |
| State compression | Same | 50-90% reduction |
| Pruning | Constant factor | None |
| Memoization | Eliminates repeats | O(unique states) |
| A* heuristic | Constant to exponential | Priority queue |

## Debugging Hard Problems

### 1. Start Small
- Test with minimal examples
- Verify algorithm on paper first
- Build up complexity gradually

### 2. Visualize State Space
- Draw state transition diagrams
- Track which states are explored
- Identify where pruning should occur

### 3. Measure Performance
- Count states explored
- Track maximum queue size
- Time different components
- Compare with theoretical bounds

### 4. Verify Correctness
- Check bidirectional search meets properly
- Validate state transitions
- Ensure no duplicate work
- Confirm visited set usage

### 5. Edge Case Testing
- Empty inputs
- Single element
- Maximum constraints
- No solution exists
- Multiple solutions

## Interview Approach for Hard Problems

### 1. Clarify Problem (2-3 minutes)
- Understand all constraints
- Clarify edge cases
- Confirm input/output format
- Ask about scale/performance requirements

### 2. Discuss Approach (5-7 minutes)
- Start with brute force
- Identify bottlenecks
- Propose optimizations
- Analyze complexity
- Get feedback before coding

### 3. Code Solution (15-20 minutes)
- Start with clear structure
- Write helper functions
- Handle edge cases
- Comment complex logic
- Test as you go

### 4. Test and Debug (5-8 minutes)
- Walk through small example
- Test edge cases
- Check complexity
- Discuss further optimizations

## Common Pitfalls in Hard Problems

1. **Premature Optimization**: Code correct solution first
2. **Overcomplicating**: Start simple, add complexity as needed
3. **Missing Edge Cases**: Handle empty, single element, no solution
4. **Wrong Complexity Analysis**: Account for all factors (N, M, alphabet size)
5. **Inefficient State Representation**: Use compact encoding
6. **Not Pruning**: Must eliminate invalid states early
7. **Memory Issues**: Consider space complexity too
8. **Off-by-One Errors**: Careful with indices and counts

## Practice Strategy

1. **Master Medium First**: Solid foundation in basic algorithms
2. **Study Patterns**: Recognize common hard problem patterns
3. **Analyze Solutions**: Understand why optimizations work
4. **Practice Similar Problems**: Variations build intuition
5. **Time Yourself**: Simulate interview conditions
6. **Explain Out Loud**: Teach concepts to solidify understanding
7. **Compare Approaches**: Learn multiple solutions per problem

## Next Steps

After mastering hard graph problems:
1. Study advanced graph algorithms (Floyd-Warshall, Johnson's)
2. Learn about network flow and matching
3. Explore computational geometry problems
4. Study approximation algorithms for NP-hard problems
5. Practice competitive programming problems
6. Learn about advanced data structures (segment trees, etc.)

## Resources

- **Books**:
  - "Introduction to Algorithms" (CLRS) - Comprehensive
  - "Algorithm Design Manual" (Skiena) - Practical
  - "Competitive Programming" - Contest techniques

- **Online**:
  - LeetCode Hard problems
  - Codeforces Division 1
  - TopCoder Algorithm tutorials
  - GeeksforGeeks advanced algorithms

- **Courses**:
  - MIT 6.046J (Advanced Algorithms)
  - Stanford CS161 (Design and Analysis of Algorithms)
  - Coursera - Algorithms specialization

- **Practice**:
  - Daily LeetCode Hard problem
  - Weekly contest participation
  - Review and understand editorial solutions
  - Implement multiple approaches per problem
