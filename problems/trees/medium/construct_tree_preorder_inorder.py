"""
PROBLEM: Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105)
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg

Given two integer arrays preorder and inorder where preorder is the preorder
traversal of a binary tree and inorder is the inorder traversal of the same tree,
construct and return the binary tree.

Example 1:
    Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
    Output: [3,9,20,null,null,15,7]

Example 2:
    Input: preorder = [-1], inorder = [-1]
    Output: [-1]

Constraints:
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values
- Each value of inorder also appears in preorder
- preorder is guaranteed to be the preorder traversal of the tree
- inorder is guaranteed to be the inorder traversal of the tree

Approach:
1. First element of preorder is always root
2. Find root in inorder to split left and right subtrees
3. Elements left of root in inorder are left subtree
4. Elements right of root in inorder are right subtree
5. Recursively build left and right subtrees
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
    def build_tree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Create hashmap for O(1) lookup of inorder indices
        inorder_map = {val: i for i, val in enumerate(inorder)}

        self.preorder_idx = 0

        def build(left, right):
            # Base case
            if left > right:
                return None

            # Get root value from preorder
            root_val = preorder[self.preorder_idx]
            root = TreeNode(root_val)
            self.preorder_idx += 1

            # Find root position in inorder
            inorder_idx = inorder_map[root_val]

            # Build left subtree (all elements before root in inorder)
            root.left = build(left, inorder_idx - 1)

            # Build right subtree (all elements after root in inorder)
            root.right = build(inorder_idx + 1, right)

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
    preorder = [3, 9, 20, 15, 7]
    inorder = [9, 3, 15, 20, 7]
    root = sol.build_tree(preorder, inorder)
    assert tree_to_list(root) == [3, 9, 20, None, None, 15, 7]

    # Test 2: Single node
    preorder2 = [-1]
    inorder2 = [-1]
    root2 = sol.build_tree(preorder2, inorder2)
    assert tree_to_list(root2) == [-1]

    # Test 3: Left-skewed tree
    preorder3 = [1, 2, 3]
    inorder3 = [3, 2, 1]
    root3 = sol.build_tree(preorder3, inorder3)
    assert root3.val == 1
    assert root3.left.val == 2
    assert root3.left.left.val == 3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
