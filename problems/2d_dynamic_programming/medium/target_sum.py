"""
PROBLEM: Target Sum (LeetCode 494)
Difficulty: Medium
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+'
and '-' before each integer in nums and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1
and concatenate them to build the expression "+2-1".

Return the number of different expressions that you can build, which evaluates to target.

Example 1:
    Input: nums = [1,1,1,1,1], target = 3
    Output: 5
    Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
    -1 + 1 + 1 + 1 + 1 = 3
    +1 - 1 + 1 + 1 + 1 = 3
    +1 + 1 - 1 + 1 + 1 = 3
    +1 + 1 + 1 - 1 + 1 = 3
    +1 + 1 + 1 + 1 - 1 = 3

Example 2:
    Input: nums = [1], target = 1
    Output: 1

Constraints:
- 1 <= nums.length <= 20
- 0 <= nums[i] <= 1000
- 0 <= sum(nums[i]) <= 1000
- -1000 <= target <= 1000

Approach:
1. This is a subset sum problem in disguise
2. Let P = positive subset, N = negative subset
3. P - N = target and P + N = sum
4. Therefore: P = (target + sum) / 2
5. Problem reduces to: count subsets with sum = (target + sum) / 2
6. Use 2D DP where dp[i][j] = ways to make sum j using first i numbers
7. Can optimize to 1D array

Time: O(n * sum) - where n is length of nums and sum is total sum
Space: O(sum) - 1D DP array
"""

from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)

        # Check if solution is possible
        if abs(target) > total or (target + total) % 2 != 0:
            return 0

        # Find the subset sum we need
        subset_sum = (target + total) // 2

        # dp[i] = number of ways to make sum i
        dp = [0] * (subset_sum + 1)
        dp[0] = 1  # One way to make 0: select nothing

        # For each number
        for num in nums:
            # Traverse backwards to avoid using same element twice
            for i in range(subset_sum, num - 1, -1):
                dp[i] += dp[i - num]

        return dp[subset_sum]


# Tests
def test():
    sol = Solution()

    assert sol.findTargetSumWays([1,1,1,1,1], 3) == 5
    assert sol.findTargetSumWays([1], 1) == 1
    assert sol.findTargetSumWays([1], 2) == 0
    assert sol.findTargetSumWays([1,0], 1) == 2
    assert sol.findTargetSumWays([100], -200) == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
