"""
PROBLEM: Generate Parentheses (LeetCode 22)
LeetCode: https://leetcode.com/problems/generate-parentheses/
Difficulty: Medium
Pattern: Stack, Backtracking
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg

Given n pairs of parentheses, write a function to generate all combinations of
well-formed parentheses.

Example 1:
    Input: n = 3
    Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
    Input: n = 1
    Output: ["()"]

Example 3:
    Input: n = 2
    Output: ["(())","()()"]

Constraints:
- 1 <= n <= 8

Approach (Backtracking):
1. Use backtracking to build valid combinations
2. Track count of open and close parentheses used
3. Rules:
   - Can add '(' if open_count < n
   - Can add ')' if close_count < open_count
4. Add to result when both counts equal n

Time: O(4^n / sqrt(n)) - Catalan number
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def generate_parenthesis(self, n: int) -> List[str]:
        result = []

        def backtrack(current: str, open_count: int, close_count: int):
            # Base case: valid combination completed
            if len(current) == 2 * n:
                result.append(current)
                return

            # Add opening parenthesis if we can
            if open_count < n:
                backtrack(current + '(', open_count + 1, close_count)

            # Add closing parenthesis if valid
            if close_count < open_count:
                backtrack(current + ')', open_count, close_count + 1)

        backtrack('', 0, 0)
        return result


# Tests
def test():
    sol = Solution()

    result1 = sol.generate_parenthesis(3)
    expected1 = ["((()))","(()())","(())()","()(())","()()()"]
    assert sorted(result1) == sorted(expected1)

    result2 = sol.generate_parenthesis(1)
    expected2 = ["()"]
    assert sorted(result2) == sorted(expected2)

    result3 = sol.generate_parenthesis(2)
    expected3 = ["(())","()()"]
    assert sorted(result3) == sorted(expected3)

    # Test n=4
    result4 = sol.generate_parenthesis(4)
    assert len(result4) == 14  # Catalan number for n=4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
