"""
PROBLEM: Binary Tree Maximum Path Sum (LeetCode 124)
Difficulty: Hard
Pattern: Trees
Companies: Amazon, Facebook, Microsoft, Google, Bloomberg

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes
in the sequence has an edge connecting them. A node can only appear in the sequence
at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.

Example 1:
    Input: root = [1,2,3]
    Output: 6
    Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6

Example 2:
    Input: root = [-10,9,20,null,null,15,7]
    Output: 42
    Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42

Constraints:
- The number of nodes in the tree is in the range [1, 3 * 10^4]
- -1000 <= Node.val <= 1000

Approach:
1. For each node, calculate max path sum that includes that node
2. Path can be: node only, node + left, node + right, or node + left + right
3. Max path through node = node.val + max(0, left_path) + max(0, right_path)
4. Return value is max single path (for parent): node.val + max(0, left_path or right_path)
5. Track global maximum

Time: O(n) - visit every node once
Space: O(h) - recursion stack where h is height of tree
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def max_path_sum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')

        def max_gain(node):
            if not node:
                return 0

            # Get max path sum from left and right subtrees
            # Ignore negative paths
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)

            # Path sum including current node and both children
            path_sum = node.val + left_gain + right_gain

            # Update global maximum
            self.max_sum = max(self.max_sum, path_sum)

            # Return max gain if we continue this path upward
            # (can only include one child)
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_sum


# Tests
def test():
    sol = Solution()

    # Test 1: Simple tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert sol.max_path_sum(root) == 6

    # Test 2: Tree with negative values
    root2 = TreeNode(-10)
    root2.left = TreeNode(9)
    root2.right = TreeNode(20)
    root2.right.left = TreeNode(15)
    root2.right.right = TreeNode(7)
    assert sol.max_path_sum(root2) == 42

    # Test 3: Single node
    root3 = TreeNode(1)
    assert sol.max_path_sum(root3) == 1

    # Test 4: All negative
    root4 = TreeNode(-3)
    assert sol.max_path_sum(root4) == -3

    # Test 5: Path doesn't include root
    root5 = TreeNode(-10)
    root5.left = TreeNode(2)
    root5.right = TreeNode(3)
    root5.left.left = TreeNode(4)
    root5.left.right = TreeNode(5)
    assert sol.max_path_sum(root5) == 11  # 4 + 2 + 5

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
