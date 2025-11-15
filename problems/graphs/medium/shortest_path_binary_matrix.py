"""
PROBLEM: Shortest Path in Binary Matrix (LeetCode 1091)
Difficulty: Medium
Pattern: BFS, Graphs
Companies: Amazon, Google, Meta, Microsoft

DESCRIPTION:
Given an n x n binary matrix grid, return the length of the shortest clear path
in the matrix. If there is no clear path, return -1.

A clear path in a binary matrix is a path from the top-left cell (0, 0) to the
bottom-right cell (n - 1, n - 1) such that:
- All visited cells are 0
- All adjacent cells of the path are 8-directionally connected
  (they share an edge or corner)

The length of a clear path is the number of visited cells.

EXAMPLES:
Example 1:
Input: grid = [[0,1],[1,0]]
Output: 2

Example 2:
Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
Output: 4

Example 3:
Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
Output: -1

CONSTRAINTS:
- n == grid.length
- n == grid[i].length
- 1 <= n <= 100
- grid[i][j] is 0 or 1

APPROACH:
Use BFS to find shortest path (BFS guarantees shortest path in unweighted graph):
1. Start from (0, 0) if it's 0, otherwise return -1
2. Use queue for BFS with (row, col, distance)
3. Explore 8 directions for each cell
4. Mark visited cells to avoid revisiting
5. Return distance when reaching (n-1, n-1)

TIME COMPLEXITY: O(n²)
- Each cell visited at most once

SPACE COMPLEXITY: O(n²)
- Queue can contain up to O(n²) cells
- Visited set of size O(n²)

WHY THIS PROBLEM IS IMPORTANT:
- Extremely frequently asked at Amazon (top 15)
- Tests 8-directional movement (more complex than 4-directional)
- Classic BFS shortest path problem
- Simpler than A* but tests same concepts
"""

from typing import List
from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        """
        Find shortest path from top-left to bottom-right with 8-directional movement.
        """
        n = len(grid)

        # Edge cases
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return -1

        if n == 1:
            return 1 if grid[0][0] == 0 else -1

        # 8 directions: up, down, left, right, and 4 diagonals
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),  # Up-left, Up, Up-right
            (0, -1),
            (0, 1),  # Left, Right
            (1, -1),
            (1, 0),
            (1, 1),  # Down-left, Down, Down-right
        ]

        # BFS: (row, col, distance)
        queue = deque([(0, 0, 1)])
        grid[0][0] = 1  # Mark as visited (reuse grid to save space)

        while queue:
            row, col, dist = queue.popleft()

            # Check if we reached the destination
            if row == n - 1 and col == n - 1:
                return dist

            # Explore 8 directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                # Check if new position is valid and unvisited
                if (
                    0 <= new_row < n
                    and 0 <= new_col < n
                    and grid[new_row][new_col] == 0
                ):
                    queue.append((new_row, new_col, dist + 1))
                    grid[new_row][new_col] = 1  # Mark as visited

        return -1  # No path found


def test_shortest_path_binary_matrix():
    """Test cases for Shortest Path in Binary Matrix"""
    solution = Solution()

    # Test case 1: Simple 2x2
    assert solution.shortestPathBinaryMatrix([[0, 1], [1, 0]]) == 2

    # Test case 2: Diagonal path
    assert solution.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4

    # Test case 3: No path (start blocked)
    assert solution.shortestPathBinaryMatrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]]) == -1

    # Test case 4: Single cell (valid)
    assert solution.shortestPathBinaryMatrix([[0]]) == 1

    # Test case 5: Single cell (blocked)
    assert solution.shortestPathBinaryMatrix([[1]]) == -1

    # Test case 6: No path (destination blocked)
    assert solution.shortestPathBinaryMatrix([[0, 0], [0, 1]]) == -1

    # Test case 7: All zeros (direct diagonal)
    assert solution.shortestPathBinaryMatrix([[0, 0], [0, 0]]) == 2

    # Test case 8: Longer path
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert solution.shortestPathBinaryMatrix(grid) == 3

    # Test case 9: Complex maze
    grid = [
        [0, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]
    result = solution.shortestPathBinaryMatrix(grid)
    assert result == 5

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_shortest_path_binary_matrix()
