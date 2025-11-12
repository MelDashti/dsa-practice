# Tries - Hard Problems

## Advanced Concepts

### Trie + Backtracking Combination

Hard trie problems often combine tries with other algorithms:
- **Backtracking**: For exploring multiple paths (word search, puzzles)
- **DFS**: For graph-like traversal on board + trie
- **Dynamic Programming**: For optimization problems with prefix matching
- **Bit Manipulation**: For binary tries (XOR problems)

### 2D Grid + Trie Integration

When searching for words in a 2D grid:
1. **Trie stores dictionary**: O(1) prefix checking
2. **Backtracking explores grid**: All possible paths
3. **Pruning with trie**: Abandon paths not matching any prefix

**Why This Works**:
- Trie prevents exploring invalid paths early
- Without trie: Must check each path against all words
- With trie: Stop as soon as prefix doesn't match any word

### Complexity Considerations

**Naive approach**: For each cell, try each word
- Time: O(cells * words * word_length) = O(m*n*w*l)

**Trie approach**: For each cell, DFS with trie pruning
- Time: O(m*n*4^l) where l is max word length
- Much better when many words share prefixes

## Problems in This Section

### 1. Word Search II (LC 212)

**Concept**: Find all words from dictionary that exist in a 2D board

**Given**:
- `board`: m x n grid of characters
- `words`: List of dictionary words

**Find**: All words that can be formed by adjacent cells (no reuse)

**Difficulty Factors**:
1. Must handle multiple words efficiently
2. Board can be traversed in any direction (4-directional)
3. Can't reuse cells in same word
4. Need to avoid checking invalid prefixes

**Pattern**: Trie + DFS Backtracking

**Time Complexity**: O(m * n * 4^L) where L is max word length
**Space Complexity**: O(w * L) for trie, where w is number of words

#### Key Insights

1. **Build Trie First**: Store all words in trie for O(1) prefix lookup
2. **DFS from Each Cell**: Try starting word from every position
3. **Backtracking**: Mark visited, explore, unmark (restore state)
4. **Prune Early**: If current path not a prefix, stop immediately
5. **Avoid Duplicates**: Mark found words or remove from trie

#### Solution Structure

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store complete word at end node

class Solution:
    def findWords(self, board, words):
        # Step 1: Build trie from words
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word  # Store word at leaf

        # Step 2: DFS from each cell
        result = []
        rows, cols = len(board), len(board[0])

        def dfs(r, c, node):
            # Get character at current position
            char = board[r][c]

            # Check if character exists in trie
            if char not in node.children:
                return

            # Move to next node
            next_node = node.children[char]

            # Check if we found a word
            if next_node.word:
                result.append(next_node.word)
                next_node.word = None  # Avoid duplicates

            # Mark as visited
            board[r][c] = '#'

            # Explore 4 directions
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    board[nr][nc] != '#'):
                    dfs(nr, nc, next_node)

            # Backtrack: restore cell
            board[r][c] = char

            # Optimization: remove leaf nodes
            if not next_node.children:
                del node.children[char]

        # Start DFS from each cell
        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return result
```

#### Detailed Algorithm Walkthrough

**Example**:
```python
board = [
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]
```

**Step 1**: Build Trie
```
        root
       /    \
      o      p   e   r
      |      |   |   |
      a      e   a   a
      |      |   |   |
      t      a   t   i
      |         [eat] |
      h              n
    [oath]        [rain]
```

**Step 2**: DFS from each cell
- Start at (0,0) = 'o'
  - Check if 'o' in root.children → Yes
  - Mark (0,0) as visited
  - Try 4 directions...
  - Eventually find "oath": o(0,0) → a(1,0) → t(1,1) → h(2,1)

**Step 3**: Continue for all cells

**Step 4**: Return ["oath", "eat"]

#### Optimizations

##### 1. Store Word at End Node
```python
# Instead of just marking is_end = True
node.word = "complete_word"  # Easy to add to result

# When found:
if node.word:
    result.append(node.word)
    node.word = None  # Prevent duplicates
```

##### 2. Remove Matched Words from Trie
```python
# After finding word, remove it from trie
if next_node.word:
    result.append(next_node.word)
    next_node.word = None

# Also prune empty branches
if not next_node.children:
    del node.children[char]
```

This reduces search space for remaining searches!

##### 3. Early Termination
```python
# If no words left in trie, stop
if not root.children:
    return result
```

##### 4. Board Modification vs Visited Set
```python
# Approach 1: Modify board (saves space)
board[r][c] = '#'  # Mark visited
# ... DFS ...
board[r][c] = char  # Restore

# Approach 2: Use visited set (preserves board)
visited = set()
visited.add((r, c))
# ... DFS ...
visited.remove((r, c))

# Approach 1 is better: O(1) space vs O(L) space
```

#### Edge Cases

```python
# 1. No words found
board = [['a','b'],['c','d']]
words = ["xyz"]
# Result: []

# 2. Single cell board
board = [['a']]
words = ["a"]
# Result: ["a"]

# 3. Word longer than possible path
board = [['a','b']]
words = ["abcdef"]  # Can't form on 2-cell board
# Result: []

# 4. Duplicate words in dictionary
words = ["oath", "oath"]
# Should return ["oath"] only once

# 5. Word is prefix of another
words = ["oa", "oath"]
# Both should be found
```

#### Common Pitfalls

1. **Not pruning with trie**: Without trie, time complexity explodes
2. **Forgetting to backtrack**: Must restore board state
3. **Duplicate results**: Need to remove word from trie after finding
4. **Not checking bounds**: Array index out of bounds
5. **Incorrect visited marking**: Using wrong marker or not restoring

#### Complexity Analysis

**Time**:
- Building trie: O(W * L) where W = number of words, L = avg length
- DFS: O(M * N * 4^L) where M,N = board dimensions, L = max word length
  - Each cell is starting point: M * N
  - Each position has up to 4 choices: 4^L
  - But pruning with trie reduces this significantly!

**Space**:
- Trie: O(W * L)
- Recursion stack: O(L)
- Total: O(W * L)

#### Alternative Approaches

##### Approach 1: Without Trie (Naive)
```python
def findWords(board, words):
    result = []
    for word in words:
        if self.exists(board, word):
            result.append(word)
    return result

# Time: O(W * M * N * 4^L) - Much worse!
```

##### Approach 2: Trie + BFS
```python
# Use BFS instead of DFS
# Less intuitive, harder to implement backtracking
# Generally DFS is preferred for this problem
```

#### Advanced Optimizations

##### 1. Bidirectional Search
```python
# Search from both start and end simultaneously
# Can reduce search space
# More complex to implement
```

##### 2. Trie Compression
```python
# Compress single-child paths in trie
# Saves space but adds complexity
```

##### 3. Parallel Processing
```python
# Process different starting cells in parallel
# Good for very large boards
```

## Advanced Patterns

### Pattern 1: Trie + DFS Backtracking Template

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Or is_end + reconstruct

class Solution:
    def trieBacktrack(self, board, words):
        # 1. Build trie
        root = self.buildTrie(words)

        # 2. DFS from each position
        result = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                self.dfs(board, i, j, root, result)

        return result

    def dfs(self, board, r, c, node, result):
        # Boundary check
        if not (0 <= r < len(board) and 0 <= c < len(board[0])):
            return

        char = board[r][c]

        # Check if valid path in trie
        if char not in node.children or char == '#':
            return

        # Move to next node
        node = node.children[char]

        # Check if found complete word
        if node.word:
            result.append(node.word)
            node.word = None  # Avoid duplicates

        # Mark visited
        board[r][c] = '#'

        # Explore neighbors
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            self.dfs(board, r+dr, c+dc, node, result)

        # Backtrack
        board[r][c] = char

        # Prune trie
        if not node.children:
            del parent.children[char]  # Need parent reference
```

### Pattern 2: Trie Node with Additional Data

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None
        self.count = 0  # How many times found
        self.positions = []  # Where found on board
        self.parent = None  # For pruning
```

### Pattern 3: Multi-Source BFS with Trie

```python
def multiSourceSearch(board, words):
    """Start from all cells simultaneously"""
    root = buildTrie(words)
    queue = deque()

    # Add all cells as starting points
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] in root.children:
                queue.append((r, c, root, set([(r,c)]), ""))

    result = set()

    while queue:
        r, c, node, visited, path = queue.popleft()
        char = board[r][c]
        node = node.children[char]
        path += char

        if node.word:
            result.add(node.word)

        # Explore neighbors...

    return list(result)
```

## Problem-Solving Strategy

### Step 1: Recognize Pattern
- Multiple words to search → Trie
- 2D grid traversal → Backtracking
- Path finding → DFS

### Step 2: Design Data Structure
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store word for easy access
```

### Step 3: Build Trie
```python
root = TrieNode()
for word in words:
    insert(root, word)
```

### Step 4: DFS with Backtracking
```python
for each cell:
    dfs(cell, root)

def dfs(cell, node):
    # Check validity
    # Mark visited
    # Recurse on neighbors
    # Backtrack
```

### Step 5: Optimize
- Prune matched words from trie
- Remove empty trie branches
- Early termination when trie empty

## Tips for Hard Trie Problems

1. **Always use trie for multiple word searches**: O(1) prefix check
2. **Combine with appropriate algorithm**: DFS, DP, backtracking
3. **Prune aggressively**: Remove found words, empty branches
4. **Test with large inputs**: Ensure optimizations work
5. **Handle edge cases**: Empty board, single cell, no matches
6. **Consider space-time tradeoffs**: Store word vs reconstruct

## Common Mistakes

1. **Not using trie**: Time limit exceeded
2. **Forgetting to backtrack**: Wrong results
3. **Not handling duplicates**: Same word appears multiple times
4. **Inefficient trie building**: Should be O(W*L), not more
5. **Not pruning trie**: Wastes time on already-found words
6. **Incorrect boundary checks**: Index errors

## Beyond This Problem

Related hard problems:
- **Stream of Characters** (LC 1032): Trie with suffix matching
- **Word Squares** (LC 425): Trie + backtracking for square formation
- **Concatenated Words** (LC 472): Trie + DP
- **Alien Dictionary** (LC 269): Topological sort (different approach)
- **Longest Word in Dictionary** (LC 720): Trie traversal

## Key Takeaways

1. **Trie + Backtracking is powerful**: Essential pattern for grid word problems
2. **Pruning is crucial**: Removes found words and empty branches
3. **In-place modification**: Use board itself for visited tracking
4. **Store word in node**: Simplifies result collection
5. **Practice backtracking**: Must restore state correctly

## Real-World Applications

1. **Crossword Solving**: Find valid words in puzzle
2. **Scrabble/Boggle**: Find all possible words
3. **Word Games**: Validate and find words in grid
4. **Text Processing**: Extract dictionary words from grid
5. **OCR Post-Processing**: Match recognized characters to dictionary

## Further Study

- **Suffix Trees**: For more complex string matching
- **Aho-Corasick Algorithm**: Multiple pattern matching
- **Compressed Tries**: Space optimization
- **Ternary Search Trees**: Alternative to tries
- **Radix Trees**: Compressed version of tries

## Practice Progression

1. Implement basic trie (LC 208)
2. Add wildcard search (LC 211)
3. Master Word Search II (LC 212)
4. Try Word Search (LC 79) with single word
5. Extend to other trie+backtracking problems
6. Optimize for performance on large inputs

## Final Notes

Word Search II is a classic hard problem that appears frequently in interviews. Master this and you'll have strong foundation in:
- Trie data structures
- Backtracking algorithms
- DFS on 2D grids
- Optimization techniques
- Combining multiple algorithmic approaches

The key insight is recognizing that tries make prefix checking O(1), which turns an impossible brute force solution into an efficient one.
