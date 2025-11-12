"""
PROBLEM: Jump Game II (LeetCode 45)
Difficulty: Medium
Pattern: Greedy
Companies: Google, Amazon, Apple, Microsoft, Meta

You are given a 0-indexed array of integers nums of length n. You are initially positioned
at nums[0]. Each element nums[i] represents the maximum length of a forward jump from index i.

Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such
that you can always reach nums[n - 1].

Example 1:
    Input: nums = [2,3,1,1,4]
    Output: 2
    Explanation: The minimum number of jumps to reach the last index is 2.
                 Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
    Input: nums = [2,3,0,6,9]
    Output: 2

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 1000

Approach (Greedy BFS):
1. Use two pointers: current_end (end of jump range), farthest (furthest we can reach)
2. For each position in current range, update farthest reachable position
3. When we reach current_end, increment jumps and extend range
4. Continue until we reach or pass the end
5. Greedy choice: minimize jumps by maximizing reach

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        Return minimum number of jumps to reach last index.

        Strategy:
        - current_end: the end of range for current jump count
        - farthest: furthest position we can reach from current range
        - When we exhaust current_end, we need another jump
        """
        jumps = 0
        current_end = 0
        farthest = 0

        # Don't need to check the last element
        for i in range(len(nums) - 1):
            # Update furthest position reachable
            farthest = max(farthest, i + nums[i])

            # If we've reached the end of current jump range
            if i == current_end:
                jumps += 1
                current_end = farthest

                # Early exit if we can already reach the end
                if current_end >= len(nums) - 1:
                    break

        return jumps


# Tests
def test():
    sol = Solution()

    assert sol.jump([2, 3, 1, 1, 4]) == 2
    assert sol.jump([2, 3, 0, 6, 9]) == 2
    assert sol.jump([1, 1, 1, 0]) == 3
    assert sol.jump([2, 0, 0]) == 1
    assert sol.jump([1, 2, 1, 0]) == 2
    assert sol.jump([1, 3, 1, 1, 1]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
