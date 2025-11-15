"""
PROBLEM: Reorganize String (LeetCode 767)
Difficulty: Medium
Pattern: Greedy, Heap/Priority Queue
Companies: Amazon, Meta, Google, Bloomberg, Apple

DESCRIPTION:
Given a string s, rearrange the characters of s so that any two adjacent characters
are not the same.

Return any possible rearrangement of s or return "" if not possible.

EXAMPLES:
Example 1:
Input: s = "aab"
Output: "aba"

Example 2:
Input: s = "aaab"
Output: ""

CONSTRAINTS:
- 1 <= s.length <= 500
- s consists of lowercase English letters

APPROACH:
Use a greedy approach with a max heap:
1. Count frequency of each character
2. Use max heap to always pick the character with highest frequency
3. Alternate between top 2 most frequent characters
4. If at any point we can't find a valid character, return ""

Key insight: If max frequency > (len(s) + 1) / 2, impossible to rearrange

TIME COMPLEXITY: O(n log k) where k = 26 (unique characters)
- O(n) to count frequencies
- O(n log 26) ≈ O(n) for heap operations

SPACE COMPLEXITY: O(k) where k = 26
- Hash map and heap for character frequencies

WHY THIS PROBLEM IS IMPORTANT:
- Very frequently asked at Amazon and Meta
- Tests greedy thinking with heap data structure
- Common pattern for "arrangement" problems
- Real-world application in task scheduling
"""

from typing import Counter
import heapq


class Solution:
    def reorganizeString(self, s: str) -> str:
        """
        Reorganize string so no two adjacent characters are same.
        """
        # Count character frequencies
        freq = Counter(s)

        # Check if reorganization is possible
        max_freq = max(freq.values())
        if max_freq > (len(s) + 1) // 2:
            return ""

        # Max heap: store (-frequency, character)
        max_heap = [(-count, char) for char, count in freq.items()]
        heapq.heapify(max_heap)

        result = []
        prev_count, prev_char = 0, ''

        while max_heap:
            # Get character with highest frequency
            count, char = heapq.heappop(max_heap)
            result.append(char)

            # Add back previous character if it still has occurrences
            if prev_count < 0:
                heapq.heappush(max_heap, (prev_count, prev_char))

            # Update previous for next iteration
            prev_count = count + 1  # Increase since count is negative
            prev_char = char

        return ''.join(result)


class SolutionOptimized:
    """
    Optimized O(n) solution using even-odd positioning.
    """

    def reorganizeString(self, s: str) -> str:
        """
        Place most frequent characters at even indices, then odd indices.
        """
        freq = Counter(s)
        max_freq = max(freq.values())

        if max_freq > (len(s) + 1) // 2:
            return ""

        # Sort characters by frequency (descending)
        sorted_chars = sorted(freq.items(), key=lambda x: -x[1])

        result = [''] * len(s)
        index = 0

        # Place characters starting from most frequent
        for char, count in sorted_chars:
            for _ in range(count):
                result[index] = char
                index += 2  # Place at even positions first

                # When even positions filled, switch to odd
                if index >= len(s):
                    index = 1

        return ''.join(result)


def test_reorganize_string():
    """Test cases for Reorganize String"""
    solution = Solution()
    solution_opt = SolutionOptimized()

    def is_valid(s: str, original: str) -> bool:
        """Check if reorganized string is valid"""
        if len(s) != len(original):
            return False
        # Check no adjacent characters are same
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                return False
        # Check same character frequencies
        return Counter(s) == Counter(original)

    test_cases = [
        ("aab", True),
        ("aaab", False),
        ("vvvlo", True),
        ("a", True),
        ("aa", True),
        ("aaa", False),
        ("aaabb", True),
        ("bbbbbbbbbbaaaaaaaaa", False),
    ]

    for s, should_succeed in test_cases:
        result1 = solution.reorganizeString(s)
        result2 = solution_opt.reorganizeString(s)

        if should_succeed:
            assert is_valid(result1, s), f"Invalid result for {s}: {result1}"
            assert is_valid(result2, s), f"Invalid result for {s}: {result2}"
        else:
            assert result1 == "", f"Should return empty for {s}"
            assert result2 == "", f"Should return empty for {s}"

    print("✅ All test cases passed!")


if __name__ == "__main__":
    test_reorganize_string()
