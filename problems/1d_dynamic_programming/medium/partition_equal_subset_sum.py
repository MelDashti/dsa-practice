"""
PROBLEM: Partition Equal Subset Sum (LeetCode 416)
LeetCode: https://leetcode.com/problems/partition-equal-subset-sum/
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given a non-empty array nums containing only positive integers, find if the
array can be partitioned into two subsets such that the sum of elements in both
subsets is equal.

Example 1:
    Input: nums = [1,5,11,5]
    Output: true
    Explanation: The array can be partitioned as [1, 5, 5] and [11].

Example 2:
    Input: nums = [1,2,3,5]
    Output: false
    Explanation: The array cannot be partitioned into equal sum subsets.

Constraints:
- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100

Approach:
1. This is a subset sum problem (0/1 knapsack variant)
2. If total sum is odd, cannot partition equally
3. If total sum is even, find if subset with sum = total/2 exists
4. Use DP: dp[i] = true if sum i is achievable
5. For each number, update dp array from right to left
6. dp[i] = dp[i] OR dp[i - num] (include current number or not)

Time: O(n * sum) - for each number, update all possible sums
Space: O(sum) - dp array
"""

from typing import List


class Solution:
    def can_partition(self, nums: List[int]) -> bool:
        total_sum = sum(nums)

        # If total sum is odd, cannot partition into equal subsets
        if total_sum % 2 != 0:
            return False

        target = total_sum // 2

        # dp[i] represents if sum i is achievable
        dp = [False] * (target + 1)
        dp[0] = True  # Sum 0 is always achievable (empty subset)

        # Process each number
        for num in nums:
            # Traverse from right to left to avoid using same element twice
            for i in range(target, num - 1, -1):
                dp[i] = dp[i] or dp[i - num]

        return dp[target]


# Tests
def test():
    sol = Solution()

    assert sol.can_partition([1,5,11,5]) == True
    assert sol.can_partition([1,2,3,5]) == False
    assert sol.can_partition([1,2,3,4]) == True
    assert sol.can_partition([1,1]) == True
    assert sol.can_partition([1,2,5]) == False
    assert sol.can_partition([100]) == False
    assert sol.can_partition([1,1,1,1]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
