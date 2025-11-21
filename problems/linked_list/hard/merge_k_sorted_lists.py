"""
PROBLEM: Merge k Sorted Lists (LeetCode 23)
Difficulty: Hard
Pattern: Linked List, Heap, Divide and Conquer
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

You are given an array of k linked-lists lists, each linked-list is sorted in
ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

Example 1:
    Input: lists = [[1,4,5],[1,3,4],[2,6]]
    Output: [1,1,2,3,4,4,5,6]
    Explanation: The linked-lists are:
    [
      1->4->5,
      1->3->4,
      2->6
    ]
    merging them into one sorted list:
    1->1->2->3->4->4->5->6

Example 2:
    Input: lists = []
    Output: []

Example 3:
    Input: lists = [[]]
    Output: []

Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order
- The sum of lists[i].length will not exceed 10^4

Approach:
1. Use min heap to efficiently get smallest element among k lists
2. Push first node from each list to heap
3. Pop smallest, add to result, push next node from that list
4. Continue until heap is empty

Alternative: Divide and conquer - merge lists in pairs

Time: O(N log k) - N total nodes, heap operations are O(log k)
Space: O(k) - heap size
"""

from typing import List, Optional
import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    # Make ListNode comparable for heap
    def __lt__(self, other):
        return self.val < other.val


class Solution:
    def merge_k_lists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None

        heap = []

        # Add first node from each list to heap
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, node)

        dummy = ListNode(0)
        current = dummy

        while heap:
            # Get smallest node
            node = heapq.heappop(heap)
            current.next = node
            current = current.next

            # Add next node from same list
            if node.next:
                heapq.heappush(heap, node.next)

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
    lists1 = [create_list([1,4,5]), create_list([1,3,4]), create_list([2,6])]
    result1 = sol.merge_k_lists(lists1)
    assert list_to_array(result1) == [1,1,2,3,4,4,5,6]

    # Test 2
    lists2 = []
    result2 = sol.merge_k_lists(lists2)
    assert list_to_array(result2) == []

    # Test 3
    lists3 = [create_list([])]
    result3 = sol.merge_k_lists(lists3)
    assert list_to_array(result3) == []

    # Test 4
    lists4 = [create_list([1,2,3]), create_list([4,5,6])]
    result4 = sol.merge_k_lists(lists4)
    assert list_to_array(result4) == [1,2,3,4,5,6]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
