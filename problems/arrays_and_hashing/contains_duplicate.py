"""
PROBLEM: Contains Duplicate (LeetCode 217)
Difficulty: Easy
Pattern: Arrays & Hashing

Given an integer array nums, return true if any value appears at least twice
in the array, and return false if every element is distinct.

Example 1:
    Input: nums = [1,2,3,1]
    Output: true

Example 2:
    Input: nums = [1,2,3,4]
    Output: false

Example 3:
    Input: nums = [1,1,1,3,3,4,3,2,4,2]
    Output: true

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Approach:
1. Use a hash set to track seen numbers
2. For each number, check if it's already in the set
3. If yes, return true (duplicate found)
4. If no, add to set and continue
5. If we finish the loop, return false

Time: O(n) - single pass through array
Space: O(n) - hash set storage
"""

from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False


# Tests
def test():
    sol = Solution()

    assert sol.containsDuplicate([1,2,3,1]) == True
    assert sol.containsDuplicate([1,2,3,4]) == False
    assert sol.containsDuplicate([1,1,1,3,3,4,3,2,4,2]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
