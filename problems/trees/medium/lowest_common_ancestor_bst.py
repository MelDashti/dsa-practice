"""
PROBLEM: Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google, LinkedIn

Given a binary search tree (BST), find the lowest common ancestor (LCA) node of
two given nodes in the BST.

According to the definition of LCA: "The lowest common ancestor is defined between
two nodes p and q as the lowest node in T that has both p and q as descendants
(where we allow a node to be a descendant of itself)."

Example 1:
    Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
    Output: 6
    Explanation: The LCA of nodes 2 and 8 is 6

Example 2:
    Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
    Output: 2
    Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself

Example 3:
    Input: root = [2,1], p = 2, q = 1
    Output: 2

Constraints:
- The number of nodes in the tree is in the range [2, 10^5]
- -10^9 <= Node.val <= 10^9
- All Node.val are unique
- p != q
- p and q will exist in the BST

Approach:
1. Use BST property: left subtree < root < right subtree
2. If both p and q are less than root, LCA is in left subtree
3. If both p and q are greater than root, LCA is in right subtree
4. Otherwise, root is the LCA (split point)
5. Can be done iteratively or recursively

Time: O(h) - where h is height of tree
Space: O(1) - iterative approach, O(h) for recursive
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        curr = root

        while curr:
            # Both nodes are in left subtree
            if p.val < curr.val and q.val < curr.val:
                curr = curr.left
            # Both nodes are in right subtree
            elif p.val > curr.val and q.val > curr.val:
                curr = curr.right
            # Split point found (or one of the nodes is the current node)
            else:
                return curr

        return None


# Tests
def test():
    sol = Solution()

    # Test 1: LCA in middle
    root = TreeNode(6)
    root.left = TreeNode(2)
    root.right = TreeNode(8)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    root.left.right.left = TreeNode(3)
    root.left.right.right = TreeNode(5)

    result = sol.lowestCommonAncestor(root, root.left, root.right)
    assert result.val == 6

    # Test 2: LCA is one of the nodes
    result2 = sol.lowestCommonAncestor(root, root.left, root.left.right)
    assert result2.val == 2

    # Test 3: Simple tree
    root2 = TreeNode(2)
    root2.left = TreeNode(1)
    result3 = sol.lowestCommonAncestor(root2, root2, root2.left)
    assert result3.val == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
