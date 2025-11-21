"""
PROBLEM: Merge Two Sorted Lists (LeetCode 21)
LeetCode: https://leetcode.com/problems/merge-two-sorted-lists/
Difficulty: Easy
Pattern: Linked List
Companies: Amazon, Microsoft, Apple, Facebook, Google, Adobe

You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing
together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
    Input: list1 = [1,2,4], list2 = [1,3,4]
    Output: [1,1,2,3,4,4]

Example 2:
    Input: list1 = [], list2 = []
    Output: []

Example 3:
    Input: list1 = [], list2 = [0]
    Output: [0]

Constraints:
- The number of nodes in both lists is in the range [0, 50]
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order

Approach:
1. Create dummy node to simplify edge cases
2. Use current pointer starting at dummy
3. Compare nodes from both lists
4. Attach smaller node to current and move that list pointer forward
5. Move current pointer forward
6. After loop, attach remaining nodes from non-empty list
7. Return dummy.next

Time: O(n + m) - visit each node once
Space: O(1) - only using pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def merge_two_lists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next

        # Attach remaining nodes
        if list1:
            current.next = list1
        if list2:
            current.next = list2

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
    list1 = create_list([1,2,4])
    list2 = create_list([1,3,4])
    result1 = sol.merge_two_lists(list1, list2)
    assert list_to_array(result1) == [1,1,2,3,4,4]

    # Test 2
    list3 = create_list([])
    list4 = create_list([])
    result2 = sol.merge_two_lists(list3, list4)
    assert list_to_array(result2) == []

    # Test 3
    list5 = create_list([])
    list6 = create_list([0])
    result3 = sol.merge_two_lists(list5, list6)
    assert list_to_array(result3) == [0]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
