"""
PROBLEM: Koko Eating Bananas (LeetCode 875)
Difficulty: Medium
Pattern: Binary Search
Companies: Amazon, Google, Facebook, Bloomberg

Koko loves to eat bananas. There are n piles of bananas, the ith pile has
piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses
some pile of bananas and eats k bananas from that pile. If the pile has less
than k bananas, she eats all of them instead and will not eat any more bananas
during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas
before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Example 1:
    Input: piles = [3,6,7,11], h = 8
    Output: 4
    Explanation: At speed 4, she can eat all bananas in 1+2+2+3 = 8 hours

Example 2:
    Input: piles = [30,11,23,4,20], h = 5
    Output: 30
    Explanation: At speed 30, she can eat each pile in exactly 1 hour

Example 3:
    Input: piles = [30,11,23,4,20], h = 6
    Output: 23

Constraints:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9

Approach:
1. Binary search on the eating speed (k)
2. Range: [1, max(piles)]
3. For each speed, calculate total hours needed
4. If hours <= h, try smaller speed (move right pointer left)
5. If hours > h, need faster speed (move left pointer right)
6. Return the minimum valid speed

Time: O(n * log(max(piles))) - binary search * calculating hours for each speed
Space: O(1) - only using variables
"""

from typing import List
import math


class Solution:
    def min_eating_speed(self, piles: List[int], h: int) -> int:
        def can_finish(speed: int) -> bool:
            """Check if Koko can finish all bananas at given speed within h hours"""
            hours = 0
            for pile in piles:
                hours += math.ceil(pile / speed)
            return hours <= h

        left, right = 1, max(piles)
        result = right

        while left <= right:
            mid = left + (right - left) // 2

            if can_finish(mid):
                result = mid  # This speed works, try to find smaller
                right = mid - 1
            else:
                left = mid + 1  # Too slow, need faster speed

        return result


# Tests
def test():
    sol = Solution()

    assert sol.min_eating_speed([3,6,7,11], 8) == 4
    assert sol.min_eating_speed([30,11,23,4,20], 5) == 30
    assert sol.min_eating_speed([30,11,23,4,20], 6) == 23
    assert sol.min_eating_speed([3,6,7,11], 4) == 11
    assert sol.min_eating_speed([1], 1) == 1
    assert sol.min_eating_speed([1000000000], 2) == 500000000

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
