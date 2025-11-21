"""
PROBLEM: Find Minimum in Rotated Sorted Array (LeetCode 153)
LeetCode: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
Difficulty: Medium
Pattern: Binary Search
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg

Suppose an array of length n sorted in ascending order is rotated between
1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:
- [4,5,6,7,0,1,2] if it was rotated 4 times
- [0,1,2,4,5,6,7] if it was rotated 7 times

Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results
in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the sorted rotated array nums of unique elements, return the minimum
element of this array.

You must write an algorithm that runs in O(log n) time.

Example 1:
    Input: nums = [3,4,5,1,2]
    Output: 1
    Explanation: The original array was [1,2,3,4,5] rotated 3 times

Example 2:
    Input: nums = [4,5,6,7,0,1,2]
    Output: 0
    Explanation: The original array was [0,1,2,4,5,6,7] rotated 4 times

Example 3:
    Input: nums = [11,13,15,17]
    Output: 11
    Explanation: The original array was [11,13,15,17] and it was rotated 4 times

Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers of nums are unique
- nums is sorted and rotated between 1 and n times

Approach:
1. Use binary search to find the inflection point (where rotation happened)
2. Compare middle element with rightmost element
3. If mid > right, minimum is in right half (left = mid + 1)
4. If mid <= right, minimum is in left half including mid (right = mid)
5. Continue until left == right

Time: O(log n) - binary search
Space: O(1) - only using pointers
"""

from typing import List


class Solution:
    def find_min(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2

            # If mid element is greater than right element,
            # the minimum is in the right half
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                # The minimum is in the left half (including mid)
                right = mid

        return nums[left]


# Tests
def test():
    sol = Solution()

    assert sol.find_min([3,4,5,1,2]) == 1
    assert sol.find_min([4,5,6,7,0,1,2]) == 0
    assert sol.find_min([11,13,15,17]) == 11
    assert sol.find_min([1]) == 1
    assert sol.find_min([2,1]) == 1
    assert sol.find_min([1,2]) == 1
    assert sol.find_min([3,1,2]) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
