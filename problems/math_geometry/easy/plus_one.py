"""
PROBLEM: Plus One (LeetCode 66)
Difficulty: Easy
Pattern: Array, Math, Simulation
Companies: Amazon, Apple, Facebook, Google, Microsoft

You are given a large integer represented as an integer array digits, where each
digits[i] is the ith digit of the integer. The digits are ordered from most
significant to least significant in left-to-right order. The large integer does
not contain a leading zero.

Increment the large integer by one and return the resulting array of digits.

Example 1:
    Input: digits = [1,2,3]
    Output: [1,2,4]

Example 2:
    Input: digits = [4,3,2,1]
    Output: [4,3,2,2]

Example 3:
    Input: digits = [9]
    Output: [1,0]

Example 4:
    Input: digits = [9,9,9]
    Output: [1,0,0,0]

Constraints:
- 1 <= digits.length <= 100
- 0 <= digits[i] <= 9
- digits does not contain a leading zero

Approach:
1. Start from the rightmost digit (least significant)
2. Add 1 to it
3. Handle carry: if digit becomes 10, set it to 0 and carry 1 to next digit
4. Continue from right to left
5. If we still have carry after processing all digits, insert 1 at the beginning

Time: O(n) where n is length of digits
Space: O(1) excluding output array
"""


class Solution:
    def plus_one(self, digits: list[int]) -> list[int]:
        # Start from the rightmost digit
        for i in range(len(digits) - 1, -1, -1):
            digits[i] += 1

            # If no carry needed, we're done
            if digits[i] < 10:
                return digits

            # Handle carry
            digits[i] = 0

        # If we reach here, we had carry all the way
        return [1] + digits


# Tests
def test():
    sol = Solution()

    # Test 1
    assert sol.plus_one([1, 2, 3]) == [1, 2, 4]

    # Test 2
    assert sol.plus_one([4, 3, 2, 1]) == [4, 3, 2, 2]

    # Test 3
    assert sol.plus_one([9]) == [1, 0]

    # Test 4
    assert sol.plus_one([9, 9, 9]) == [1, 0, 0, 0]

    # Test 5
    assert sol.plus_one([8, 9, 9]) == [9, 0, 0]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
