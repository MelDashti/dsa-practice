"""
PROBLEM: Sliding Window Median (LeetCode 480)
Difficulty: Hard
Pattern: Two Heaps, Sliding Window
Companies: Google, Amazon, Meta, Apple

DESCRIPTION:
The median is the middle value in an ordered integer list. If the size of the list
is even, there is no middle value. So the median is the mean of the two middle values.

Implement the medianSlidingWindow function to find the median of each window of size k
which is sliding along the array nums. Return the medians as an array of doubles.

EXAMPLES:
Example 1:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
Explanation:
Window position                Median
---------------               -----
[1  3  -1] -3  5  3  6  7       1
 1 [3  -1  -3] 5  3  6  7      -1
 1  3 [-1  -3  5] 3  6  7      -1
 1  3  -1 [-3  5  3] 6  7       3
 1  3  -1  -3 [5  3  6] 7       5
 1  3  -1  -3  5 [3  6  7]      6

Example 2:
Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]

CONSTRAINTS:
- 1 <= k <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1

APPROACH:
Use Two Heaps pattern (similar to Find Median from Data Stream):
1. Maintain two heaps:
   - max_heap: stores smaller half of window (negated for max heap behavior)
   - min_heap: stores larger half of window
2. Balance heaps so that max_heap.size() >= min_heap.size()
3. When sliding window:
   - Add new element to appropriate heap
   - Remove outgoing element (lazy deletion with hashmap)
   - Rebalance heaps
   - Calculate median from heap tops

The challenge is efficiently removing elements from middle of heaps (lazy deletion).

TIME COMPLEXITY: O(n * k) where n is array length
- For each window: O(k log k) for rebalancing in worst case
- With optimization (lazy deletion), can achieve O(n log k)

SPACE COMPLEXITY: O(k)
- Two heaps of size k/2 each

WHY THIS PROBLEM IS IMPORTANT:
- Combines Two Heaps pattern with Sliding Window
- Two Heaps pattern is underrepresented in NeetCode 150
- Frequently asked at Google and Amazon
- Tests advanced heap manipulation and lazy deletion
- Harder variant of "Find Median from Data Stream"
"""

from typing import List
from collections import defaultdict
import heapq


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        """
        Find median of each sliding window using two heaps.
        """
        # Max heap for smaller half (negate values for max heap)
        max_heap = []
        # Min heap for larger half
        min_heap = []
        # Track elements to be removed (lazy deletion)
        to_remove = defaultdict(int)

        result = []

        # Helper function to balance heaps
        def balance():
            # max_heap should have same or one more element than min_heap
            if len(max_heap) > len(min_heap) + 1:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))
            elif len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

        # Helper to clean heap tops
        def clean_heap(heap, is_max_heap=False):
            while heap:
                val = -heap[0] if is_max_heap else heap[0]
                if to_remove[val] > 0:
                    to_remove[val] -= 1
                    heapq.heappop(heap)
                else:
                    break

        # Helper to add element to heaps
        def add_element(num):
            if not max_heap or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
            else:
                heapq.heappush(min_heap, num)
            balance()

        # Helper to remove element from heaps
        def remove_element(num):
            to_remove[num] += 1
            if num <= -max_heap[0]:
                # Element is in max_heap (smaller half)
                if num == -max_heap[0]:
                    heapq.heappop(max_heap)
                    to_remove[num] -= 1
                # Rebalance as we removed from max_heap
            else:
                # Element is in min_heap (larger half)
                if num == min_heap[0]:
                    heapq.heappop(min_heap)
                    to_remove[num] -= 1

            clean_heap(max_heap, True)
            clean_heap(min_heap, False)
            balance()
            clean_heap(max_heap, True)
            clean_heap(min_heap, False)

        # Helper to get median
        def get_median():
            if k % 2 == 1:
                return float(-max_heap[0])
            else:
                return (-max_heap[0] + min_heap[0]) / 2.0

        # Initialize first window
        for i in range(k):
            add_element(nums[i])

        result.append(get_median())

        # Slide the window
        for i in range(k, len(nums)):
            # Remove outgoing element
            outgoing = nums[i - k]
            remove_element(outgoing)

            # Add incoming element
            incoming = nums[i]
            add_element(incoming)

            result.append(get_median())

        return result


def test_sliding_window_median():
    """Test cases for Sliding Window Median"""
    solution = Solution()

    # Test case 1: Basic example
    result = solution.medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3)
    expected = [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    assert result == expected, f"Expected {expected}, got {result}"

    # Test case 2: Even k
    result = solution.medianSlidingWindow([1, 2, 3, 4], 2)
    expected = [1.5, 2.5, 3.5]
    assert result == expected

    # Test case 3: k = 1
    result = solution.medianSlidingWindow([1, 3, -1], 1)
    expected = [1.0, 3.0, -1.0]
    assert result == expected

    # Test case 4: k equals array length
    result = solution.medianSlidingWindow([1, 2, 3, 4, 5], 5)
    expected = [3.0]
    assert result == expected

    # Test case 5: Negative numbers
    result = solution.medianSlidingWindow([-1, -2, -3, -4], 2)
    expected = [-1.5, -2.5, -3.5]
    assert result == expected

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_sliding_window_median()
