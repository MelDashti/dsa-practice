"""
PROBLEM: Pacific Atlantic Water Flow (LeetCode 417)
LeetCode: https://leetcode.com/problems/pacific-atlantic-water-flow/
Difficulty: Medium
Pattern: Graphs (DFS/BFS)
Companies: Google, Amazon, Facebook, Microsoft

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean.
The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches
the island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an m x n integer
matrix heights where heights[r][c] represents the height above sea level of the cell at
coordinate (r, c).

The island receives a lot of rain, and the rain water can flow to neighboring cells directly
north, south, east, and west if the neighboring cell's height is less than or equal to the
current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.

Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain
water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.

Example 1:
    Input: heights = [
        [1,2,2,3,5],
        [3,2,3,4,4],
        [2,4,5,3,1],
        [6,7,1,4,5],
        [5,1,1,2,4]
    ]
    Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

Example 2:
    Input: heights = [[1]]
    Output: [[0,0]]

Constraints:
- m == heights.length
- n == heights[r].length
- 1 <= m, n <= 200
- 0 <= heights[r][c] <= 10^5

Approach:
1. Start from ocean borders and work backwards (water flows up)
2. Run DFS from Pacific borders (top row, left column)
3. Run DFS from Atlantic borders (bottom row, right column)
4. Find cells reachable from both oceans (intersection)
5. Water can flow to neighbors if neighbor height >= current height

Time: O(m * n) - visit each cell at most twice
Space: O(m * n) - two sets to track reachable cells
"""

from typing import List


class Solution:
    def pacific_atlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []

        rows, cols = len(heights), len(heights[0])
        pacific = set()
        atlantic = set()

        def dfs(r, c, visited, prev_height):
            # Check bounds, if already visited, or if water can't flow
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or heights[r][c] < prev_height):
                return

            visited.add((r, c))

            # Explore all 4 directions
            dfs(r + 1, c, visited, heights[r][c])
            dfs(r - 1, c, visited, heights[r][c])
            dfs(r, c + 1, visited, heights[r][c])
            dfs(r, c - 1, visited, heights[r][c])

        # DFS from Pacific borders (top and left)
        for c in range(cols):
            dfs(0, c, pacific, heights[0][c])
            dfs(rows - 1, c, atlantic, heights[rows - 1][c])

        for r in range(rows):
            dfs(r, 0, pacific, heights[r][0])
            dfs(r, cols - 1, atlantic, heights[r][cols - 1])

        # Find intersection
        result = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in pacific and (r, c) in atlantic:
                    result.append([r, c])

        return result


# Tests
def test():
    sol = Solution()

    # Test 1: 5x5 grid
    heights1 = [
        [1,2,2,3,5],
        [3,2,3,4,4],
        [2,4,5,3,1],
        [6,7,1,4,5],
        [5,1,1,2,4]
    ]
    result1 = sol.pacific_atlantic(heights1)
    expected1 = [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    assert sorted(result1) == sorted(expected1)

    # Test 2: Single cell
    heights2 = [[1]]
    assert sol.pacific_atlantic(heights2) == [[0,0]]

    # Test 3: All same height
    heights3 = [
        [1,1,1],
        [1,1,1],
        [1,1,1]
    ]
    result3 = sol.pacific_atlantic(heights3)
    assert len(result3) == 9  # All cells can reach both oceans

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
