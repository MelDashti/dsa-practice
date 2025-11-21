"""
PROBLEM: Kth Largest Element in a Stream (LeetCode 703)
LeetCode: https://leetcode.com/problems/kth-largest-element-in-a-stream/
Difficulty: Easy
Pattern: Heap, Design
Companies: Amazon, Facebook, Google, Microsoft

Design a class to find the kth largest element in a stream. Note that it is
the kth largest element in the sorted order, not the kth distinct element.

Implement KthLargest class:
- KthLargest(int k, int[] nums) Initializes the object with the integer k and
  the stream of integers nums.
- int add(int val) Appends the integer val to the stream and returns the element
  representing the kth largest element in the stream.

Example 1:
    Input:
    ["KthLargest", "add", "add", "add", "add", "add"]
    [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]

    Output:
    [null, 4, 5, 5, 8, 8]

    Explanation:
    KthLargest kth_largest = new KthLargest(3, [4, 5, 8, 2]);
    kth_largest.add(3);   // return 4
    kth_largest.add(5);   // return 5
    kth_largest.add(10);  // return 5
    kth_largest.add(9);   // return 8
    kth_largest.add(4);   // return 8

Constraints:
- 1 <= k <= 10^4
- 0 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- -10^4 <= val <= 10^4
- At most 10^4 calls will be made to add

Approach:
1. Use a min heap of size k to track k largest elements
2. The root of min heap will be the kth largest element
3. Initialize heap with first k elements
4. For each new element, if larger than min, replace min and heapify
5. Return the minimum (root) which is the kth largest

Time: O(log k) - add operation, O(n log k) - initialization
Space: O(k) - heap stores k elements
"""

import heapq


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)

        # Keep only k largest elements
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]


# Tests
def test():
    # Test 1
    kth_largest = KthLargest(3, [4, 5, 8, 2])
    assert kth_largest.add(3) == 4
    assert kth_largest.add(5) == 5
    assert kth_largest.add(10) == 5
    assert kth_largest.add(9) == 8
    assert kth_largest.add(4) == 8

    # Test 2
    kth2 = KthLargest(1, [])
    assert kth2.add(-3) == -3
    assert kth2.add(-2) == -2
    assert kth2.add(-4) == -2
    assert kth2.add(0) == 0
    assert kth2.add(4) == 4

    # Test 3
    kth3 = KthLargest(2, [0])
    assert kth3.add(-1) == -1
    assert kth3.add(1) == 0
    assert kth3.add(-2) == 0
    assert kth3.add(-4) == 0
    assert kth3.add(3) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
