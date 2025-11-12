"""
PROBLEM: Insert Interval
Difficulty: Medium
Pattern: Intervals
Companies: Google, Facebook, Amazon, Microsoft
LeetCode: 57

You are given a list of non-overlapping intervals sorted by their start time.
Insert a new interval and merge overlapping intervals if necessary.

Example 1:
    intervals = [[1,2],[3,5],[6,9]]
    newInterval = [2,5]
    Output: [[1,5],[6,9]]

Example 2:
    intervals = [[1,5]]
    newInterval = [2,3]
    Output: [[1,5]]

Example 3:
    intervals = [[1,5]]
    newInterval = [6,8]
    Output: [[1,5],[6,8]]

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^5
- newInterval.length == 2
- 0 <= newInterval[0] <= newInterval[1] <= 10^5

Approach:
1. Add all intervals that end before new interval starts
2. Merge all overlapping intervals with the new interval
3. Add all intervals that start after merged interval ends

Time: O(n)
Space: O(n)
"""

from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        result = []
        new_start, new_end = newInterval

        for start, end in intervals:
            # If current interval ends before new interval starts, add it to result
            if end < new_start:
                result.append([start, end])
            # If current interval starts after new interval ends, add new interval and current
            elif start > new_end:
                result.append([new_start, new_end])
                new_start, new_end = start, end
            # Overlapping intervals, merge them
            else:
                new_start = min(new_start, start)
                new_end = max(new_end, end)

        # Don't forget to add the last merged interval
        result.append([new_start, new_end])
        return result


# Tests
def test():
    sol = Solution()

    assert sol.insert([[1,2],[3,5],[6,9]], [2,5]) == [[1,5],[6,9]]
    assert sol.insert([[1,5]], [2,3]) == [[1,5]]
    assert sol.insert([[1,5]], [6,8]) == [[1,5],[6,8]]
    assert sol.insert([[3,5],[6,9]], [1,2]) == [[1,2],[3,5],[6,9]]
    assert sol.insert([], [5,7]) == [[5,7]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
