"""
PROBLEM: Hand of Straights (LeetCode 846)
Difficulty: Medium
Pattern: Greedy, Sorting
Companies: Google, Meta, Amazon

Alice has some number of cards and she wants to rearrange the cards into groups so that
each group is one of the following sequences:

1. Any sequence of consecutive cards of length groupSize.
   - For example, if she has cards [17,13,11,2,3,5,7] and groupSize = 5, one valid group
     would be [13,11,2,3,5] since they form a sequence of 5 consecutive cards.

Determine if she can successfully divide all the cards into groups of consecutive cards
of length groupSize, or return false otherwise.

Example 1:
    Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
    Output: true
    Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]

Example 2:
    Input: hand = [1,2,3,4,5], groupSize = 4
    Output: false
    Explanation: Alice's hand can't be rearranged into groups of 4.

Constraints:
- 1 <= hand.length <= 10^4
- 0 <= hand[i] <= 10^9
- 1 <= groupSize <= hand.length

Approach (Greedy with Counting):
1. Check if total cards divisible by groupSize
2. Count frequency of each card value
3. Sort unique card values
4. For each card in sorted order (smallest first):
   - Try to form a group starting with this card
   - Greedy: always start new groups with smallest available card
   - Verify we have consecutive cards needed

Time: O(n log n) - sorting
Space: O(n) - frequency map
"""

from typing import List
from collections import Counter


class Solution:
    def is_n_straight_hand(self, hand: List[int], groupSize: int) -> bool:
        """
        Determine if cards can be divided into groups of consecutive cards.

        Strategy:
        - Use frequency counter to track available cards
        - Iterate through sorted unique cards
        - For each card, greedily form as many groups as possible
        - Each group must have consecutive cards
        """
        # Base check: total cards must be divisible by groupSize
        if len(hand) % groupSize != 0:
            return False

        # Count frequency of each card
        card_count = Counter(hand)

        # Sort unique cards
        sorted_cards = sorted(card_count.keys())

        # Try to form groups
        for card in sorted_cards:
            # If this card is still available
            while card_count[card] > 0:
                # Try to form a group starting with this card
                for i in range(groupSize):
                    current_card = card + i

                    # Check if we have the required card
                    if card_count[current_card] == 0:
                        return False

                    # Use one copy of this card
                    card_count[current_card] -= 1

        return True


# Tests
def test():
    sol = Solution()

    assert sol.is_n_straight_hand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3) == True
    assert sol.is_n_straight_hand([1, 2, 3, 4, 5], 4) == False
    assert sol.is_n_straight_hand([1, 1, 2, 2, 3, 3, 4, 4], 4) == True
    assert sol.is_n_straight_hand([1, 2, 3], 2) == False
    assert sol.is_n_straight_hand([1], 1) == True
    assert sol.is_n_straight_hand([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
