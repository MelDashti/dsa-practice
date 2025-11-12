# Trees - Medium Problems

## Advanced Concepts

### Binary Search Tree (BST) Properties

A **Binary Search Tree** is a binary tree with an ordering property:
- All nodes in the left subtree have values **less than** the root
- All nodes in the right subtree have values **greater than** the root
- This property holds for every subtree

**Why BST matters:**
- Enables O(log n) search in balanced trees
- Inorder traversal gives sorted sequence
- Many problems exploit the ordering property

```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True

    if not (min_val < root.val < max_val):
        return False

    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))
```

### Lowest Common Ancestor (LCA)

The **Lowest Common Ancestor** of two nodes is the deepest node that has both as descendants.

**Key Properties:**
1. If one node is ancestor of other, that node is the LCA
2. LCA is where paths from root to two nodes diverge
3. In BST, can use value comparisons to find efficiently

### Tree Construction

Building trees from traversal arrays requires understanding:
1. **Preorder**: Root comes first, then left subtree, then right subtree
2. **Inorder**: Left subtree, then root, then right subtree
3. **Postorder**: Left subtree, then right subtree, then root

**Key Insight**: Preorder/Postorder tells you where root is, Inorder tells you which nodes are in left vs right subtree.

## Problems in This Section

### 1. Lowest Common Ancestor of BST (LC 235)
**Concept**: Find LCA using BST property
- **Pattern**: Recursive/Iterative with value comparison
- **Time**: O(h) where h is height
- **Space**: O(h) recursive, O(1) iterative

**Key Insight**:
- If both nodes are less than current, LCA is in left subtree
- If both nodes are greater than current, LCA is in right subtree
- Otherwise, current node is the LCA

```python
def lowestCommonAncestor(root, p, q):
    if p.val < root.val > q.val:
        return lowestCommonAncestor(root.left, p, q)
    elif p.val > root.val < q.val:
        return lowestCommonAncestor(root.right, p, q)
    else:
        return root
```

### 2. Binary Tree Level Order Traversal (LC 102)
**Concept**: BFS to collect nodes by level
- **Pattern**: Queue-based BFS with level tracking
- **Time**: O(n)
- **Space**: O(w) where w is max width

**Key Insight**: Use queue size to process one complete level at a time.

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        level_size = len(queue)  # Important: capture size before loop

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### 3. Binary Tree Right Side View (LC 199)
**Concept**: Get rightmost node at each level
- **Pattern**: BFS or DFS with level tracking
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: Either take last node at each level (BFS) or first node visited at each depth going right-first (DFS).

### 4. Count Good Nodes in Binary Tree (LC 1448)
**Concept**: Count nodes where value >= all ancestors
- **Pattern**: DFS with max value tracking
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: Pass down the maximum value seen so far on the path.

```python
def goodNodes(root):
    def dfs(node, max_val):
        if not node:
            return 0

        count = 1 if node.val >= max_val else 0
        max_val = max(max_val, node.val)

        count += dfs(node.left, max_val)
        count += dfs(node.right, max_val)

        return count

    return dfs(root, root.val)
```

### 5. Validate Binary Search Tree (LC 98)
**Concept**: Check if tree satisfies BST property
- **Pattern**: DFS with min/max bounds
- **Time**: O(n)
- **Space**: O(h)

**Key Insight**: Each node must be within a valid range based on ancestors.

**Common Pitfall**: Don't just compare with immediate parent; must check against all ancestors.

```python
def isValidBST(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True

    if not (min_val < root.val < max_val):
        return False

    return (isValidBST(root.left, min_val, root.val) and
            isValidBST(root.right, root.val, max_val))
```

### 6. Kth Smallest Element in BST (LC 230)
**Concept**: Find kth smallest using BST property
- **Pattern**: Inorder traversal (gives sorted order)
- **Time**: O(n) worst case, O(k) average
- **Space**: O(h)

**Key Insight**: Inorder traversal of BST gives elements in ascending order.

```python
def kthSmallest(root, k):
    def inorder(node):
        if not node:
            return None

        # Check left subtree
        left = inorder(node.left)
        if left is not None:
            return left

        # Check current node
        self.count += 1
        if self.count == k:
            return node.val

        # Check right subtree
        return inorder(node.right)

    self.count = 0
    return inorder(root)
```

### 7. Construct Binary Tree from Preorder and Inorder (LC 105)
**Concept**: Build tree from two traversal arrays
- **Pattern**: Recursive construction with array slicing
- **Time**: O(n)
- **Space**: O(n)

**Key Insight**:
- Preorder's first element is root
- Find root in inorder to determine left/right subtree elements
- Recursively build left and right subtrees

```python
def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None

    root = TreeNode(preorder[0])
    mid = inorder.index(root.val)

    root.left = buildTree(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree(preorder[mid+1:], inorder[mid+1:])

    return root
```

### 8. Construct Binary Tree from Inorder and Postorder (LC 106)
**Concept**: Build tree from inorder and postorder
- **Pattern**: Similar to preorder/inorder but root is at end
- **Time**: O(n)
- **Space**: O(n)

**Key Insight**: Postorder's last element is root.

## Advanced Patterns

### Pattern 1: BFS with Level Tracking
```python
def level_order_pattern(root):
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        level_size = len(queue)  # Capture level size
        level = []

        for _ in range(level_size):  # Process entire level
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### Pattern 2: DFS with Path Information
```python
def dfs_with_path(node, path_info):
    if not node:
        return base_case

    # Update path info
    path_info = update(path_info, node.val)

    # Process current node with path context
    result = process(node, path_info)

    # Recurse on children
    left = dfs_with_path(node.left, path_info)
    right = dfs_with_path(node.right, path_info)

    return combine(result, left, right)
```

### Pattern 3: BST Search Optimization
```python
def bst_search(root, target):
    if not root:
        return None

    if target < root.val:
        return bst_search(root.left, target)
    elif target > root.val:
        return bst_search(root.right, target)
    else:
        return root
```

### Pattern 4: Tree Construction from Arrays
```python
def construct_tree(arr1, arr2):
    if not arr1 or not arr2:
        return None

    # Find root from one array
    root_val = find_root(arr1)
    root = TreeNode(root_val)

    # Use other array to split into left/right
    split_idx = arr2.index(root_val)

    # Recursively build subtrees
    root.left = construct_tree(
        arr1[left_start:left_end],
        arr2[:split_idx]
    )
    root.right = construct_tree(
        arr1[right_start:right_end],
        arr2[split_idx+1:]
    )

    return root
```

## Common Techniques

### 1. Range Validation for BST
Always pass min and max bounds down the tree to validate BST property globally, not just locally.

### 2. Level-by-Level Processing
Use queue size to process exactly one level at a time in BFS.

### 3. Index Mapping for Construction
Use a hashmap to store indices in inorder array for O(1) lookup during tree construction.

```python
inorder_map = {val: idx for idx, val in enumerate(inorder)}
# Now can find position in O(1) instead of O(n)
```

### 4. Early Termination in BST
Exploit BST property to avoid searching entire tree.

## Common Pitfalls

1. **BST Validation**: Don't just check immediate children; must validate against all ancestors
2. **Array Slicing**: Can be expensive (O(n)); consider using index pointers instead
3. **Level Order**: Forgetting to capture queue size before inner loop
4. **Tree Construction**: Getting array indices wrong when splitting
5. **Inorder Traversal**: Need to maintain state (count, result) across recursive calls

## Tips for Success

1. **Draw It Out**: Visualize the tree and traversal order
2. **Identify Tree Type**: Is it a BST? Does that help?
3. **Choose Traversal**: DFS for paths/depths, BFS for levels
4. **Track State**: What information needs to flow down? Up? Both?
5. **Test Edge Cases**: Single node, all left/right children, balanced vs skewed
6. **Optimize**: Can you use BST property? Can you avoid array slicing?

## Practice Progression

1. **Level Order Traversal** - Master BFS pattern
2. **Validate BST** - Understand range validation
3. **LCA in BST** - Use BST property for optimization
4. **Kth Smallest** - Combine inorder with early termination
5. **Count Good Nodes** - Track path information
6. **Right Side View** - Multiple solution approaches
7. **Tree Construction** - Complex recursion with array manipulation

## Complexity Analysis

| Problem | Time | Space | Key Factor |
|---------|------|-------|------------|
| LCA BST | O(h) | O(h) | Height-based search |
| Level Order | O(n) | O(w) | Width for queue |
| Validate BST | O(n) | O(h) | Visit all nodes |
| Kth Smallest | O(k+h) | O(h) | Early termination possible |
| Tree Construction | O(n) | O(n) | Build entire tree |
| Right Side View | O(n) | O(h) or O(w) | DFS or BFS |

## Additional Insights

### When to Use DFS vs BFS
- **Use DFS when**: Tracking paths, working with depths, recursive is natural
- **Use BFS when**: Working with levels, finding shortest paths, need breadth-first order

### BST Advantage
Many BST problems can be solved in O(h) instead of O(n) by exploiting the ordering property.

### Tree Construction Strategy
1. Identify where root is in one traversal
2. Use other traversal to find left/right subtree elements
3. Recursively build subtrees with correct array slices
