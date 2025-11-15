"""
PROBLEM: Find K Pairs with Smallest Sums (LeetCode 373)
Difficulty: Medium
Pattern: Heap/Priority Queue, K-way Merge
Companies: Google, Amazon, Uber, Airbnb

DESCRIPTION:
You are given two integer arrays nums1 and nums2 sorted in ascending order and
an integer k.

Define a pair (u, v) which consists of one element from the first array and one
element from the second array.

Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.

EXAMPLES:
Example 1:
Input: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
Output: [[1,2],[1,4],[1,6]]
Explanation: The first 3 pairs are: [1,2], [1,4], [1,6]
The next pairs would be [7,2], [7,4], [11,2]

Example 2:
Input: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
Output: [[1,1],[1,1]]
Explanation: The first 2 pairs are: [1,1], [1,1]
Then [1,2], [2,1], [1,2], [2,2], [1,3], [1,3], [2,3]

Example 3:
Input: nums1 = [1,2], nums2 = [3], k = 3
Output: [[1,3],[2,3]]

CONSTRAINTS:
- 1 <= nums1.length, nums2.length <= 10^5
- -10^9 <= nums1[i], nums2[i] <= 10^9
- nums1 and nums2 are sorted in ascending order
- 1 <= k <= 10^4

APPROACH:
Use min heap with K-way merge pattern:
1. Start by adding pairs (nums1[0], nums2[j]) for all j (or up to k)
2. Pop smallest sum pair from heap
3. If popped pair is (nums1[i], nums2[j]), add (nums1[i+1], nums2[j]) if i+1 exists
4. Repeat k times or until heap is empty

Key insight: Since arrays are sorted, if we have (i, j), the next candidate
is (i+1, j), not (i, j+1) because we already considered all nums2 elements.

TIME COMPLEXITY: O(k log k)
- At most k elements in heap, pop k times

SPACE COMPLEXITY: O(k)
- Heap stores at most k elements

WHY THIS PROBLEM IS IMPORTANT:
- K-way Merge pattern (underrepresented in NeetCode 150)
- Frequently asked at Google and Amazon
- Tests optimization thinking (not brute force all pairs)
- Similar pattern to "Merge K Sorted Lists"
"""

from typing import List
import heapq


class Solution:
    def kSmallestPairs(
        self, nums1: List[int], nums2: List[int], k: int
    ) -> List[List[int]]:
        """
        Find k pairs with smallest sums using min heap.
        """
        if not nums1 or not nums2:
            return []

        # Min heap: (sum, i, j) where i is index in nums1, j in nums2
        min_heap = []
        result = []

        # Initialize heap with pairs (nums1[0], nums2[j]) for all j
        # Only add min(k, len(nums2)) pairs to optimize
        for j in range(min(k, len(nums2))):
            heapq.heappush(min_heap, (nums1[0] + nums2[j], 0, j))

        # Extract k smallest pairs
        while min_heap and len(result) < k:
            curr_sum, i, j = heapq.heappop(min_heap)
            result.append([nums1[i], nums2[j]])

            # If there's a next element in nums1, add pair with same nums2 element
            if i + 1 < len(nums1):
                heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))

        return result


class SolutionOptimized:
    """
    Alternative approach starting with first pair only.
    """

    def kSmallestPairs(
        self, nums1: List[int], nums2: List[int], k: int
    ) -> List[List[int]]:
        """
        More memory-efficient: start with single pair.
        """
        if not nums1 or not nums2:
            return []

        # Min heap: (sum, i, j)
        min_heap = [(nums1[0] + nums2[0], 0, 0)]
        visited = {(0, 0)}
        result = []

        while min_heap and len(result) < k:
            curr_sum, i, j = heapq.heappop(min_heap)
            result.append([nums1[i], nums2[j]])

            # Try adding pair with next nums1 element
            if i + 1 < len(nums1) and (i + 1, j) not in visited:
                heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))
                visited.add((i + 1, j))

            # Try adding pair with next nums2 element
            if j + 1 < len(nums2) and (i, j + 1) not in visited:
                heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))
                visited.add((i, j + 1))

        return result


def test_k_smallest_pairs():
    """Test cases for Find K Pairs with Smallest Sums"""
    solutions = [Solution(), SolutionOptimized()]

    test_cases = [
        ([1, 7, 11], [2, 4, 6], 3, [[1, 2], [1, 4], [1, 6]]),
        ([1, 1, 2], [1, 2, 3], 2, [[1, 1], [1, 1]]),
        ([1, 2], [3], 3, [[1, 3], [2, 3]]),
        ([1, 2, 4], [1, 3, 5, 7], 5, [[1, 1], [1, 3], [2, 1], [1, 5], [2, 3]]),
    ]

    for sol in solutions:
        for nums1, nums2, k, expected in test_cases:
            result = sol.kSmallestPairs(nums1, nums2, k)
            assert (
                result == expected
            ), f"{sol.__class__.__name__} failed: got {result}, expected {expected}"

    print("✅ All test cases passed for all solutions!")


if __name__ == "__main__":
    test_k_smallest_pairs()
