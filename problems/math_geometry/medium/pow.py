"""
PROBLEM: Pow(x, n) (LeetCode 50)
Difficulty: Medium
Pattern: Math, Recursion, Binary Exponentiation
Companies: Amazon, Apple, Bloomberg, Facebook, Google, Microsoft

Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).

Example 1:
    Input: x = 2.00000, n = 10
    Output: 1024.00000

Example 2:
    Input: x = 2.10000, n = 3
    Output: 9.26100

Example 3:
    Input: x = 2.00000, n = -2
    Output: 0.25000
    Explanation: 2^-2 = 1/2^2 = 1/4 = 0.25

Constraints:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1
- -10^4 <= x^n <= 10^4

Approach:
1. Use binary exponentiation (fast exponentiation)
2. Convert exponent to binary representation
3. For each bit, square the result and multiply when bit is 1
4. Handle negative exponents by using 1/x and positive exponent
5. Handle special cases (x=1, n=0, n=INT_MIN)

Time: O(log n) - binary exponentiation
Space: O(log n) - recursion stack depth
"""


class Solution:
    def my_pow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0

        # Handle negative exponent
        if n < 0:
            x = 1 / x
            n = -n

        return self._pow_helper(x, n)

    def _pow_helper(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0

        if n == 1:
            return x

        # Use binary exponentiation
        half = self._pow_helper(x, n // 2)

        if n % 2 == 0:
            return half * half
        else:
            return half * half * x


# Tests
def test():
    sol = Solution()

    # Test 1
    result1 = sol.my_pow(2.0, 10)
    assert abs(result1 - 1024.0) < 1e-6

    # Test 2
    result2 = sol.my_pow(2.1, 3)
    assert abs(result2 - 9.261) < 1e-6

    # Test 3
    result3 = sol.my_pow(2.0, -2)
    assert abs(result3 - 0.25) < 1e-6

    # Test 4
    result4 = sol.my_pow(1.0, 2147483647)
    assert abs(result4 - 1.0) < 1e-6

    # Test 5
    result5 = sol.my_pow(2.0, 0)
    assert abs(result5 - 1.0) < 1e-6

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
