"""
PROBLEM: Merge Intervals
Difficulty: Medium
Pattern: Intervals
Companies: Google, Facebook, Amazon, Microsoft, Apple
LeetCode: 56

Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals and return an array of non-overlapping
intervals sorted by start time.

Example 1:
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]
    (Intervals [1,3] and [2,6] overlap, merge them to [1,6])

Example 2:
    intervals = [[1,4],[4,5]]
    Output: [[1,5]]

Example 3:
    intervals = [[1,4],[2,3]]
    Output: [[1,4]]

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4

Approach:
1. Sort intervals by start time
2. Iterate through sorted intervals
3. Merge if current interval overlaps with previous
4. Otherwise, add previous interval to result

Time: O(n log n) due to sorting
Space: O(1) or O(n) depending on sorting space
"""

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])

        result = [intervals[0]]

        for current_start, current_end in intervals[1:]:
            last_start, last_end = result[-1]

            # If current interval overlaps with last interval in result
            if current_start <= last_end:
                # Merge by updating the end of last interval
                result[-1] = [last_start, max(last_end, current_end)]
            else:
                # No overlap, add current interval to result
                result.append([current_start, current_end])

        return result


# Tests
def test():
    sol = Solution()

    assert sol.merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert sol.merge([[1,4],[4,5]]) == [[1,5]]
    assert sol.merge([[1,4],[2,3]]) == [[1,4]]
    assert sol.merge([[1,2]]) == [[1,2]]
    assert sol.merge([[1,5],[2,3]]) == [[1,5]]
    assert sol.merge([[2,3],[4,5],[6,7],[8,9],[1,10]]) == [[1,10]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
