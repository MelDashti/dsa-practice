"""
PROBLEM: Largest Rectangle in Histogram (LeetCode 84)
LeetCode: https://leetcode.com/problems/largest-rectangle-in-histogram/
Difficulty: Hard
Pattern: Stack, Monotonic Stack
Companies: Amazon, Google, Facebook, Microsoft, Bloomberg

Given an array of integers heights representing the histogram's bar height where the
width of each bar is 1, return the area of the largest rectangle in the histogram.

Example 1:
    Input: heights = [2,1,5,6,2,3]
    Output: 10
    Explanation: The largest rectangle is shown in the red area, which has an area = 10 units.
    Bars at indices 2 and 3 with heights 5 and 6 form rectangle of width 2 and height 5.

Example 2:
    Input: heights = [2,4]
    Output: 4
    Explanation: The largest rectangle has height 2 and width 2.

Example 3:
    Input: heights = [1]
    Output: 1

Constraints:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4

Approach (Monotonic Stack):
1. Use stack to maintain indices in increasing height order
2. For each bar:
   - While current bar is shorter than stack top:
     - Pop index and calculate rectangle area with that height
     - Width extends from next stack element to current position
   - Push current index
3. Process remaining stack elements
4. Track maximum area seen

Key insight: For each bar, find the maximum rectangle where that bar is the shortest.
This requires finding how far left and right we can extend from that bar.

Time: O(n) - each element pushed/popped once
Space: O(n) - stack storage
"""

from typing import List


class Solution:
    def largest_rectangle_area(self, heights: List[int]) -> int:
        max_area = 0
        stack = []  # stores (index, height) pairs

        for i, h in enumerate(heights):
            start = i

            # Pop while current height is less than stack top
            while stack and stack[-1][1] > h:
                index, height = stack.pop()
                # Calculate area with popped height
                max_area = max(max_area, height * (i - index))
                # Update start to popped index (can extend left)
                start = index

            stack.append((start, h))

        # Process remaining bars in stack
        for i, h in stack:
            # These bars can extend to the end
            max_area = max(max_area, h * (len(heights) - i))

        return max_area


# Tests
def test():
    sol = Solution()

    assert sol.largest_rectangle_area([2,1,5,6,2,3]) == 10
    assert sol.largest_rectangle_area([2,4]) == 4
    assert sol.largest_rectangle_area([1]) == 1
    assert sol.largest_rectangle_area([2,1,2]) == 3
    assert sol.largest_rectangle_area([3,6,5,7,4,8,1,0]) == 20
    assert sol.largest_rectangle_area([1,1,1,1,1]) == 5
    assert sol.largest_rectangle_area([4,2,0,3,2,5]) == 6

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
