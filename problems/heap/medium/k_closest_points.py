"""
PROBLEM: K Closest Points to Origin (LeetCode 973)
Difficulty: Medium
Pattern: Heap, Divide and Conquer
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

Given an array of points where points[i] = [xi, yi] represents a point on the
X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance
(i.e., √((x1 - x2)^2 + (y1 - y2)^2)).

You may return the answer in any order. The answer is guaranteed to be unique
(except for the order that it is in).

Example 1:
    Input: points = [[1,3],[-2,2]], k = 1
    Output: [[-2,2]]
    Explanation:
    The distance between (1, 3) and the origin is sqrt(10).
    The distance between (-2, 2) and the origin is sqrt(8).
    Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
    We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].

Example 2:
    Input: points = [[3,3],[5,-1],[-2,4]], k = 2
    Output: [[3,3],[-2,4]]
    Explanation: The answer [[-2,4],[3,3]] would also be accepted.

Constraints:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4

Approach:
1. Use max heap of size k to track k closest points
2. Store tuples of (-distance, point) in heap (negative for max heap)
3. For each point, calculate distance squared (no need for sqrt)
4. If heap size < k, add point
5. If current point closer than farthest in heap, replace
6. Return all points from heap

Time: O(n log k) - process n points, each heap operation is log k
Space: O(k) - heap stores k points
"""

import heapq


class Solution:
    def k_closest(self, points: list[list[int]], k: int) -> list[list[int]]:
        # Max heap to store k closest points
        # Store (-distance, point) for max heap behavior
        max_heap = []

        for x, y in points:
            # Calculate distance squared (no need for sqrt)
            dist = x * x + y * y

            if len(max_heap) < k:
                heapq.heappush(max_heap, (-dist, [x, y]))
            elif dist < -max_heap[0][0]:
                heapq.heapreplace(max_heap, (-dist, [x, y]))

        return [point for _, point in max_heap]


# Tests
def test():
    sol = Solution()

    # Test 1
    result1 = sol.k_closest([[1, 3], [-2, 2]], 1)
    assert result1 == [[-2, 2]]

    # Test 2
    result2 = sol.k_closest([[3, 3], [5, -1], [-2, 4]], 2)
    assert sorted(result2) == sorted([[3, 3], [-2, 4]])

    # Test 3
    result3 = sol.k_closest([[1, 3], [-2, 2], [2, -2]], 2)
    assert sorted(result3) == sorted([[-2, 2], [2, -2]])

    # Test 4
    result4 = sol.k_closest([[0, 1], [1, 0]], 2)
    assert sorted(result4) == sorted([[0, 1], [1, 0]])

    # Test 5
    result5 = sol.k_closest([[1, 1], [1, 1], [1, 1]], 2)
    assert len(result5) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
