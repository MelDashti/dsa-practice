"""
PROBLEM: Swim in Rising Water (LeetCode 778)
Difficulty: Hard
Pattern: Advanced Graphs, Binary Search, BFS/DFS, Modified Dijkstra
Companies: Google, Amazon, Facebook, Microsoft

You are given an n x n integer matrix grid where each value grid[i][j] represents
the elevation at that point (i, j).

The rain starts to fall. At time t, the depth of the water everywhere is t. You can
swim from a square to another 4-directionally adjacent square if and only if the
elevation of both squares individually are at most t. You can swim infinite distances
in zero time. Of course, you must stay within the boundaries of the grid during your
swim.

Return the least time until you can reach the bottom right square (n - 1, n - 1) if
you start at the top left square (0, 0).

Example 1:
    Input: grid = [[0,2],[1,3]]
    Output: 3
    Explanation:
    At time 0, you are in grid location (0, 0).
    You cannot go anywhere else because 4-directionally adjacent neighbors have a higher elevation than t = 0.
    You cannot reach point (1, 1) until time 3.
    When the depth of water is 3, we can swim anywhere inside the grid.

Example 2:
    Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
    Output: 16
    Explanation: The final route is shown.
    We need to wait until time 16 so that (0, 0) and (4, 4) are connected.

Constraints:
- n == grid.length
- n == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] < n^2
- Each value grid[i][j] is unique

Approach:
1. Use modified Dijkstra's algorithm (priority queue)
2. Instead of sum of distances, track maximum elevation encountered
3. Always process cell with minimum max elevation first
4. Start from (0,0), target is (n-1, n-1)
5. For each cell, explore 4-directional neighbors
6. Track the maximum elevation needed to reach each cell

Time: O(N^2 log N) where N is grid dimension
Space: O(N^2) for visited set and priority queue
"""

from typing import List
import heapq


class Solution:
    def swim_in_water(self, grid: List[List[int]]) -> int:
        n = len(grid)
        visited = set()
        min_heap = [(grid[0][0], 0, 0)]  # (max_elevation, row, col)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while min_heap:
            max_elev, row, col = heapq.heappop(min_heap)

            if (row, col) in visited:
                continue

            visited.add((row, col))

            # Reached destination
            if row == n - 1 and col == n - 1:
                return max_elev

            # Explore neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if (0 <= new_row < n and 0 <= new_col < n and
                        (new_row, new_col) not in visited):
                    new_max_elev = max(max_elev, grid[new_row][new_col])
                    heapq.heappush(min_heap, (new_max_elev, new_row, new_col))

        return -1  # Should never reach here if input is valid


# Tests
def test():
    sol = Solution()

    # Test 1: Small 2x2 grid
    grid1 = [[0, 2], [1, 3]]
    assert sol.swim_in_water(grid1) == 3

    # Test 2: Larger grid
    grid2 = [
        [0, 1, 2, 3, 4],
        [24, 23, 22, 21, 5],
        [12, 13, 14, 15, 16],
        [11, 17, 18, 19, 20],
        [10, 9, 8, 7, 6]
    ]
    assert sol.swim_in_water(grid2) == 16

    # Test 3: Single cell
    grid3 = [[0]]
    assert sol.swim_in_water(grid3) == 0

    # Test 4: 2x2 with different values
    grid4 = [[0, 1], [2, 3]]
    assert sol.swim_in_water(grid4) == 3

    # Test 5: Path with low elevations
    grid5 = [[0, 3], [1, 2]]
    assert sol.swim_in_water(grid5) == 2

    # Test 6: 3x3 grid
    grid6 = [[3, 4, 5], [2, 7, 6], [1, 0, 8]]
    assert sol.swim_in_water(grid6) == 8

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
