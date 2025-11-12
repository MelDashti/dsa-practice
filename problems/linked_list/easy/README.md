# Linked List - Easy Problems

## Overview

Easy linked list problems introduce fundamental operations on this dynamic data structure. Understanding linked lists is crucial as they form the foundation for many advanced data structures (stacks, queues, graphs) and algorithms.

## Key Concepts

### What is a Linked List?

A linked list is a linear data structure where elements (nodes) are not stored contiguously:
- Each node contains data and a reference (pointer) to the next node
- Head points to the first node
- Last node points to null/None
- Dynamic size (grows and shrinks as needed)

**Node Structure**:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Linked List vs Array

| Aspect | Array | Linked List |
|--------|-------|-------------|
| Access | O(1) by index | O(n) - must traverse |
| Insertion (beginning) | O(n) - shift elements | O(1) - update pointers |
| Insertion (end) | O(1) amortized | O(n) - must find end |
| Deletion | O(n) - shift elements | O(1) if have reference |
| Memory | Contiguous | Scattered |
| Cache | Cache-friendly | Cache-unfriendly |

### When to Use Linked Lists

- Frequent insertions/deletions at beginning
- Unknown or dynamic size
- Implementing stacks, queues, or hash tables
- Memory-constrained environments (no reallocation)
- When random access is not needed

## Common Linked List Patterns

### 1. Two Pointer (Fast & Slow)
Used for: Finding middle, cycle detection, kth from end
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is now at middle
```

### 2. Dummy Node
Simplifies edge cases (operations at head)
```python
dummy = ListNode(0)
dummy.next = head
# Operate on dummy.next
return dummy.next
```

### 3. Previous Pointer Tracking
For deletions and reversals
```python
prev = None
curr = head
while curr:
    next_temp = curr.next
    curr.next = prev
    prev = curr
    curr = next_temp
```

## Problems in This Section

### 1. Reverse Linked List (LC 206)
**Concept**: Pointer manipulation and reversal

**Key Ideas**:
- Reverse the direction of all next pointers
- Track three pointers: prev, curr, next
- Iterative: O(n) time, O(1) space
- Recursive: O(n) time, O(n) space (call stack)

**Pattern**: Basic pointer manipulation

**Iterative Approach**:
```python
def reverseList(head):
    prev = None
    curr = head

    while curr:
        next_temp = curr.next  # Save next
        curr.next = prev       # Reverse pointer
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward

    return prev  # New head
```

**Visualization**:
```
Original: 1 → 2 → 3 → 4 → 5 → None

Step 1: None ← 1   2 → 3 → 4 → 5 → None
             prev curr

Step 2: None ← 1 ← 2   3 → 4 → 5 → None
                  prev curr

Step 3: None ← 1 ← 2 ← 3   4 → 5 → None
                      prev curr

Continue until curr is None, return prev
```

**Recursive Approach**:
```python
def reverseList(head):
    if not head or not head.next:
        return head

    new_head = reverseList(head.next)
    head.next.next = head
    head.next = None

    return new_head
```

**Time Complexity**: O(n)
**Space Complexity**: O(1) iterative, O(n) recursive

---

### 2. Merge Two Sorted Lists (LC 21)
**Concept**: Merging with dummy node pattern

**Key Ideas**:
- Use dummy node to simplify edge cases
- Compare heads of both lists
- Attach smaller node to result
- Move pointer in the list we took from
- Attach remaining list at the end

**Pattern**: Two-pointer with dummy node

**Implementation**:
```python
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Attach remaining nodes
    current.next = l1 if l1 else l2

    return dummy.next
```

**Visualization**:
```
l1: 1 → 3 → 5
l2: 2 → 4 → 6

Result: dummy → 1 → 2 → 3 → 4 → 5 → 6
```

**Time Complexity**: O(m + n)
**Space Complexity**: O(1)

---

### 3. Linked List Cycle (LC 141)
**Concept**: Floyd's Cycle Detection (Tortoise and Hare)

**Key Ideas**:
- Use two pointers: slow (moves 1 step) and fast (moves 2 steps)
- If there's a cycle, fast will eventually catch slow
- If no cycle, fast will reach None
- Proof: In cycle, fast gains 1 step per iteration

**Pattern**: Two-pointer (fast and slow)

**Implementation**:
```python
def hasCycle(head):
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next

    return True
```

**Visualization**:
```
No cycle:
1 → 2 → 3 → 4 → 5 → None
slow     fast
Eventually fast reaches None

With cycle:
1 → 2 → 3 → 4 → 5
    ↑           ↓
    ←  ←  ←  ←

slow and fast will meet inside the cycle
```

**Why It Works**:
- Distance between slow and fast decreases by 1 each iteration
- In cycle, they must eventually meet
- Meeting point proves cycle exists

**Time Complexity**: O(n)
**Space Complexity**: O(1)

## Common Techniques

### Dummy Node Pattern
**When to use**: Operations that might modify head

```python
def someOperation(head):
    dummy = ListNode(0)
    dummy.next = head
    # Work with dummy.next instead of head
    # ...
    return dummy.next  # Return new head
```

**Benefits**:
- No special case for head
- Simplifies insertion/deletion at beginning
- Cleaner code

### Two Pointer Technique
**Fast and Slow**:
```python
# Find middle
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is at middle
```

**Previous and Current**:
```python
# For deletions
prev = None
curr = head
while curr:
    if should_delete(curr):
        prev.next = curr.next
    else:
        prev = curr
    curr = curr.next
```

### Pointer Reversal
**Standard pattern for reversing**:
```python
prev = None
curr = head
while curr:
    next_temp = curr.next
    curr.next = prev
    prev = curr
    curr = next_temp
return prev
```

## Learning Path

1. **Understand node structure**: How nodes connect
2. **Master traversal**: Simple iteration through list
3. **Practice Reverse Linked List**: Core pointer manipulation
4. **Learn dummy node pattern**: Simplifies many problems
5. **Master two-pointer**: Fast/slow technique
6. **Solve variations**: Reverse in groups, remove elements

## Tips for Success

1. **Draw diagrams**: Visualize pointer changes
2. **Check null/None**: Always verify before dereferencing
3. **Track three pointers**: prev, curr, next for complex operations
4. **Use dummy node**: For operations at head
5. **Test edge cases**:
   - Empty list (None)
   - Single node
   - Two nodes
   - Operations at head/tail

## Common Mistakes to Avoid

1. **Null pointer dereference**: Checking `node.next` when `node` is None
2. **Losing references**: Not saving `next` before changing `curr.next`
3. **Wrong return value**: Returning `head` when it's changed (use dummy)
4. **Off-by-one errors**: In cycle detection or finding nth node
5. **Not handling empty list**: Forgetting to check if `head` is None

## Edge Cases to Test

```python
# Empty list
head = None

# Single node
head = ListNode(1)

# Two nodes
head = ListNode(1, ListNode(2))

# All same values
head = ListNode(1, ListNode(1, ListNode(1)))

# Cycle at various positions
# - Cycle from head
# - Cycle in middle
# - No cycle
```

## Debugging Tips

1. **Print list**: Helper function to visualize
   ```python
   def print_list(head):
       values = []
       curr = head
       while curr:
           values.append(curr.val)
           curr = curr.next
       print(" → ".join(map(str, values)))
   ```

2. **Check pointers at each step**:
   ```python
   print(f"prev={prev.val if prev else None}")
   print(f"curr={curr.val if curr else None}")
   print(f"next={next_temp.val if next_temp else None}")
   ```

3. **Verify list structure**: No lost nodes, no cycles (unless intended)

## Practice Exercises

To solidify understanding:
1. Delete a node given only pointer to that node
2. Find nth node from end using one pass
3. Remove all nodes with specific value
4. Check if linked list is palindrome
5. Detect cycle and find cycle start
6. Find intersection point of two linked lists

## Next Steps

Once comfortable with easy problems:
- **Medium problems**: Complex pointer manipulation, multiple passes
- **Dummy node variations**: Sentinel nodes, multiple dummies
- **Advanced two-pointer**: Finding intersection, complex cycle problems
- **In-place modifications**: Constant space solutions

## Key Takeaways

- Linked lists trade random access for efficient insertion/deletion
- Always check for None before dereferencing
- Dummy nodes simplify edge cases
- Two-pointer technique solves many problems efficiently
- Drawing diagrams is essential for understanding
- Pointer manipulation requires careful sequencing
- Edge cases: empty list, single node, cycles

## Complexity Summary

| Operation | Linked List | Array |
|-----------|-------------|-------|
| Access ith element | O(n) | O(1) |
| Search | O(n) | O(n) |
| Insert at beginning | O(1) | O(n) |
| Insert at end | O(n) | O(1) amortized |
| Delete at beginning | O(1) | O(n) |
| Delete at end | O(n) | O(1) |
| Reverse | O(n) | O(n) |

## Additional Resources

- Visualize linked list operations: VisuAlgo, LeetCode Playground
- Practice pointer manipulation with pen and paper first
- Understand memory management in your language
- Study how real-world data structures use linked lists (HashMap buckets, etc.)
