"""
PROBLEM: Subsets (LeetCode 78)
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given an integer array nums of unique elements, return all possible subsets
(the power set).

The solution set must not contain duplicate subsets. Return the solution in
any order.

Example 1:
    Input: nums = [1,2,3]
    Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Example 2:
    Input: nums = [0]
    Output: [[],[0]]

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique

Approach:
1. Use backtracking to generate all possible subsets
2. For each element, we have two choices: include it or exclude it
3. Start with empty subset and recursively build subsets
4. At each step, add current subset to result
5. Recursively explore including next element and excluding it

Time: O(n * 2^n) - 2^n subsets, each taking O(n) to copy
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        current = []

        def backtrack(index):
            # Add current subset to result
            result.append(current[:])

            # Try adding each remaining element
            for i in range(index, len(nums)):
                current.append(nums[i])
                backtrack(i + 1)
                current.pop()

        backtrack(0)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.subsets([1,2,3])
    expected1 = [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    assert sorted([sorted(x) for x in result1]) == sorted([sorted(x) for x in expected1])

    # Test case 2
    result2 = sol.subsets([0])
    expected2 = [[],[0]]
    assert sorted([sorted(x) for x in result2]) == sorted([sorted(x) for x in expected2])

    # Test case 3
    result3 = sol.subsets([1,2])
    expected3 = [[],[1],[2],[1,2]]
    assert sorted([sorted(x) for x in result3]) == sorted([sorted(x) for x in expected3])

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
