"""
PROBLEM: Climbing Stairs (LeetCode 70)
Difficulty: Easy
Pattern: 1-D Dynamic Programming
Companies: Amazon, Google, Adobe, Apple, Microsoft

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you
climb to the top?

Example 1:
    Input: n = 2
    Output: 2
    Explanation: There are two ways to climb to the top:
    1. 1 step + 1 step
    2. 2 steps

Example 2:
    Input: n = 3
    Output: 3
    Explanation: There are three ways to climb to the top:
    1. 1 step + 1 step + 1 step
    2. 1 step + 2 steps
    3. 2 steps + 1 step

Constraints:
- 1 <= n <= 45

Approach:
1. This is a Fibonacci sequence problem
2. To reach step n, we can come from step n-1 or n-2
3. So ways(n) = ways(n-1) + ways(n-2)
4. Base cases: ways(1) = 1, ways(2) = 2
5. Use dynamic programming to avoid redundant calculations
6. Can optimize space by only storing last two values

Time: O(n) - single pass through n steps
Space: O(1) - only store two variables
"""


class Solution:
    def climb_stairs(self, n: int) -> int:
        if n <= 2:
            return n

        # Initialize for first two steps
        prev2 = 1  # ways to reach step 1
        prev1 = 2  # ways to reach step 2

        # Calculate for steps 3 to n
        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2 = prev1
            prev1 = current

        return prev1


# Tests
def test():
    sol = Solution()

    assert sol.climb_stairs(2) == 2
    assert sol.climb_stairs(3) == 3
    assert sol.climb_stairs(4) == 5
    assert sol.climb_stairs(5) == 8
    assert sol.climb_stairs(1) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
