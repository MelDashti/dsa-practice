"""
PROBLEM: Longest Consecutive Sequence (LeetCode 128)
LeetCode: https://leetcode.com/problems/longest-consecutive-sequence/
Difficulty: Medium
Pattern: Arrays & Hashing
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:
    Input: nums = [100,4,200,1,3,2]
    Output: 4
    Explanation: The longest consecutive sequence is [1, 2, 3, 4]

Example 2:
    Input: nums = [0,3,7,2,5,8,4,6,0,1]
    Output: 9
    Explanation: The longest consecutive sequence is [0,1,2,3,4,5,6,7,8]

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Approach:
1. Convert array to set for O(1) lookups
2. For each number, check if it's the start of a sequence (num-1 not in set)
3. If it's a start, count consecutive numbers
4. Track the maximum length found

Time: O(n) - each number visited at most twice
Space: O(n) - set storage
"""

from typing import List


class Solution:
    def longest_consecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        num_set = set(nums)
        max_length = 0

        for num in num_set:
            # Check if this is the start of a sequence
            if num - 1 not in num_set:
                current_num = num
                current_length = 1

                # Count consecutive numbers
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1

                max_length = max(max_length, current_length)

        return max_length


# Tests
def test():
    sol = Solution()

    assert sol.longest_consecutive([100,4,200,1,3,2]) == 4
    assert sol.longest_consecutive([0,3,7,2,5,8,4,6,0,1]) == 9
    assert sol.longest_consecutive([]) == 0
    assert sol.longest_consecutive([1]) == 1
    assert sol.longest_consecutive([1,2,0,1]) == 3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
