"""
PROBLEM: Product of Array Except Self (LeetCode 238)
Difficulty: Medium
Pattern: Arrays & Hashing, Prefix Sum
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given an integer array nums, return an array answer such that answer[i] is
equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example 1:
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]

Example 2:
    Input: nums = [-1,1,0,-3,3]
    Output: [0,0,9,0,0]

Constraints:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix is guaranteed to fit in 32-bit integer

Follow up: Can you solve it in O(1) extra space complexity?
(The output array does not count as extra space)

Approach:
1. Create result array with products of all elements to the left
2. Multiply by products of all elements to the right
3. Use prefix and suffix product approach

Time: O(n) - two passes through array
Space: O(1) not counting output array
"""

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n

        # First pass: calculate prefix products
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]

        # Second pass: calculate suffix products and multiply
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]

        return result


# Tests
def test():
    sol = Solution()

    assert sol.productExceptSelf([1,2,3,4]) == [24,12,8,6]
    assert sol.productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0]
    assert sol.productExceptSelf([2,3,4,5]) == [60,40,30,24]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
