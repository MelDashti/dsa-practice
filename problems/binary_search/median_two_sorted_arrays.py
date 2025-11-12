"""
PROBLEM: Median of Two Sorted Arrays (LeetCode 4)
Difficulty: Hard
Pattern: Binary Search
Companies: Amazon, Google, Facebook, Microsoft, Apple

Given two sorted arrays nums1 and nums2 of size m and n respectively, return
the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Example 1:
    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.00000
    Explanation: merged array = [1,2,3] and median is 2

Example 2:
    Input: nums1 = [1,2], nums2 = [3,4]
    Output: 2.50000
    Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5

Constraints:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

Approach:
1. Binary search on the smaller array to find the correct partition
2. Partition both arrays such that:
   - Left side has (m+n+1)//2 elements total
   - All elements on left <= all elements on right
3. The partition is correct when:
   - maxLeft1 <= minRight2 and maxLeft2 <= minRight1
4. If total length is odd, median is max of left side
5. If even, median is average of max(left) and min(right)

Time: O(log(min(m, n))) - binary search on smaller array
Space: O(1) - only using variables
"""

from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Ensure nums1 is the smaller array for optimization
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        left, right = 0, m

        while left <= right:
            # Partition nums1 and nums2
            partition1 = left + (right - left) // 2
            partition2 = (m + n + 1) // 2 - partition1

            # Get max of left side and min of right side for both arrays
            maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
            minRight1 = float('inf') if partition1 == m else nums1[partition1]

            maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
            minRight2 = float('inf') if partition2 == n else nums2[partition2]

            # Check if we found the correct partition
            if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
                # If total length is odd
                if (m + n) % 2 == 1:
                    return max(maxLeft1, maxLeft2)
                # If total length is even
                else:
                    return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
            elif maxLeft1 > minRight2:
                # Too far right in nums1, go left
                right = partition1 - 1
            else:
                # Too far left in nums1, go right
                left = partition1 + 1

        return 0.0  # Should never reach here


# Tests
def test():
    sol = Solution()

    assert sol.findMedianSortedArrays([1,3], [2]) == 2.0
    assert sol.findMedianSortedArrays([1,2], [3,4]) == 2.5
    assert sol.findMedianSortedArrays([0,0], [0,0]) == 0.0
    assert sol.findMedianSortedArrays([], [1]) == 1.0
    assert sol.findMedianSortedArrays([2], []) == 2.0
    assert sol.findMedianSortedArrays([1,3], [2,7]) == 2.5
    assert sol.findMedianSortedArrays([1,2,3,4,5], [6,7,8,9,10]) == 5.5

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
