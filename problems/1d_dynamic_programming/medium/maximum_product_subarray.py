"""
PROBLEM: Maximum Product Subarray (LeetCode 152)
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Microsoft, Apple, Facebook, Google

Given an integer array nums, find a contiguous non-empty subarray within the
array that has the largest product, and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

A subarray is a contiguous subsequence of the array.

Example 1:
    Input: nums = [2,3,-2,4]
    Output: 6
    Explanation: [2,3] has the largest product 6.

Example 2:
    Input: nums = [-2,0,-1]
    Output: 0
    Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer

Approach:
1. Track both maximum and minimum product ending at current position
2. Negative number can flip max and min (negative * negative = positive)
3. For each number, calculate:
   - New max = max(num, num * prev_max, num * prev_min)
   - New min = min(num, num * prev_max, num * prev_min)
4. Keep track of global maximum
5. Handle zeros by resetting the product

Time: O(n) - single pass through array
Space: O(1) - only store variables
"""

from typing import List


class Solution:
    def max_product(self, nums: List[int]) -> int:
        if not nums:
            return 0

        # Initialize with first element
        max_prod = nums[0]
        min_prod = nums[0]
        result = nums[0]

        for i in range(1, len(nums)):
            num = nums[i]

            # If current number is negative, swap max and min
            # because negative * max becomes min and negative * min becomes max
            if num < 0:
                max_prod, min_prod = min_prod, max_prod

            # Calculate new max and min
            max_prod = max(num, max_prod * num)
            min_prod = min(num, min_prod * num)

            # Update result
            result = max(result, max_prod)

        return result


# Tests
def test():
    sol = Solution()

    assert sol.max_product([2,3,-2,4]) == 6
    assert sol.max_product([-2,0,-1]) == 0
    assert sol.max_product([-2]) == -2
    assert sol.max_product([0,2]) == 2
    assert sol.max_product([-2,3,-4]) == 24
    assert sol.max_product([2,-5,-2,-4,3]) == 24

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
