"""
PROBLEM: Reorder List (LeetCode 143)
Difficulty: Medium
Pattern: Linked List
Companies: Amazon, Facebook, Microsoft, Google, Bloomberg

You are given the head of a singly linked-list. The list can be represented as:
L0 → L1 → ... → Ln-1 → Ln

Reorder the list to be on the following form:
L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...

You may not modify the values in the list's nodes. Only nodes themselves may be changed.

Example 1:
    Input: head = [1,2,3,4]
    Output: [1,4,2,3]

Example 2:
    Input: head = [1,2,3,4,5]
    Output: [1,5,2,4,3]

Constraints:
- The number of nodes in the list is in the range [1, 5 * 10^4]
- 1 <= Node.val <= 1000

Approach:
1. Find the middle of the list using slow/fast pointers
2. Reverse the second half of the list
3. Merge the two halves by alternating nodes
4. First half: head to mid, Second half: reversed from mid+1 to end

Time: O(n) - three passes (find mid, reverse, merge)
Space: O(1) - only using pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorder_list(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return

        # Step 1: Find middle of list
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse second half
        second = slow.next
        slow.next = None  # Split the list
        prev = None
        while second:
            next_node = second.next
            second.next = prev
            prev = second
            second = next_node
        second = prev  # New head of reversed second half

        # Step 3: Merge two halves
        first = head
        while second:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next = temp1
            first = temp1
            second = temp2


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
    head1 = create_list([1,2,3,4])
    sol.reorder_list(head1)
    assert list_to_array(head1) == [1,4,2,3]

    # Test 2
    head2 = create_list([1,2,3,4,5])
    sol.reorder_list(head2)
    assert list_to_array(head2) == [1,5,2,4,3]

    # Test 3
    head3 = create_list([1,2])
    sol.reorder_list(head3)
    assert list_to_array(head3) == [1,2]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
