"""
PROBLEM: Merge Triplets to Form Target Triplet (LeetCode 1899)
LeetCode: https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
Difficulty: Medium
Pattern: Greedy
Companies: Google, Meta, Amazon

You are given a 2D list of triplets triplets where triplets[i] = [ai, bi, ci]. You want to
form a target triplet [x, y, z].

You are able to update the triplet triplets[i] = [ai, bi, ci] to [max(ai, x), max(bi, y),
max(ci, z)]. Note that the operation can be performed any number of times and in any order.

Given target = [x, y, z], return true if it is possible to form the target triplet by
updating the given triplets, otherwise return false.

Example 1:
    Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
    Output: true
    Explanation:
    - Start with [2,5,3]
    - Update [1,8,4] to [max(1,2), max(8,7), max(4,5)] = [2,8,5]
    - Now we have [2,8,5] which >= target [2,7,5]

Example 2:
    Input: triplets = [[1,3,2],[2,5,6]], target = [5,5,5]
    Output: false

Constraints:
- 1 <= triplets.length <= 10^5
- triplets[i].length == 3
- 1 <= ai, bi, ci <= 2000
- 1 <= x, y, z <= 2000

Approach (Greedy):
1. Key insight: we want triplets where EACH component <= target component
2. We can only merge helpful triplets (ones that don't exceed any target value)
3. Start current triplet as [0, 0, 0]
4. For each valid triplet, take maximum of each component
5. Check if final result == target

Time: O(n) - single pass through triplets
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def merge_triplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        """
        Check if we can form target triplet by merging given triplets.

        Strategy:
        - Only consider triplets where no component exceeds target
        - Start with current = [0, 0, 0]
        - For valid triplets, update current to max of each component
        - Check if final current matches target
        """
        current = [0, 0, 0]

        for triplet in triplets:
            # Skip triplets that exceed any target dimension
            if (triplet[0] > target[0] or triplet[1] > target[1] or
                triplet[2] > target[2]):
                continue

            # Update current to maximum of each component
            current[0] = max(current[0], triplet[0])
            current[1] = max(current[1], triplet[1])
            current[2] = max(current[2], triplet[2])

        return current == target


# Tests
def test():
    sol = Solution()

    assert sol.merge_triplets([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]) == True
    assert sol.merge_triplets([[1, 3, 2], [2, 5, 6]], [5, 5, 5]) == False
    assert sol.merge_triplets([[1, 1, 1]], [1, 1, 1]) == True
    assert sol.merge_triplets([[2, 2, 2], [1, 1, 1]], [2, 2, 2]) == True
    assert sol.merge_triplets([[3, 2, 2]], [2, 2, 2]) == False
    assert sol.merge_triplets([[2, 0, 0], [0, 2, 0], [0, 0, 2]], [2, 2, 2]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
