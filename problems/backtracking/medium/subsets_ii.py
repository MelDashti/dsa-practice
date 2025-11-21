"""
PROBLEM: Subsets II (LeetCode 90)
LeetCode: https://leetcode.com/problems/subsets-ii/
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Facebook, Microsoft, Google, Apple

Given an integer array nums that may contain duplicates, return all possible
subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in
any order.

Example 1:
    Input: nums = [1,2,2]
    Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]

Example 2:
    Input: nums = [0]
    Output: [[],[0]]

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10

Approach:
1. Sort the array first to group duplicates together
2. Use backtracking to generate subsets
3. To avoid duplicate subsets, skip duplicate elements at same recursion level
4. If current element equals previous and we didn't use previous, skip current
5. This ensures we only generate unique subsets

Time: O(n * 2^n) - 2^n subsets, each taking O(n) to copy
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def subsets_with_dup(self, nums: List[int]) -> List[List[int]]:
        result = []
        current = []
        nums.sort()  # Sort to handle duplicates

        def backtrack(index):
            # Add current subset to result
            result.append(current[:])

            # Try adding each remaining element
            for i in range(index, len(nums)):
                # Skip duplicates at same level
                if i > index and nums[i] == nums[i-1]:
                    continue

                current.append(nums[i])
                backtrack(i + 1)
                current.pop()

        backtrack(0)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.subsets_with_dup([1,2,2])
    expected1 = [[],[1],[1,2],[1,2,2],[2],[2,2]]
    assert sorted([sorted(x) for x in result1]) == sorted([sorted(x) for x in expected1])

    # Test case 2
    result2 = sol.subsets_with_dup([0])
    expected2 = [[],[0]]
    assert sorted([sorted(x) for x in result2]) == sorted([sorted(x) for x in expected2])

    # Test case 3
    result3 = sol.subsets_with_dup([4,4,4,1,4])
    # Should not have duplicate subsets
    result_set = set(tuple(sorted(x)) for x in result3)
    assert len(result_set) == len(result3)

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
