"""
PROBLEM: Find Median from Data Stream (LeetCode 295)
Difficulty: Hard
Pattern: Heap, Design
Companies: Amazon, Google, Facebook, Microsoft, Apple, Bloomberg

The median is the middle value in an ordered integer list. If the size of the
list is even, there is no middle value, and the median is the mean of the two
middle values.

Implement the MedianFinder class:
- MedianFinder() initializes the MedianFinder object.
- void add_num(int num) adds the integer num from the data stream to the data structure.
- double find_median() returns the median of all elements so far.

Example 1:
    Input:
    ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
    [[], [1], [2], [], [3], []]
    Output:
    [null, null, null, 1.5, null, 2.0]

    Explanation:
    MedianFinder medianFinder = new MedianFinder();
    medianFinder.add_num(1);    // arr = [1]
    medianFinder.add_num(2);    // arr = [1, 2]
    medianFinder.find_median(); // return 1.5 (i.e., (1 + 2) / 2)
    medianFinder.add_num(3);    // arr = [1, 2, 3]
    medianFinder.find_median(); // return 2.0

Constraints:
- -10^5 <= num <= 10^5
- There will be at least one element in the data structure before calling findMedian.
- At most 5 * 10^4 calls will be made to addNum and findMedian.

Follow up:
- If all integer numbers from the stream are in the range [0, 100], how would
  you optimize your solution?
- If 99% of all integer numbers from the stream are in the range [0, 100], how
  would you optimize your solution?

Approach:
1. Use two heaps: max heap for smaller half, min heap for larger half
2. Keep heaps balanced (sizes differ by at most 1)
3. Max heap stores smaller numbers, min heap stores larger numbers
4. Median is either average of two tops or top of larger heap
5. When adding:
   - Add to max heap first
   - Move max from max heap to min heap
   - Balance if min heap becomes larger

Time: O(log n) - addNum, O(1) - findMedian
Space: O(n) - store all numbers
"""

import heapq


class MedianFinder:
    def __init__(self):
        # Max heap for smaller half (negate values for max heap)
        self.small = []
        # Min heap for larger half
        self.large = []

    def add_num(self, num: int) -> None:
        # Add to max heap (smaller half)
        heapq.heappush(self.small, -num)

        # Move largest from small to large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance heaps (small can be at most 1 larger than large)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]

        return (-self.small[0] + self.large[0]) / 2.0


# Tests
def test():
    # Test 1
    medianFinder = MedianFinder()
    medianFinder.add_num(1)
    medianFinder.add_num(2)
    assert medianFinder.find_median() == 1.5
    medianFinder.add_num(3)
    assert medianFinder.find_median() == 2.0

    # Test 2
    mf2 = MedianFinder()
    mf2.add_num(6)
    assert mf2.find_median() == 6.0
    mf2.add_num(10)
    assert mf2.find_median() == 8.0
    mf2.add_num(2)
    assert mf2.find_median() == 6.0
    mf2.add_num(6)
    assert mf2.find_median() == 6.0
    mf2.add_num(5)
    assert mf2.find_median() == 6.0

    # Test 3
    mf3 = MedianFinder()
    mf3.add_num(-1)
    assert mf3.find_median() == -1.0
    mf3.add_num(-2)
    assert mf3.find_median() == -1.5
    mf3.add_num(-3)
    assert mf3.find_median() == -2.0

    # Test 4
    mf4 = MedianFinder()
    for i in range(1, 6):
        mf4.add_num(i)
    assert mf4.find_median() == 3.0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
