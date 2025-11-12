"""
PROBLEM: Kth Smallest Element in a BST (LeetCode 230)
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg

Given the root of a binary search tree, and an integer k, return the kth smallest
value (1-indexed) of all the values of the nodes in the tree.

Example 1:
    Input: root = [3,1,4,null,2], k = 1
    Output: 1

Example 2:
    Input: root = [5,3,6,2,4,null,null,1], k = 3
    Output: 3

Constraints:
- The number of nodes in the tree is n
- 1 <= k <= n <= 10^4
- 0 <= Node.val <= 10^4

Follow up: If the BST is modified often (insert/delete) and you need to find
the kth smallest frequently, how would you optimize?

Approach:
1. Use inorder traversal of BST (left -> root -> right)
2. Inorder traversal visits nodes in ascending order
3. Keep counter and stop when we reach kth element
4. Can be done iteratively with stack or recursively

Time: O(n) - in worst case visit all nodes
Space: O(h) - recursion/stack space where h is height
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.count = 0
        self.result = 0

        def inorder(node):
            if not node:
                return

            # Traverse left subtree
            inorder(node.left)

            # Process current node
            self.count += 1
            if self.count == k:
                self.result = node.val
                return

            # Traverse right subtree
            inorder(node.right)

        inorder(root)
        return self.result


# Tests
def test():
    sol = Solution()

    # Test 1: Example 1
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.right = TreeNode(2)
    assert sol.kthSmallest(root, 1) == 1

    # Test 2: Example 2
    root2 = TreeNode(5)
    root2.left = TreeNode(3)
    root2.right = TreeNode(6)
    root2.left.left = TreeNode(2)
    root2.left.right = TreeNode(4)
    root2.left.left.left = TreeNode(1)
    assert sol.kthSmallest(root2, 3) == 3

    # Test 3: Single node
    root3 = TreeNode(1)
    assert sol.kthSmallest(root3, 1) == 1

    # Test 4: Find largest
    root4 = TreeNode(2)
    root4.left = TreeNode(1)
    root4.right = TreeNode(3)
    assert sol.kthSmallest(root4, 3) == 3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
