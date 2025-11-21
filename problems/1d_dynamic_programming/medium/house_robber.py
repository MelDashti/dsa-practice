"""
PROBLEM: House Robber (LeetCode 198)
LeetCode: https://leetcode.com/problems/house-robber/
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Google, Apple, Microsoft, Facebook

You are a professional robber planning to rob houses along a street. Each house
has a certain amount of money stashed, the only constraint stopping you from
robbing each of them is that adjacent houses have security systems connected and
it will automatically contact the police if two adjacent houses were broken into
on the same night.

Given an integer array nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the police.

Example 1:
    Input: nums = [1,2,3,1]
    Output: 4
    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
    Total amount you can rob = 1 + 3 = 4.

Example 2:
    Input: nums = [2,7,9,3,1]
    Output: 12
    Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
    Total amount you can rob = 2 + 9 + 1 = 12.

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400

Approach:
1. For each house, decide whether to rob it or skip it
2. If we rob house i, we can't rob house i-1, so add nums[i] + max_at_i-2
3. If we skip house i, max remains max_at_i-1
4. dp[i] = max(nums[i] + dp[i-2], dp[i-1])
5. Optimize space by only keeping last two values

Time: O(n) - single pass through array
Space: O(1) - only store two variables
"""

from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        # prev2 represents max money up to i-2
        # prev1 represents max money up to i-1
        prev2 = 0
        prev1 = 0

        for num in nums:
            # Either rob current house + prev2, or skip current house (prev1)
            current = max(num + prev2, prev1)
            prev2 = prev1
            prev1 = current

        return prev1


# Tests
def test():
    sol = Solution()

    assert sol.rob([1,2,3,1]) == 4
    assert sol.rob([2,7,9,3,1]) == 12
    assert sol.rob([5,3,4,11,2]) == 16
    assert sol.rob([1]) == 1
    assert sol.rob([2,1,1,2]) == 4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
