"""
PROBLEM: Car Fleet (LeetCode 853)
Difficulty: Medium
Pattern: Stack, Sorting
Companies: Amazon, Google, Microsoft, Apple

There are n cars going to the same destination along a one-lane road. The destination
is target miles away.

You are given two integer arrays position and speed, both of length n, where
position[i] is the position of the ith car and speed[i] is the speed of the ith car
(in miles per hour).

A car can never pass another car ahead of it, but it can catch up to it and drive
bumper to bumper at the same speed. The faster car will slow down to match the slower
car's speed. The distance between these two cars is ignored (i.e., they are assumed
to have the same position).

A car fleet is some non-empty set of cars driving at the same position and same speed.
Note that a single car is also a car fleet.

If a car catches up to a car fleet right at the destination point, it will still be
considered as one car fleet.

Return the number of car fleets that will arrive at the destination.

Example 1:
    Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
    Output: 3
    Explanation:
    - Car at position 10 arrives at time (12-10)/2 = 1
    - Car at position 8 arrives at time (12-8)/4 = 1
    - Car at position 0 arrives at time (12-0)/1 = 12
    - Car at position 5 arrives at time (12-5)/1 = 7
    - Car at position 3 arrives at time (12-3)/3 = 3

    Cars starting at 10 and 8 become a fleet, meeting at position 12 at time 1.
    Car starting at 0 makes a fleet by itself at time 12.
    Cars starting at 5 and 3 become a fleet at time 7.

Example 2:
    Input: target = 10, position = [3], speed = [3]
    Output: 1
    Explanation: There is only one car, hence there is only one fleet.

Example 3:
    Input: target = 100, position = [0,2,4], speed = [4,2,1]
    Output: 1
    Explanation: All cars will meet and form one fleet at position 4.

Constraints:
- n == position.length == speed.length
- 1 <= n <= 10^5
- 0 < target <= 10^6
- 0 <= position[i] < target
- All the values of position are unique.
- 0 < speed[i] <= 10^6

Approach:
1. Sort cars by starting position (descending order)
2. Calculate time to reach target for each car
3. Use stack to track fleet arrival times
4. If current car arrives later than previous, it's a new fleet
5. Otherwise, it catches up and joins the fleet

Time: O(n log n) - sorting dominates
Space: O(n) - sorting and stack storage
"""

from typing import List


class Solution:
    def car_fleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # Pair position with speed and sort by position (descending)
        cars = sorted(zip(position, speed), reverse=True)

        stack = []

        for pos, spd in cars:
            # Calculate time to reach target
            time = (target - pos) / spd

            # If stack is empty or current car takes longer, it's a new fleet
            if not stack or time > stack[-1]:
                stack.append(time)
            # Otherwise, current car catches up to previous fleet

        return len(stack)


# Tests
def test():
    sol = Solution()

    assert sol.car_fleet(12, [10,8,0,5,3], [2,4,1,1,3]) == 3
    assert sol.car_fleet(10, [3], [3]) == 1
    assert sol.car_fleet(100, [0,2,4], [4,2,1]) == 1
    assert sol.car_fleet(10, [6,8], [3,2]) == 2
    assert sol.car_fleet(10, [0,4,2], [2,1,3]) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
