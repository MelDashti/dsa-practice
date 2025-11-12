"""
PROBLEM: Trapping Rain Water (LeetCode 42)
Difficulty: Hard
Pattern: Two Pointers, Dynamic Programming
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

Given n non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.

Example 1:
    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: The elevation map traps 6 units of rain water

Example 2:
    Input: height = [4,2,0,3,2,5]
    Output: 9

Constraints:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

Approach (Two Pointers):
1. Use two pointers and track max heights from left and right
2. Water trapped at position depends on min(left_max, right_max) - height
3. Move pointer with smaller max height
4. Update max heights and add trapped water

Why this works:
- Water level at position = min(max_left, max_right)
- Move smaller side because it's the limiting factor

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max = height[left]
        right_max = height[right]
        water = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += right_max - height[right]

        return water


# Tests
def test():
    sol = Solution()

    assert sol.trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
    assert sol.trap([4,2,0,3,2,5]) == 9
    assert sol.trap([4,2,3]) == 1
    assert sol.trap([]) == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
