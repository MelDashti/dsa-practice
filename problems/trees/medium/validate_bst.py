"""
PROBLEM: Validate Binary Search Tree (LeetCode 98)
LeetCode: https://leetcode.com/problems/validate-binary-search-tree/
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Facebook, Microsoft, Google, Bloomberg

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key
- The right subtree of a node contains only nodes with keys greater than the node's key
- Both the left and right subtrees must also be binary search trees

Example 1:
    Input: root = [2,1,3]
    Output: true

Example 2:
    Input: root = [5,1,4,null,null,3,6]
    Output: false
    Explanation: The root node's value is 5 but its right child's value is 4

Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -2^31 <= Node.val <= 2^31 - 1

Approach:
1. Use DFS with valid range for each node
2. Root can be any value
3. Left children must be in range (min, node.val)
4. Right children must be in range (node.val, max)
5. Recursively validate all nodes

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
    def is_valid_bst(self, root: Optional[TreeNode]) -> bool:
        def validate(node, min_val, max_val):
            if not node:
                return True

            # Check if current node violates BST property
            if node.val <= min_val or node.val >= max_val:
                return False

            # Validate left and right subtrees with updated ranges
            return (validate(node.left, min_val, node.val) and
                    validate(node.right, node.val, max_val))

        return validate(root, float('-inf'), float('inf'))


# Tests
def test():
    sol = Solution()

    # Test 1: Valid BST
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    assert sol.is_valid_bst(root) == True

    # Test 2: Invalid BST
    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)
    assert sol.is_valid_bst(root2) == False

    # Test 3: Single node
    root3 = TreeNode(1)
    assert sol.is_valid_bst(root3) == True

    # Test 4: Edge case with equal values
    root4 = TreeNode(1)
    root4.left = TreeNode(1)
    assert sol.is_valid_bst(root4) == False

    # Test 5: Valid larger BST
    root5 = TreeNode(5)
    root5.left = TreeNode(3)
    root5.right = TreeNode(7)
    root5.left.left = TreeNode(2)
    root5.left.right = TreeNode(4)
    root5.right.left = TreeNode(6)
    root5.right.right = TreeNode(8)
    assert sol.is_valid_bst(root5) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
