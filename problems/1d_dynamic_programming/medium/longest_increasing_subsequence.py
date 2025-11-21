"""
PROBLEM: Longest Increasing Subsequence (LeetCode 300)
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Microsoft, Google, Facebook, Apple

Given an integer array nums, return the length of the longest strictly
increasing subsequence.

A subsequence is a sequence that can be derived from an array by deleting some
or no elements without changing the order of the remaining elements.

Example 1:
    Input: nums = [10,9,2,5,3,7,101,18]
    Output: 4
    Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:
    Input: nums = [0,1,0,3,2,3]
    Output: 4

Example 3:
    Input: nums = [7,7,7,7,7,7,7]
    Output: 1

Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

Approach:
1. Use dynamic programming approach
2. dp[i] = length of longest increasing subsequence ending at index i
3. For each i, check all previous elements j < i
4. If nums[i] > nums[j], then dp[i] = max(dp[i], dp[j] + 1)
5. Answer is maximum value in dp array

Alternative (Binary Search): O(n log n)
- Maintain array of smallest tail elements for each length
- Use binary search to find position to update

Time: O(n^2) - nested loops
Space: O(n) - dp array
"""

from typing import List


class Solution:
    def length_of_lis(self, nums: List[int]) -> int:
        if not nums:
            return 0

        n = len(nums)
        # dp[i] = length of LIS ending at index i
        dp = [1] * n

        for i in range(1, n):
            for j in range(i):
                # If current number is greater, extend the subsequence
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)


# Tests
def test():
    sol = Solution()

    assert sol.length_of_lis([10,9,2,5,3,7,101,18]) == 4
    assert sol.length_of_lis([0,1,0,3,2,3]) == 4
    assert sol.length_of_lis([7,7,7,7,7,7,7]) == 1
    assert sol.length_of_lis([1,3,6,7,9,4,10,5,6]) == 6
    assert sol.length_of_lis([1]) == 1
    assert sol.length_of_lis([1,2,3,4,5]) == 5

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
