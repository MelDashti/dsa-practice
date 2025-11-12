"""
PROBLEM: Meeting Rooms II
Difficulty: Medium
Pattern: Intervals + Min Heap
Companies: Google, Facebook, Amazon, Microsoft
LeetCode: 253

Given an array of meeting time intervals where intervals[i] = [start, end],
find the minimum number of conference rooms required.

Example 1:
    intervals = [[0,30],[5,10],[15,20]]
    Output: 2
    (Meetings [0,30] and [5,10] overlap, need 2 rooms)

Example 2:
    intervals = [[7,10],[2,4]]
    Output: 1
    (No overlap, need 1 room)

Example 3:
    intervals = [[13,15],[1,13]]
    Output: 1
    (First meeting ends at 13, second starts at 13, can reuse room)

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start < end <= 10^6

Approach (Min Heap):
1. Separate start and end times and sort both
2. Use two pointers for starts and ends
3. Track room count with a min heap (room end times)
4. When new meeting starts, check if any room is available
5. If available, remove earliest ending room; otherwise, add new room
6. Return total rooms needed

Time: O(n log n)
Space: O(n)
"""

import heapq
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0

        # Separate and sort starts and ends
        starts = sorted([interval[0] for interval in intervals])
        ends = sorted([interval[1] for interval in intervals])

        rooms = 0
        start_ptr = 0
        end_ptr = 0

        while start_ptr < len(starts):
            # If next meeting starts at or after a room becomes available
            if starts[start_ptr] >= ends[end_ptr]:
                # Reuse the room (no need to add a new one)
                rooms -= 1
                end_ptr += 1

            # Need a new room for this meeting
            rooms += 1
            start_ptr += 1

        return rooms


class SolutionHeap:
    """Alternative solution using min heap"""

    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0

        # Sort by start time
        intervals.sort()

        # Min heap to track room end times
        rooms = [intervals[0][1]]

        for start, end in intervals[1:]:
            # If earliest ending room is available (ends before current start)
            if rooms[0] <= start:
                heapq.heapreplace(rooms, end)
            else:
                # Need a new room
                heapq.heappush(rooms, end)

        return len(rooms)


# Tests
def test():
    sol = Solution()

    assert sol.minMeetingRooms([[0,30],[5,10],[15,20]]) == 2
    assert sol.minMeetingRooms([[7,10],[2,4]]) == 1
    assert sol.minMeetingRooms([[13,15],[1,13]]) == 1
    assert sol.minMeetingRooms([]) == 0
    assert sol.minMeetingRooms([[1,5],[1,5],[1,5]]) == 3

    print("✓ All tests passed for Solution")

    sol_heap = SolutionHeap()
    assert sol_heap.minMeetingRooms([[0,30],[5,10],[15,20]]) == 2
    assert sol_heap.minMeetingRooms([[7,10],[2,4]]) == 1
    assert sol_heap.minMeetingRooms([[13,15],[1,13]]) == 1
    assert sol_heap.minMeetingRooms([]) == 0
    assert sol_heap.minMeetingRooms([[1,5],[1,5],[1,5]]) == 3

    print("✓ All tests passed for SolutionHeap")


if __name__ == "__main__":
    test()
