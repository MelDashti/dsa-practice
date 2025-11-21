"""
PROBLEM: Happy Number (LeetCode 202)
Difficulty: Easy
Pattern: Hash Set, Cycle Detection, Math
Companies: Amazon, Airbnb, LinkedIn, Uber

Write an algorithm to determine if a number n is happy.

A happy number is defined by the following process:
1. Starting with any positive integer, replace the number by the sum of the squares
   of its digits
2. Repeat the process until the number equals 1 (happy) or it loops endlessly in a
   cycle which does not include 1 (unhappy)

A number which loops endlessly in a cycle which does not include 1 is unhappy.

Example 1:
    Input: n = 7
    Output: true
    Explanation: 7 → 49 → 97 → 130 → 10 → 1

Example 2:
    Input: n = 2
    Output: false

Constraints:
- 1 <= n <= 2^31 - 1

Approach:
1. Keep track of seen numbers in a set
2. Repeatedly compute sum of squares of digits
3. If we reach 1, number is happy
4. If we see a number we've seen before, we're in a cycle (unhappy)

Time: O(log n) - number of iterations until cycle or happy
Space: O(log n) - for storing seen numbers
"""


class Solution:
    def is_happy(self, n: int) -> bool:
        def get_next(num):
            total_sum = 0
            while num > 0:
                digit = num % 10
                total_sum += digit * digit
                num //= 10
            return total_sum

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = get_next(n)

        return n == 1


# Tests
def test():
    sol = Solution()

    # Test 1: Happy number
    assert sol.is_happy(7) == True

    # Test 2: Unhappy number
    assert sol.is_happy(2) == False

    # Test 3: Single digit happy
    assert sol.is_happy(1) == True

    # Test 4: Another happy number
    assert sol.is_happy(19) == True

    # Test 5: Another unhappy number
    assert sol.is_happy(3) == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
