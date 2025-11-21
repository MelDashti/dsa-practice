"""
PROBLEM: Min Cost Climbing Stairs (LeetCode 746)
LeetCode: https://leetcode.com/problems/min-cost-climbing-stairs/
Difficulty: Easy
Pattern: 1-D Dynamic Programming
Companies: Amazon, Google, Apple, Microsoft, Facebook

You are given an integer array cost where cost[i] is the cost of ith step on a
staircase. Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.

Example 1:
    Input: cost = [10,15,20]
    Output: 15
    Explanation: You will start at index 1:
    - Pay 15 and climb two steps to reach the top.
    The total cost is 15.

Example 2:
    Input: cost = [1,100,1,1,1,100,1,1,1,1]
    Output: 6
    Explanation: You will start at index 0:
    - Pay 1 and climb two steps to reach index 2.
    - Pay 1 and climb two steps to reach index 4.
    - Pay 1 and climb two steps to reach index 6.
    - Pay 1 and climb one step to reach index 7.
    - Pay 1 and climb two steps to reach index 9.
    - Pay 1 and climb one step to reach the top.
    The total cost is 6.

Constraints:
- 2 <= cost.length <= 1000
- 0 <= cost[i] <= 999

Approach:
1. Use dynamic programming to find minimum cost to reach each step
2. minCost[i] = cost[i] + min(minCost[i-1], minCost[i-2])
3. Can start from step 0 or step 1
4. Final answer is minimum of last two steps (we can skip the last step)
5. Optimize space by only keeping track of last two values

Time: O(n) - single pass through array
Space: O(1) - only store two variables
"""

from typing import List


class Solution:
    def min_cost_climbing_stairs(self, cost: List[int]) -> int:
        n = len(cost)

        # Start with first two steps
        prev2 = cost[0]
        prev1 = cost[1]

        # Calculate minimum cost for each step
        for i in range(2, n):
            current = cost[i] + min(prev1, prev2)
            prev2 = prev1
            prev1 = current

        # Return minimum of last two steps (can reach top from either)
        return min(prev1, prev2)


# Tests
def test():
    sol = Solution()

    assert sol.min_cost_climbing_stairs([10,15,20]) == 15
    assert sol.min_cost_climbing_stairs([1,100,1,1,1,100,1,1,1,1]) == 5
    assert sol.min_cost_climbing_stairs([0,0,0,1]) == 0
    assert sol.min_cost_climbing_stairs([1,2,3]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
