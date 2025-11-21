"""
PROBLEM: Search in Rotated Sorted Array (LeetCode 33)
LeetCode: https://leetcode.com/problems/search-in-rotated-sorted-array/
Difficulty: Medium
Pattern: Binary Search
Companies: Amazon, Microsoft, Facebook, Google, Apple

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown
pivot index k (1 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).

For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return
the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [4,5,6,7,0,1,2], target = 0
    Output: 4

Example 2:
    Input: nums = [4,5,6,7,0,1,2], target = 3
    Output: -1

Example 3:
    Input: nums = [1], target = 0
    Output: -1

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique
- nums is an ascending array that is possibly rotated
- -10^4 <= target <= 10^4

Approach:
1. Use modified binary search
2. At each step, determine which half is sorted
3. Check if target is in the sorted half
4. If yes, search that half; otherwise search the other half
5. Key insight: One half will always be sorted

Time: O(log n) - binary search
Space: O(1) - only using pointers
"""

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            # Determine which half is sorted
            if nums[left] <= nums[mid]:
                # Left half is sorted
                if nums[left] <= target < nums[mid]:
                    # Target is in sorted left half
                    right = mid - 1
                else:
                    # Target is in right half
                    left = mid + 1
            else:
                # Right half is sorted
                if nums[mid] < target <= nums[right]:
                    # Target is in sorted right half
                    left = mid + 1
                else:
                    # Target is in left half
                    right = mid - 1

        return -1


# Tests
def test():
    sol = Solution()

    assert sol.search([4,5,6,7,0,1,2], 0) == 4
    assert sol.search([4,5,6,7,0,1,2], 3) == -1
    assert sol.search([1], 0) == -1
    assert sol.search([1], 1) == 0
    assert sol.search([3,1], 1) == 1
    assert sol.search([5,1,3], 5) == 0
    assert sol.search([4,5,6,7,8,1,2,3], 8) == 4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
