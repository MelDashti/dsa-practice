"""
PROBLEM: Reverse Bits (LeetCode 190)
LeetCode: https://leetcode.com/problems/reverse-bits/
Difficulty: Easy
Pattern: Bit Manipulation
Companies: Adobe, Apple, Google

Reverse bits of a given 32-bit unsigned integer.

Note: Note that in some languages such as Java, there is no unsigned integer type.
In this case, the input and output both will be given as a signed integer type.
They should not affect your implementation, as the integer's internal binary
representation is the same, whether it is signed or unsigned.

Example 1:
    Input: n = 00000010100101000001111010011100
    Output:    00111001011110000101010100000010
    Explanation: The input binary string 00000010100101000001111010011100
    represents the unsigned integer 43261596, so return 964176192
    which its binary representation is 00111001011110000101010100000010

Example 2:
    Input: n = 11111111111111111111111111111101
    Output:    10111111111111111111111111111111
    Explanation: The input binary string 11111111111111111111111111111101
    represents the unsigned integer 4294967293, so return 3221225471
    which its binary representation is 10111111111111111111111111111111

Constraints:
- The input must be a binary string of length 32

Approach:
Method 1 - Bit by bit reversal:
1. Extract each bit from the input (using & and >>)
2. Add it to the result (using << and |)
3. Repeat for all 32 bits

Method 2 - Using built-in bin() and string manipulation:
1. Convert to binary, reverse, and convert back

Time: O(1) - always 32 bits
Space: O(1) - constant space
"""


class Solution:
    def reverse_bits(self, n: int) -> int:
        """
        Reverse bits by iterating through all 32 bits.

        For each bit from right to left in n:
        1. Extract the bit with n & 1
        2. Add it to result at the left side
        """
        result = 0

        for i in range(32):
            # Get the rightmost bit of n
            bit = n & 1

            # Shift result left and add the bit to the rightmost position
            result = (result << 1) | bit

            # Remove the rightmost bit from n
            n >>= 1

        return result

    def reverseBits_builtin(self, n: int) -> int:
        """
        Reverse bits using Python's bin() and string operations.
        """
        # Convert to binary (without '0b' prefix), pad to 32 bits, reverse, convert back
        return int(bin(n)[2:].zfill(32)[::-1], 2)


# Tests
def test():
    sol = Solution()

    # Test 1: 43261596 -> 964176192
    assert sol.reverse_bits(43261596) == 964176192

    # Test 2: 4294967293 -> 3221225471
    assert sol.reverse_bits(4294967293) == 3221225471

    # Simple test cases
    assert sol.reverse_bits(0) == 0
    assert sol.reverse_bits(1) == 2147483648  # 1 << 31
    assert sol.reverse_bits(2) == 1073741824  # 2 << 30

    # Test alternative method
    assert sol.reverseBits_builtin(43261596) == 964176192
    assert sol.reverseBits_builtin(1) == 2147483648

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
