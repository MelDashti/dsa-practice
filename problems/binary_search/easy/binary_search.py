"""
PROBLEM: Binary Search (LeetCode 704)
LeetCode: https://leetcode.com/problems/binary-search/
Difficulty: Easy
Pattern: Binary Search
Companies: Amazon, Microsoft, Google, Facebook, Apple

Given an array of integers nums which is sorted in ascending order, and an
integer target, write a function to search target in nums. If target exists,
then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [-1,0,3,5,9,12], target = 9
    Output: 4
    Explanation: 9 exists in nums and its index is 4

Example 2:
    Input: nums = [-1,0,3,5,9,12], target = 2
    Output: -1
    Explanation: 2 does not exist in nums so return -1

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All the integers in nums are unique
- nums is sorted in ascending order

Approach:
1. Initialize left and right pointers at start and end of array
2. While left <= right:
   - Calculate middle index
   - If middle element equals target, return middle index
   - If target is greater than middle element, search right half (left = mid + 1)
   - If target is less than middle element, search left half (right = mid - 1)
3. If not found, return -1

Time: O(log n) - halving search space each iteration
Space: O(1) - only using pointers
"""

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2  # Avoid overflow

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1


# Tests
def test():
    sol = Solution()

    assert sol.search([-1,0,3,5,9,12], 9) == 4
    assert sol.search([-1,0,3,5,9,12], 2) == -1
    assert sol.search([5], 5) == 0
    assert sol.search([5], -5) == -1
    assert sol.search([2,5], 5) == 1
    assert sol.search([2,5], 0) == -1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
