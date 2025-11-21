"""
PROBLEM: Serialize and Deserialize Binary Tree (LeetCode 297)
LeetCode: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
Difficulty: Hard
Pattern: Trees
Companies: Amazon, Facebook, Microsoft, Google, Bloomberg

Serialization is the process of converting a data structure or object into a
sequence of bits so that it can be stored in a file or memory buffer, or
transmitted across a network connection link to be reconstructed later in the
same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no
restriction on how your serialization/deserialization algorithm should work.
You just need to ensure that a binary tree can be serialized to a string and
this string can be deserialized to the original tree structure.

Example 1:
    Input: root = [1,2,3,null,null,4,5]
    Output: [1,2,3,null,null,4,5]

Example 2:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -1000 <= Node.val <= 1000

Approach:
1. Serialize: Use preorder traversal (root, left, right)
2. Use a delimiter (comma) to separate values
3. Use "null" or "N" for null nodes
4. Deserialize: Split string and reconstruct using preorder
5. Use queue/deque for easier processing

Time: O(n) - visit every node once for both operations
Space: O(n) - string storage and recursion stack
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        result = []

        def preorder(node):
            if not node:
                result.append("N")
                return
            result.append(str(node.val))
            preorder(node.left)
            preorder(node.right)

        preorder(root)
        return ",".join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree."""
        values = deque(data.split(","))

        def build():
            val = values.popleft()
            if val == "N":
                return None

            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node

        return build()


# Tests
def test():
    codec = Codec()

    # Test 1: Normal tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)

    serialized = codec.serialize(root)
    deserialized = codec.deserialize(serialized)

    # Verify structure
    assert deserialized.val == 1
    assert deserialized.left.val == 2
    assert deserialized.right.val == 3
    assert deserialized.right.left.val == 4
    assert deserialized.right.right.val == 5

    # Test 2: Empty tree
    serialized2 = codec.serialize(None)
    deserialized2 = codec.deserialize(serialized2)
    assert deserialized2 is None

    # Test 3: Single node
    root3 = TreeNode(1)
    serialized3 = codec.serialize(root3)
    deserialized3 = codec.deserialize(serialized3)
    assert deserialized3.val == 1
    assert deserialized3.left is None
    assert deserialized3.right is None

    # Test 4: Left-skewed tree
    root4 = TreeNode(1)
    root4.left = TreeNode(2)
    root4.left.left = TreeNode(3)

    serialized4 = codec.serialize(root4)
    deserialized4 = codec.deserialize(serialized4)
    assert deserialized4.val == 1
    assert deserialized4.left.val == 2
    assert deserialized4.left.left.val == 3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
