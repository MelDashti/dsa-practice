# Heap / Priority Queue - Hard Problems

## Expert-Level Concepts

### Two-Heap Pattern

The **two-heap pattern** uses one max-heap and one min-heap to maintain order statistics efficiently:

**Use Cases**:
- Find median in data stream
- Maintain sliding window median
- Balance two partitions

**Structure**:
```python
max_heap = []  # Left half (smaller elements, negated)
min_heap = []  # Right half (larger elements)

# Invariant: max_heap and min_heap differ by at most 1 in size
# max_heap[0] <= min_heap[0] (if both non-empty)
```

**Why This Works**:
- Max-heap stores smaller half (top is largest of small)
- Min-heap stores larger half (top is smallest of large)
- Median is at boundary between heaps

### Streaming Data Challenges

Processing infinite streams requires:
1. **Constant space**: Can't store all data
2. **Online algorithms**: Process each element once
3. **Efficient updates**: O(log n) per element
4. **Order statistics**: Find median, quantiles, etc.

**Two-heap pattern is optimal**: O(1) median query, O(log n) insertion.

### Advanced Heap Operations

#### Lazy Deletion
```python
# Instead of removing from middle (O(n))
# Mark as deleted and skip during pop

deleted = set()

def lazy_remove(val):
    deleted.add(val)

def pop():
    while heap and heap[0] in deleted:
        deleted.remove(heap[0])
        heapq.heappop(heap)
    return heapq.heappop(heap)
```

#### Heap with Removal by Value
```python
# Maintain element positions
class HeapWithRemoval:
    def __init__(self):
        self.heap = []
        self.position = {}  # element -> index in heap

    def push(self, val):
        self.position[val] = len(self.heap)
        heapq.heappush(self.heap, val)

    def remove(self, val):
        # Swap with last element
        idx = self.position[val]
        last = self.heap[-1]
        self.heap[idx] = last
        self.position[last] = idx
        self.heap.pop()

        # Heapify at position
        self._heapify_at(idx)
```

## Problems in This Section

### 1. Find Median from Data Stream (LC 295)

**Concept**: Design data structure supporting addNum(val) and findMedian()

**Difficulty Factors**:
1. Data arrives continuously (can't sort each time)
2. Must efficiently maintain order
3. Median requires middle elements
4. Both operations must be fast

**Pattern**: Two heaps (max-heap for left, min-heap for right)

**Time Complexity**:
- addNum: O(log n)
- findMedian: O(1)

**Space Complexity**: O(n)

#### Key Insights

1. **Two heaps maintain balance**:
   - Max-heap: smaller half of numbers
   - Min-heap: larger half of numbers

2. **Median location**:
   - If odd total: median is top of larger heap
   - If even total: median is average of both tops

3. **Balance heaps**:
   - Keep sizes equal or differ by 1
   - Ensures median is always at boundary

4. **Insertion strategy**:
   - Always add to one heap first
   - Move top to other heap if needed
   - Rebalance if size difference > 1

#### Algorithm Visualization

```
Stream: [1, 2, 3, 4, 5]

After 1:
max_heap: [1]
min_heap: []
median: 1

After 2:
max_heap: [1]
min_heap: [2]
median: (1+2)/2 = 1.5

After 3:
max_heap: [1]
min_heap: [2,3]
median: 2

After 4:
max_heap: [2,1]
min_heap: [3,4]
median: (2+3)/2 = 2.5

After 5:
max_heap: [2,1]
min_heap: [3,4,5]
median: 3
```

#### Implementation

```python
import heapq

class MedianFinder:
    def __init__(self):
        # Max-heap for smaller half (negate values)
        self.small = []

        # Min-heap for larger half
        self.large = []

    def addNum(self, num: int) -> None:
        # Add to max-heap (smaller half)
        heapq.heappush(self.small, -num)

        # Move largest from small to large
        # Ensures small <= large for all elements
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes (small can have at most 1 more)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        # If odd count, median is in small heap
        if len(self.small) > len(self.large):
            return -self.small[0]

        # If even count, median is average
        return (-self.small[0] + self.large[0]) / 2.0
```

#### Alternative Implementation (Simplified)

```python
class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        # Always add to small first
        heapq.heappush(self.small, -num)

        # Move to large if needed
        if self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Rebalance
        if len(self.small) < len(self.large):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

#### Step-by-Step Walkthrough

**Example**: Add [5, 15, 1, 3]

**Step 1: Add 5**
```
small: [-5]
large: []
median: 5
```

**Step 2: Add 15**
```
After adding to small: [-15, -5]
Top of small (15) > top of large (empty), no move needed
After rebalance:
small: [-5]
large: [15]
median: (5 + 15) / 2 = 10
```

**Step 3: Add 1**
```
After adding to small: [-5, -1]
Top of small (5) <= top of large (15), no move
Already balanced
small: [-5, -1]
large: [15]
median: 5
```

**Step 4: Add 3**
```
After adding to small: [-5, -3, -1]
Top of small (5) <= top of large (15), no move
Rebalance (small has 3, large has 1):
small: [-3, -1]
large: [5, 15]
median: (3 + 5) / 2 = 4
```

#### Edge Cases

```python
# 1. Single element
addNum(5)
median: 5

# 2. Two equal elements
addNum(5), addNum(5)
median: 5.0

# 3. Negative numbers
addNum(-1), addNum(-2), addNum(-3)
median: -2

# 4. Large range
addNum(-1000000), addNum(1000000)
median: 0.0

# 5. All same
addNum(7), addNum(7), addNum(7)
median: 7
```

#### Common Pitfalls

1. **Wrong heap type**: Forgetting to negate for max-heap
2. **Balance condition**: Getting inequality wrong
3. **Median calculation**: Wrong heap or wrong average
4. **Rebalancing**: Not maintaining size invariant
5. **Integer division**: Using // instead of / for median

#### Complexity Analysis

**Time**:
- addNum: O(log n) - heap operations
- findMedian: O(1) - just peek at tops

**Space**: O(n) - store all numbers

**Why Optimal**:
- Can't do better than O(log n) for insertion with order maintenance
- O(1) median query is best possible
- Can't use less than O(n) space (must store all numbers)

#### Alternative Approaches

**Approach 1: Maintain Sorted List**
```python
class MedianFinder:
    def __init__(self):
        self.nums = []

    def addNum(self, num):
        bisect.insort(self.nums, num)  # O(n)

    def findMedian(self):
        n = len(self.nums)
        if n % 2 == 1:
            return self.nums[n // 2]
        return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2

# Time: O(n) addNum, O(1) findMedian
# Worse than two-heap approach!
```

**Approach 2: Self-Balancing BST**
```python
# Use TreeMap or Red-Black Tree
# Same O(log n) insertion, O(1) median
# More complex to implement
```

**Approach 3: Buckets**
```python
# If range is limited, use bucket sort
# O(1) insertion, O(buckets) median
# Only works for limited range
```

#### Follow-Up Questions

**Q1: If all numbers from stream are in range [0, 100], optimize?**
```python
# Use counting array
counts = [0] * 101

def addNum(num):
    counts[num] += 1

def findMedian():
    total = sum(counts)
    target = total // 2
    count = 0
    for i in range(101):
        count += counts[i]
        if count > target:
            if total % 2 == 1:
                return i
            # Find next number for average
            ...
    return result

# Time: O(1) addNum, O(100) = O(1) findMedian
```

**Q2: If 99% of numbers are in [0, 100], optimize?**
```python
# Hybrid: buckets for [0,100], two heaps for outliers
# Most numbers handled in O(1)
```

**Q3: How to handle sliding window median?**
```python
# Need to remove old elements
# Use two heaps with lazy deletion
# Or use ordered set/multiset
```

## Advanced Patterns

### Pattern 1: Two-Heap Template

```python
class TwoHeapStructure:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def add(self, num):
        # Add to small heap
        heapq.heappush(self.small, -num)

        # Maintain order: max(small) <= min(large)
        if self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def get_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

### Pattern 2: Lazy Deletion with Heaps

```python
class HeapWithDeletion:
    def __init__(self):
        self.heap = []
        self.deleted = set()

    def push(self, val):
        heapq.heappush(self.heap, val)

    def pop(self):
        self._clean()
        return heapq.heappop(self.heap)

    def peek(self):
        self._clean()
        return self.heap[0]

    def remove(self, val):
        self.deleted.add(val)

    def _clean(self):
        while self.heap and self.heap[0] in self.deleted:
            val = heapq.heappop(self.heap)
            self.deleted.remove(val)
```

### Pattern 3: Multi-Heap Coordination

```python
# Maintain k-way partition
# Example: tertiles (3 heaps), quartiles (4 heaps)

class Tertiles:
    def __init__(self):
        self.low = []    # max-heap, bottom 1/3
        self.mid = []    # min-heap, middle 1/3
        self.high = []   # min-heap, top 1/3

    def add(self, num):
        # Add to appropriate heap
        # Rebalance to maintain equal sizes
        # Maintain order: max(low) <= min(mid) <= min(high)
        pass

    def get_tertiles(self):
        return (-self.low[0], self.mid[0], self.high[0])
```

## Advanced Techniques

### 1. Order Statistics Tree

For more complex queries (kth smallest, rank, etc.):
```python
# Use augmented BST (Red-Black Tree)
# Each node stores subtree size
# O(log n) insert, delete, kth smallest, rank
```

### 2. Segment Tree / Fenwick Tree

For range queries with updates:
```python
# Build segment tree over value range
# O(log n) updates and range sum queries
# Can compute median with binary search
```

### 3. Reservoir Sampling

For uniform random sample from stream:
```python
# Not for median, but related streaming problem
def reservoir_sample(stream, k):
    reservoir = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
    return reservoir
```

## Problem-Solving Framework

### Step 1: Identify Requirements
- What operations are needed?
- What are time constraints?
- Is data static or streaming?

### Step 2: Choose Data Structure
- Order statistics → Two heaps or BST
- Top k elements → Single heap
- Sliding window → Heaps with deletion
- Range queries → Segment tree

### Step 3: Design Invariants
- What properties must hold?
- How to maintain after each operation?
- What balance conditions are needed?

### Step 4: Implement Carefully
- Handle edge cases (empty, single element)
- Maintain invariants in all operations
- Test with various inputs

## Tips for Hard Heap Problems

1. **Two heaps for median**: Essential pattern to master
2. **Balance condition**: Always maintain size invariant
3. **Lazy deletion**: When direct removal is expensive
4. **Consider alternatives**: Sometimes BST is better
5. **Test edge cases**: Empty, single element, all equal
6. **Optimize for use case**: Know access patterns

## Common Mistakes

1. **Forgetting to negate**: For max-heap in Python
2. **Wrong balance condition**: Off-by-one errors
3. **Not cleaning deleted elements**: Memory leak with lazy deletion
4. **Integer division for median**: Use float division
5. **Not handling rebalancing**: Heaps become unbalanced
6. **Complexity analysis**: Missing hidden costs

## Beyond This Problem

Once you master median finding, try:
- **Sliding Window Median** (LC 480): Median with window
- **IPO** (LC 502): Greedy with two heaps
- **Maximal Rectangle** (LC 85): Not heap, but hard
- **Trapping Rain Water II** (LC 407): Priority queue on 2D
- **Employee Free Time** (LC 759): Interval scheduling

## Real-World Applications

1. **Network Latency Monitoring**: Track median latency
2. **Load Balancing**: Distribute requests evenly
3. **Real-Time Statistics**: Percentiles in data stream
4. **Anomaly Detection**: Detect outliers based on median
5. **Video Streaming**: Adjust quality based on bandwidth median
6. **Financial Trading**: Rolling median for trend analysis

## Key Takeaways

1. **Two-heap pattern**: Optimal for streaming median
2. **Balance is crucial**: Maintain size invariant carefully
3. **O(log n) + O(1)**: Best achievable for add + query
4. **Space is linear**: Must store all elements
5. **Lazy deletion**: Powerful technique for complex operations
6. **Alternative structures**: BST, segment tree for other queries

## Interview Strategy

When asked about median in stream:

1. **Start simple**: Mention sorted array approach
2. **Identify bottleneck**: O(n) insertion is too slow
3. **Propose two heaps**: Explain why it works
4. **Walk through example**: Show add operations
5. **Analyze complexity**: O(log n) add, O(1) median
6. **Discuss trade-offs**: Space vs time, exact vs approximate
7. **Handle follow-ups**: Limited range, sliding window, percentiles

## Mathematical Insight

**Why two heaps work**:
- Median is the "middle" value
- Two heaps partition numbers into smaller/larger halves
- Tops of heaps are closest to middle
- Balance ensures both halves are equal size

**Invariants to maintain**:
1. `|size(small) - size(large)| <= 1`
2. `max(small) <= min(large)`
3. `size(small) >= size(large)` (optional, for consistency)

**These guarantee**:
- Median is always at top(s)
- O(1) query time
- O(log n) maintenance

## Final Thoughts

The median-from-stream problem is a classic hard problem that demonstrates:
- Creative use of data structures
- Maintaining invariants
- Time-space trade-offs
- Online algorithm design

Master this pattern and you'll handle many streaming statistics problems efficiently. The two-heap technique is a fundamental pattern that appears in many contexts beyond just finding medians.
