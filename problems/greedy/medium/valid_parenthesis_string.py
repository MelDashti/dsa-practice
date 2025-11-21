"""
PROBLEM: Valid Parenthesis String (LeetCode 678)
Difficulty: Medium
Pattern: Greedy, Stack, Dynamic Programming
Companies: Google, Meta, Amazon, Apple, Microsoft

Given a string s containing only three types of characters: '(', ')' and '*', return true if
s is a valid string.

In a valid string:
- Any left parenthesis '(' must have a corresponding right parenthesis ')'.
- Any right parenthesis ')' must have a corresponding left parenthesis '('.
- '*' could be treated as a single right parenthesis ')' or a single left parenthesis '('
  or an empty string.
- An empty string is also valid.

Example 1:
    Input: s = "()"
    Output: true

Example 2:
    Input: s = "(*)"
    Output: true

Example 3:
    Input: s = "(*))"
    Output: true

Constraints:
- 1 <= s.length <= 10^4
- s[i] is '(', ')' or '*'

Approach (Greedy - Two Pass):
1. Forward pass: check that we never have more ')' than '(' + '*'
2. Backward pass: check that we never have more '(' than ')' + '*'
3. This ensures proper pairing is possible

Alternative Greedy Approach (Min/Max):
- Track min and max possible open parentheses
- '*' can be '(' (increase max) or ')' (decrease min) or empty (no change)
- If max ever becomes negative, too many closing parens
- If min becomes negative, reset to 0 (treat '*' as empty or '(')

Time: O(n) - single or double pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def check_valid_string(self, s: str) -> bool:
        """
        Check if string with wildcards is valid parenthesis string.

        Strategy (Min/Max approach):
        - Track minimum and maximum possible open parentheses count
        - For '(': both min and max increase
        - For ')': both min and max decrease
        - For '*': min decreases (treated as ')'), max increases (treated as '(')
        - If max < 0, too many ')' without hope
        - If min < 0, reset to 0 (treat '*' as empty string)
        - At end, min must be 0 (all '(' matched)
        """
        min_open = 0  # minimum possible open parentheses
        max_open = 0  # maximum possible open parentheses

        for char in s:
            if char == '(':
                min_open += 1
                max_open += 1
            elif char == ')':
                min_open -= 1
                max_open -= 1
            else:  # char == '*'
                min_open -= 1  # treat '*' as ')'
                max_open += 1  # treat '*' as '('

            # Too many ')' - no way to balance
            if max_open < 0:
                return False

            # If min becomes negative, reset to 0
            # This means we treat extra '*' as empty strings
            if min_open < 0:
                min_open = 0

        # At the end, minimum open parentheses should be 0 (all matched)
        return min_open == 0


# Tests
def test():
    sol = Solution()

    assert sol.check_valid_string("()") == True
    assert sol.check_valid_string("(*)") == True
    assert sol.check_valid_string("(*))")== True
    assert sol.check_valid_string("(") == False
    assert sol.check_valid_string("*)") == True
    assert sol.check_valid_string("(*)") == True
    assert sol.check_valid_string("(((") == False
    assert sol.check_valid_string("()()") == True
    assert sol.check_valid_string("(*())") == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
