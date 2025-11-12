# Trees - Hard Problems

## Expert-Level Concepts

### Understanding Complexity in Tree Problems

Hard tree problems typically involve:
1. **Multiple constraints** - Tracking several pieces of information simultaneously
2. **Global optimization** - Finding best path/value across entire tree
3. **State management** - Maintaining complex state during traversal
4. **Design problems** - Creating efficient data structures with tree properties

### Path Problems

**Path** in a tree context can mean:
- **Simple Path**: From any node to any descendant (going down only)
- **General Path**: Between any two nodes (can go up then down)
- **Root-to-Leaf Path**: Specific case from root to a leaf node

**Key Insight**: For general paths, at each node consider:
1. Path going through this node (left → node → right)
2. Path entirely in left subtree
3. Path entirely in right subtree

### Serialization Concepts

**Serialization** converts a data structure into a format that can be:
- Stored persistently
- Transmitted over a network
- Reconstructed later (**Deserialization**)

**Requirements for tree serialization**:
1. Must capture structure (not just values)
2. Must handle null/empty nodes
3. Deserialization must recreate exact tree
4. Should be efficient in time and space

## Problems in This Section

### 1. Binary Tree Maximum Path Sum (LC 124)

**Concept**: Find path with maximum sum between any two nodes

**Difficulty Factors**:
- Path can start and end at any nodes
- Need to handle negative values
- Must distinguish between paths ending at node vs. going through node

**Pattern**: Post-order DFS with global variable

**Time Complexity**: O(n) - visit each node once
**Space Complexity**: O(h) - recursion stack

#### Key Insights

1. **Two Return Values Conceptually**:
   - Maximum path sum going through current node to its parent (can extend upward)
   - Maximum path sum in entire subtree (might not extend upward)

2. **At Each Node**:
   - Get max gain from left child (ignore if negative)
   - Get max gain from right child (ignore if negative)
   - Update global max with path through current node: left_gain + node.val + right_gain
   - Return max single path to parent: node.val + max(left_gain, right_gain)

#### Solution Pattern

```python
def maxPathSum(root):
    max_sum = float('-inf')

    def max_gain(node):
        nonlocal max_sum

        if not node:
            return 0

        # Max gain from left and right (ignore if negative)
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)

        # Path sum going through current node
        current_path_sum = node.val + left_gain + right_gain

        # Update global maximum
        max_sum = max(max_sum, current_path_sum)

        # Return max gain to parent (can only use one path)
        return node.val + max(left_gain, right_gain)

    max_gain(root)
    return max_sum
```

#### Common Pitfalls

1. **Forgetting to handle negative paths**: Use `max(gain, 0)`
2. **Returning wrong value**: Return single path to parent, not through node
3. **Not initializing max_sum correctly**: Use `float('-inf')` not 0

#### Test Cases to Consider

```python
# Single node
root = TreeNode(-3)  # Answer: -3

# All negative
#      -10
#     /    \
#   -20    -30  # Answer: -10

# Path doesn't include root
#       1
#      / \
#     2   3
#    / \
#   4   5  # Answer: 11 (4+2+5)
```

### 2. Serialize and Deserialize Binary Tree (LC 297)

**Concept**: Design algorithm to encode/decode tree to/from string

**Difficulty Factors**:
- Must preserve exact structure including null nodes
- Handle any tree shape (balanced, skewed, etc.)
- Ensure efficient encoding/decoding

**Pattern**: DFS (preorder) or BFS with delimiter

**Time Complexity**: O(n) for both operations
**Space Complexity**: O(n) for string and recursion/queue

#### Key Insights

1. **Need to mark null nodes**: Can't distinguish structure without them
2. **Preorder works well**: Root first, then subtrees (easy to rebuild)
3. **Use delimiters**: Separate values (comma) and mark nulls (N, null, #, etc.)

#### Approach 1: Preorder DFS

```python
class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        def dfs(node):
            if not node:
                return "N"  # Null marker

            # Preorder: root, left, right
            return (str(node.val) + "," +
                    dfs(node.left) + "," +
                    dfs(node.right))

        return dfs(root)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        def dfs(vals):
            val = next(vals)

            if val == "N":
                return None

            node = TreeNode(int(val))
            node.left = dfs(vals)
            node.right = dfs(vals)

            return node

        vals = iter(data.split(","))
        return dfs(vals)
```

#### Approach 2: Level-Order BFS

```python
from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return ""

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()

            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("N")

        return ",".join(result)

    def deserialize(self, data):
        if not data:
            return None

        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1

        while queue and i < len(values):
            node = queue.popleft()

            # Process left child
            if values[i] != "N":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1

            # Process right child
            if i < len(values) and values[i] != "N":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1

        return root
```

#### Design Choices

| Aspect | Preorder DFS | Level-Order BFS |
|--------|-------------|-----------------|
| Code Complexity | Simpler | More complex indexing |
| Space | O(h) recursion | O(w) queue |
| Traversal Order | Depth-first | Breadth-first |
| Serialized String | Depth pattern | Level pattern |

#### Common Pitfalls

1. **Not handling null nodes**: Tree structure is lost
2. **Delimiter issues**: Values might contain delimiter character
3. **String parsing errors**: Off-by-one in indexing
4. **Iterator exhaustion**: In DFS, need to share iterator state

#### Test Cases

```python
# Complete binary tree
#      1
#     / \
#    2   3
#   / \
#  4   5
# Serialized (preorder): "1,2,4,N,N,5,N,N,3,N,N"

# Skewed tree
#   1
#    \
#     2
#      \
#       3
# Serialized: "1,N,2,N,3,N,N"

# Single node
#   1
# Serialized: "1,N,N"

# Empty tree
# Serialized: ""
```

## Advanced Patterns

### Pattern 1: Path Through Node vs Path to Node

```python
def path_problem(root):
    global_max = float('-inf')

    def dfs(node):
        nonlocal global_max

        if not node:
            return 0

        # Get values from children
        left = dfs(node.left)
        right = dfs(node.right)

        # Update global considering path THROUGH node
        global_max = max(global_max, left + node.val + right)

        # Return path TO node (only one branch)
        return node.val + max(left, right)

    dfs(root)
    return global_max
```

**When to use**: Problems asking for "maximum path sum", "longest path", etc.

### Pattern 2: State Machine in Traversal

```python
def stateful_traversal(root):
    def dfs(node, state):
        if not node:
            return base_case

        # Update state based on current node
        new_state = transition(state, node)

        # Recurse with updated state
        left_result = dfs(node.left, new_state)
        right_result = dfs(node.right, new_state)

        # Combine results
        return combine(left_result, right_result, node, state)

    return dfs(root, initial_state)
```

**When to use**: Problems tracking complex conditions along paths.

### Pattern 3: Tree Serialization Template

```python
class Codec:
    def serialize(self, root):
        # Choose: preorder DFS or level-order BFS
        # Mark null nodes explicitly
        # Use delimiter between values
        pass

    def deserialize(self, data):
        # Parse string into values
        # Reconstruct using same traversal order
        # Handle null nodes appropriately
        pass
```

## Complexity Optimization Techniques

### 1. Avoid Repeated Work
Cache results of subtrees if accessed multiple times (memoization).

### 2. Early Termination
In path problems, skip subtrees that can't improve the answer.

### 3. In-place Modifications
If allowed, modify tree structure instead of creating new one.

### 4. Choose Right Traversal
- DFS uses O(h) space (recursion stack)
- BFS uses O(w) space (queue)
- Choose based on tree shape

## Problem-Solving Framework

### Step 1: Understand the Constraints
- What constitutes a valid path/structure?
- Are negative values possible?
- What does "maximum" or "optimal" mean?

### Step 2: Identify the Pattern
- Is it a path problem? → Use global variable + return value technique
- Is it a design problem? → Think about what information to store
- Does it need serialization? → Choose DFS or BFS approach

### Step 3: Handle Edge Cases
- Empty tree
- Single node
- All negative values (for path problems)
- Skewed tree (all left or all right)

### Step 4: Optimize
- Can you avoid extra space?
- Can you terminate early?
- Is there a better traversal order?

## Tips for Hard Tree Problems

1. **Draw Multiple Examples**: Try balanced, skewed, and special cases
2. **Separate Concerns**: What to return vs. what to track globally
3. **State Management**: Be explicit about what information flows where
4. **Test Incrementally**: Build up from simple cases
5. **Consider Multiple Approaches**: DFS vs. BFS, iterative vs. recursive
6. **Validate Assumptions**: Does your solution work for all tree shapes?

## Common Mistakes

### Maximum Path Sum
- Returning path through node instead of path to node
- Not handling negative values with max(gain, 0)
- Forgetting single-node case

### Serialization
- Not marking null nodes
- Using wrong delimiter
- Mixing up serialization and deserialization traversal orders
- Not handling empty tree

## Practice Strategy

1. **Start with Maximum Path Sum**:
   - Master the "global max + return value" pattern
   - This pattern appears in many hard problems

2. **Then Serialize/Deserialize**:
   - Try both DFS and BFS approaches
   - Understand why both work
   - Compare trade-offs

3. **Generalize the Patterns**:
   - Apply path pattern to other problems (longest univalue path, etc.)
   - Apply serialization to other tree structures (BST, N-ary tree, etc.)

## Beyond These Problems

Once you master these, you can tackle:
- **Binary Tree Cameras** (LC 968) - State machine pattern
- **Longest Univalue Path** (LC 687) - Path pattern variant
- **Vertical Order Traversal** (LC 987) - Complex BFS with sorting
- **Recover BST** (LC 99) - Inorder with mutation
- **Max Sum BST** (LC 1373) - Combines validation with path sum

## Time & Space Analysis

| Problem | Time | Space | Bottleneck |
|---------|------|-------|------------|
| Max Path Sum | O(n) | O(h) | Must visit all nodes |
| Serialize | O(n) | O(n) | Store all values |
| Deserialize | O(n) | O(n) | Recreate all nodes |

**Optimization**: Both problems are already optimal - can't do better than O(n) time since we must process every node.

## Key Takeaways

1. **Global vs Local**: Many hard problems require tracking both global optimum and local return value
2. **Null Handling**: Explicit null markers are crucial for serialization
3. **Multiple Solutions**: Often multiple approaches work; choose based on requirements
4. **Pattern Recognition**: Once you see the patterns, hard problems become manageable
5. **Practice**: These patterns appear repeatedly in tree problems

## Further Reading

- **Path Problems**: Study how to handle paths that don't include root
- **Tree DP**: Many problems can be framed as dynamic programming on trees
- **Design Patterns**: Understand when to use DFS vs BFS for serialization
- **State Machines**: Learn to track complex state during traversals
