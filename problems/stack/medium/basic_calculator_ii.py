"""
PROBLEM: Basic Calculator II (LeetCode 227)
Difficulty: Medium
Pattern: Stack, String Parsing
Companies: Meta, Amazon, Google, Microsoft, Apple

DESCRIPTION:
Given a string s which represents an expression, evaluate this expression and
return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate
results will be in the range of [-2^31, 2^31 - 1].

Note: You are not allowed to use any built-in function which evaluates strings
as mathematical expressions, such as eval().

EXAMPLES:
Example 1:
Input: s = "3+2*2"
Output: 7

Example 2:
Input: s = " 3/2 "
Output: 1

Example 3:
Input: s = " 3+5 / 2 "
Output: 5

CONSTRAINTS:
- 1 <= s.length <= 3 * 10^5
- s consists of integers and operators ('+', '-', '*', '/') separated by spaces
- s represents a valid expression
- All intermediate results will be in the range of [-2^31, 2^31 - 1]
- The division operator '/' represents integer division truncating toward zero

APPROACH:
Use a stack to handle operator precedence:
1. Iterate through string building numbers
2. When we hit an operator or end of string:
   - For '+': push number to stack
   - For '-': push negative number to stack
   - For '*': pop from stack, multiply, push back
   - For '/': pop from stack, divide (truncate toward zero), push back
3. Sum all numbers in stack for final result

TIME COMPLEXITY: O(n) where n is length of string
- Single pass through string + O(n) to sum stack

SPACE COMPLEXITY: O(n)
- Stack stores up to n/2 numbers

WHY THIS PROBLEM IS IMPORTANT:
- Extremely frequently asked at FAANG (top 20 most common)
- Tests operator precedence handling without parentheses
- More common than Basic Calculator I in real interviews
- Foundation for more complex parsing problems
"""


class Solution:
    def calculate(self, s: str) -> int:
        """
        Evaluate arithmetic expression with +, -, *, /.
        Handle operator precedence using a stack.
        """
        if not s:
            return 0

        stack = []
        num = 0
        operator = '+'  # Initialize with '+' for first number

        for i, char in enumerate(s):
            if char.isdigit():
                # Build multi-digit numbers
                num = num * 10 + int(char)

            # Process when we hit an operator or reach end of string
            # (char != ' ') handles trailing spaces
            if char in '+-*/' or i == len(s) - 1:
                if char == ' ' and i != len(s) - 1:
                    continue

                if operator == '+':
                    stack.append(num)
                elif operator == '-':
                    stack.append(-num)
                elif operator == '*':
                    stack.append(stack.pop() * num)
                elif operator == '/':
                    # Python division truncates toward negative infinity
                    # We need truncation toward zero for this problem
                    stack.append(int(stack.pop() / num))

                # Update operator and reset number (if not at end)
                if i != len(s) - 1:
                    operator = char
                    num = 0

        # Sum all values in stack
        return sum(stack)


class SolutionNoStack:
    """
    Alternative O(1) space solution without using stack.
    """

    def calculate(self, s: str) -> int:
        """
        Evaluate expression with O(1) space by tracking last result.
        """
        if not s:
            return 0

        result = 0
        num = 0
        last_num = 0
        operator = '+'

        for i, char in enumerate(s):
            if char.isdigit():
                num = num * 10 + int(char)

            if char in '+-*/' or i == len(s) - 1:
                if char == ' ' and i != len(s) - 1:
                    continue

                if operator == '+':
                    result += last_num
                    last_num = num
                elif operator == '-':
                    result += last_num
                    last_num = -num
                elif operator == '*':
                    last_num = last_num * num
                elif operator == '/':
                    last_num = int(last_num / num)

                if i != len(s) - 1:
                    operator = char
                    num = 0

        result += last_num
        return result


def test_basic_calculator_ii():
    """Test cases for Basic Calculator II"""
    solution = Solution()
    solution_no_stack = SolutionNoStack()

    test_cases = [
        ("3+2*2", 7),
        (" 3/2 ", 1),
        (" 3+5 / 2 ", 5),
        ("42", 42),
        ("1-1+1", 1),
        ("2*3*4", 24),
        ("100/2*3", 150),
        ("14-3/2", 13),
        ("0-2147483647", -2147483647),
        ("1+2*5/3+6/4*2", 6),
        ("  1  + 2  * 3  ", 7),
    ]

    for expression, expected in test_cases:
        assert solution.calculate(expression) == expected, f"Failed on {expression}"
        assert (
            solution_no_stack.calculate(expression) == expected
        ), f"Failed on {expression} (no stack)"

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_basic_calculator_ii()
