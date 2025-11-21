"""
PROBLEM: Counting Bits (LeetCode 338)
Difficulty: Easy
Pattern: Bit Manipulation, Dynamic Programming
Companies: Adobe, Google, Facebook, Apple

Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n),
ans[i] is the number of 1's in the binary representation of i.

Example 1:
    Input: n = 5
    Output: [0,1,1,2,1,2]
    Explanation:
    0 --> 0
    1 --> 1
    2 --> 10
    3 --> 11
    4 --> 100
    5 --> 101

Example 2:
    Input: n = 2
    Output: [0,1,1]

Example 3:
    Input: n = 0
    Output: [0]

Constraints:
- 0 <= n <= 10^5

Approach:
Method 1 - Brian Kernighan (remove rightmost 1):
- For each number i, use i & (i - 1) to get the number with rightmost 1 removed
- ans[i] = ans[i & (i-1)] + 1

Method 2 - Right shift (divide by 2):
- For each number i: ans[i] = ans[i >> 1] + (i & 1)
- If i is even (last bit is 0), count of 1s is same as i//2
- If i is odd (last bit is 1), count of 1s is 1 + count of i//2

Method 3 - Most significant bit:
- i & (i - 1) removes the highest set bit
- ans[i] = ans[i & (i-1)] + 1

Time: O(n) - single pass
Space: O(1) - excluding output array
"""

from typing import List


class Solution:
    def count_bits(self, n: int) -> List[int]:
        """
        Count bits using dynamic programming with right shift.

        Logic: i >> 1 removes the last bit
        If i is even: last bit is 0, so count is same as i//2
        If i is odd: last bit is 1, so count is 1 + count of i//2
        """
        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)

        return ans

    def countBits_kernighan(self, n: int) -> List[int]:
        """
        Count bits using Brian Kernighan's approach with DP.

        i & (i - 1) removes the rightmost 1 bit.
        So count of 1s in i = count of 1s in (i & (i-1)) + 1
        """
        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            ans[i] = ans[i & (i - 1)] + 1

        return ans

    def countBits_msb(self, n: int) -> List[int]:
        """
        Count bits using most significant bit approach.
        """
        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            # Remove the highest set bit
            ans[i] = ans[i & (i - 1)] + 1

        return ans


# Tests
def test():
    sol = Solution()

    assert sol.count_bits(5) == [0, 1, 1, 2, 1, 2]
    assert sol.count_bits(2) == [0, 1, 1]
    assert sol.count_bits(0) == [0]
    assert sol.count_bits(1) == [0, 1]
    assert sol.count_bits(3) == [0, 1, 1, 2]

    # Test alternative implementations
    assert sol.countBits_kernighan(5) == [0, 1, 1, 2, 1, 2]
    assert sol.countBits_kernighan(2) == [0, 1, 1]

    assert sol.countBits_msb(5) == [0, 1, 1, 2, 1, 2]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
