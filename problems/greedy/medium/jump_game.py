"""
PROBLEM: Jump Game (LeetCode 55)
LeetCode: https://leetcode.com/problems/jump-game/
Difficulty: Medium
Pattern: Greedy, Dynamic Programming
Companies: Google, Amazon, Microsoft, Apple, Meta

You are given an integer array nums. You are initially positioned at the array's first index,
and each element in the array represents your maximum jump length from that position.

Determine if you can reach the last index of the array. Return true if you can reach the last
index, or false otherwise.

Example 1:
    Input: nums = [2,3,1,1,4]
    Output: true
    Explanation: Jump 1 step from index 0 to 1, then 3 steps to last index.

Example 2:
    Input: nums = [3,2,1,0,4]
    Output: false
    Explanation: Will always arrive at index 3. Maximum jump length is 0, so can't proceed.

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

Approach (Greedy):
1. Track the furthest index we can reach
2. Iterate through array, updating max reachable index
3. If current index is unreachable, return false
4. If we can reach the end, return true
5. Greedy choice: always try to reach furthest possible position

Time: O(n) - single pass
Space: O(1) - constant space
"""

from typing import List


class Solution:
    def can_jump(self, nums: List[int]) -> bool:
        """
        Determine if we can reach the last index.

        Strategy:
        - max_reach tracks the furthest index we can reach
        - For each index we can reach, update max_reach
        - If at any point max_reach < current index, we're stuck
        """
        max_reach = 0

        for i in range(len(nums)):
            # If current index is beyond what we can reach, impossible
            if i > max_reach:
                return False

            # Update the furthest we can reach from current position
            max_reach = max(max_reach, i + nums[i])

            # If we can reach or pass the last index, success
            if max_reach >= len(nums) - 1:
                return True

        return True


# Tests
def test():
    sol = Solution()

    assert sol.can_jump([2, 3, 1, 1, 4]) == True
    assert sol.can_jump([3, 2, 1, 0, 4]) == False
    assert sol.can_jump([0]) == True
    assert sol.can_jump([2, 0, 0]) == True
    assert sol.can_jump([0, 2, 3]) == False
    assert sol.can_jump([2, 5, 0, 0]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
