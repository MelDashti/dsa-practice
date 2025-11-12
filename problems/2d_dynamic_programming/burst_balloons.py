"""
PROBLEM: Burst Balloons (LeetCode 312)
Difficulty: Hard
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

You are given n balloons, indexed from 0 to n - 1. Each balloon is painted with
a number on it represented by an array nums. You are asked to burst all the balloons.

If you burst the ith balloon, you will get nums[i - 1] * nums[i] * nums[i + 1]
coins. If i - 1 or i + 1 goes out of bounds of the array, then treat it as if
there is a balloon with a 1 painted on it.

Return the maximum coins you can collect by bursting the balloons wisely.

Example 1:
    Input: nums = [3,1,5,8]
    Output: 167
    Explanation:
    nums = [3,1,5,8] --> [3,5,8] --> [3,8] --> [8] --> []
    coins =  3*1*5    +   3*5*8   +  1*3*8  + 1*8*1 = 167

Example 2:
    Input: nums = [1,5]
    Output: 10

Constraints:
- n == nums.length
- 1 <= n <= 300
- 0 <= nums[i] <= 100

Approach:
1. Think backwards: instead of which balloon to burst first, think which to burst last
2. Add virtual balloons with value 1 at both ends
3. Use 2D DP where dp[left][right] = max coins bursting balloons between left and right
4. For each subarray [left, right], try bursting each balloon i last
5. When balloon i is burst last, all balloons between left and i, and i and right
   are already burst
6. Coins = nums[left] * nums[i] * nums[right] + dp[left][i] + dp[i][right]

Time: O(n^3) - three nested loops for left, right, and last balloon
Space: O(n^2) - DP table
"""

from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        # Add virtual balloons with value 1 at both ends
        nums = [1] + nums + [1]
        n = len(nums)

        # dp[left][right] = max coins bursting balloons between left and right
        dp = [[0] * n for _ in range(n)]

        # Length of subarray
        for length in range(2, n):
            # Starting position
            for left in range(n - length):
                right = left + length

                # Try bursting each balloon last
                for i in range(left + 1, right):
                    # Coins from bursting balloon i last
                    coins = nums[left] * nums[i] * nums[right]
                    # Add coins from left and right subarrays
                    coins += dp[left][i] + dp[i][right]
                    # Update max
                    dp[left][right] = max(dp[left][right], coins)

        return dp[0][n - 1]


# Tests
def test():
    sol = Solution()

    assert sol.maxCoins([3,1,5,8]) == 167
    assert sol.maxCoins([1,5]) == 10
    assert sol.maxCoins([1]) == 1
    assert sol.maxCoins([3,1,5]) == 35
    assert sol.maxCoins([9,76,64,21,97,60,5]) == 1088290

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
