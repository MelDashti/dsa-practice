"""
PROBLEM: Permutations (LeetCode 46)
LeetCode: https://leetcode.com/problems/permutations/
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Microsoft, Apple, Facebook, Google

Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Example 1:
    Input: nums = [1,2,3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Example 2:
    Input: nums = [0,1]
    Output: [[0,1],[1,0]]

Example 3:
    Input: nums = [1]
    Output: [[1]]

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique

Approach:
1. Use backtracking to generate all permutations
2. At each step, try placing each unused number at current position
3. Mark number as used, recurse, then unmark (backtrack)
4. Base case: when all positions filled, add permutation to result
5. Use a set or boolean array to track which numbers are used

Time: O(n! * n) - n! permutations, each taking O(n) to build
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        current = []
        used = set()

        def backtrack():
            # Base case: permutation is complete
            if len(current) == len(nums):
                result.append(current[:])
                return

            # Try adding each unused number
            for num in nums:
                if num not in used:
                    current.append(num)
                    used.add(num)
                    backtrack()
                    current.pop()
                    used.remove(num)

        backtrack()
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.permute([1,2,3])
    expected1 = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    assert sorted(result1) == sorted(expected1)

    # Test case 2
    result2 = sol.permute([0,1])
    expected2 = [[0,1],[1,0]]
    assert sorted(result2) == sorted(expected2)

    # Test case 3
    result3 = sol.permute([1])
    assert result3 == [[1]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
