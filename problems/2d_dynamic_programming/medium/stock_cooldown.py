"""
PROBLEM: Best Time to Buy and Sell Stock with Cooldown (LeetCode 309)
Difficulty: Medium
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

You are given an array prices where prices[i] is the price of a given stock on
the ith day.

Find the maximum profit you can achieve. You may complete as many transactions
as you like (i.e., buy one and sell one share of the stock multiple times) with
the following restrictions:

- After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously (i.e., you must
sell the stock before you buy again).

Example 1:
    Input: prices = [1,2,3,0,2]
    Output: 3
    Explanation: transactions = [buy, sell, cooldown, buy, sell]

Example 2:
    Input: prices = [1]
    Output: 0

Constraints:
- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000

Approach:
1. Use state machine with 3 states: can buy, can sell (holding), cooldown
2. Track max profit at each state for each day
3. Transitions:
   - buy[i] = max(buy[i-1], cooldown[i-1] - prices[i])
   - sell[i] = max(sell[i-1], buy[i-1] + prices[i])
   - cooldown[i] = max(cooldown[i-1], sell[i-1])
4. Can optimize space by only keeping previous state

Time: O(n) - single pass through prices
Space: O(1) - only store constant state variables
"""

from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices or len(prices) < 2:
            return 0

        # State variables
        # sold: max profit if we just sold
        # held: max profit if we're holding stock
        # reset: max profit if we're in cooldown/reset state
        sold = 0
        held = -prices[0]
        reset = 0

        for i in range(1, len(prices)):
            prev_sold = sold
            prev_held = held
            prev_reset = reset

            # If we sell today, we must have held stock yesterday
            sold = prev_held + prices[i]

            # If we hold today, either we held yesterday or we buy today (from reset)
            held = max(prev_held, prev_reset - prices[i])

            # If we reset today, either we reset yesterday or we sold yesterday
            reset = max(prev_reset, prev_sold)

        # Maximum profit is either in sold or reset state
        return max(sold, reset)


# Tests
def test():
    sol = Solution()

    assert sol.maxProfit([1,2,3,0,2]) == 3
    assert sol.maxProfit([1]) == 0
    assert sol.maxProfit([1,2]) == 1
    assert sol.maxProfit([2,1]) == 0
    assert sol.maxProfit([1,2,3,4,5]) == 4
    assert sol.maxProfit([5,4,3,2,1]) == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
