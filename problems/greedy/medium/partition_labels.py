"""
PROBLEM: Partition Labels (LeetCode 763)
Difficulty: Medium
Pattern: Greedy, String
Companies: Amazon, Google, Meta, Apple, Microsoft

You are given a string s. We want to partition the string into as many parts as possible
so that each letter appears in at most one part.

Return a list of integers representing the size of these parts.

Example 1:
    Input: s = "ababcbacaddefegdehijhklij"
    Output: [9,7,8]
    Explanation:
    The partition is "ababcbaca", "defegde", "hijhklij".
    This is a partition so that each letter appears in at most one part.

Example 2:
    Input: s = "eccbbcb"
    Output: [4,3]
    Explanation: The partition is "ecbb", "bcb".

Constraints:
- 1 <= s.length <= 500
- s consists of lowercase English letters.

Approach (Greedy):
1. Track last occurrence of each character
2. Iterate through string, track end boundary of current partition
3. Extend boundary if characters within current range appear later
4. When we reach the boundary, we can create a partition
5. Greedy choice: partition as early as possible while including all needed chars

Time: O(n) - preprocessing + single pass
Space: O(1) - at most 26 characters
"""

from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        """
        Partition string so each character appears in at most one part.

        Strategy:
        - Build map of last occurrence index for each character
        - Iterate through string, tracking the rightmost boundary needed
        - When current index reaches boundary, we can partition
        """
        # Find last occurrence of each character
        last_occurrence = {}
        for i, char in enumerate(s):
            last_occurrence[char] = i

        partitions = []
        start = 0
        end = 0

        for i, char in enumerate(s):
            # Expand end to include all occurrences of this character
            end = max(end, last_occurrence[char])

            # If we've reached the end boundary, create a partition
            if i == end:
                partitions.append(end - start + 1)
                start = end + 1

        return partitions


# Tests
def test():
    sol = Solution()

    assert sol.partitionLabels("ababcbacaddefegdehijhklij") == [9, 8, 8]
    assert sol.partitionLabels("eccbbcb") == [1, 6]
    assert sol.partitionLabels("a") == [1]
    assert sol.partitionLabels("abba") == [4]
    assert sol.partitionLabels("abc") == [1, 1, 1]
    assert sol.partitionLabels("aaabbbccc") == [3, 3, 3]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
