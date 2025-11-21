"""
PROBLEM: Two Sum (LeetCode 1)
LeetCode: https://leetcode.com/problems/two-sum/
Difficulty: Easy
Pattern: Arrays & Hashing
Companies: Amazon, Apple, Google, Facebook, Microsoft

Given an array of integers nums and an integer target, return indices of the
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may
not use the same element twice. You can return the answer in any order.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: nums[0] + nums[1] == 9, so we return [0, 1]

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Example 3:
    Input: nums = [3,3], target = 6
    Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists

Approach:
1. Use hash map to store seen numbers and their indices
2. For each number, calculate complement = target - num
3. Check if complement exists in hash map
4. If yes, return [index_of_complement, current_index]
5. If no, add current number to hash map

Time: O(n) - single pass through array
Space: O(n) - hash map storage
"""

from typing import List


class Solution:
    def two_sum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # value -> index

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i

        return []  # Should never reach here per problem constraints


# Tests
def test():
    sol = Solution()

    assert sol.two_sum([2,7,11,15], 9) == [0,1]
    assert sol.two_sum([3,2,4], 6) == [1,2]
    assert sol.two_sum([3,3], 6) == [0,1]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
