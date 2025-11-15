"""
PROBLEM: Basic Calculator (LeetCode 224)
Difficulty: Hard
Pattern: Stack, String Parsing
Companies: Meta, Google, Amazon, Apple, Microsoft

DESCRIPTION:
Given a string s representing a valid expression, implement a basic calculator to
evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as
mathematical expressions, such as eval().

EXAMPLES:
Example 1:
Input: s = "1 + 1"
Output: 2

Example 2:
Input: s = " 2-1 + 2 "
Output: 3

Example 3:
Input: s = "(1+(4+5+2)-3)+(6+8)"
Output: 23

CONSTRAINTS:
- 1 <= s.length <= 3 * 10^5
- s consists of digits, '+', '-', '(', ')', and ' '
- s represents a valid expression
- '+' is not used as a unary operation
- '-' could be used as a unary operation and in this case won't be adjacent to other operators
- There will be no two consecutive operators in the input
- Every number and running calculation will fit in a signed 32-bit integer

APPROACH:
Use a stack to handle parentheses and track signs:
1. Maintain current number, result, and sign
2. Use stack to save state when entering parentheses
3. When encountering '(', push current result and sign to stack
4. When encountering ')', pop from stack and apply saved state
5. Process digits to form numbers, apply operations with signs

TIME COMPLEXITY: O(n) where n is length of string
- Single pass through the string

SPACE COMPLEXITY: O(n)
- Stack can store up to O(n) elements in worst case (nested parentheses)

WHY THIS PROBLEM IS IMPORTANT:
- Classic stack problem for expression evaluation
- Very frequently asked at Meta and Google
- Tests string parsing and state management
- Foundation for calculator problems (I, II, III)
- Real-world application in compilers and interpreters
"""


class Solution:
    def calculate(self, s: str) -> int:
        """
        Evaluate arithmetic expression with +, -, and parentheses.
        """
        stack = []
        result = 0
        number = 0
        sign = 1  # 1 for positive, -1 for negative

        for char in s:
            if char.isdigit():
                # Build the current number (handle multi-digit numbers)
                number = number * 10 + int(char)

            elif char == '+':
                # Add previous number to result with its sign
                result += sign * number
                number = 0
                sign = 1  # Next number is positive

            elif char == '-':
                # Add previous number to result with its sign
                result += sign * number
                number = 0
                sign = -1  # Next number is negative

            elif char == '(':
                # Save current state before entering parentheses
                stack.append(result)
                stack.append(sign)

                # Reset for new sub-expression
                result = 0
                sign = 1

            elif char == ')':
                # Complete the current sub-expression
                result += sign * number
                number = 0

                # Pop the sign before the parentheses
                result *= stack.pop()

                # Pop the result before the parentheses and add
                result += stack.pop()

        # Add the last number (if any)
        result += sign * number

        return result


def test_basic_calculator():
    """Test cases for Basic Calculator"""
    solution = Solution()

    # Test case 1: Simple addition
    assert solution.calculate("1 + 1") == 2

    # Test case 2: Mixed operations
    assert solution.calculate(" 2-1 + 2 ") == 3

    # Test case 3: With parentheses
    assert solution.calculate("(1+(4+5+2)-3)+(6+8)") == 23

    # Test case 4: Nested parentheses
    assert solution.calculate("((1+2)+(3+4))") == 10

    # Test case 5: Negative numbers
    assert solution.calculate("2-(5-6)") == 3

    # Test case 6: Complex nested
    assert solution.calculate("1-(5)") == -4
    assert solution.calculate("1-(-2)") == 3

    # Test case 7: Multiple digits
    assert solution.calculate("123") == 123
    assert solution.calculate("12+34") == 46

    # Test case 8: Spaces
    assert solution.calculate("   123   ") == 123

    # Test case 9: Complex expression
    assert solution.calculate("(7)-(0)+(4)") == 11
    assert solution.calculate("2-(1-2)") == 3

    # Test case 10: Deep nesting
    assert solution.calculate("1+(2+(3+(4+5)))") == 15

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_basic_calculator()
