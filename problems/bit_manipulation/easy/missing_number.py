"""
PROBLEM: Missing Number (LeetCode 268)
Difficulty: Easy
Pattern: Bit Manipulation, Array, Math
Companies: Amazon, Apple, Google, Facebook, LinkedIn

Given an array nums containing n distinct numbers in the range [0, n],
return the only number in the range that is missing from the array.

Follow-up: Could you implement a solution using only O(1) extra space complexity
and O(n) runtime complexity?

Example 1:
    Input: nums = [3,0,1]
    Output: 2
    Explanation: n = 3 since there are 3 numbers, so all numbers are in the range [0,3].
    2 is the missing number in the range since it does not appear in nums.

Example 2:
    Input: nums = [0,1]
    Output: 2
    Explanation: n = 2 since there are 2 numbers, so all numbers are in the range [0,2].
    2 is the missing number in the range since it does not appear in nums.

Example 3:
    Input: nums = [9,6,4,2,3,5,7,0,1]
    Output: 8

Constraints:
- n == nums.length
- 1 <= n <= 10^4
- 0 <= nums[i] <= n
- All the numbers of nums are unique

Approach:
Method 1 - XOR:
- XOR all numbers from 0 to n: result1
- XOR all numbers in the array: result2
- XOR result1 and result2 to get missing number
- Since a ^ a = 0 and a ^ 0 = a, pairs cancel out

Method 2 - Math (Gauss formula):
- Sum of 0 to n = n * (n + 1) / 2
- Missing number = expected_sum - actual_sum

Method 3 - Hash Set:
- Use a set to track which numbers are present
- Find the missing one

Time: O(n) - single pass (XOR or Math)
Space: O(1) - constant space (XOR or Math) or O(n) for hash set
"""

from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        """
        Find missing number using XOR.

        XOR approach:
        - XOR all numbers 0 to n
        - XOR all numbers in array
        - Result is the missing number (all present numbers cancel out)
        """
        result = len(nums)  # Start with n (since we need 0 to n)

        for i, num in enumerate(nums):
            result ^= i ^ num

        return result

    def missingNumber_math(self, nums: List[int]) -> int:
        """
        Find missing number using mathematical approach (Gauss formula).

        Expected sum of 0 to n = n * (n + 1) / 2
        Missing number = expected_sum - actual_sum
        """
        n = len(nums)
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(nums)
        return expected_sum - actual_sum

    def missingNumber_set(self, nums: List[int]) -> int:
        """
        Find missing number using hash set.
        """
        num_set = set(nums)
        for i in range(len(nums) + 1):
            if i not in num_set:
                return i


# Tests
def test():
    sol = Solution()

    assert sol.missingNumber([3, 0, 1]) == 2
    assert sol.missingNumber([0, 1]) == 2
    assert sol.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    assert sol.missingNumber([0]) == 1
    assert sol.missingNumber([1]) == 0
    assert sol.missingNumber([0, 2]) == 1

    # Test alternative implementations
    assert sol.missingNumber_math([3, 0, 1]) == 2
    assert sol.missingNumber_math([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8

    assert sol.missingNumber_set([3, 0, 1]) == 2
    assert sol.missingNumber_set([0, 1]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
