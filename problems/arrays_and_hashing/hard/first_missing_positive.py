"""
PROBLEM: First Missing Positive (LeetCode 41)
Difficulty: Hard
Pattern: Cyclic Sort, Arrays & Hashing
Companies: Amazon, Microsoft, Apple, Meta, Google

DESCRIPTION:
Given an unsorted integer array nums, return the smallest missing positive integer.

You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

EXAMPLES:
Example 1:
Input: nums = [1,2,0]
Output: 3
Explanation: The numbers in the range [1,2] are all in the array.

Example 2:
Input: nums = [3,4,-1,1]
Output: 2
Explanation: 1 is in the array but 2 is missing.

Example 3:
Input: nums = [7,8,9,11,12]
Output: 1
Explanation: The smallest positive integer 1 is missing.

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1

APPROACH:
This problem uses the Cyclic Sort pattern. The key insight is that for an array of
length n, the answer must be in the range [1, n+1]. We can use the array itself as
a hash table by placing each number i at index i-1.

Algorithm:
1. Place each number in its correct position (number i at index i-1)
2. Ignore numbers <= 0 or > n as they don't affect the answer
3. Scan the array to find the first position where nums[i] != i+1

TIME COMPLEXITY: O(n)
- Each number is visited at most twice (once for placement, once for verification)

SPACE COMPLEXITY: O(1)
- We modify the array in-place

WHY THIS PROBLEM IS IMPORTANT:
- Tests understanding of index-as-hash-map technique
- Cyclic Sort pattern (underrepresented in NeetCode 150)
- Frequently asked at Amazon (top 10 most asked)
- Tests ability to achieve O(n) time with O(1) space constraints
"""

from typing import List


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        Find the smallest missing positive integer using cyclic sort pattern.

        The idea is to place each positive integer i at index i-1.
        Then scan to find the first position where the number doesn't match.
        """
        n = len(nums)

        # Step 1: Place each number in its correct position
        # Number i should be at index i-1 (1-indexed to 0-indexed)
        i = 0
        while i < n:
            # Correct position for nums[i] is nums[i]-1
            correct_pos = nums[i] - 1

            # Place nums[i] at correct position if:
            # - It's a positive integer (> 0)
            # - It's within range [1, n]
            # - It's not already in the correct position
            if 0 < nums[i] <= n and nums[i] != nums[correct_pos]:
                # Swap nums[i] with the number at its correct position
                nums[i], nums[correct_pos] = nums[correct_pos], nums[i]
            else:
                i += 1

        # Step 2: Find the first missing positive
        # The first index i where nums[i] != i+1 means i+1 is missing
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        # If all positions [1, n] are filled correctly, return n+1
        return n + 1


def test_first_missing_positive():
    """Test cases for First Missing Positive"""
    solution = Solution()

    # Test case 1: Missing number in middle
    assert solution.firstMissingPositive([1, 2, 0]) == 3

    # Test case 2: Missing number at start
    assert solution.firstMissingPositive([3, 4, -1, 1]) == 2

    # Test case 3: All numbers out of range
    assert solution.firstMissingPositive([7, 8, 9, 11, 12]) == 1

    # Test case 4: Single element
    assert solution.firstMissingPositive([1]) == 2
    assert solution.firstMissingPositive([2]) == 1

    # Test case 5: Consecutive sequence
    assert solution.firstMissingPositive([1, 2, 3, 4, 5]) == 6

    # Test case 6: With duplicates and negatives
    assert solution.firstMissingPositive([1, 1, 2, 2, 3, 3]) == 4
    assert solution.firstMissingPositive([-1, -2, -3]) == 1

    # Test case 7: Large gap
    assert solution.firstMissingPositive([1000, 1001, 1002]) == 1

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_first_missing_positive()
