"""
PROBLEM: Find the Duplicate Number (LeetCode 287)
Difficulty: Medium
Pattern: Linked List (Floyd's Cycle Detection), Array, Two Pointers
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

Given an array of integers nums containing n + 1 integers where each integer is
in the range [1, n] inclusive.

There is only one repeated number in nums, return this repeated number.

You must solve the problem without modifying the array nums and uses only constant
extra space.

Example 1:
    Input: nums = [1,3,4,2,2]
    Output: 2

Example 2:
    Input: nums = [3,1,3,4,2]
    Output: 3

Example 3:
    Input: nums = [3,3,3,3,3]
    Output: 3

Constraints:
- 1 <= n <= 10^5
- nums.length == n + 1
- 1 <= nums[i] <= n
- All the integers in nums appear only once except for precisely one integer which appears two or more times

Follow up:
- How can we prove that at least one duplicate number must exist in nums?
- Can you solve the problem in linear runtime complexity?

Approach:
1. Treat array as implicit linked list where nums[i] points to nums[nums[i]]
2. Use Floyd's Cycle Detection algorithm
3. Phase 1: Find intersection point in cycle using slow/fast pointers
4. Phase 2: Find entrance to cycle (duplicate number)
5. Move slow to start, keep fast at intersection
6. Move both one step at a time until they meet at cycle entrance

Time: O(n) - two passes through array
Space: O(1) - only using two pointers
"""

from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # Phase 1: Find intersection point in the cycle
        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        # Phase 2: Find the entrance to the cycle (duplicate number)
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow


# Tests
def test():
    sol = Solution()

    assert sol.findDuplicate([1,3,4,2,2]) == 2
    assert sol.findDuplicate([3,1,3,4,2]) == 3
    assert sol.findDuplicate([3,3,3,3,3]) == 3
    assert sol.findDuplicate([2,5,9,6,9,3,8,9,7,1,4]) == 9

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
