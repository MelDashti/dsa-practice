"""
PROBLEM: House Robber II (LeetCode 213)
LeetCode: https://leetcode.com/problems/house-robber-ii/
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Apple, Facebook

You are a professional robber planning to rob houses along a street. Each house
has a certain amount of money stashed. All houses at this place are arranged in
a circle. That means the first house is the neighbor of the last one. Meanwhile,
adjacent houses have security systems connected, and it will automatically contact
the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the police.

Example 1:
    Input: nums = [2,3,2]
    Output: 3
    Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2),
    because they are adjacent houses.

Example 2:
    Input: nums = [1,2,3,1]
    Output: 4
    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
    Total amount you can rob = 1 + 3 = 4.

Example 3:
    Input: nums = [1,2,3]
    Output: 3

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000

Approach:
1. Since houses are circular, first and last house are adjacent
2. We can't rob both first and last house
3. Solution: max(rob houses 0 to n-2, rob houses 1 to n-1)
4. Use House Robber I solution for each range
5. Handle edge case where there's only one house

Time: O(n) - two passes through array
Space: O(1) - only store variables
"""

from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])

        # Helper function to rob a linear array
        def rob_linear(houses):
            prev2 = 0
            prev1 = 0

            for house in houses:
                current = max(house + prev2, prev1)
                prev2 = prev1
                prev1 = current

            return prev1

        # Case 1: Rob houses from 0 to n-2 (exclude last house)
        # Case 2: Rob houses from 1 to n-1 (exclude first house)
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


# Tests
def test():
    sol = Solution()

    assert sol.rob([2,3,2]) == 3
    assert sol.rob([1,2,3,1]) == 4
    assert sol.rob([1,2,3]) == 3
    assert sol.rob([1]) == 1
    assert sol.rob([1,2]) == 2
    assert sol.rob([200,3,140,20,10]) == 340

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
