"""
PROBLEM: Subtree of Another Tree (LeetCode 572)
LeetCode: https://leetcode.com/problems/subtree-of-another-tree/
Difficulty: Easy
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google

Given the roots of two binary trees root and sub_root, return true if there is
a subtree of root with the same structure and node values of sub_root and false
otherwise.

A subtree of a binary tree is a tree that consists of a node in tree and all of
this node's descendants. The tree could also be considered as a subtree of itself.

Example 1:
    Input: root = [3,4,5,1,2], sub_root = [4,1,2]
    Output: true

Example 2:
    Input: root = [3,4,5,1,2,null,null,null,null,0], sub_root = [4,1,2]
    Output: false

Constraints:
- The number of nodes in the root tree is in the range [1, 2000]
- The number of nodes in the sub_root tree is in the range [1, 1000]
- -10^4 <= root.val <= 10^4
- -10^4 <= sub_root.val <= 10^4

Approach:
1. For each node in root, check if subtree starting at that node is same as sub_root
2. Use helper function to check if two trees are identical
3. Recursively check left and right subtrees
4. Return true if we find a match

Time: O(m * n) - where m is nodes in root, n is nodes in sub_root
Space: O(h) - recursion stack where h is height of tree
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def is_subtree(self, root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
        if not root:
            return False

        # Check if current tree is same as sub_root
        if self.is_same_tree(root, sub_root):
            return True

        # Check left and right subtrees
        return self.is_subtree(root.left, sub_root) or self.is_subtree(root.right, sub_root)

    def is_same_tree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.is_same_tree(p.left, q.left) and self.is_same_tree(p.right, q.right)


# Tests
def test():
    sol = Solution()

    # Test 1: Valid subtree
    root = TreeNode(3)
    root.left = TreeNode(4)
    root.right = TreeNode(5)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(2)

    sub_root = TreeNode(4)
    sub_root.left = TreeNode(1)
    sub_root.right = TreeNode(2)

    assert sol.is_subtree(root, sub_root) == True

    # Test 2: Not a valid subtree
    root2 = TreeNode(3)
    root2.left = TreeNode(4)
    root2.right = TreeNode(5)
    root2.left.left = TreeNode(1)
    root2.left.right = TreeNode(2)
    root2.left.right.left = TreeNode(0)

    sub_root2 = TreeNode(4)
    sub_root2.left = TreeNode(1)
    sub_root2.right = TreeNode(2)

    assert sol.is_subtree(root2, sub_root2) == False

    # Test 3: Single node
    root3 = TreeNode(1)
    sub_root3 = TreeNode(1)
    assert sol.is_subtree(root3, sub_root3) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
