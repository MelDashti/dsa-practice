"""
PROBLEM: Unique Paths (LeetCode 62)
Difficulty: Medium
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

There is a robot on an m x n grid. The robot is initially located at the
top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right
corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right
at any point in time.

Given the two integers m and n, return the number of possible unique paths that
the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 10^9.

Example 1:
    Input: m = 3, n = 7
    Output: 28

Example 2:
    Input: m = 3, n = 2
    Output: 3
    Explanation: From the top-left corner, there are a total of 3 ways to reach
    the bottom-right corner:
    1. Right -> Down -> Down
    2. Down -> Down -> Right
    3. Down -> Right -> Down

Constraints:
- 1 <= m, n <= 100

Approach:
1. Use 2D DP where dp[i][j] = number of ways to reach cell (i, j)
2. Base case: dp[0][j] = 1 (only one way to reach any cell in first row)
3. Base case: dp[i][0] = 1 (only one way to reach any cell in first column)
4. For any other cell: dp[i][j] = dp[i-1][j] + dp[i][j-1]
5. Can optimize space to O(n) by only keeping one row

Time: O(m * n) - fill entire grid
Space: O(n) - only store one row
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Use single row for space optimization
        dp = [1] * n

        # Start from second row
        for i in range(1, m):
            for j in range(1, n):
                # Current cell = paths from above + paths from left
                dp[j] = dp[j] + dp[j - 1]

        return dp[n - 1]


# Tests
def test():
    sol = Solution()

    assert sol.uniquePaths(3, 7) == 28
    assert sol.uniquePaths(3, 2) == 3
    assert sol.uniquePaths(1, 1) == 1
    assert sol.uniquePaths(3, 3) == 6
    assert sol.uniquePaths(10, 10) == 48620

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
