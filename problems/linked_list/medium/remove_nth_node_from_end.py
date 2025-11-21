"""
PROBLEM: Remove Nth Node From End of List (LeetCode 19)
Difficulty: Medium
Pattern: Linked List, Two Pointers
Companies: Amazon, Microsoft, Apple, Facebook, Google, Adobe

Given the head of a linked list, remove the nth node from the end of the list
and return its head.

Example 1:
    Input: head = [1,2,3,4,5], n = 2
    Output: [1,2,3,5]

Example 2:
    Input: head = [1], n = 1
    Output: []

Example 3:
    Input: head = [1,2], n = 1
    Output: [1]

Constraints:
- The number of nodes in the list is sz
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

Follow up: Could you do this in one pass?

Approach:
1. Use two pointers with dummy node to handle edge cases
2. Move fast pointer n steps ahead
3. Move both pointers until fast reaches end
4. Slow pointer will be at node before target
5. Remove target node by adjusting pointers

Time: O(n) - single pass through list
Space: O(1) - only using pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def remove_nth_from_end(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        slow = dummy
        fast = dummy

        # Move fast pointer n steps ahead
        for _ in range(n):
            fast = fast.next

        # Move both pointers until fast reaches end
        while fast.next:
            slow = slow.next
            fast = fast.next

        # Remove nth node from end
        slow.next = slow.next.next

        return dummy.next


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
    result1 = sol.remove_nth_from_end(head1, 2)
    assert list_to_array(result1) == [1,2,3,5]

    # Test 2
    head2 = create_list([1])
    result2 = sol.remove_nth_from_end(head2, 1)
    assert list_to_array(result2) == []

    # Test 3
    head3 = create_list([1,2])
    result3 = sol.remove_nth_from_end(head3, 1)
    assert list_to_array(result3) == [1]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
