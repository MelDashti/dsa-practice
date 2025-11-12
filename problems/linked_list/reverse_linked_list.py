"""
PROBLEM: Reverse Linked List (LeetCode 206)
Difficulty: Easy
Pattern: Linked List
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
    Input: head = [1,2,3,4,5]
    Output: [5,4,3,2,1]

Example 2:
    Input: head = [1,2]
    Output: [2,1]

Example 3:
    Input: head = []
    Output: []

Constraints:
- The number of nodes in the list is the range [0, 5000]
- -5000 <= Node.val <= 5000

Approach:
1. Use three pointers: prev (None), current (head), next
2. Iterate through list
3. For each node, reverse its next pointer to point to prev
4. Move all three pointers forward
5. Return prev (new head)

Time: O(n) - single pass through list
Space: O(1) - only using pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        current = head

        while current:
            next_node = current.next  # Save next node
            current.next = prev       # Reverse pointer
            prev = current            # Move prev forward
            current = next_node       # Move current forward

        return prev


# Tests
def test():
    sol = Solution()

    # Helper function to create linked list from array
    def create_list(arr):
        if not arr:
            return None
        head = ListNode(arr[0])
        current = head
        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    # Helper function to convert linked list to array
    def list_to_array(head):
        arr = []
        current = head
        while current:
            arr.append(current.val)
            current = current.next
        return arr

    # Test 1
    head1 = create_list([1,2,3,4,5])
    result1 = sol.reverseList(head1)
    assert list_to_array(result1) == [5,4,3,2,1]

    # Test 2
    head2 = create_list([1,2])
    result2 = sol.reverseList(head2)
    assert list_to_array(result2) == [2,1]

    # Test 3
    head3 = create_list([])
    result3 = sol.reverseList(head3)
    assert list_to_array(result3) == []

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
