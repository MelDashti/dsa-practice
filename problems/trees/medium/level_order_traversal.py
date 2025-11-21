"""
PROBLEM: Binary Tree Level Order Traversal (LeetCode 102)
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg

Given the root of a binary tree, return the level order traversal of its nodes'
values. (i.e., from left to right, level by level).

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[9,20],[15,7]]

Example 2:
    Input: root = [1]
    Output: [[1]]

Example 3:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 2000]
- -1000 <= Node.val <= 1000

Approach:
1. Use BFS with a queue to traverse level by level
2. Process each level separately by tracking level size
3. Add all nodes at current level to result
4. Add their children to queue for next level
5. Return the result list

Time: O(n) - visit every node once
Space: O(n) - queue storage
"""

from typing import List, Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def level_order(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result


# Tests
def test():
    sol = Solution()

    # Test 1: Normal tree
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert sol.level_order(root) == [[3], [9, 20], [15, 7]]

    # Test 2: Single node
    root2 = TreeNode(1)
    assert sol.level_order(root2) == [[1]]

    # Test 3: Empty tree
    assert sol.level_order(None) == []

    # Test 4: Unbalanced tree
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    root3.left.left = TreeNode(3)
    assert sol.level_order(root3) == [[1], [2], [3]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
