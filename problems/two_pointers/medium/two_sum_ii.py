"""
PROBLEM: Two Sum II - Input Array Is Sorted (LeetCode 167)
Difficulty: Medium
Pattern: Two Pointers
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing
order, find two numbers such that they add up to a specific target number. Let these
two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one as an integer
array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the
same element twice.

Example 1:
    Input: numbers = [2,7,11,15], target = 9
    Output: [1,2]
    Explanation: 2 + 7 = 9, so index1 = 1, index2 = 2

Example 2:
    Input: numbers = [2,3,4], target = 6
    Output: [1,3]

Example 3:
    Input: numbers = [-1,0], target = -1
    Output: [1,2]

Constraints:
- 2 <= numbers.length <= 3 * 10^4
- -1000 <= numbers[i] <= 1000
- numbers is sorted in non-decreasing order
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution

Approach:
1. Use two pointers: left at start, right at end
2. Calculate sum of numbers[left] + numbers[right]
3. If sum == target, return [left+1, right+1] (1-indexed)
4. If sum < target, move left pointer right
5. If sum > target, move right pointer left

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def two_sum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                return [left + 1, right + 1]  # 1-indexed
            elif current_sum < target:
                left += 1
            else:
                right -= 1

        return []  # Should never reach here per problem constraints


# Tests
def test():
    sol = Solution()

    assert sol.two_sum([2,7,11,15], 9) == [1,2]
    assert sol.two_sum([2,3,4], 6) == [1,3]
    assert sol.two_sum([-1,0], -1) == [1,2]
    assert sol.two_sum([1,2,3,4,5], 9) == [4,5]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
