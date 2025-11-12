"""
PROBLEM: Daily Temperatures (LeetCode 739)
Difficulty: Medium
Pattern: Stack, Monotonic Stack
Companies: Amazon, Google, Facebook, Bloomberg, Microsoft

Given an array of integers temperatures represents the daily temperatures, return an
array answer such that answer[i] is the number of days you have to wait after the ith
day to get a warmer temperature. If there is no future day for which this is possible,
keep answer[i] == 0 instead.

Example 1:
    Input: temperatures = [73,74,75,71,69,72,76,73]
    Output: [1,1,4,2,1,1,0,0]
    Explanation:
    - Day 0: 73°F, next warmer is 74°F at day 1 (wait 1 day)
    - Day 1: 74°F, next warmer is 75°F at day 2 (wait 1 day)
    - Day 2: 75°F, next warmer is 76°F at day 6 (wait 4 days)
    - Day 3: 71°F, next warmer is 72°F at day 5 (wait 2 days)
    - Day 4: 69°F, next warmer is 72°F at day 5 (wait 1 day)
    - Day 5: 72°F, next warmer is 76°F at day 6 (wait 1 day)
    - Day 6: 76°F, no warmer day (wait 0 days)
    - Day 7: 73°F, no warmer day (wait 0 days)

Example 2:
    Input: temperatures = [30,40,50,60]
    Output: [1,1,1,0]

Example 3:
    Input: temperatures = [30,60,90]
    Output: [1,1,0]

Constraints:
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100

Approach (Monotonic Stack):
1. Use stack to store indices of temperatures
2. Stack maintains decreasing temperature order
3. For each day, pop from stack while current temp is warmer
4. For popped indices, calculate days difference
5. Push current index to stack

Time: O(n) - each element pushed/popped once
Space: O(n) - stack storage
"""

from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        result = [0] * n
        stack = []  # stores indices

        for i in range(n):
            # While current temp is warmer than stack top
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev_index = stack.pop()
                result[prev_index] = i - prev_index

            stack.append(i)

        return result


# Tests
def test():
    sol = Solution()

    assert sol.dailyTemperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]
    assert sol.dailyTemperatures([30,40,50,60]) == [1,1,1,0]
    assert sol.dailyTemperatures([30,60,90]) == [1,1,0]
    assert sol.dailyTemperatures([89,62,70,58,47,47,46,76,100,70]) == [8,1,5,4,3,2,1,1,0,0]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
