"""
PROBLEM: Gas Station (LeetCode 134)
Difficulty: Medium
Pattern: Greedy
Companies: Google, Meta, Amazon, Uber

There are n gas stations along a circular route, where the amount of gas at the ith
station is gas[i], and the cost of traveling from station i to station (i + 1) is cost[i].

You have an empty tank at the start, and you can travel from a station to its next station
if you have enough gas. Return the starting station's index if you can travel around the
circuit once in the clockwise direction, or -1 if you cannot.

Example 1:
    Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
    Output: 3
    Explanation: Start at station 3 (index 3) and collect 4 unit of gas.
                 Your tank = 0 + 4 = 4
                 Travel to station 4. Your tank = 4 - 1 + 5 = 8
                 Travel to station 0. Your tank = 8 - 2 + 1 = 7
                 Travel to station 1. Your tank = 7 - 3 + 2 = 6
                 Travel to station 2. Your tank = 6 - 4 + 3 = 5
                 Travel to station 3. The cost is 5. Your tank = 5 - 5 + 4 = 4

Example 2:
    Input: gas = [2,3,4], cost = [3,4,3]
    Output: -1

Constraints:
- n == gas.length == cost.length
- 1 <= n <= 10^5
- 0 <= gas[i], cost[i] <= 10^4

Approach (Greedy):
1. If total gas < total cost, impossible to complete circuit
2. Track current tank and reset if it goes negative
3. When tank goes negative, the next station is a better start
4. Greedy choice: if we fail at station i, stations 0 to i can't be the start

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def can_complete_circuit(self, gas: List[int], cost: List[int]) -> int:
        """
        Find starting gas station index to complete circuit.

        Strategy:
        - First check if solution exists (total_gas >= total_cost)
        - Use greedy approach: if at station i we can't proceed,
          start must be after i (stations before i won't work either)
        """
        # If total gas is less than total cost, impossible
        if sum(gas) < sum(cost):
            return -1

        total_tank = 0
        start_station = 0

        for i in range(len(gas)):
            # Add gas and subtract cost
            total_tank += gas[i] - cost[i]

            # If tank goes negative, can't start from any station <= i
            # Try starting from next station
            if total_tank < 0:
                start_station = i + 1
                total_tank = 0

        return start_station


# Tests
def test():
    sol = Solution()

    assert sol.can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert sol.can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert sol.can_complete_circuit([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]) == 4
    assert sol.can_complete_circuit([3, 3], [3, 4]) == -1
    assert sol.can_complete_circuit([4], [5]) == -1
    assert sol.can_complete_circuit([5], [5]) == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
