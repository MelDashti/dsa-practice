"""
PROBLEM: Invert Binary Tree (LeetCode 226)
LeetCode: https://leetcode.com/problems/invert-binary-tree/
Difficulty: Easy
Pattern: Trees
Companies: Google, Amazon, Facebook, Microsoft, Bloomberg

Given the root of a binary tree, invert the tree, and return its root.

Example 1:
    Input: root = [4,2,7,1,3,6,9]
    Output: [4,7,2,9,6,3,1]

Example 2:
    Input: root = [2,1,3]
    Output: [2,3,1]

Example 3:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100

Approach:
1. Base case: if root is None, return None
2. Recursively invert left and right subtrees
3. Swap left and right children
4. Return the root

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
    def invert_tree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        # Swap left and right children
        root.left, root.right = root.right, root.left

        # Recursively invert subtrees
        self.invert_tree(root.left)
        self.invert_tree(root.right)

        return root


# Tests
def test():
    sol = Solution()

    # Test 1: Normal tree
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(9)

    result = sol.invert_tree(root)
    assert result.val == 4
    assert result.left.val == 7
    assert result.right.val == 2
    assert result.left.left.val == 9
    assert result.left.right.val == 6
    assert result.right.left.val == 3
    assert result.right.right.val == 1

    # Test 2: Single node
    root2 = TreeNode(1)
    result2 = sol.invert_tree(root2)
    assert result2.val == 1
    assert result2.left is None
    assert result2.right is None

    # Test 3: Empty tree
    result3 = sol.invert_tree(None)
    assert result3 is None

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
