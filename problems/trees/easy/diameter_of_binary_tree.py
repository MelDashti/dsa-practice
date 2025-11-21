"""
PROBLEM: Diameter of Binary Tree (LeetCode 543)
Difficulty: Easy
Pattern: Trees
Companies: Facebook, Amazon, Microsoft, Google, Apple

Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two
nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges
between them.

Example 1:
    Input: root = [1,2,3,4,5]
    Output: 3
    Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3]

Example 2:
    Input: root = [1,2]
    Output: 1

Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -100 <= Node.val <= 100

Approach:
1. For each node, the diameter passing through it is left_height + right_height
2. Use DFS to calculate height of each subtree
3. Track maximum diameter seen during traversal
4. Return the maximum diameter

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
    def diameter_of_binary_tree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0

        def height(node):
            if not node:
                return 0

            left_height = height(node.left)
            right_height = height(node.right)

            # Update diameter at this node
            self.diameter = max(self.diameter, left_height + right_height)

            return 1 + max(left_height, right_height)

        height(root)
        return self.diameter


# Tests
def test():
    sol = Solution()

    # Test 1: Normal tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    assert sol.diameter_of_binary_tree(root) == 3

    # Test 2: Simple tree
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    assert sol.diameter_of_binary_tree(root2) == 1

    # Test 3: Single node
    root3 = TreeNode(1)
    assert sol.diameter_of_binary_tree(root3) == 0

    # Test 4: Diameter doesn't pass through root
    root4 = TreeNode(1)
    root4.left = TreeNode(2)
    root4.left.left = TreeNode(3)
    root4.left.left.left = TreeNode(4)
    root4.left.left.left.left = TreeNode(5)
    assert sol.diameter_of_binary_tree(root4) == 4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
