"""
PROBLEM: Top K Frequent Elements (LeetCode 347)
Difficulty: Medium
Pattern: Arrays & Hashing, Heap
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.

Example 1:
    Input: nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]

Example 2:
    Input: nums = [1], k = 1
    Output: [1]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array]
- It is guaranteed that the answer is unique

Follow up: Your algorithm's time complexity must be better than O(n log n),
where n is the array's size.

Approach 1 - Bucket Sort:
1. Count frequency of each element
2. Create buckets where index = frequency
3. Iterate from highest frequency to get k elements

Approach 2 - Heap:
1. Count frequency of each element
2. Use heap to get top k elements

Time: O(n) for bucket sort, O(n log k) for heap
Space: O(n)
"""

from typing import List
from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Count frequencies
        count = Counter(nums)

        # Bucket sort approach
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)

        # Collect top k from highest frequency
        result = []
        for i in range(len(buckets) - 1, 0, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result

        return result

    # Alternative using heap
    def topKFrequent_heap(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        return [num for num, _ in count.most_common(k)]


# Tests
def test():
    sol = Solution()

    result1 = sol.topKFrequent([1,1,1,2,2,3], 2)
    assert sorted(result1) == [1,2]

    assert sol.topKFrequent([1], 1) == [1]

    result2 = sol.topKFrequent([4,1,-1,2,-1,2,3], 2)
    assert sorted(result2) == [-1,2]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
