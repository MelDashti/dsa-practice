"""
PROBLEM: Letter Combinations of a Phone Number (LeetCode 17)
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Facebook, Microsoft, Apple, Google

Given a string containing digits from 2-9 inclusive, return all possible
letter combinations that the number could represent. Return the answer in
any order.

A mapping of digits to letters (just like on the telephone buttons) is given
below. Note that 1 does not map to any letters.

2: "abc"
3: "def"
4: "ghi"
5: "jkl"
6: "mno"
7: "pqrs"
8: "tuv"
9: "wxyz"

Example 1:
    Input: digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
    Input: digits = ""
    Output: []

Example 3:
    Input: digits = "2"
    Output: ["a","b","c"]

Constraints:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9']

Approach:
1. Create a mapping of digits to letters
2. Use backtracking to build all combinations
3. At each step, try all letters mapped to current digit
4. Recursively build combination for remaining digits
5. Base case: when combination length equals digits length, add to result
6. Return empty list if input is empty

Time: O(4^n * n) where n is length of digits, 4 is max letters per digit
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def letter_combinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        # Digit to letters mapping
        phone_map = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }

        result = []
        current = []

        def backtrack(index):
            # Base case: combination is complete
            if index == len(digits):
                result.append(''.join(current))
                return

            # Get letters for current digit
            letters = phone_map[digits[index]]

            # Try each letter
            for letter in letters:
                current.append(letter)
                backtrack(index + 1)
                current.pop()

        backtrack(0)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.letter_combinations("23")
    expected1 = ["ad","ae","af","bd","be","bf","cd","ce","cf"]
    assert sorted(result1) == sorted(expected1)

    # Test case 2
    result2 = sol.letter_combinations("")
    assert result2 == []

    # Test case 3
    result3 = sol.letter_combinations("2")
    expected3 = ["a","b","c"]
    assert sorted(result3) == sorted(expected3)

    # Test case 4
    result4 = sol.letter_combinations("7")
    expected4 = ["p","q","r","s"]
    assert sorted(result4) == sorted(expected4)

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
