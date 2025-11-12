"""
PROBLEM: Clone Graph (LeetCode 133)
Difficulty: Medium
Pattern: Graphs (DFS/BFS)
Companies: Facebook, Amazon, Microsoft, Google, Bloomberg

Given a reference of a node in a connected undirected graph, return a deep copy
(clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}

Test case format:
For simplicity, each node's value is the same as the node's index (1-indexed).
For example, the first node with val == 1, the second node with val == 2, and so on.
The graph is represented in the test case using an adjacency list.

Example 1:
    Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
    Output: [[2,4],[1,3],[2,4],[1,3]]
    Explanation: There are 4 nodes in the graph.
    1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
    2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
    3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
    4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).

Example 2:
    Input: adjList = [[]]
    Output: [[]]
    Explanation: The input contains one empty list. The graph consists of only one node
    with val = 1 and it does not have any neighbors.

Example 3:
    Input: adjList = []
    Output: []
    Explanation: This an empty graph, it does not have any nodes.

Constraints:
- The number of nodes in the graph is in the range [0, 100]
- 1 <= Node.val <= 100
- Node.val is unique for each node
- There are no repeated edges and no self-loops in the graph
- The Graph is connected and all nodes can be visited starting from the given node

Approach:
1. Use DFS/BFS with a hashmap to track old_node -> new_node mapping
2. For each node, create a clone and add to hashmap
3. Recursively clone all neighbors
4. Return the cloned node

Time: O(N + E) - visit all nodes and edges
Space: O(N) - hashmap to store cloned nodes
"""

from typing import Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        # Map old node to new node
        old_to_new = {}

        def dfs(node):
            if node in old_to_new:
                return old_to_new[node]

            # Create a copy of the node
            copy = Node(node.val)
            old_to_new[node] = copy

            # Clone all neighbors
            for neighbor in node.neighbors:
                copy.neighbors.append(dfs(neighbor))

            return copy

        return dfs(node)


# Tests
def test():
    sol = Solution()

    # Test 1: 4-node graph
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node1.neighbors = [node2, node4]
    node2.neighbors = [node1, node3]
    node3.neighbors = [node2, node4]
    node4.neighbors = [node1, node3]

    cloned = sol.cloneGraph(node1)
    assert cloned.val == 1
    assert len(cloned.neighbors) == 2
    assert cloned.neighbors[0].val == 2
    assert cloned.neighbors[1].val == 4
    # Ensure it's a deep copy
    assert cloned is not node1
    assert cloned.neighbors[0] is not node2

    # Test 2: Single node
    single = Node(1)
    cloned_single = sol.cloneGraph(single)
    assert cloned_single.val == 1
    assert len(cloned_single.neighbors) == 0
    assert cloned_single is not single

    # Test 3: Empty graph
    assert sol.cloneGraph(None) is None

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
