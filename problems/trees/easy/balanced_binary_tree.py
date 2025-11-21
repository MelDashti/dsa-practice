"""
PROBLEM: Balanced Binary Tree (LeetCode 110)
LeetCode: https://leetcode.com/problems/balanced-binary-tree/
Difficulty: Easy
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Bloomberg

Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is a binary tree in which the depth of the two
subtrees of every node never differs by more than one.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: true

Example 2:
    Input: root = [1,2,2,3,3,null,null,4,4]
    Output: false

Example 3:
    Input: root = []
    Output: true

Constraints:
- The number of nodes in the tree is in the range [0, 5000]
- -10^4 <= Node.val <= 10^4

Approach:
1. For each node, check if left and right subtrees are balanced
2. Check if height difference between left and right is <= 1
3. Return height if balanced, -1 if not balanced
4. Use bottom-up approach to avoid redundant calculations

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
    def is_balanced(self, root: Optional[TreeNode]) -> bool:
        def height(node):
            # Returns height if balanced, -1 if not balanced
            if not node:
                return 0

            left_height = height(node.left)
            if left_height == -1:
                return -1

            right_height = height(node.right)
            if right_height == -1:
                return -1

            # Check if current node is balanced
            if abs(left_height - right_height) > 1:
                return -1

            return 1 + max(left_height, right_height)

        return height(root) != -1


# Tests
def test():
    sol = Solution()

    # Test 1: Balanced tree
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert sol.is_balanced(root) == True

    # Test 2: Not balanced
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(2)
    root2.left.left = TreeNode(3)
    root2.left.right = TreeNode(3)
    root2.left.left.left = TreeNode(4)
    root2.left.left.right = TreeNode(4)
    assert sol.is_balanced(root2) == False

    # Test 3: Empty tree
    assert sol.is_balanced(None) == True

    # Test 4: Single node
    root3 = TreeNode(1)
    assert sol.is_balanced(root3) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
