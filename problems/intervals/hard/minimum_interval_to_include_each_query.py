"""
PROBLEM: Minimum Interval to Include Each Query
Difficulty: Hard
Pattern: Intervals + Sorting + Min Heap
Companies: Google, Facebook, Amazon, Microsoft
LeetCode: 1851

You are given a 2D integer array intervals, where intervals[i] = [left, right],
and you are also given a 1D integer array queries.

For each query, find the smallest interval that contains each query.
The answer for each query is the size of the smallest interval.
If no interval contains the query, the answer is -1.

Example 1:
    intervals = [[1,4],[2,8],[1,6]]
    queries = [2,4,6]
    Output: [4,6,6]
    Query 2: Intervals [1,4], [2,8], [1,6] contain 2, sizes 4,6,6, smallest is 4
    Query 4: Intervals [1,4], [2,8], [1,6] contain 4, sizes 4,6,6, smallest is 4 (but answer is 6?)
    Query 6: Intervals [2,8], [1,6] contain 6, sizes 7,6, smallest is 6

Example 2:
    intervals = [[2,3],[2,5],[1,8],[5,8]]
    queries = [6,1,1,2]
    Output: [2,-1,4,1]

Constraints:
- 1 <= intervals.length <= 10^5
- 1 <= queries.length <= 10^5
- intervals[i].length == 2
- 1 <= left_i <= right_i <= 10^9
- 1 <= queries[j] <= 10^9

Approach:
1. Create array of (query, original_index) to track original positions
2. Sort intervals by start, and queries by value
3. Use a min heap to track interval sizes
4. For each query, add all intervals that could contain it
5. Remove intervals that end before the query
6. The smallest remaining interval is the answer
7. Restore original query order

Time: O((n + m) log n) where n = intervals.length, m = queries.length
Space: O(n + m)
"""

import heapq
from typing import List


class Solution:
    def min_interval_for_each_query(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # Sort intervals by start time
        intervals.sort()

        # Create (query_value, original_index) and sort by query value
        queries_with_idx = [(q, i) for i, q in enumerate(queries)]
        queries_with_idx.sort()

        result = [0] * len(queries)
        min_heap = []  # (interval_size, end_time)
        interval_idx = 0

        for query, original_idx in queries_with_idx:
            # Add all intervals that start <= query
            while interval_idx < len(intervals) and intervals[interval_idx][0] <= query:
                left, right = intervals[interval_idx]
                size = right - left + 1
                heapq.heappush(min_heap, (size, right))
                interval_idx += 1

            # Remove intervals that end < query (don't contain query)
            while min_heap and min_heap[0][1] < query:
                heapq.heappop(min_heap)

            # Smallest valid interval or -1 if none
            if min_heap:
                result[original_idx] = min_heap[0][0]
            else:
                result[original_idx] = -1

        return result


# Tests
def test():
    sol = Solution()

    assert sol.min_interval_for_each_query([[1,4],[2,8],[1,6]], [2,4,6]) == [4,4,6]
    assert sol.min_interval_for_each_query([[2,3],[2,5],[1,8],[5,8]], [6,1,1,2]) == [4,8,8,2]
    assert sol.min_interval_for_each_query([[1,1]], [1]) == [1]
    assert sol.min_interval_for_each_query([[1,2],[1,3],[3,4]], [1,2,3]) == [2,2,2]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
