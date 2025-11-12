"""
PROBLEM: Detect Squares (LeetCode 2013)
Difficulty: Medium
Pattern: Hash Map, Geometry, Counting
Companies: Amazon, Google, TikTok

You are given a stream of points on the X-Y plane. Design an algorithm that:

1. Adds new points from the stream into a data structure. Duplicate points are
   allowed and should be treated as different points.
2. Given a query point, counts the number of possible squares that can be formed
   by using the query point as one corner of the square.

A square has 4 corners with positive (non-zero) area, and its edges are parallel
to the axes.

Since the answer may be very large, return the count modulo 10^9 + 7.

Example:
    Input:
        ["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
        [[], [[4,6]], [[9,6]], [[4,1]], [[5,4]], [[1,4]], [[0,0]], [[0,0]]]
    Output: [null, null, null, null, 0, 0, null, 1]

Constraints:
- 0 <= x, y <= 10^9
- At most 5000 calls will be made to add and count combined
- At most 1000 unique points will be added

Approach:
1. Use hash map to store counts of each point
2. For each query point, find all possible squares with this point as one corner
3. For a square with corners at (x, y), (x+d, y), (x+d, y+d), (x, y+d):
   - Check if other three corners exist in our points map
   - Count all valid squares

Time: O(n) for each count query where n is unique x-coordinates
Space: O(n) for storing points
"""

from collections import defaultdict


class DetectSquares:
    def __init__(self):
        self.points = defaultdict(int)
        self.x_coords = defaultdict(set)

    def add(self, point: list[int]) -> None:
        """
        Add a point to the data structure.
        """
        x, y = point[0], point[1]
        self.points[(x, y)] += 1
        self.x_coords[x].add(y)

    def count(self, point: list[int]) -> int:
        """
        Count the number of possible squares with the given point as one corner.
        """
        x, y = point[0], point[1]
        result = 0
        MOD = 10**9 + 7

        # Check all points with same x-coordinate
        for y2 in self.x_coords[x]:
            # y2 is a different y-coordinate, so side length is |y2 - y|
            if y == y2:
                continue

            side_length = abs(y2 - y)

            # For a square, the other two points should be at:
            # (x + side_length, y) and (x + side_length, y2)
            # or (x - side_length, y) and (x - side_length, y2)

            # Check for square to the right
            if (x + side_length, y) in self.points and \
               (x + side_length, y2) in self.points:
                result += (self.points[(x, y2)] *
                          self.points[(x + side_length, y)] *
                          self.points[(x + side_length, y2)]) % MOD

            # Check for square to the left
            if (x - side_length, y) in self.points and \
               (x - side_length, y2) in self.points:
                result += (self.points[(x, y2)] *
                          self.points[(x - side_length, y)] *
                          self.points[(x - side_length, y2)]) % MOD

        return result % MOD


# Tests
def test():
    # Test 1: Simple square (2x2)
    ds = DetectSquares()
    ds.add([0, 0])
    ds.add([2, 0])
    ds.add([0, 2])
    ds.add([2, 2])
    # Query from (0, 0) should find 1 square
    assert ds.count([0, 0]) == 1

    # Test 2: No squares (incomplete set)
    ds2 = DetectSquares()
    ds2.add([0, 0])
    ds2.add([1, 0])
    assert ds2.count([0, 0]) == 0

    # Test 3: Small square (1x1)
    ds3 = DetectSquares()
    ds3.add([0, 0])
    ds3.add([1, 0])
    ds3.add([0, 1])
    ds3.add([1, 1])
    result = ds3.count([0, 0])
    assert result == 1

    # Test 4: Query from different corner
    ds4 = DetectSquares()
    ds4.add([0, 0])
    ds4.add([1, 0])
    ds4.add([0, 1])
    ds4.add([1, 1])
    result = ds4.count([1, 1])
    assert result == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
