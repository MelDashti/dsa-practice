# Linked List - Medium Problems

## Overview

Medium linked list problems combine multiple techniques and require deeper understanding of pointer manipulation, space-time tradeoffs, and creative problem-solving. These problems often involve multiple passes, complex pointer patterns, or integration with other data structures.

## Key Concepts

### Advanced Techniques

1. **Runner Technique**: Using pointers at different speeds
2. **In-place Reversal**: Reversing portions of the list
3. **Hash Table Integration**: Trading space for time
4. **Dummy Node Variations**: Multiple dummies or sentinels
5. **Cycle Detection Extensions**: Finding cycle start, intersection
6. **Design Problems**: Implementing complex data structures

## Problems in This Section

### 1. Reorder List (LC 143)
**Concept**: Multiple techniques combined (find middle, reverse, merge)

**Problem**: Reorder L₀→L₁→...→Lₙ₋₁→Lₙ to L₀→Lₙ→L₁→Lₙ₋₁→L₂→Lₙ₋₂→...

**Key Ideas**:
1. Find middle using fast/slow pointers
2. Reverse second half
3. Merge two halves alternately

**Pattern**: Multi-step transformation

**Algorithm**:
```python
def reorderList(head):
    if not head or not head.next:
        return

    # Step 1: Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: Reverse second half
    second = slow.next
    slow.next = None
    prev = None
    while second:
        temp = second.next
        second.next = prev
        prev = second
        second = temp

    # Step 3: Merge two halves
    first = head
    second = prev
    while second:
        temp1 = first.next
        temp2 = second.next
        first.next = second
        second.next = temp1
        first = temp1
        second = temp2
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

### 2. Remove Nth Node From End (LC 19)
**Concept**: Two-pointer with gap

**Key Ideas**:
- Use two pointers with n gap between them
- When fast reaches end, slow is at (n-1)th from end
- Use dummy node to handle removing head
- One-pass solution

**Pattern**: Two-pointer with offset

**Implementation**:
```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy

    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next

    # Remove nth node
    slow.next = slow.next.next

    return dummy.next
```

**Time Complexity**: O(n) - single pass
**Space Complexity**: O(1)

---

### 3. Copy List with Random Pointer (LC 138)
**Concept**: Deep copy with random pointers

**Key Ideas**:
- Each node has next and random pointer
- Need to create independent copy
- Hash map: old node → new node mapping
- Alternative: Interweave new nodes, then separate

**Pattern**: Hash table for node mapping

**Hash Map Approach**:
```python
def copyRandomList(head):
    if not head:
        return None

    # First pass: create all nodes
    old_to_new = {}
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next

    # Second pass: set next and random
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next

    return old_to_new[head]
```

**Interweaving Approach (O(1) space)**:
```python
def copyRandomList(head):
    if not head:
        return None

    # Step 1: Create new nodes interweaved
    curr = head
    while curr:
        new_node = Node(curr.val)
        new_node.next = curr.next
        curr.next = new_node
        curr = new_node.next

    # Step 2: Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # Step 3: Separate lists
    curr = head
    new_head = head.next
    while curr:
        new_node = curr.next
        curr.next = new_node.next
        if new_node.next:
            new_node.next = new_node.next.next
        curr = curr.next

    return new_head
```

**Time Complexity**: O(n)
**Space Complexity**: O(n) with hash map, O(1) with interweaving

---

### 4. Add Two Numbers (LC 2)
**Concept**: Digit-by-digit addition with carry

**Key Ideas**:
- Numbers stored in reverse (least significant first)
- Add corresponding digits + carry
- Handle different lengths
- Don't forget final carry

**Pattern**: Simultaneous traversal with state

**Implementation**:
```python
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        total = val1 + val2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)

        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next
```

**Time Complexity**: O(max(m, n))
**Space Complexity**: O(max(m, n))

---

### 5. Find Duplicate Number (LC 287)
**Concept**: Cycle detection in array as linked list

**Key Ideas**:
- Array contains numbers 1 to n with one duplicate
- Treat array as linked list: nums[i] is pointer to next
- Duplicate creates a cycle
- Use Floyd's cycle detection to find cycle entrance

**Pattern**: Array as linked list + cycle detection

**Implementation**:
```python
def findDuplicate(nums):
    # Phase 1: Find intersection point
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find cycle entrance (duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

**Why It Works**:
```
Array: [1, 3, 4, 2, 2]
Treat as: 0→1→3→2→4→2 (cycle at 2)

Index:  0  1  2  3  4
Value: [1, 3, 4, 2, 2]

0 → 1 → 3 → 2 → 4
            ↑    ↓
            ← ← ←

Cycle entrance = duplicate number
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

### 6. LRU Cache (LC 146)
**Concept**: Doubly linked list + hash map

**Key Ideas**:
- Hash map: O(1) access by key
- Doubly linked list: O(1) reorder (move to front/remove)
- Most recent at head, least recent at tail
- Evict from tail when capacity exceeded

**Pattern**: Combined data structures for optimal performance

**Implementation**:
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node
        self.head = Node()  # Dummy head
        self.tail = Node()  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from list"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        """Add node right after head"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # Move to front (most recently used)
        self._remove(node)
        self._add_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Evict LRU (tail.prev)
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
```

**Time Complexity**: O(1) for both get and put
**Space Complexity**: O(capacity)

## Common Patterns

### Pattern 1: Multi-Step Transformation
```python
def complex_operation(head):
    # Step 1: Find middle/split
    middle = find_middle(head)

    # Step 2: Reverse part
    reversed_part = reverse(middle)

    # Step 3: Merge/combine
    result = merge(head, reversed_part)

    return result
```

### Pattern 2: Two Pointer with Gap
```python
def nth_from_end(head, n):
    fast = slow = head

    # Create gap of n
    for _ in range(n):
        fast = fast.next

    # Move together until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next

    return slow
```

### Pattern 3: Hash Map for Node Mapping
```python
def deep_copy(head):
    old_to_new = {}

    # First pass: create all nodes
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next

    # Second pass: connect pointers
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        curr = curr.next

    return old_to_new[head]
```

### Pattern 4: Dummy + Carry State
```python
def add_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        # Process digits + carry
        # Create new node
        # Update carry

    return dummy.next
```

## Advanced Insights

### Why Doubly Linked List for LRU?
- **Move to front**: O(1) with direct node access
- **Remove from anywhere**: O(1) with prev pointer
- **Singly linked**: Would need O(n) to find prev for removal

### Cycle Detection Mathematics
```
Phase 1: Fast catches slow
- Slow moves k steps
- Fast moves 2k steps
- Meet at distance k from start of cycle

Phase 2: Find entrance
- Start slow from beginning
- Both move 1 step at a time
- Meet at cycle entrance
```

### Space-Time Tradeoffs
| Problem | With Space | Without Space |
|---------|------------|---------------|
| Copy Random List | O(n) space, O(n) time | O(1) space, O(n) time |
| Find Duplicate | O(n) space, O(n) time | O(1) space, O(n) time |

## Learning Path

1. **Master Reorder List**: Combines three techniques
2. **Practice Remove Nth**: Two-pointer with gap
3. **Understand Copy Random**: Hash map vs in-place
4. **Study Add Two Numbers**: State management with carry
5. **Master Find Duplicate**: Clever array→list conversion
6. **Implement LRU Cache**: Design problem with multiple structures

## Tips for Success

1. **Break complex problems into steps**: Identify sub-operations
2. **Draw diagrams**: Visualize pointer changes at each step
3. **Use helper functions**: Modularize operations (reverse, merge)
4. **Test edge cases**:
   - Empty list
   - Single/two nodes
   - Operations at boundaries
5. **Consider space-time tradeoffs**: Hash map vs clever pointer tricks

## Common Mistakes to Avoid

1. **Losing references**: Save next/prev before modifying pointers
2. **Off-by-one in two-pointer**: Gap calculation matters
3. **Forgetting to update both pointers**: In doubly linked list
4. **Not handling edge cases**: Empty list, single node
5. **Memory leaks**: In languages with manual memory management
6. **Wrong dummy placement**: For operations at head

## Debugging Techniques

1. **Print at each step**:
   ```python
   def print_list_state(name, head):
       vals = []
       curr = head
       while curr and len(vals) < 20:  # Prevent infinite loop
           vals.append(curr.val)
           curr = curr.next
       print(f"{name}: {' → '.join(map(str, vals))}")
   ```

2. **Check pointers**:
   ```python
   assert node.next.prev == node  # For doubly linked list
   ```

3. **Visualize structure**:
   - Draw state before and after operations
   - Trace through small examples by hand

## Interview Tips

1. **Clarify requirements**: In-place? Space constraints? Doubly linked?
2. **Start with brute force**: Then optimize
3. **Explain trade-offs**: Space vs time, multiple passes vs single
4. **Code modularly**: Helper functions for reverse, find_middle, etc.
5. **Test thoroughly**: Edge cases, null checks, cycle detection

## Practice Strategy

1. Implement basic operations first (reverse, find middle, merge)
2. Combine techniques for complex problems
3. Try both approaches (hash map vs in-place)
4. Measure actual time/space in your environment
5. Solve related problems to reinforce patterns

## Next Steps

Once comfortable with medium problems:
- **Hard problems**: More complex combinations, advanced patterns
- **Design variations**: Different cache policies, complex data structures
- **Optimization**: Constant space solutions, single-pass algorithms
- **Advanced applications**: Skip lists, XOR linked lists

## Key Takeaways

- Medium problems often combine multiple basic techniques
- Dummy nodes simplify boundary cases
- Two-pointer technique extends to gaps and different speeds
- Hash maps trade space for simpler logic
- In-place solutions possible but often trickier
- Design problems require understanding of multiple data structures
- Breaking problems into steps makes them manageable
- Always consider space-time tradeoffs

## Complexity Reference

| Problem | Time | Space | Technique |
|---------|------|-------|-----------|
| Reorder List | O(n) | O(1) | Multi-step |
| Remove Nth | O(n) | O(1) | Two-pointer gap |
| Copy Random | O(n) | O(n)/O(1) | Hash map/Interweave |
| Add Two Numbers | O(n) | O(n) | Carry state |
| Find Duplicate | O(n) | O(1) | Cycle detection |
| LRU Cache | O(1) ops | O(capacity) | DLL + Hash map |
