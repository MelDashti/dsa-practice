"""
PROBLEM: Count Good Nodes in Binary Tree (LeetCode 1448)
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Microsoft, Facebook

Given a binary tree root, a node X in the tree is named good if in the path from
root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

Example 1:
    Input: root = [3,1,4,3,null,1,5]
    Output: 4
    Explanation: Nodes in blue are good.
    Root Node (3) is always a good node.
    Node 4 -> (3,4) is the maximum value in the path starting from the root.
    Node 5 -> (3,4,5) is the maximum value in the path
    Node 3 -> (3,1,3) is the maximum value in the path.

Example 2:
    Input: root = [3,3,null,4,2]
    Output: 3
    Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.

Example 3:
    Input: root = [1]
    Output: 1
    Explanation: Root is considered as good.

Constraints:
- The number of nodes in the binary tree is in the range [1, 10^5]
- Each node's value is between [-10^4, 10^4]

Approach:
1. Use DFS to traverse the tree
2. Track the maximum value seen on the path from root to current node
3. If current node value >= max value, it's a good node
4. Update max value and recursively check children
5. Return count of good nodes

Time: O(n) - visit every node once
Space: O(h) - recursion stack where h is height of tree
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def good_nodes(self, root: TreeNode) -> int:
        def dfs(node, max_val):
            if not node:
                return 0

            # Check if current node is good
            count = 1 if node.val >= max_val else 0

            # Update max value for children
            new_max = max(max_val, node.val)

            # Count good nodes in left and right subtrees
            count += dfs(node.left, new_max)
            count += dfs(node.right, new_max)

            return count

        return dfs(root, float('-inf'))


# Tests
def test():
    sol = Solution()

    # Test 1: Example 1
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.left = TreeNode(3)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(5)
    assert sol.good_nodes(root) == 4

    # Test 2: Example 2
    root2 = TreeNode(3)
    root2.left = TreeNode(3)
    root2.left.left = TreeNode(4)
    root2.left.right = TreeNode(2)
    assert sol.good_nodes(root2) == 3

    # Test 3: Single node
    root3 = TreeNode(1)
    assert sol.good_nodes(root3) == 1

    # Test 4: All nodes are good
    root4 = TreeNode(1)
    root4.left = TreeNode(2)
    root4.right = TreeNode(3)
    root4.left.left = TreeNode(4)
    assert sol.good_nodes(root4) == 4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
