"""
PROBLEM: Kth Largest Element in an Array (LeetCode 215)
LeetCode: https://leetcode.com/problems/kth-largest-element-in-an-array/
Difficulty: Medium
Pattern: Heap, Divide and Conquer, Quickselect
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

Given an integer array nums and an integer k, return the kth largest element
in the array.

Note that it is the kth largest element in the sorted order, not the kth
distinct element.

Can you solve it without sorting?

Example 1:
    Input: nums = [3,2,1,5,6,4], k = 2
    Output: 5

Example 2:
    Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
    Output: 4

Constraints:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Approach:
1. Use min heap of size k to track k largest elements
2. Iterate through all numbers
3. Maintain heap of size k (remove smallest if size exceeds k)
4. The root of heap is the kth largest element
5. Alternative: could use quickselect for O(n) average time

Time: O(n log k) - process n elements, each heap operation is log k
Space: O(k) - heap stores k elements
"""

import heapq


class Solution:
    def find_kth_largest(self, nums: list[int], k: int) -> int:
        # Use min heap of size k
        min_heap = []

        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return min_heap[0]


# Tests
def test():
    sol = Solution()

    # Test 1
    assert sol.find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5

    # Test 2
    assert sol.find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    # Test 3
    assert sol.find_kth_largest([1], 1) == 1

    # Test 4
    assert sol.find_kth_largest([1, 2], 1) == 2

    # Test 5
    assert sol.find_kth_largest([7, 6, 5, 4, 3, 2, 1], 2) == 6

    # Test 6
    assert sol.find_kth_largest([-1, -1], 2) == -1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
