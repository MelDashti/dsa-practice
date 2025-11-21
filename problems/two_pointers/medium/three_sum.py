"""
PROBLEM: 3Sum (LeetCode 15)
Difficulty: Medium
Pattern: Two Pointers
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2],[-1,0,1]]
    Explanation:
    nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0
    nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0
    nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0

Example 2:
    Input: nums = [0,1,1]
    Output: []

Example 3:
    Input: nums = [0,0,0]
    Output: [[0,0,0]]

Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

Approach:
1. Sort the array
2. For each number, use two pointers to find pairs that sum to -nums[i]
3. Skip duplicates to avoid duplicate triplets
4. Left pointer starts after current, right pointer at end

Time: O(n^2) - n iterations with two pointers
Space: O(1) not counting output array
"""

from typing import List


class Solution:
    def three_sum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []

        for i in range(len(nums)):
            # Skip duplicates for first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Two pointers for remaining two numbers
            left, right = i + 1, len(nums) - 1
            target = -nums[i]

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    result.append([nums[i], nums[left], nums[right]])

                    # Skip duplicates for second number
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1

                    # Skip duplicates for third number
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return result


# Tests
def test():
    sol = Solution()

    result1 = sol.three_sum([-1,0,1,2,-1,-4])
    expected1 = [[-1,-1,2],[-1,0,1]]
    assert sorted(result1) == sorted(expected1)

    assert sol.three_sum([0,1,1]) == []
    assert sol.three_sum([0,0,0]) == [[0,0,0]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
