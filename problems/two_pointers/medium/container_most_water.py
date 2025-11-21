"""
PROBLEM: Container With Most Water (LeetCode 11)
Difficulty: Medium
Pattern: Two Pointers
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49
    Explanation: The max area is between height[1]=8 and height[8]=7
    Area = min(8,7) * (8-1) = 7 * 7 = 49

Example 2:
    Input: height = [1,1]
    Output: 1

Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

Approach:
1. Use two pointers at both ends of array
2. Calculate area = min(height[left], height[right]) * (right - left)
3. Move the pointer with smaller height inward
4. Track maximum area found

Why move smaller height?
- Moving larger height can't increase area (width decreases, height limited by smaller)
- Moving smaller height might find taller line

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def max_area(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            # Calculate current area
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height
            max_area = max(max_area, current_area)

            # Move the pointer with smaller height
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area


# Tests
def test():
    sol = Solution()

    assert sol.max_area([1,8,6,2,5,4,8,3,7]) == 49
    assert sol.max_area([1,1]) == 1
    assert sol.max_area([4,3,2,1,4]) == 16
    assert sol.max_area([1,2,1]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
