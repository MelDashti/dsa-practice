"""
PROBLEM: Reverse Nodes in k-Group (LeetCode 25)
Difficulty: Hard
Pattern: Linked List
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

Given the head of a linked list, reverse the nodes of the list k at a time, and
return the modified list.

k is a positive integer and is less than or equal to the length of the linked list.
If the number of nodes is not a multiple of k then left-out nodes, in the end,
should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

Example 1:
    Input: head = [1,2,3,4,5], k = 2
    Output: [2,1,4,3,5]

Example 2:
    Input: head = [1,2,3,4,5], k = 3
    Output: [3,2,1,4,5]

Constraints:
- The number of nodes in the list is n
- 1 <= k <= n <= 5000
- 0 <= Node.val <= 1000

Follow-up: Can you solve the problem in O(1) extra memory space?

Approach:
1. Check if there are k nodes remaining
2. If yes, reverse those k nodes
3. Connect with previous group and move to next group
4. If no, leave remaining nodes as is
5. Use dummy node to handle edge cases

Time: O(n) - visit each node twice (count and reverse)
Space: O(1) - only using pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverse_k_group(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # Check if there are k nodes remaining
            kth = self.get_kth(group_prev, k)
            if not kth:
                break

            group_next = kth.next

            # Reverse k nodes
            prev, curr = kth.next, group_prev.next
            while curr != group_next:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp

            # Connect with previous group
            tmp = group_prev.next
            group_prev.next = kth
            group_prev = tmp

        return dummy.next

    def get_kth(self, curr, k):
        """Get the kth node from curr"""
        while curr and k > 0:
            curr = curr.next
            k -= 1
        return curr


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
    result1 = sol.reverse_k_group(head1, 2)
    assert list_to_array(result1) == [2,1,4,3,5]

    # Test 2
    head2 = create_list([1,2,3,4,5])
    result2 = sol.reverse_k_group(head2, 3)
    assert list_to_array(result2) == [3,2,1,4,5]

    # Test 3
    head3 = create_list([1,2,3,4,5])
    result3 = sol.reverse_k_group(head3, 1)
    assert list_to_array(result3) == [1,2,3,4,5]

    # Test 4
    head4 = create_list([1])
    result4 = sol.reverse_k_group(head4, 1)
    assert list_to_array(result4) == [1]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
