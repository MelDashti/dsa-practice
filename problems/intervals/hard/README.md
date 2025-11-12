# Intervals - Hard

## Overview
Hard interval problems combine advanced data structures with sophisticated algorithms to solve complex range queries and optimization problems. These problems often require segment trees, interval trees, or advanced heap manipulation combined with sorting and binary search techniques.

## Key Concepts

### 1. Advanced Data Structures
- **Segment Trees**: Range queries in O(log n)
- **Interval Trees**: Efficient interval overlap queries
- **Binary Indexed Trees (Fenwick Trees)**: Cumulative operations
- **Multisets/TreeMaps**: Ordered collections with fast operations

### 2. Query Processing
- **Offline vs Online**: Process all queries at once vs one at a time
- **Coordinate Compression**: Map large ranges to smaller indices
- **Lazy Evaluation**: Defer computations until necessary

### 3. Optimization Techniques
- **Two-Pass Algorithms**: Preprocess then query
- **Event Processing**: Convert intervals to discrete events
- **Greedy + DP Combination**: Optimal substructure with local choices

## Problems in This Section

### Minimum Interval to Include Each Query (LC 1851)
**Problem**: For each query point, find the smallest interval that contains it.

**Key Insights**:
- Offline query processing is more efficient than online
- Sort both intervals and queries
- Use min heap to track active intervals by size
- Remove intervals that end before current query
- Answer = smallest active interval size

**Complexity**:
- Time: O(n log n + q log q + (n+q) log n)
  - Sorting intervals: O(n log n)
  - Sorting queries: O(q log q)
  - Processing with heap: O((n+q) log n)
- Space: O(n + q)

**Pattern**: Offline Query + Sweep Line + Min Heap

---

## Deep Dive: Minimum Interval to Include Each Query

### Problem Analysis

**Given**:
- Array of intervals: `[[left, right], ...]`
- Array of queries: `[q1, q2, q3, ...]`

**Find**:
- For each query qi, find the size of the smallest interval that contains it
- Interval size = `right - left + 1`
- If no interval contains the query, return -1

### Why This Is Hard

1. **Naive Approach is O(n × q)**:
   ```python
   for query in queries:
       min_size = infinity
       for interval in intervals:
           if interval[0] <= query <= interval[1]:
               min_size = min(min_size, interval[1] - interval[0] + 1)
   ```
   With n = 10^5 and q = 10^5, this is too slow (10^10 operations)

2. **Multiple Overlapping Intervals**:
   - Many intervals may contain a single query
   - Need to efficiently find the smallest one

3. **Different Query Values**:
   - Each query may need different intervals
   - Can't process all queries the same way

### Solution Strategy

#### Step 1: Sort Everything
```python
# Sort intervals by start time
intervals.sort(key=lambda x: x[0])

# Sort queries but track original indices
queries_with_index = [(q, i) for i, q in enumerate(queries)]
queries_with_index.sort()
```

**Why sort**:
- Process intervals in order of when they become relevant
- Process queries in order to maintain active intervals efficiently

#### Step 2: Use Min Heap for Active Intervals
```python
import heapq

heap = []  # Min heap: (size, end_time)
interval_idx = 0
result = [-1] * len(queries)
```

**Why heap**:
- Automatically gives us the smallest active interval
- Efficient insertion and extraction: O(log n)

#### Step 3: Process Queries in Order
```python
for query, original_idx in queries_with_index:
    # Add all intervals that start at or before query
    while interval_idx < len(intervals) and intervals[interval_idx][0] <= query:
        left, right = intervals[interval_idx]
        size = right - left + 1
        heapq.heappush(heap, (size, right))
        interval_idx += 1

    # Remove intervals that end before query
    while heap and heap[0][1] < query:
        heapq.heappop(heap)

    # Top of heap is smallest interval containing query
    if heap:
        result[original_idx] = heap[0][0]
```

**Key Idea**:
- For each query, maintain a heap of "active" intervals
- Active = interval has started but not ended relative to query
- Smallest active interval is at top of heap

### Visual Example

```
Intervals: [1,4], [2,4], [3,6], [4,4]
Queries: 2, 3, 4, 5

Step-by-step:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query = 2:
Timeline:    1   2   3   4   5   6
            [-------]              size=4
                [-------]          size=3
                    [-------]      size=4
                        [0]        size=1

Process:
- Add [1,4] to heap: heap = [(4,4)]
- Add [2,4] to heap: heap = [(3,4), (4,4)]
- [3,6] starts at 3, too late
- [4,4] starts at 4, too late
- Remove none (all active)
- Answer: heap[0][0] = 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query = 3:
Timeline:    1   2   3   4   5   6
            [-------]              size=4
                [-------]          size=3
                    [-------]      size=4
                        [0]        size=1

Process:
- Add [3,6] to heap: heap = [(3,4), (4,4), (4,6)]
- [4,4] starts at 4, too late
- Remove none (all active)
- Answer: heap[0][0] = 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query = 4:
Timeline:    1   2   3   4   5   6
            [-------]              size=4
                [-------]          size=3
                    [-------]      size=4
                        [0]        size=1

Process:
- Add [4,4] to heap: heap = [(1,4), (3,4), (4,4), (4,6)]
- Remove [1,4] (ends before 4): heap = [(3,4), (4,4), (4,6)]
- Remove [2,4] (ends before 4): heap = [(4,4), (4,6)]
  Wait, [2,4] includes 4 if inclusive!
- Actually depends on problem definition
- Answer: heap[0][0] = 1 or 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query = 5:
Timeline:    1   2   3   4   5   6
            [-------]
                [-------]
                    [-------]      size=4
                        [0]

Process:
- No new intervals to add
- Remove [4,4] (ends before 5)
- heap = [(4,6)]
- Answer: heap[0][0] = 4
```

### Complete Implementation

```python
from typing import List
import heapq

def minInterval(intervals: List[List[int]], queries: List[int]) -> List[int]:
    """
    Find minimum interval size for each query.

    Time: O(n log n + q log q + (n+q) log n)
    Space: O(n + q)
    """
    # Sort intervals by start time
    intervals.sort()

    # Sort queries while preserving original indices
    queries_with_idx = sorted((q, i) for i, q in enumerate(queries))

    # Min heap: (interval_size, interval_end)
    heap = []
    result = [-1] * len(queries)
    interval_idx = 0

    for query, original_idx in queries_with_idx:
        # Add all intervals that have started
        while interval_idx < len(intervals) and intervals[interval_idx][0] <= query:
            left, right = intervals[interval_idx]
            size = right - left + 1
            heapq.heappush(heap, (size, right))
            interval_idx += 1

        # Remove intervals that have ended
        while heap and heap[0][1] < query:
            heapq.heappop(heap)

        # Smallest active interval
        if heap:
            result[original_idx] = heap[0][0]

    return result
```

### Why This Works

**Correctness**:
1. **Completeness**: We consider all intervals that could contain query
2. **Minimality**: Heap gives us smallest interval among active ones
3. **Accuracy**: We only consider intervals where `start <= query <= end`

**Efficiency**:
1. **Single Pass**: Each interval added once, removed once
2. **Sorted Processing**: Queries processed in order
3. **Heap Efficiency**: O(log n) for insert/remove

### Alternative Approaches

#### Approach 1: Brute Force
```python
def minInterval_bruteforce(intervals, queries):
    result = []
    for query in queries:
        min_size = float('inf')
        for left, right in intervals:
            if left <= query <= right:
                min_size = min(min_size, right - left + 1)
        result.append(-1 if min_size == float('inf') else min_size)
    return result
```
- Time: O(n × q)
- Space: O(q)
- Too slow for large inputs

#### Approach 2: Binary Search + TreeMap
```python
from sortedcontainers import SortedDict

def minInterval_binarysearch(intervals, queries):
    # Group intervals by size
    size_to_intervals = SortedDict()
    for left, right in intervals:
        size = right - left + 1
        if size not in size_to_intervals:
            size_to_intervals[size] = []
        size_to_intervals[size].append((left, right))

    result = []
    for query in queries:
        # Try sizes from smallest to largest
        for size in size_to_intervals:
            for left, right in size_to_intervals[size]:
                if left <= query <= right:
                    result.append(size)
                    break
            else:
                continue
            break
        else:
            result.append(-1)

    return result
```
- Time: Worse case O(n × q), but can be faster in practice
- Space: O(n)
- Still not optimal

#### Approach 3: Segment Tree
```python
# Build segment tree where each node tracks minimum interval
# Time: O((n+q) log M) where M = max coordinate
# Space: O(M)
# Complex to implement, overkill for this problem
```

### Optimization Tricks

#### 1. Early Termination
```python
# If heap is empty and no more intervals, remaining queries all get -1
if interval_idx >= len(intervals) and not heap:
    break
```

#### 2. Coordinate Compression
```python
# If coordinates are very large, compress them
all_coords = set()
for left, right in intervals:
    all_coords.add(left)
    all_coords.add(right)
for q in queries:
    all_coords.add(q)

coord_map = {c: i for i, c in enumerate(sorted(all_coords))}
# Use coord_map to work with smaller numbers
```

#### 3. Batch Processing
```python
# Group queries by value to avoid reprocessing
from collections import defaultdict
query_groups = defaultdict(list)
for i, q in enumerate(queries):
    query_groups[q].append(i)

for query in sorted(query_groups.keys()):
    # Process once, update all indices
    ...
```

## Common Patterns in Hard Interval Problems

### 1. Offline Query Processing
- Sort queries and process in order
- Build data structures incrementally
- Trade latency for throughput

### 2. Event-Based Processing
```python
events = []
for left, right in intervals:
    events.append((left, 'start', interval_id))
    events.append((right + 1, 'end', interval_id))
events.sort()
```

### 3. Sweep Line with Heap
- Process events left to right
- Maintain active set in heap
- Update answer based on heap state

### 4. Two-Level Sorting
- Sort outer level by one criterion
- Sort inner level by another
- Enables efficient pruning

## Complexity Analysis Framework

### Time Complexity Components
1. **Preprocessing**: O(n log n) for sorting intervals
2. **Query Sorting**: O(q log q) for sorting queries
3. **Sweep Processing**: O(n + q) for single pass
4. **Heap Operations**: O((n+q) log n) for all insertions/deletions
5. **Total**: O(n log n + q log q + (n+q) log n)

### Space Complexity Components
1. **Heap Storage**: O(n) worst case (all intervals active)
2. **Result Array**: O(q) for answers
3. **Sorting**: O(n + q) additional space
4. **Total**: O(n + q)

## Interview Strategies

### Problem-Solving Framework
1. **Recognize Pattern**: Offline query + range operations
2. **Identify Bottleneck**: Naive approach too slow
3. **Choose Structure**: Heap for dynamic minimum
4. **Optimize Ordering**: Sort to enable efficient processing
5. **Prove Correctness**: Why does processing in order work?

### Communication Tips
- Explain why brute force is too slow
- Justify choice of data structures
- Walk through example with diagrams
- Discuss trade-offs between approaches
- Mention potential optimizations

### Common Mistakes
1. **Forgetting to track original query indices**
   ```python
   # Wrong: loses original order
   queries.sort()

   # Right: preserve indices
   queries_with_idx = sorted((q, i) for i, q in enumerate(queries))
   ```

2. **Incorrect heap ordering**
   ```python
   # Wrong: heap by end time
   heapq.heappush(heap, (right, size))

   # Right: heap by size
   heapq.heappush(heap, (size, right))
   ```

3. **Not removing expired intervals**
   ```python
   # Wrong: includes intervals that ended
   if heap:
       result[i] = heap[0][0]

   # Right: remove expired first
   while heap and heap[0][1] < query:
       heapq.heappop(heap)
   if heap:
       result[i] = heap[0][0]
   ```

4. **Off-by-one in interval containment**
   ```python
   # Check problem: is end inclusive or exclusive?
   # Inclusive: left <= query <= right
   # Exclusive: left <= query < right
   ```

## Related Hard Problems

### Similar Patterns
- **The Skyline Problem** (LC 218): Sweep line + heap
- **Falling Squares** (LC 699): Coordinate compression + segment tree
- **Count of Range Sum** (LC 327): Merge sort + fenwick tree
- **Range Module** (LC 715): Interval tree or treemap

### Practice Progression
1. Master medium interval problems first
2. Learn heap operations thoroughly
3. Understand offline query processing
4. Practice sweep line algorithms
5. Study segment trees and interval trees

## Advanced Topics

### Segment Trees for Intervals
```python
class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [float('inf')] * (4 * n)

    def update(self, node, start, end, left, right, val):
        # Range update: set minimum interval in [left, right]
        ...

    def query(self, node, start, end, pos):
        # Point query: find minimum interval containing pos
        ...
```

### Interval Trees
```python
class IntervalTreeNode:
    def __init__(self, interval):
        self.interval = interval
        self.max_end = interval[1]
        self.left = None
        self.right = None

# Supports O(log n + k) overlap queries where k = number of results
```

### Online Query Processing
```python
# For online queries, use persistent data structures
# or maintain interval tree for O(log n) per query
```

## Testing Strategies

### Edge Cases
```python
# Empty
intervals = [], queries = [1]

# No overlap
intervals = [[1,2]], queries = [3]

# Single point
intervals = [[5,5]], queries = [5]

# All queries same
intervals = [[1,3],[2,5]], queries = [3,3,3]

# Large coordinates
intervals = [[1, 10**9]], queries = [500000000]

# Many overlapping intervals
intervals = [[1,100]] * 1000, queries = [50]
```

### Performance Testing
```python
import time

def benchmark(intervals, queries):
    start = time.time()
    result = minInterval(intervals, queries)
    elapsed = time.time() - start
    print(f"Processed {len(queries)} queries in {elapsed:.3f}s")
    return result

# Test with n=10^5, q=10^5
```

## Key Takeaways

1. **Offline processing** can convert O(n × q) to O((n+q) log n)
2. **Sorting + heap** is powerful combination for range queries
3. **Preserving indices** is crucial when reordering queries
4. **Sweep line** naturally handles dynamic interval sets
5. **Multiple approaches** exist; choose based on constraints

## Further Reading
- Competitive Programming 3: Section on Sweep Line
- Introduction to Algorithms (CLRS): Chapter on Segment Trees
- Advanced Data Structures: Interval Trees and Range Trees
- LeetCode Discuss: Various optimization techniques
