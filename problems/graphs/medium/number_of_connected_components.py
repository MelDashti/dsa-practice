"""
PROBLEM: Number of Connected Components in an Undirected Graph (LeetCode 323)
LeetCode: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
Difficulty: Medium
Pattern: Graphs (Union Find, DFS)
Companies: Google, Amazon, Facebook, Microsoft, LinkedIn

You have a graph of n nodes labeled from 0 to n - 1. You are given an integer n and an
array edges where edges[i] = [ai, bi] indicates that there is an undirected edge between
nodes ai and bi in the graph.

Return the number of connected components in the graph.

Example 1:
    Input: n = 5, edges = [[0,1],[1,2],[3,4]]
    Output: 2
    Explanation: There are two connected components: {0,1,2} and {3,4}

Example 2:
    Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
    Output: 1
    Explanation: All nodes are connected in one component

Constraints:
- 1 <= n <= 2000
- 0 <= edges.length <= 5000
- edges[i].length == 2
- 0 <= ai <= bi < n
- ai != bi
- There are no repeated edges

Approach:
1. Use Union Find to group connected nodes
2. For each edge, union the two nodes
3. Count number of unique parents (roots)
4. Each unique parent represents one connected component

Time: O(E * α(n)) - where E is number of edges, α is inverse Ackermann
Space: O(n) - parent and rank arrays
"""

from typing import List


class Solution:
    def count_components(self, n: int, edges: List[List[int]]) -> int:
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
                return 0  # Already in same component

            # Union by rank
            if rank[p1] > rank[p2]:
                parent[p2] = p1
                rank[p1] += rank[p2]
            else:
                parent[p1] = p2
                rank[p2] += rank[p1]

            return 1  # Successfully merged two components

        # Start with n components
        components = n

        # Process each edge
        for node1, node2 in edges:
            components -= union(node1, node2)

        return components


# Tests
def test():
    sol = Solution()

    # Test 1: Two components
    assert sol.count_components(5, [[0,1],[1,2],[3,4]]) == 2

    # Test 2: One component
    assert sol.count_components(5, [[0,1],[1,2],[2,3],[3,4]]) == 1

    # Test 3: All disconnected
    assert sol.count_components(4, []) == 4

    # Test 4: Three components
    assert sol.count_components(6, [[0,1],[2,3]]) == 4

    # Test 5: Single node
    assert sol.count_components(1, []) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
