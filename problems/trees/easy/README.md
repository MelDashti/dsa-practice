# Trees - Easy Problems

## Core Concepts

### What is a Binary Tree?

A **binary tree** is a hierarchical data structure where each node has at most two children, referred to as the left child and right child. Binary trees are fundamental to many algorithms and data structures.

**Basic Structure:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Key Properties

1. **Root**: The topmost node with no parent
2. **Leaf**: A node with no children
3. **Height**: The longest path from root to any leaf
4. **Depth**: The distance from root to a specific node
5. **Level**: All nodes at the same depth

### Tree Traversal Methods

Understanding traversal is crucial for solving tree problems:

#### 1. Depth-First Search (DFS)
- **Preorder**: Root → Left → Right
- **Inorder**: Left → Root → Right (gives sorted order in BST)
- **Postorder**: Left → Right → Root

```python
def inorder(root):
    if not root:
        return
    inorder(root.left)
    print(root.val)
    inorder(root.right)
```

#### 2. Breadth-First Search (BFS)
- Level-by-level traversal using a queue

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    queue = deque([root])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result
```

### Recursive Thinking

Most tree problems are naturally solved recursively because:
1. Trees have a recursive structure (each subtree is also a tree)
2. Problems can often be broken down into subproblems on left and right subtrees
3. Base case is usually when node is None

**Recursive Pattern:**
```python
def solve(root):
    # Base case
    if not root:
        return base_value

    # Recursive case
    left_result = solve(root.left)
    right_result = solve(root.right)

    # Combine results
    return combine(left_result, right_result, root.val)
```

## Problems in This Section

### 1. Invert Binary Tree (LC 226)
**Concept**: Mirror reflection of the tree
- **Pattern**: Simple DFS/BFS with node swapping
- **Time**: O(n) - visit each node once
- **Space**: O(h) - recursion stack height

**Key Insight**: Swap left and right children at each node recursively.

### 2. Maximum Depth of Binary Tree (LC 104)
**Concept**: Find the longest path from root to leaf
- **Pattern**: Recursive DFS
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: Depth = 1 + max(left_depth, right_depth)

### 3. Diameter of Binary Tree (LC 543)
**Concept**: Longest path between any two nodes
- **Pattern**: DFS with global variable or return multiple values
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: At each node, diameter could be through that node (left_height + right_height) or in one of its subtrees.

### 4. Balanced Binary Tree (LC 110)
**Concept**: Check if tree is height-balanced
- **Pattern**: Bottom-up DFS returning height and balance status
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: A tree is balanced if |left_height - right_height| <= 1 for all nodes.

### 5. Same Tree (LC 100)
**Concept**: Check if two trees are identical
- **Pattern**: Simultaneous traversal
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: Trees are same if roots match and left/right subtrees are same.

### 6. Subtree of Another Tree (LC 572)
**Concept**: Check if one tree is a subtree of another
- **Pattern**: Combination of tree traversal and tree comparison
- **Time**: O(m * n) where m, n are sizes of the trees
- **Space**: O(h)

**Key Insight**: For each node in main tree, check if subtree rooted there matches the target tree.

## Common Patterns for Easy Tree Problems

### Pattern 1: Simple Recursive Traversal
```python
def process(root):
    if not root:
        return base_case

    # Process current node
    result = some_operation(root.val)

    # Recurse on children
    left = process(root.left)
    right = process(root.right)

    return combine(result, left, right)
```

### Pattern 2: Compare Two Trees
```python
def compare(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False

    return (p.val == q.val and
            compare(p.left, q.left) and
            compare(p.right, q.right))
```

### Pattern 3: Height/Depth Calculation
```python
def height(root):
    if not root:
        return 0
    return 1 + max(height(root.left), height(root.right))
```

## Tips for Success

1. **Start with Base Cases**: Always handle None/empty tree first
2. **Think Recursively**: Break problem into smaller subproblems
3. **Draw Examples**: Visualize small trees to understand the pattern
4. **Consider Edge Cases**: Single node, empty tree, skewed tree
5. **Track Return Values**: Be clear about what each recursive call returns
6. **Use Helper Functions**: Sometimes you need extra parameters (like parent, depth, etc.)

## Practice Progression

1. Start with **Maximum Depth** - simplest recursive pattern
2. Move to **Same Tree** - introduces comparison logic
3. Try **Invert Binary Tree** - adds modification aspect
4. Practice **Balanced Tree** - combines height calculation with validation
5. Tackle **Diameter** - requires thinking about paths through nodes
6. Finish with **Subtree** - combines multiple patterns

## Time & Space Complexity Cheatsheet

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| DFS Traversal | O(n) | O(h) | h is height, worst case O(n) for skewed tree |
| BFS Traversal | O(n) | O(w) | w is max width, worst case O(n/2) for complete tree |
| Search | O(n) | O(h) | Must potentially visit all nodes |
| Height | O(n) | O(h) | Visit all nodes once |

## Additional Resources

- Visualize trees at: visualgo.net/en/bst
- Practice drawing recursion trees to understand call stack
- Remember: If stuck, try solving for a tree with 1-3 nodes first
