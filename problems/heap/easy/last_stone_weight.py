"""
PROBLEM: Last Stone Weight (LeetCode 1046)
Difficulty: Easy
Pattern: Heap
Companies: Amazon, Microsoft, Apple

You are given an array of integers stones where stones[i] is the weight of the
ith stone.

We are playing a game with the stones. On each turn, we choose the heaviest two
stones and smash them together. Suppose the heaviest two stones have weights x
and y with x <= y. The result of this smash is:
- If x == y, both stones are destroyed, and
- If x != y, the stone of weight x is destroyed, and the stone of weight y has
  new weight y - x.

At the end of the game, there is at most one stone left.

Return the weight of the last remaining stone. If there are no stones left,
return 0.

Example 1:
    Input: stones = [2,7,4,1,8,1]
    Output: 1
    Explanation:
    We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
    we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
    we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
    we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

Example 2:
    Input: stones = [1]
    Output: 1

Constraints:
- 1 <= stones.length <= 30
- 1 <= stones[i] <= 1000

Approach:
1. Use max heap to always get two heaviest stones
2. Python has min heap, so negate values for max heap
3. Pop two largest, calculate difference
4. If difference > 0, push back to heap
5. Continue until 0 or 1 stones remain

Time: O(n log n) - n operations, each log n
Space: O(n) - heap storage
"""

import heapq


class Solution:
    def last_stone_weight(self, stones: list[int]) -> int:
        # Convert to max heap by negating values
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)

        while len(max_heap) > 1:
            # Get two heaviest stones
            first = -heapq.heappop(max_heap)
            second = -heapq.heappop(max_heap)

            # If they're different, push the difference back
            if first != second:
                heapq.heappush(max_heap, -(first - second))

        # Return last stone weight or 0 if no stones left
        return -max_heap[0] if max_heap else 0


# Tests
def test():
    sol = Solution()

    # Test 1
    assert sol.last_stone_weight([2, 7, 4, 1, 8, 1]) == 1

    # Test 2
    assert sol.last_stone_weight([1]) == 1

    # Test 3
    assert sol.last_stone_weight([2, 2]) == 0

    # Test 4
    assert sol.last_stone_weight([1, 3]) == 2

    # Test 5
    assert sol.last_stone_weight([3, 7, 2]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
