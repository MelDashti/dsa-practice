"""
PROBLEM: Min Cost to Connect All Points (LeetCode 1584)
Difficulty: Medium
Pattern: Advanced Graphs, Minimum Spanning Tree, Prim's Algorithm
Companies: Amazon, Google, Microsoft, Facebook, Uber

You are given an array points representing integer coordinates of some points on a
2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance
between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. All points are connected if
there is exactly one simple path between any two points.

Example 1:
    Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    Output: 20
    Explanation:
    We can connect the points as shown to get the minimum total cost of 20.
    Notice that there is a unique path between every pair of points.

Example 2:
    Input: points = [[3,12],[-2,5],[-4,1]]
    Output: 18

Example 3:
    Input: points = [[0,0],[1,1],[1,0],[-1,1]]
    Output: 4

Constraints:
- 1 <= points.length <= 1000
- -10^6 <= xi, yi <= 10^6
- All pairs (xi, yi) are distinct

Approach:
1. Use Prim's algorithm to build Minimum Spanning Tree (MST)
2. Start from any point (e.g., point 0)
3. Use min heap to always select edge with minimum cost
4. Keep track of visited points to avoid cycles
5. Add edge costs to total until all points are connected

Alternative: Kruskal's algorithm with Union-Find

Time: O(N^2 log N) where N is number of points
Space: O(N^2) for storing all edges in heap
"""

from typing import List
import heapq


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        # Prim's algorithm
        visited = set()
        min_heap = [(0, 0)]  # (cost, point_index)
        total_cost = 0

        while len(visited) < n:
            cost, i = heapq.heappop(min_heap)

            if i in visited:
                continue

            visited.add(i)
            total_cost += cost

            # Add all edges from current point to unvisited points
            for j in range(n):
                if j not in visited:
                    manhattan_dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                    heapq.heappush(min_heap, (manhattan_dist, j))

        return total_cost


# Tests
def test():
    sol = Solution()

    # Test 1: Example from problem
    points1 = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
    assert sol.minCostConnectPoints(points1) == 20

    # Test 2: Three points
    points2 = [[3, 12], [-2, 5], [-4, 1]]
    assert sol.minCostConnectPoints(points2) == 18

    # Test 3: Four points forming a square
    points3 = [[0, 0], [1, 1], [1, 0], [-1, 1]]
    assert sol.minCostConnectPoints(points3) == 4

    # Test 4: Two points
    points4 = [[0, 0], [1, 1]]
    assert sol.minCostConnectPoints(points4) == 2

    # Test 5: Single point
    points5 = [[0, 0]]
    assert sol.minCostConnectPoints(points5) == 0

    # Test 6: Collinear points
    points6 = [[0, 0], [1, 0], [2, 0]]
    assert sol.minCostConnectPoints(points6) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
