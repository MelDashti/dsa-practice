"""
PROBLEM: Combination Sum (LeetCode 39)
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Facebook, Microsoft, Apple, Google

Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen
numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times.
Two combinations are unique if the frequency of at least one of the chosen
numbers is different.

Example 1:
    Input: candidates = [2,3,6,7], target = 7
    Output: [[2,2,3],[7]]
    Explanation:
    2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
    7 is a candidate, and 7 = 7.

Example 2:
    Input: candidates = [2,3,5], target = 8
    Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
    Input: candidates = [2], target = 1
    Output: []

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40

Approach:
1. Use backtracking to explore all possible combinations
2. For each candidate, we can either use it again or move to next candidate
3. Keep track of current combination and remaining sum
4. Base case: if remaining sum is 0, add current combination to result
5. If remaining sum < 0, backtrack
6. To avoid duplicates, only consider candidates from current index onwards

Time: O(n^(t/m)) where n is number of candidates, t is target, m is minimal candidate
Space: O(t/m) - recursion depth
"""

from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        current = []

        def backtrack(index, remaining):
            # Base case: found valid combination
            if remaining == 0:
                result.append(current[:])
                return

            # Base case: exceeded target
            if remaining < 0:
                return

            # Try each candidate from current index
            for i in range(index, len(candidates)):
                current.append(candidates[i])
                # Can reuse same candidate, so pass i (not i+1)
                backtrack(i, remaining - candidates[i])
                current.pop()

        backtrack(0, target)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.combinationSum([2,3,6,7], 7)
    expected1 = [[2,2,3],[7]]
    assert sorted([sorted(x) for x in result1]) == sorted([sorted(x) for x in expected1])

    # Test case 2
    result2 = sol.combinationSum([2,3,5], 8)
    expected2 = [[2,2,2,2],[2,3,3],[3,5]]
    assert sorted([sorted(x) for x in result2]) == sorted([sorted(x) for x in expected2])

    # Test case 3
    result3 = sol.combinationSum([2], 1)
    assert result3 == []

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
