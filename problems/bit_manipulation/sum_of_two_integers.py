"""
PROBLEM: Sum of Two Integers (LeetCode 371)
Difficulty: Medium
Pattern: Bit Manipulation
Companies: Google, Facebook, Apple, Amazon

Given two integers a and b, return their sum without using the operators + and -.

Constraint: Both a and b can be in the range [-2^31, 2^31 - 1] and the result
is guaranteed to fit in a 32-bit signed integer.

Example 1:
    Input: a = 1, b = 2
    Output: 3

Example 2:
    Input: a = 2, b = 3
    Output: 5

Example 3:
    Input: a = -1, b = 1
    Output: 0

Example 4:
    Input: a = -2, b = 3
    Output: 1

Constraints:
- -2^31 <= a, b <= 2^31 - 1
- The result will fit in a 32-bit signed integer

Approach:
Bit manipulation with XOR and AND:
1. XOR (a ^ b) gives sum without carry
2. AND (a & b) gives carry bits
3. Left shift carry by 1 to get actual carry value
4. Repeat until no carry remains

Key operations:
- a ^ b: addition without considering carry
- a & b: produces carry, left shift gives actual carry to add
- Continue until b becomes 0

For negative numbers in Python:
- Use bit mask (0xFFFFFFFF) to handle 32-bit signed integers
- Python's arbitrary precision requires special handling for negative numbers

Time: O(1) - at most 32 iterations for 32-bit integers
Space: O(1) - constant space
"""


class Solution:
    def getSum(self, a: int, b: int) -> int:
        """
        Calculate sum using bit manipulation.

        Process:
        1. Sum without carry: a ^ b
        2. Carry: (a & b) << 1
        3. Repeat until no carry
        4. Handle 32-bit signed integer overflow
        """
        # Define 32-bit mask
        MASK = 0xFFFFFFFF
        INT_MAX = 0x7FFFFFFF  # 2^31 - 1

        while b != 0:
            # Sum without carry
            sum_without_carry = (a ^ b) & MASK

            # Carry
            carry = ((a & b) << 1) & MASK

            a = sum_without_carry
            b = carry

        # Handle negative numbers (convert back from 32-bit unsigned to signed)
        # If the most significant bit is 1, it's negative
        if a > INT_MAX:
            # Convert from 32-bit unsigned to signed
            a = ~(a ^ MASK)

        return a

    def getSum_simple(self, a: int, b: int) -> int:
        """
        Simplified version for understanding the algorithm.
        Note: This doesn't properly handle 32-bit overflow in Python.
        """
        while b != 0:
            carry = (a & b) << 1
            a = a ^ b
            b = carry

        return a


# Tests
def test():
    sol = Solution()

    assert sol.getSum(1, 2) == 3
    assert sol.getSum(2, 3) == 5
    assert sol.getSum(-1, 1) == 0
    assert sol.getSum(-2, 3) == 1
    assert sol.getSum(0, 0) == 0
    assert sol.getSum(1, 1) == 2
    assert sol.getSum(-1, -1) == -2
    assert sol.getSum(5, 7) == 12
    assert sol.getSum(-5, 10) == 5

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
