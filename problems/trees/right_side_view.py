"""
PROBLEM: Binary Tree Right Side View (LeetCode 199)
Difficulty: Medium
Pattern: Trees
Companies: Amazon, Facebook, Microsoft, Google, Bloomberg

Given the root of a binary tree, imagine yourself standing on the right side of
it, return the values of the nodes you can see ordered from top to bottom.

Example 1:
    Input: root = [1,2,3,null,5,null,4]
    Output: [1,3,4]

Example 2:
    Input: root = [1,null,3]
    Output: [1,3]

Example 3:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100

Approach:
1. Use BFS (level order traversal) with a queue
2. For each level, the rightmost node is the last one processed
3. Add the rightmost node of each level to result
4. Alternative: DFS where we track depth and add first node at each depth

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
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                # Add rightmost node of this level
                if i == level_size - 1:
                    result.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result


# Tests
def test():
    sol = Solution()

    # Test 1: Normal tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    assert sol.rightSideView(root) == [1, 3, 4]

    # Test 2: Right-skewed tree
    root2 = TreeNode(1)
    root2.right = TreeNode(3)
    assert sol.rightSideView(root2) == [1, 3]

    # Test 3: Empty tree
    assert sol.rightSideView(None) == []

    # Test 4: Left-skewed tree
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    root3.left.left = TreeNode(3)
    assert sol.rightSideView(root3) == [1, 2, 3]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
