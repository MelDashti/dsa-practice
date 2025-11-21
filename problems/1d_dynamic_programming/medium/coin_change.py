"""
PROBLEM: Coin Change (LeetCode 322)
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

You are given an integer array coins representing coins of different
denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that
amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
    Input: coins = [1,2,5], amount = 11
    Output: 3
    Explanation: 11 = 5 + 5 + 1

Example 2:
    Input: coins = [2], amount = 3
    Output: -1

Example 3:
    Input: coins = [1], amount = 0
    Output: 0

Constraints:
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4

Approach:
1. Use dynamic programming with bottom-up approach
2. dp[i] = minimum coins needed to make amount i
3. For each amount, try all coins and take minimum
4. dp[i] = min(dp[i], dp[i - coin] + 1) for all coins
5. Initialize dp array with amount + 1 (impossible value)
6. Base case: dp[0] = 0 (zero coins for zero amount)

Time: O(amount * n) - for each amount, try all coins
Space: O(amount) - dp array
"""

from typing import List


class Solution:
    def coin_change(self, coins: List[int], amount: int) -> int:
        # Initialize dp array with amount + 1 (impossible value)
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0  # Base case: 0 coins for 0 amount

        # For each amount from 1 to target
        for i in range(1, amount + 1):
            # Try each coin
            for coin in coins:
                if coin <= i:
                    # Take minimum of current value or using this coin
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        # If dp[amount] is still impossible value, return -1
        return dp[amount] if dp[amount] != amount + 1 else -1


# Tests
def test():
    sol = Solution()

    assert sol.coin_change([1,2,5], 11) == 3
    assert sol.coin_change([2], 3) == -1
    assert sol.coin_change([1], 0) == 0
    assert sol.coin_change([1], 1) == 1
    assert sol.coin_change([1], 2) == 2
    assert sol.coin_change([1,3,4,5], 7) == 2
    assert sol.coin_change([2,5,10,1], 27) == 4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
