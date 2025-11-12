"""
PROBLEM: Coin Change II (LeetCode 518)
Difficulty: Medium
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

You are given an integer array coins representing coins of different denominations
and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of
money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.

Example 1:
    Input: amount = 5, coins = [1,2,5]
    Output: 4
    Explanation: there are four ways to make up the amount:
    5=5
    5=2+2+1
    5=2+1+1+1
    5=1+1+1+1+1

Example 2:
    Input: amount = 3, coins = [2]
    Output: 0
    Explanation: the amount of 3 cannot be made up just with coins of 2.

Example 3:
    Input: amount = 10, coins = [10]
    Output: 1

Constraints:
- 1 <= coins.length <= 300
- 1 <= coins[i] <= 5000
- All the values of coins are unique.
- 0 <= amount <= 5000

Approach:
1. Use 2D DP where dp[i][j] = number of ways to make amount j using first i coins
2. Base case: dp[i][0] = 1 (one way to make 0: use no coins)
3. For each coin, for each amount:
   - Don't use coin: dp[i][j] = dp[i-1][j]
   - Use coin (if possible): dp[i][j] += dp[i][j-coin]
4. Can optimize to 1D array

Time: O(n * amount) - where n is number of coins
Space: O(amount) - 1D DP array
"""

from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        # dp[i] represents number of ways to make amount i
        dp = [0] * (amount + 1)
        dp[0] = 1  # One way to make 0: use no coins

        # For each coin
        for coin in coins:
            # Update all amounts that can include this coin
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]

        return dp[amount]


# Tests
def test():
    sol = Solution()

    assert sol.change(5, [1,2,5]) == 4
    assert sol.change(3, [2]) == 0
    assert sol.change(10, [10]) == 1
    assert sol.change(0, [1]) == 1
    assert sol.change(4, [1,2,3]) == 4
    assert sol.change(500, [3,5,7,8,9,10,11]) == 35502874

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
