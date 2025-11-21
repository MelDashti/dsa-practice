"""
PROBLEM: Meeting Rooms
Difficulty: Easy
Pattern: Intervals
Companies: Google, Facebook, Amazon
LeetCode: 252

Given an array of meeting time intervals where intervals[i] = [start, end],
determine if a person could attend all meetings.

Example 1:
    intervals = [[0,30],[5,10],[15,20]]
    Output: false
    (Conflict: [0,30] overlaps with [5,10])

Example 2:
    intervals = [[7,10],[2,4]]
    Output: true
    (No conflicts)

Example 3:
    intervals = []
    Output: true
    (No meetings, can attend all)

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start < end <= 10^6

Approach:
1. Sort intervals by start time
2. Check if any two consecutive intervals overlap
3. Two intervals overlap if current start < previous end
4. Return true if no overlaps found

Time: O(n log n) due to sorting
Space: O(1)
"""

from typing import List


class Solution:
    def can_attend_meetings(self, intervals: List[List[int]]) -> bool:
        # Sort intervals by start time
        intervals.sort()

        # Check consecutive intervals for overlap
        for i in range(len(intervals) - 1):
            # If current meeting starts before previous meeting ends, there's a conflict
            if intervals[i][1] > intervals[i + 1][0]:
                return False

        return True


# Tests
def test():
    sol = Solution()

    assert sol.can_attend_meetings([[0,30],[5,10],[15,20]]) == False
    assert sol.can_attend_meetings([[7,10],[2,4]]) == True
    assert sol.can_attend_meetings([]) == True
    assert sol.can_attend_meetings([[1,2],[1,2]]) == False
    assert sol.can_attend_meetings([[1,5],[15,20],[5,10]]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
