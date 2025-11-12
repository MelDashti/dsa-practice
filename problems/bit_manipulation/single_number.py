"""
PROBLEM: Single Number (LeetCode 136)
Difficulty: Easy
Pattern: Bit Manipulation
Companies: Amazon, Apple, Google, Facebook, Microsoft

Given a non-empty array of integers nums, every element appears twice except for one element
that appears exactly once. Find that single element.

You must implement a solution with a linear time complexity and use only constant extra space.

Example 1:
    Input: nums = [2,2,1]
    Output: 1

Example 2:
    Input: nums = [4,1,2,1,2]
    Output: 4

Example 3:
    Input: nums = [1]
    Output: 1

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element in the array appears twice except for one element which appears exactly once

Approach:
XOR has the property that a ^ a = 0 and a ^ 0 = a
When we XOR all numbers together, pairs cancel out (become 0)
and we're left with the single number

Time: O(n) - single pass through array
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Find the single number that appears once using XOR.

        XOR properties:
        - a ^ a = 0 (same numbers cancel out)
        - a ^ 0 = a (XOR with 0 returns the number)
        - XOR is commutative and associative
        """
        result = 0
        for num in nums:
            result ^= num
        return result


# Tests
def test():
    sol = Solution()

    assert sol.singleNumber([2, 2, 1]) == 1
    assert sol.singleNumber([4, 1, 2, 1, 2]) == 4
    assert sol.singleNumber([1]) == 1
    assert sol.singleNumber([1, 2, 1, 3, 2]) == 3
    assert sol.singleNumber([-1, -1, 5]) == 5

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
