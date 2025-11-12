"""
PROBLEM: Valid Parentheses (LeetCode 20)
Difficulty: Easy
Pattern: Stack
Companies: Amazon, Facebook, Microsoft, Google, Bloomberg

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
    Input: s = "()"
    Output: true

Example 2:
    Input: s = "()[]{}"
    Output: true

Example 3:
    Input: s = "(]"
    Output: false
    Explanation: Opening bracket '(' is closed by ']'

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'

Approach:
1. Use a stack to track opening brackets
2. For each character:
   - If opening bracket: push to stack
   - If closing bracket: check if stack is empty or top doesn't match
3. At the end, stack should be empty (all brackets closed)

Time: O(n) - single pass through string
Space: O(n) - stack storage in worst case
"""


class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}

        for char in s:
            if char in mapping:
                # Closing bracket
                if not stack or stack[-1] != mapping[char]:
                    return False
                stack.pop()
            else:
                # Opening bracket
                stack.append(char)

        return len(stack) == 0


# Tests
def test():
    sol = Solution()

    assert sol.isValid("()") == True
    assert sol.isValid("()[]{}") == True
    assert sol.isValid("(]") == False
    assert sol.isValid("([)]") == False
    assert sol.isValid("{[]}") == True
    assert sol.isValid("") == True
    assert sol.isValid("(") == False
    assert sol.isValid(")") == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
