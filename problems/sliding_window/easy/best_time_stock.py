"""
PROBLEM: Best Time to Buy and Sell Stock (LeetCode 121)
Difficulty: Easy
Pattern: Sliding Window, Dynamic Programming
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing
a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve
any profit, return 0.

Example 1:
    Input: prices = [7,1,5,3,6,4]
    Output: 5
    Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5

Example 2:
    Input: prices = [7,6,4,3,1]
    Output: 0
    Explanation: No profitable transaction possible

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4

Approach:
1. Track minimum price seen so far
2. For each price, calculate profit if sold at current price
3. Update max profit

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def max_profit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            # Update minimum price
            min_price = min(min_price, price)

            # Calculate profit if selling at current price
            profit = price - min_price

            # Update maximum profit
            max_profit = max(max_profit, profit)

        return max_profit


# Tests
def test():
    sol = Solution()

    assert sol.max_profit([7,1,5,3,6,4]) == 5
    assert sol.max_profit([7,6,4,3,1]) == 0
    assert sol.max_profit([1,2]) == 1
    assert sol.max_profit([2,4,1]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
