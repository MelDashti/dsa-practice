"""
PROBLEM: Redundant Connection (LeetCode 684)
Difficulty: Medium
Pattern: Graphs (Union Find)
Companies: Amazon, Google, Microsoft, Facebook

In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one
additional edge added. The added edge has two different vertices chosen from 1 to n, and
was not an edge that already existed. The graph is represented as an array edges of length n
where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there
are multiple answers, return the answer that occurs last in the input.

Example 1:
    Input: edges = [[1,2],[1,3],[2,3]]
    Output: [2,3]

Example 2:
    Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
    Output: [1,4]

Constraints:
- n == edges.length
- 3 <= n <= 1000
- edges[i].length == 2
- 1 <= ai < bi <= edges.length
- ai != bi
- There are no repeated edges
- The given graph is connected

Approach:
1. Use Union Find (Disjoint Set Union) data structure
2. Process edges one by one
3. For each edge, check if nodes are already connected
4. If yes, this edge creates a cycle - return it
5. Otherwise, union the two nodes

Time: O(n * α(n)) - where α is inverse Ackermann function (nearly constant)
Space: O(n) - parent and rank arrays
"""

from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = list(range(n + 1))  # 1-indexed
        rank = [1] * (n + 1)

        def find(node):
            # Find with path compression
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            # Union by rank
            p1, p2 = find(node1), find(node2)

            if p1 == p2:
                return False  # Already connected - cycle detected

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
                return [node1, node2]

        return []


# Tests
def test():
    sol = Solution()

    # Test 1: Simple triangle
    assert sol.findRedundantConnection([[1,2],[1,3],[2,3]]) == [2,3]

    # Test 2: Multiple cycles possible
    assert sol.findRedundantConnection([[1,2],[2,3],[3,4],[1,4],[1,5]]) == [1,4]

    # Test 3: Linear with one extra edge
    assert sol.findRedundantConnection([[1,2],[2,3],[3,1]]) == [3,1]

    # Test 4: Four nodes
    assert sol.findRedundantConnection([[1,2],[2,3],[3,4],[4,1]]) == [4,1]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
