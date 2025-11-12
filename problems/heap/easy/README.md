# Heap / Priority Queue - Easy Problems

## Core Concepts

### What is a Heap?

A **Heap** (or **Priority Queue**) is a specialized tree-based data structure that satisfies the heap property:
- **Max Heap**: Parent node is always greater than or equal to children
- **Min Heap**: Parent node is always less than or equal to children

**Key Characteristics**:
- Complete binary tree (all levels filled except possibly last)
- Efficient insertion and extraction of min/max element
- Typically implemented using an array

### Why Use Heaps?

Heaps excel at maintaining sorted order while allowing efficient insertions:

| Operation | Heap | Sorted Array | Unsorted Array |
|-----------|------|--------------|----------------|
| Find Min/Max | O(1) | O(1) | O(n) |
| Insert | O(log n) | O(n) | O(1) |
| Extract Min/Max | O(log n) | O(n) | O(n) |
| Build from n items | O(n) | O(n log n) | O(1) |

**Use heaps when**: You need repeated access to min/max while adding elements.

### Heap Implementation in Python

Python provides `heapq` module for min-heap operations:

```python
import heapq

# Create a min heap
heap = []

# Add elements - O(log n)
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
# heap is now [1, 5, 3] (internal structure)

# Get minimum (peek) - O(1)
min_val = heap[0]  # Returns 1, doesn't remove

# Remove and return minimum - O(log n)
min_val = heapq.heappop(heap)  # Returns 1

# Build heap from list - O(n)
nums = [5, 3, 7, 1]
heapq.heapify(nums)  # nums becomes min heap

# Get k largest/smallest - O(n log k)
k_largest = heapq.nlargest(3, nums)
k_smallest = heapq.nsmallest(3, nums)
```

### Max Heap in Python

Python's heapq only provides min-heap. For max-heap, negate values:

```python
import heapq

# Max heap using negation
max_heap = []

# Add elements (negate to convert)
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -1)
heapq.heappush(max_heap, -3)

# Get maximum (negate back)
max_val = -max_heap[0]  # Returns 5

# Remove maximum
max_val = -heapq.heappop(max_heap)  # Returns 5
```

### Heap as Array

Heaps are stored as arrays with parent-child relationships:

```
Index:   0   1   2   3   4   5   6
Array:  [1,  3,  2,  7,  5,  4,  6]

Tree representation:
        1
       / \
      3   2
     / \ / \
    7  5 4  6
```

**Index formulas**:
- Parent of node at index `i`: `(i - 1) // 2`
- Left child of node at index `i`: `2 * i + 1`
- Right child of node at index `i`: `2 * i + 2`

### Heap Operations

#### 1. Heapify Up (Bubble Up)
After inserting at end, move element up if it violates heap property:

```python
def heapify_up(heap, index):
    parent = (index - 1) // 2

    # While not at root and parent is larger
    while index > 0 and heap[parent] > heap[index]:
        # Swap with parent
        heap[parent], heap[index] = heap[index], heap[parent]
        index = parent
        parent = (index - 1) // 2
```

#### 2. Heapify Down (Bubble Down)
After removing root, move element down if it violates heap property:

```python
def heapify_down(heap, index):
    n = len(heap)

    while True:
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        # Check left child
        if left < n and heap[left] < heap[smallest]:
            smallest = left

        # Check right child
        if right < n and heap[right] < heap[smallest]:
            smallest = right

        # If heap property satisfied, done
        if smallest == index:
            break

        # Swap and continue
        heap[index], heap[smallest] = heap[smallest], heap[index]
        index = smallest
```

## Problems in This Section

### 1. Kth Largest Element in a Stream (LC 703)

**Concept**: Design class to find kth largest element in a stream

**Pattern**: Maintain min-heap of size k

**Time Complexity**:
- Constructor: O(n log k)
- Add: O(log k)

**Space Complexity**: O(k)

#### Key Insights

1. **Min-heap of size k**: Keep k largest elements
2. **Root is answer**: Smallest of k largest elements = kth largest
3. **Add operation**: If larger than root, replace root

#### Why This Works

```
Example: k=3, stream = [4,5,8,2]

After 4: heap = [4]          3rd largest = 4
After 5: heap = [4,5]        3rd largest = 4
After 8: heap = [4,5,8]      3rd largest = 4
After 2: heap = [4,5,8]      3rd largest = 4 (2 not added)
After 3: heap = [4,5,8]      3rd largest = 4 (3 not added)
After 5: heap = [5,5,8]      3rd largest = 5 (replaced 4)
```

#### Implementation

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)

        # Keep only k largest elements
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        # Add to heap
        heapq.heappush(self.heap, val)

        # Maintain size k
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)

        # Root is kth largest
        return self.heap[0]
```

#### Common Pitfalls

1. **Using max-heap**: Need min-heap to efficiently remove smallest of k largest
2. **Not maintaining size k**: Heap grows unbounded
3. **Off-by-one errors**: kth largest, not (k-1)th

### 2. Last Stone Weight (LC 1046)

**Concept**: Smash two heaviest stones, add difference back until one or zero stones remain

**Pattern**: Max-heap for repeated max extraction

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

#### Key Insights

1. **Max-heap**: Need to repeatedly get two heaviest stones
2. **Negate for max-heap**: Python heapq is min-heap
3. **Loop until <= 1 stone**: Continue smashing until done

#### Algorithm

```
stones = [2,7,4,1,8,1]

Step 1: Get max two: 8 and 7, diff = 1, stones = [1,2,4,1,1]
Step 2: Get max two: 4 and 2, diff = 2, stones = [1,1,1,2]
Step 3: Get max two: 2 and 1, diff = 1, stones = [1,1,1]
Step 4: Get max two: 1 and 1, diff = 0, stones = [1]
Result: 1
```

#### Implementation

```python
import heapq

def lastStoneWeight(stones: List[int]) -> int:
    # Convert to max heap (negate values)
    heap = [-stone for stone in stones]
    heapq.heapify(heap)

    while len(heap) > 1:
        # Get two heaviest stones
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)

        # If different weights, add difference back
        if first != second:
            heapq.heappush(heap, -(first - second))

    # Return last stone weight or 0 if all destroyed
    return -heap[0] if heap else 0
```

#### Alternative: Sort Each Time (Inefficient)

```python
def lastStoneWeight(stones):
    while len(stones) > 1:
        stones.sort()  # O(n log n) every iteration!
        first = stones.pop()
        second = stones.pop()

        if first != second:
            stones.append(first - second)

    return stones[0] if stones else 0

# Time: O(n^2 log n) - much worse!
```

#### Common Pitfalls

1. **Forgetting to negate**: Using min-heap instead of max-heap
2. **Not handling equal weights**: Both stones destroyed
3. **Not checking empty heap**: When all stones destroyed

## Common Patterns

### Pattern 1: Maintain K Elements

```python
# Keep k smallest/largest elements
heap = []

for num in nums:
    heapq.heappush(heap, num)
    if len(heap) > k:
        heapq.heappop(heap)

# For k largest: use min-heap, pop smallest
# For k smallest: use max-heap (negate), pop largest
```

### Pattern 2: Repeated Min/Max Extraction

```python
heap = list(nums)
heapq.heapify(heap)

while len(heap) > 1:
    # Process smallest/largest elements
    val1 = heapq.heappop(heap)
    val2 = heapq.heappop(heap)

    # Compute result and potentially add back
    result = process(val1, val2)
    if result:
        heapq.heappush(heap, result)
```

### Pattern 3: Max Heap Using Negation

```python
# Max heap
max_heap = [-x for x in nums]
heapq.heapify(max_heap)

# Get max
max_val = -heapq.heappop(max_heap)

# Add to max heap
heapq.heappush(max_heap, -value)
```

## Heap vs Other Data Structures

### When to Use Heap

Use heap when you need:
- Repeated access to min/max element
- Dynamic insertion with min/max queries
- K largest/smallest elements
- Priority-based processing

### Alternatives

| Need | Use | Why |
|------|-----|-----|
| Single min/max | min()/max() | O(n) but simpler |
| Fully sorted | sort() | O(n log n) but sorted once |
| Both min and max | Two heaps | One max-heap, one min-heap |
| Sorted + frequent updates | Balanced BST | O(log n) insert/delete/search |
| Fixed size window | Deque | O(1) operations on ends |

## Complexity Cheatsheet

| Operation | Time | Explanation |
|-----------|------|-------------|
| heappush | O(log n) | Heapify up from leaf |
| heappop | O(log n) | Heapify down from root |
| heapify | O(n) | Build heap from array |
| peek (heap[0]) | O(1) | Just access root |
| nlargest/nsmallest | O(n log k) | k is parameter |
| heappushpop | O(log n) | Push then pop, optimized |
| heapreplace | O(log n) | Pop then push, optimized |

## Tips for Heap Problems

1. **Identify pattern**: Need repeated min/max? → Heap
2. **Choose heap type**: Min for smallest, max for largest
3. **Handle max heap**: Negate values in Python
4. **Maintain size**: For "k largest/smallest", keep heap size = k
5. **Consider alternatives**: Sometimes sorting is simpler
6. **Test edge cases**: Empty heap, single element, equal values

## Common Mistakes

1. **Wrong heap type**: Using min when need max (or vice versa)
2. **Not negating for max heap**: Forgetting to negate values
3. **Not maintaining heap size**: For k problems, must pop when size > k
4. **Assuming sorted array**: Heap is partially sorted, not fully
5. **Inefficient operations**: Using O(n) operations when O(log n) available

## Practice Progression

1. **Start with Kth Largest**: Understand maintaining k elements
2. **Try Last Stone Weight**: Practice max-heap with negation
3. **Implement your own heap**: Understand heapify up/down
4. **Visualize operations**: Draw heap tree during operations
5. **Compare with alternatives**: When is heap better than sorting?

## Beyond Easy Problems

Once comfortable with these, you're ready for:
- **K Closest Points** (LC 973): Heap with custom comparator
- **Kth Largest Element** (LC 215): Quick select vs heap
- **Task Scheduler** (LC 621): Greedy with heap
- **Find Median** (LC 295): Two heaps pattern
- **Merge K Sorted Lists** (LC 23): Heap for k-way merge

## Real-World Applications

1. **Task Scheduling**: Process highest priority tasks first
2. **Event Simulation**: Process events in time order
3. **Top K Problems**: Find top k items in stream
4. **Load Balancing**: Assign tasks to least loaded server
5. **Dijkstra's Algorithm**: Find shortest path (min-heap of distances)

## Key Takeaways

1. **Heap = Priority Queue**: Get min/max efficiently with dynamic updates
2. **Min-heap by default**: Python heapq is always min-heap
3. **Negate for max-heap**: Simple trick to simulate max-heap
4. **Maintain size k**: For "k largest", keep min-heap of size k
5. **O(log n) operations**: Much faster than sorting for repeated operations
6. **Complete binary tree**: Enables efficient array representation

## Visual Learning

```
Min Heap Example:
Array: [1, 3, 2, 7, 5, 4, 6]

Tree:     1
        /   \
       3     2
      / \   / \
     7   5 4   6

Operations:
- Push 0: Add at end, bubble up to root
- Pop: Remove root, replace with last, bubble down

Max Heap (negated):
To maintain max heap [7,5,6,1,3,2,4]
Store as min heap [-7,-5,-6,-1,-3,-2,-4]
Negate when reading: -(-7) = 7
```

## Additional Resources

- Visualize heap operations: visualgo.net/en/heap
- Practice drawing heap trees
- Implement heapify from scratch for deeper understanding
- Study heap sort algorithm (uses heaps for sorting)
