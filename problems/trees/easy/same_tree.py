"""
PROBLEM: Same Tree (LeetCode 100)
Difficulty: Easy
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg

Given the roots of two binary trees p and q, write a function to check if they
are the same or not.

Two binary trees are considered the same if they are structurally identical,
and the nodes have the same value.

Example 1:
    Input: p = [1,2,3], q = [1,2,3]
    Output: true

Example 2:
    Input: p = [1,2], q = [1,null,2]
    Output: false

Example 3:
    Input: p = [1,2,1], q = [1,1,2]
    Output: false

Constraints:
- The number of nodes in both trees is in the range [0, 100]
- -10^4 <= Node.val <= 10^4

Approach:
1. Base case: if both nodes are None, return True
2. If one is None and other is not, return False
3. If values are different, return False
4. Recursively check left and right subtrees
5. Return True only if both subtrees are the same

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
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # Both are None
        if not p and not q:
            return True

        # One is None, other is not
        if not p or not q:
            return False

        # Values are different
        if p.val != q.val:
            return False

        # Check both subtrees
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


# Tests
def test():
    sol = Solution()

    # Test 1: Same trees
    p1 = TreeNode(1)
    p1.left = TreeNode(2)
    p1.right = TreeNode(3)

    q1 = TreeNode(1)
    q1.left = TreeNode(2)
    q1.right = TreeNode(3)

    assert sol.isSameTree(p1, q1) == True

    # Test 2: Different structure
    p2 = TreeNode(1)
    p2.left = TreeNode(2)

    q2 = TreeNode(1)
    q2.right = TreeNode(2)

    assert sol.isSameTree(p2, q2) == False

    # Test 3: Different values
    p3 = TreeNode(1)
    p3.left = TreeNode(2)
    p3.right = TreeNode(1)

    q3 = TreeNode(1)
    q3.left = TreeNode(1)
    q3.right = TreeNode(2)

    assert sol.isSameTree(p3, q3) == False

    # Test 4: Both empty
    assert sol.isSameTree(None, None) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
