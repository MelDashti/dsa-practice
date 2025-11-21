"""
PROBLEM: Copy List with Random Pointer (LeetCode 138)
LeetCode: https://leetcode.com/problems/copy-list-with-random-pointer/
Difficulty: Medium
Pattern: Linked List, Hash Table
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg

A linked list of length n is given such that each node contains an additional
random pointer, which could point to any node in the list, or null.

Construct a deep copy of the list. The deep copy should consist of exactly n
brand new nodes, where each new node has its value set to the value of its
corresponding original node. Both the next and random pointer of the new nodes
should point to new nodes in the copied list such that the pointers in the
original list and copied list represent the same list state. None of the
pointers in the new list should point to nodes in the original list.

Return the head of the copied linked list.

Example 1:
    Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
    Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]

Example 2:
    Input: head = [[1,1],[2,1]]
    Output: [[1,1],[2,1]]

Example 3:
    Input: head = [[3,null],[3,0],[3,null]]
    Output: [[3,null],[3,0],[3,null]]

Constraints:
- 0 <= n <= 1000
- -10^4 <= Node.val <= 10^4
- Node.random is null or is pointing to some node in the linked list

Approach:
1. Create a hash map to store mapping from original to copied nodes
2. First pass: create all new nodes and store in map
3. Second pass: connect next and random pointers using map
4. Return copied head from map

Time: O(n) - two passes through list
Space: O(n) - hash map storage
"""

from typing import Optional


class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copy_random_list(self, head: Optional[Node]) -> Optional[Node]:
        if not head:
            return None

        # Map from original node to copied node
        old_to_new = {}

        # First pass: create all nodes
        current = head
        while current:
            old_to_new[current] = Node(current.val)
            current = current.next

        # Second pass: connect next and random pointers
        current = head
        while current:
            if current.next:
                old_to_new[current].next = old_to_new[current.next]
            if current.random:
                old_to_new[current].random = old_to_new[current.random]
            current = current.next

        return old_to_new[head]


# Tests
def test():
    sol = Solution()

    # Helper function to create list with random pointers
    def create_list_with_random(values):
        if not values:
            return None

        nodes = [Node(val) for val, _ in values]

        # Connect next pointers
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]

        # Connect random pointers
        for i, (_, random_idx) in enumerate(values):
            if random_idx is not None:
                nodes[i].random = nodes[random_idx]

        return nodes[0]

    # Helper function to verify deep copy
    def verify_copy(original, copy):
        if not original and not copy:
            return True
        if not original or not copy:
            return False

        orig_nodes = []
        copy_nodes = []

        curr = original
        while curr:
            orig_nodes.append(curr)
            curr = curr.next

        curr = copy
        while curr:
            copy_nodes.append(curr)
            curr = curr.next

        if len(orig_nodes) != len(copy_nodes):
            return False

        for i in range(len(orig_nodes)):
            # Check values match
            if orig_nodes[i].val != copy_nodes[i].val:
                return False
            # Check nodes are different objects
            if orig_nodes[i] is copy_nodes[i]:
                return False
            # Check random pointer structure matches
            if orig_nodes[i].random is None:
                if copy_nodes[i].random is not None:
                    return False
            else:
                orig_random_idx = orig_nodes.index(orig_nodes[i].random)
                if copy_nodes[i].random is None:
                    return False
                copy_random_idx = copy_nodes.index(copy_nodes[i].random)
                if orig_random_idx != copy_random_idx:
                    return False

        return True

    # Test 1
    head1 = create_list_with_random([(7, None), (13, 0), (11, 4), (10, 2), (1, 0)])
    result1 = sol.copy_random_list(head1)
    assert verify_copy(head1, result1)

    # Test 2
    head2 = create_list_with_random([(1, 1), (2, 1)])
    result2 = sol.copy_random_list(head2)
    assert verify_copy(head2, result2)

    # Test 3
    head3 = create_list_with_random([(3, None), (3, 0), (3, None)])
    result3 = sol.copy_random_list(head3)
    assert verify_copy(head3, result3)

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
