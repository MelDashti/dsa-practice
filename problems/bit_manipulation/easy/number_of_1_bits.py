"""
PROBLEM: Number of 1 Bits (LeetCode 191)
LeetCode: https://leetcode.com/problems/number-of-1-bits/
Difficulty: Easy
Pattern: Bit Manipulation
Companies: Apple, Amazon, Adobe

Write a function that takes an unsigned integer and returns the number of '1' bits
it has (also known as the Hamming weight).

Example 1:
    Input: n = 11
    Output: 3
    Explanation: The input binary string is "1011", which has three '1' bits

Example 2:
    Input: n = 128
    Output: 1
    Explanation: The input binary string is "10000000", which has one '1' bit

Example 3:
    Input: n = 2147483645
    Output: 30

Constraints:
- The input must be a binary string of length 32

Approach:
Method 1 - Bitwise AND with right shift:
1. Check if the rightmost bit is 1 using n & 1
2. Right shift n to check next bit
3. Repeat 32 times

Method 2 - Brian Kernighan's Algorithm (Optimal):
- Use n & (n - 1) which removes the rightmost 1 bit
- Continue until n becomes 0
- Count iterations

Time: O(k) where k is the number of 1 bits (Kernighan) or O(1) since 32 bits (if using shift)
Space: O(1) - constant space
"""


class Solution:
    def hamming_weight(self, n: int) -> int:
        """
        Count the number of 1 bits using Brian Kernighan's algorithm.

        Key insight: n & (n - 1) removes the rightmost 1 bit
        Example: 1011 & 1010 = 1010 (removed rightmost 1)
        """
        count = 0
        while n:
            n &= n - 1  # Remove the rightmost 1 bit
            count += 1
        return count

    def hammingWeight_shift(self, n: int) -> int:
        """
        Count the number of 1 bits by checking each bit position.
        """
        count = 0
        while n:
            count += n & 1  # Check if rightmost bit is 1
            n >>= 1  # Right shift by 1
        return count


# Tests
def test():
    sol = Solution()

    # Test with both methods
    assert sol.hamming_weight(11) == 3  # "1011" has 3 ones
    assert sol.hamming_weight(128) == 1  # "10000000" has 1 one
    assert sol.hamming_weight(2147483645) == 30
    assert sol.hamming_weight(0) == 0
    assert sol.hamming_weight(1) == 1
    assert sol.hamming_weight(3) == 2  # "11"
    assert sol.hamming_weight(7) == 3  # "111"

    assert sol.hammingWeight_shift(11) == 3
    assert sol.hammingWeight_shift(128) == 1
    assert sol.hammingWeight_shift(0) == 0
    assert sol.hammingWeight_shift(7) == 3

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
