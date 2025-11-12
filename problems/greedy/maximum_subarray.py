"""
PROBLEM: Maximum Subarray (LeetCode 53)
Difficulty: Medium
Pattern: Greedy, Dynamic Programming
Companies: Amazon, Microsoft, Apple, Adobe, Google

Given an integer array nums, find the contiguous subarray (containing at least one number)
which has the largest sum and return its sum. A subarray is a contiguous part of an array.

Example 1:
    Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
    Output: 6
    Explanation: [4,-1,2,1] has the largest sum = 6.

Example 2:
    Input: nums = [5,4,-1,7,8]
    Output: 23

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Approach (Kadane's Algorithm):
1. Track maximum sum ending at current position
2. At each position, decide: extend existing subarray or start new one
3. Keep track of overall maximum
4. Greedy choice: always take locally maximum sum

Time: O(n) - single pass through array
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Find maximum subarray sum using Kadane's algorithm.

        Strategy:
        - current_sum tracks the max sum ending at current position
        - If adding current number decreases sum, start fresh from current number
        - Track overall maximum throughout iteration
        """
        max_current = max_global = nums[0]

        for i in range(1, len(nums)):
            # Either extend existing subarray or start new from current element
            max_current = max(nums[i], max_current + nums[i])

            # Update global maximum
            max_global = max(max_global, max_current)

        return max_global


# Tests
def test():
    sol = Solution()

    assert sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert sol.maxSubArray([5, 4, -1, 7, 8]) == 23
    assert sol.maxSubArray([-1]) == -1
    assert sol.maxSubArray([-2, 1]) == 1
    assert sol.maxSubArray([0, -2, 3, -1, 1, 2]) == 5
    assert sol.maxSubArray([-13, -3, -20]) == -3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
