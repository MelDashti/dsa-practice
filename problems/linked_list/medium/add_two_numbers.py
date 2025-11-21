"""
PROBLEM: Add Two Numbers (LeetCode 2)
LeetCode: https://leetcode.com/problems/add-two-numbers/
Difficulty: Medium
Pattern: Linked List, Math
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single
digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [7,0,8]
    Explanation: 342 + 465 = 807

Example 2:
    Input: l1 = [0], l2 = [0]
    Output: [0]

Example 3:
    Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
    Output: [8,9,9,9,0,0,0,1]

Constraints:
- The number of nodes in each linked list is in the range [1, 100]
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros

Approach:
1. Use dummy node to build result list
2. Iterate through both lists simultaneously
3. Add corresponding digits and carry
4. Create new node with sum % 10
5. Update carry = sum // 10
6. Handle remaining digits and final carry

Time: O(max(m, n)) - iterate through longer list
Space: O(max(m, n)) - result list
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def add_two_numbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            total = val1 + val2 + carry
            carry = total // 10
            current.next = ListNode(total % 10)

            current = current.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

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
    l1 = create_list([2,4,3])
    l2 = create_list([5,6,4])
    result1 = sol.add_two_numbers(l1, l2)
    assert list_to_array(result1) == [7,0,8]

    # Test 2
    l3 = create_list([0])
    l4 = create_list([0])
    result2 = sol.add_two_numbers(l3, l4)
    assert list_to_array(result2) == [0]

    # Test 3
    l5 = create_list([9,9,9,9,9,9,9])
    l6 = create_list([9,9,9,9])
    result3 = sol.add_two_numbers(l5, l6)
    assert list_to_array(result3) == [8,9,9,9,0,0,0,1]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
