"""
PROBLEM: Find First and Last Position of Element in Sorted Array (LeetCode 34)
Difficulty: Medium
Pattern: Binary Search
Companies: Amazon, Meta, Google, Microsoft, Apple

DESCRIPTION:
Given an array of integers nums sorted in non-decreasing order, find the starting
and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

EXAMPLES:
Example 1:
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:
Input: nums = [], target = 0
Output: [-1,-1]

CONSTRAINTS:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array
- -10^9 <= target <= 10^9

APPROACH:
Use binary search twice:
1. First binary search to find the leftmost (first) occurrence
2. Second binary search to find the rightmost (last) occurrence

For finding the left boundary:
- When nums[mid] >= target, move right pointer (could be the answer or need to go left)
- When nums[mid] < target, move left pointer

For finding the right boundary:
- When nums[mid] <= target, move left pointer (could be the answer or need to go right)
- When nums[mid] > target, move right pointer

TIME COMPLEXITY: O(log n)
- Two binary searches, each O(log n)

SPACE COMPLEXITY: O(1)
- Only using constant extra space

WHY THIS PROBLEM IS IMPORTANT:
- Classic binary search variation (find boundaries)
- Very frequently asked at FAANG (especially Amazon, Meta)
- Tests deep understanding of binary search edge cases
- Foundation for more complex binary search problems
"""

from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        Find the starting and ending position of target in sorted array.
        """
        if not nums:
            return [-1, -1]

        left = self.findLeft(nums, target)
        if left == -1:
            return [-1, -1]

        right = self.findRight(nums, target)
        return [left, right]

    def findLeft(self, nums: List[int], target: int) -> int:
        """
        Binary search to find the leftmost (first) occurrence of target.
        """
        left, right = 0, len(nums) - 1
        result = -1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                result = mid  # Found target, but keep searching left
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return result

    def findRight(self, nums: List[int], target: int) -> int:
        """
        Binary search to find the rightmost (last) occurrence of target.
        """
        left, right = 0, len(nums) - 1
        result = -1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                result = mid  # Found target, but keep searching right
                left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return result


def test_search_range():
    """Test cases for Find First and Last Position"""
    solution = Solution()

    # Test case 1: Target appears multiple times
    assert solution.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]

    # Test case 2: Target not in array
    assert solution.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]

    # Test case 3: Empty array
    assert solution.searchRange([], 0) == [-1, -1]

    # Test case 4: Single element (found)
    assert solution.searchRange([1], 1) == [0, 0]

    # Test case 5: Single element (not found)
    assert solution.searchRange([1], 0) == [-1, -1]

    # Test case 6: Target appears once
    assert solution.searchRange([1, 2, 3, 4, 5], 3) == [2, 2]

    # Test case 7: All elements are target
    assert solution.searchRange([5, 5, 5, 5, 5], 5) == [0, 4]

    # Test case 8: Target at boundaries
    assert solution.searchRange([1, 2, 3, 4, 5], 1) == [0, 0]
    assert solution.searchRange([1, 2, 3, 4, 5], 5) == [4, 4]

    # Test case 9: Large array with duplicates
    assert solution.searchRange([1, 1, 2, 2, 2, 2, 3, 3, 3, 4], 2) == [2, 5]
    assert solution.searchRange([1, 1, 2, 2, 2, 2, 3, 3, 3, 4], 3) == [6, 8]

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_search_range()
