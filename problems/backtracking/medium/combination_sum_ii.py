"""
PROBLEM: Combination Sum II (LeetCode 40)
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Microsoft, Facebook, Apple, Google

Given a collection of candidate numbers (candidates) and a target number
(target), find all unique combinations in candidates where the candidate
numbers sum to target.

Each number in candidates may only be used once in the combination.

Note: The solution set must not contain duplicate combinations.

Example 1:
    Input: candidates = [10,1,2,7,6,1,5], target = 8
    Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

Example 2:
    Input: candidates = [2,5,2,1,2], target = 5
    Output: [[1,2,2],[5]]

Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30

Approach:
1. Sort the array to handle duplicates
2. Use backtracking to explore combinations
3. Each element can only be used once, so pass i+1 to next recursion
4. Skip duplicate elements at same recursion level to avoid duplicate combinations
5. If remaining sum is 0, add current combination to result
6. If remaining sum < 0 or exceeded array, backtrack

Time: O(2^n) - each element can be included or excluded
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def combination_sum2(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        current = []
        candidates.sort()  # Sort to handle duplicates

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
                # Skip duplicates at same level
                if i > index and candidates[i] == candidates[i-1]:
                    continue

                # Early termination: if current candidate exceeds remaining, stop
                if candidates[i] > remaining:
                    break

                current.append(candidates[i])
                # Each number used only once, so pass i+1
                backtrack(i + 1, remaining - candidates[i])
                current.pop()

        backtrack(0, target)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.combination_sum2([10,1,2,7,6,1,5], 8)
    expected1 = [[1,1,6],[1,2,5],[1,7],[2,6]]
    assert sorted([sorted(x) for x in result1]) == sorted([sorted(x) for x in expected1])

    # Test case 2
    result2 = sol.combination_sum2([2,5,2,1,2], 5)
    expected2 = [[1,2,2],[5]]
    assert sorted([sorted(x) for x in result2]) == sorted([sorted(x) for x in expected2])

    # Test case 3
    result3 = sol.combination_sum2([1], 1)
    expected3 = [[1]]
    assert result3 == expected3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
