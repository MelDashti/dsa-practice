"""
PROBLEM: Evaluate Reverse Polish Notation (LeetCode 150)
Difficulty: Medium
Pattern: Stack
Companies: Amazon, Facebook, Bloomberg, LinkedIn, Google

You are given an array of strings tokens that represents an arithmetic expression
in Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:
- The valid operators are '+', '-', '*', and '/'.
- Each operand may be an integer or another expression.
- The division between two integers always truncates toward zero.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in reverse polish notation.
- The answer and all intermediate calculations can be represented in a 32-bit integer.

Example 1:
    Input: tokens = ["2","1","+","3","*"]
    Output: 9
    Explanation: ((2 + 1) * 3) = 9

Example 2:
    Input: tokens = ["4","13","5","/","+"]
    Output: 6
    Explanation: (4 + (13 / 5)) = 6

Example 3:
    Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
    Output: 22
    Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5 = 22

Constraints:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200]

Approach:
1. Use a stack to store numbers
2. For each token:
   - If number: push to stack
   - If operator: pop two numbers, apply operation, push result
3. Return the final value in stack

Time: O(n) - single pass through tokens
Space: O(n) - stack storage
"""

from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        operators = {'+', '-', '*', '/'}

        for token in tokens:
            if token not in operators:
                # It's a number
                stack.append(int(token))
            else:
                # It's an operator - pop two operands
                b = stack.pop()
                a = stack.pop()

                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    # Truncate toward zero
                    stack.append(int(a / b))

        return stack[0]


# Tests
def test():
    sol = Solution()

    assert sol.evalRPN(["2","1","+","3","*"]) == 9
    assert sol.evalRPN(["4","13","5","/","+"]) == 6
    assert sol.evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"]) == 22
    assert sol.evalRPN(["3","11","+","5","-"]) == 9
    assert sol.evalRPN(["18"]) == 18

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
