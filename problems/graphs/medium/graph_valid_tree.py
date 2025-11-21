"""
PROBLEM: Graph Valid Tree (LeetCode 261)
Difficulty: Medium
Pattern: Graphs (Union Find, DFS)
Companies: Google, Facebook, Amazon, Microsoft, LinkedIn

You have a graph of n nodes labeled from 0 to n - 1. You are given an integer n and an
array edges where edges[i] = [ai, bi] indicates that there is an undirected edge between
nodes ai and bi in the graph.

Return true if the edges of the given graph make up a valid tree, and false otherwise.

A valid tree must satisfy:
1. The graph must be fully connected (all nodes reachable)
2. The graph must have no cycles
3. For n nodes, a tree must have exactly n-1 edges

Example 1:
    Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
    Output: true

Example 2:
    Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
    Output: false
    Explanation: There is a cycle between nodes 1, 2, and 3

Constraints:
- 1 <= n <= 2000
- 0 <= edges.length <= 5000
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- There are no self-loops or repeated edges

Approach:
1. A valid tree has exactly n-1 edges
2. Use Union Find to detect cycles
3. If union fails (nodes already connected), there's a cycle
4. After processing all edges, check if there's only 1 component

Time: O(E * α(n)) - where E is number of edges, α is inverse Ackermann
Space: O(n) - parent and rank arrays
"""

from typing import List


class Solution:
    def valid_tree(self, n: int, edges: List[List[int]]) -> bool:
        # A tree with n nodes must have exactly n-1 edges
        if len(edges) != n - 1:
            return False

        parent = list(range(n))
        rank = [1] * n

        def find(node):
            # Find with path compression
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            # Union by rank
            p1, p2 = find(node1), find(node2)

            if p1 == p2:
                return False  # Cycle detected

            # Union by rank
            if rank[p1] > rank[p2]:
                parent[p2] = p1
                rank[p1] += rank[p2]
            else:
                parent[p1] = p2
                rank[p2] += rank[p1]

            return True

        # Process each edge
        for node1, node2 in edges:
            if not union(node1, node2):
                return False  # Cycle detected

        return True


# Tests
def test():
    sol = Solution()

    # Test 1: Valid tree
    assert sol.valid_tree(5, [[0,1],[0,2],[0,3],[1,4]]) == True

    # Test 2: Has cycle
    assert sol.valid_tree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]]) == False

    # Test 3: Disconnected graph
    assert sol.valid_tree(4, [[0,1],[2,3]]) == False

    # Test 4: Too many edges
    assert sol.valid_tree(4, [[0,1],[0,2],[0,3],[1,2],[1,3]]) == False

    # Test 5: Single node
    assert sol.valid_tree(1, []) == True

    # Test 6: Two nodes connected
    assert sol.valid_tree(2, [[0,1]]) == True

    # Test 7: Two nodes disconnected
    assert sol.valid_tree(2, []) == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
