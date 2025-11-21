"""
PROBLEM: Non-overlapping Intervals
Difficulty: Medium
Pattern: Intervals + Greedy
Companies: Google, Facebook, Amazon, Microsoft
LeetCode: 435

Given an array of intervals, find the minimum number of intervals you need
to remove to make the rest of the intervals non-overlapping.

Two intervals [a,b] and [c,d] do not overlap if a >= d or c >= b.

Example 1:
    intervals = [[1,2],[2,3],[3,4],[1,3]]
    Output: 1
    (Remove [1,3], remaining [[1,2],[2,3],[3,4]] are non-overlapping)

Example 2:
    intervals = [[1,2],[1,2],[1,2]]
    Output: 2
    (Keep one [1,2], remove two)

Example 3:
    intervals = [[1,2],[2,3]]
    Output: 0
    (Already non-overlapping)

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- -10^4 <= start_i <= end_i <= 10^4

Approach (Greedy):
1. Sort intervals by end time (greedy: keep intervals that end earlier)
2. Keep track of end time of last kept interval
3. If current interval starts at or after last end, keep it
4. Otherwise, skip current interval (remove it)
5. Count removed intervals

Time: O(n log n) due to sorting
Space: O(1)
"""

from typing import List


class Solution:
    def erase_overlap_intervals(self, intervals: List[List[int]]) -> int:
        # Sort by end time (greedy approach)
        intervals.sort(key=lambda x: x[1])

        end = intervals[0][1]
        removed = 0

        for start, curr_end in intervals[1:]:
            # If current interval overlaps (starts before last end)
            if start < end:
                # Remove current interval (skip it)
                removed += 1
            else:
                # No overlap, keep current interval
                end = curr_end

        return removed


# Tests
def test():
    sol = Solution()

    assert sol.erase_overlap_intervals([[1,2],[2,3],[3,4],[1,3]]) == 1
    assert sol.erase_overlap_intervals([[1,2],[1,2],[1,2]]) == 2
    assert sol.erase_overlap_intervals([[1,2],[2,3]]) == 0
    assert sol.erase_overlap_intervals([[0,2],[1,3],[2,4]]) == 1
    assert sol.erase_overlap_intervals([[1,2],[1,2]]) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
