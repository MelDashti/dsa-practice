"""
PROBLEM: Maximum Depth of Binary Tree (LeetCode 104)
Difficulty: Easy
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google, Apple

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path
from the root node down to the farthest leaf node.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: 3

Example 2:
    Input: root = [1,null,2]
    Output: 2

Example 3:
    Input: root = []
    Output: 0

Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -100 <= Node.val <= 100

Approach:
1. Base case: if root is None, return 0
2. Recursively find max depth of left subtree
3. Recursively find max depth of right subtree
4. Return 1 + max(left_depth, right_depth)

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
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)

        return 1 + max(left_depth, right_depth)


# Tests
def test():
    sol = Solution()

    # Test 1: Normal tree
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert sol.maxDepth(root) == 3

    # Test 2: Single path
    root2 = TreeNode(1)
    root2.right = TreeNode(2)
    assert sol.maxDepth(root2) == 2

    # Test 3: Empty tree
    assert sol.maxDepth(None) == 0

    # Test 4: Single node
    root3 = TreeNode(1)
    assert sol.maxDepth(root3) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
