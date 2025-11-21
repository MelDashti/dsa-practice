"""
PROBLEM: Linked List Cycle (LeetCode 141)
LeetCode: https://leetcode.com/problems/linked-list-cycle/
Difficulty: Easy
Pattern: Linked List, Two Pointers
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be
reached again by continuously following the next pointer. Internally, pos is used
to denote the index of the node that tail's next pointer is connected to. Note that
pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

Example 1:
    Input: head = [3,2,0,-4], pos = 1
    Output: true
    Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

Example 2:
    Input: head = [1,2], pos = 0
    Output: true
    Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.

Example 3:
    Input: head = [1], pos = -1
    Output: false
    Explanation: There is no cycle in the linked list.

Constraints:
- The number of the nodes in the list is in the range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list

Follow up: Can you solve it using O(1) (i.e. constant) memory?

Approach:
1. Use Floyd's Cycle Detection (slow and fast pointers)
2. Slow moves one step, fast moves two steps
3. If they meet, there's a cycle
4. If fast reaches end, no cycle

Time: O(n) - visit each node at most once
Space: O(1) - only using two pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def has_cycle(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return False

        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False


# Tests
def test():
    sol = Solution()

    # Test 1: Cycle at position 1
    head1 = ListNode(3)
    node2 = ListNode(2)
    node3 = ListNode(0)
    node4 = ListNode(-4)
    head1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2  # Creates cycle
    assert sol.has_cycle(head1) == True

    # Test 2: Cycle at position 0
    head2 = ListNode(1)
    node2_2 = ListNode(2)
    head2.next = node2_2
    node2_2.next = head2  # Creates cycle
    assert sol.has_cycle(head2) == True

    # Test 3: No cycle
    head3 = ListNode(1)
    assert sol.has_cycle(head3) == False

    # Test 4: Empty list
    assert sol.has_cycle(None) == False

    # Test 5: List with no cycle
    head5 = ListNode(1)
    head5.next = ListNode(2)
    head5.next.next = ListNode(3)
    assert sol.has_cycle(head5) == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
