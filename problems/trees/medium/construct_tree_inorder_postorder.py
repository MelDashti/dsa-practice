"""
PROBLEM: Construct Binary Tree from Inorder and Postorder Traversal (LeetCode 106)
LeetCode: https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google

Given two integer arrays inorder and postorder where inorder is the inorder
traversal of a binary tree and postorder is the postorder traversal of the same
tree, construct and return the binary tree.

Example 1:
    Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
    Output: [3,9,20,null,null,15,7]

Example 2:
    Input: inorder = [-1], postorder = [-1]
    Output: [-1]

Constraints:
- 1 <= inorder.length <= 3000
- postorder.length == inorder.length
- -3000 <= inorder[i], postorder[i] <= 3000
- inorder and postorder consist of unique values
- Each value of postorder also appears in inorder
- inorder is guaranteed to be the inorder traversal of the tree
- postorder is guaranteed to be the postorder traversal of the tree

Approach:
1. Last element of postorder is always root
2. Find root in inorder to split left and right subtrees
3. Elements left of root in inorder are left subtree
4. Elements right of root in inorder are right subtree
5. Build right subtree first (since we process postorder from right to left)
6. Use hashmap for O(1) lookup of root position in inorder

Time: O(n) - build each node once
Space: O(n) - hashmap and recursion stack
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def build_tree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        # Create hashmap for O(1) lookup of inorder indices
        inorder_map = {val: i for i, val in enumerate(inorder)}

        self.postorder_idx = len(postorder) - 1

        def build(left, right):
            # Base case
            if left > right:
                return None

            # Get root value from postorder (from right to left)
            root_val = postorder[self.postorder_idx]
            root = TreeNode(root_val)
            self.postorder_idx -= 1

            # Find root position in inorder
            inorder_idx = inorder_map[root_val]

            # Build right subtree first (since we process postorder right to left)
            root.right = build(inorder_idx + 1, right)

            # Build left subtree
            root.left = build(left, inorder_idx - 1)

            return root

        return build(0, len(inorder) - 1)


# Tests
def test():
    sol = Solution()

    def tree_to_list(root):
        """Helper to convert tree to list for testing"""
        if not root:
            return []
        result = []
        queue = [root]
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        return result

    # Test 1: Normal tree
    inorder = [9, 3, 15, 20, 7]
    postorder = [9, 15, 7, 20, 3]
    root = sol.build_tree(inorder, postorder)
    assert tree_to_list(root) == [3, 9, 20, None, None, 15, 7]

    # Test 2: Single node
    inorder2 = [-1]
    postorder2 = [-1]
    root2 = sol.build_tree(inorder2, postorder2)
    assert tree_to_list(root2) == [-1]

    # Test 3: Right-skewed tree
    inorder3 = [1, 2, 3]
    postorder3 = [3, 2, 1]
    root3 = sol.build_tree(inorder3, postorder3)
    assert root3.val == 1
    assert root3.right.val == 2
    assert root3.right.right.val == 3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
