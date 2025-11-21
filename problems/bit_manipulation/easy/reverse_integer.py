"""
PROBLEM: Reverse Integer (LeetCode 7)
LeetCode: https://leetcode.com/problems/reverse-integer/
Difficulty: Medium
Pattern: Math, Bit Manipulation
Companies: Apple, Amazon, Google, Facebook, Microsoft, Bloomberg

Given a signed 32-bit integer x, return x with its digits reversed.
If reversing x causes the value to go outside the signed 32-bit integer range
[-2^31, 2^31 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers (signed or unsigned).

Example 1:
    Input: x = 123
    Output: 321

Example 2:
    Input: x = -123
    Output: -321

Example 3:
    Input: x = 120
    Output: 21

Example 4:
    Input: x = 0
    Output: 0

Constraints:
- -2^31 <= x <= 2^31 - 1

Approach:
Method 1 - Numeric manipulation:
1. Handle sign separately
2. Extract digits one by one using modulo
3. Build reversed number by multiplying and adding
4. Check for overflow at each step

Method 2 - String manipulation:
1. Convert to string
2. Reverse if positive, reverse and negate if negative
3. Convert back to integer
4. Check for overflow

Overflow handling:
- Check before adding: if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7)
- For negative: similar check with INT_MIN

Time: O(log|x|) - number of digits in x
Space: O(1) - constant space
"""


class Solution:
    def reverse(self, x: int) -> int:
        """
        Reverse integer with overflow checking.

        Process:
        1. Store sign separately
        2. Work with absolute value
        3. Extract last digit using modulo
        4. Build reversed number
        5. Check for overflow before adding each digit
        6. Apply sign back
        """
        INT_MIN = -2**31
        INT_MAX = 2**31 - 1

        result = 0
        num = abs(x)

        while num != 0:
            digit = num % 10
            num //= 10

            # Check for overflow before adding digit
            # If result > INT_MAX // 10, we'll overflow
            # If result == INT_MAX // 10, check if digit will cause overflow
            if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
                return 0

            result = result * 10 + digit

        # Apply original sign
        result = result if x > 0 else -result

        # Final overflow check (should be covered above, but just in case)
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result

    def reverse_string(self, x: int) -> int:
        """
        Reverse integer using string manipulation.
        """
        INT_MIN = -2**31
        INT_MAX = 2**31 - 1

        # Handle sign
        sign = -1 if x < 0 else 1
        x = abs(x)

        # Reverse using string
        reversed_num = int(str(x)[::-1])

        # Apply sign
        result = sign * reversed_num

        # Check overflow
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result


# Tests
def test():
    sol = Solution()

    assert sol.reverse(123) == 321
    assert sol.reverse(-123) == -321
    assert sol.reverse(120) == 21
    assert sol.reverse(0) == 0
    assert sol.reverse(1534236469) == 0  # Overflow case
    assert sol.reverse(1) == 1
    assert sol.reverse(-1) == -1
    assert sol.reverse(100) == 1
    assert sol.reverse(-100) == -1
    assert sol.reverse(2147483647) == 0  # INT_MAX, should overflow

    # Test alternative implementation
    assert sol.reverse_string(123) == 321
    assert sol.reverse_string(-123) == -321
    assert sol.reverse_string(120) == 21
    assert sol.reverse_string(0) == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
