"""
PROBLEM: Multiply Strings (LeetCode 43)
LeetCode: https://leetcode.com/problems/multiply-strings/
Difficulty: Medium
Pattern: String, Math, Simulation
Companies: Amazon, Apple, Bloomberg, Facebook, Google, Microsoft, Snapchat

Given two non-negative integers num1 and num2 represented as strings, return the
product of num1 and num2, also represented as a string.

Note: You must not use any built-in BigInteger library or convert the inputs to
integer directly.

Example 1:
    Input: num1 = "123", num2 = "456"
    Output: "56088"

Example 2:
    Input: num1 = "0", num2 = "0"
    Output: "0"

Example 3:
    Input: num1 = "2", num2 = "3"
    Output: "6"

Constraints:
- 1 <= num1.length, num2.length <= 200
- num1 and num2 consist of digits only
- Both num1 and num2 do not contain any leading zero, except the number 0 itself

Approach:
1. Create result array of size len(num1) + len(num2)
2. Multiply each digit of num1 with each digit of num2
3. Store product at appropriate position in result array
4. Handle carries by processing from right to left
5. Convert result array back to string, removing leading zeros

Time: O(m * n) where m and n are lengths of num1 and num2
Space: O(m + n) for result array
"""


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        result = [0] * (m + n)

        # Reverse multiply: process digits from right to left
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                # Multiply digits
                product = int(num1[i]) * int(num2[j])

                # Position in result array
                pos1 = i + j
                pos2 = i + j + 1

                # Add to existing value at pos2
                total = product + result[pos2]

                # Update values with carry
                result[pos2] = total % 10
                result[pos1] += total // 10

        # Convert result array to string
        result_str = "".join(map(str, result))

        # Remove leading zeros
        return result_str.lstrip("0") or "0"


# Tests
def test():
    sol = Solution()

    # Test 1
    assert sol.multiply("123", "456") == "56088"

    # Test 2
    assert sol.multiply("0", "0") == "0"

    # Test 3
    assert sol.multiply("2", "3") == "6"

    # Test 4
    assert sol.multiply("0", "123") == "0"

    # Test 5
    assert sol.multiply("999", "999") == "998001"

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
