# Intervals - Medium

## Overview
Medium interval problems build upon basic overlap detection and introduce operations like merging, inserting, and optimizing interval arrangements. These problems require more sophisticated data structure usage and often involve greedy algorithms or priority queues.

## Key Concepts

### 1. Interval Merging
Combining overlapping or adjacent intervals into a single interval:
- `[1,3]` + `[2,6]` → `[1,6]`
- `[1,4]` + `[4,5]` → `[1,5]` (if endpoints touch)

### 2. Interval Insertion
Adding a new interval to an existing sorted list while maintaining properties:
- May require merging with existing intervals
- Must maintain sorted order
- Handle overlaps with multiple intervals

### 3. Interval Scheduling
Selecting maximum number of non-overlapping intervals:
- Classic greedy algorithm problem
- Sort by end time (not start time!)
- Always choose the interval that ends earliest

### 4. Resource Allocation
Determining minimum resources needed for overlapping intervals:
- Equivalent to finding maximum overlap at any point
- Use sweep line algorithm or min heap
- Track active intervals at each time point

## Problems in This Section

### Merge Intervals (LC 56)
**Problem**: Merge all overlapping intervals.

**Key Insights**:
- Sort by start time first
- Merge consecutive intervals if they overlap
- Two intervals merge if: `prev.end >= curr.start`

**Approach**:
```python
# Sort: O(n log n)
# Single pass merge: O(n)
# Space for result: O(n)
```

**Pattern**: Greedy + Sorting

---

### Insert Interval (LC 57)
**Problem**: Insert a new interval into a sorted list and merge if necessary.

**Key Insights**:
- Three phases: before, overlapping, after
- Add intervals before the new one (no overlap)
- Merge all overlapping intervals
- Add remaining intervals after

**Approach**:
```python
# Before: intervals ending before new interval starts
# Merge: all intervals that overlap with new interval
# After: intervals starting after new interval ends
# Time: O(n), Space: O(n)
```

**Pattern**: Three-way partition

---

### Non-overlapping Intervals (LC 435)
**Problem**: Find minimum number of intervals to remove to make remaining non-overlapping.

**Key Insights**:
- Equivalent to finding maximum non-overlapping intervals
- Greedy: Always keep interval with earliest end time
- Sort by end time, not start time!
- Answer = total - maximum_non_overlapping

**Approach**:
```python
# Sort by end time: O(n log n)
# Greedy selection: O(n)
# Total: O(n log n)
```

**Pattern**: Greedy + Activity Selection

---

### Meeting Rooms II (LC 253)
**Problem**: Find minimum number of conference rooms needed.

**Key Insights**:
- Equivalent to maximum number of overlapping intervals
- Use min heap to track room end times
- When meeting starts, remove rooms that have freed up
- Answer = maximum heap size during iteration

**Approach**:
```python
# Sort by start time: O(n log n)
# Heap operations: O(n log n)
# Total: O(n log n), Space: O(n)
```

**Alternative Approach** (Two Pointers):
```python
# Separate start and end times
# Sort both arrays
# Use two pointers to track active rooms
# Time: O(n log n), Space: O(n)
```

**Pattern**: Sweep Line + Min Heap

## Advanced Patterns

### 1. Sweep Line Algorithm
Process events in chronological order:
```python
events = []
for start, end in intervals:
    events.append((start, 1))   # +1 for start
    events.append((end, -1))    # -1 for end

events.sort()
current = max_overlap = 0
for time, delta in events:
    current += delta
    max_overlap = max(max_overlap, current)
```

### 2. Greedy Selection
For interval scheduling:
```python
# Sort by end time
intervals.sort(key=lambda x: x[1])

count = 0
last_end = float('-inf')

for start, end in intervals:
    if start >= last_end:
        count += 1
        last_end = end
```

### 3. Binary Search on Intervals
Finding insertion point or overlap:
```python
def find_overlap_point(intervals, target):
    left, right = 0, len(intervals) - 1

    while left <= right:
        mid = (left + right) // 2
        if intervals[mid][1] < target[0]:
            left = mid + 1
        elif intervals[mid][0] > target[1]:
            right = mid - 1
        else:
            return mid  # Found overlap

    return -1  # No overlap
```

## Comparison of Approaches

### Merge vs Insert
| Aspect | Merge Intervals | Insert Interval |
|--------|----------------|-----------------|
| Input | Unsorted intervals | Sorted intervals + new interval |
| Sorting | Required | Already sorted |
| Time | O(n log n) | O(n) |
| Pattern | Sort then merge | Three-way partition |

### Scheduling vs Room Allocation
| Aspect | Non-overlapping | Meeting Rooms II |
|--------|----------------|-------------------|
| Goal | Maximum selection | Minimum resources |
| Sort by | End time | Start time |
| Data Structure | Array | Min Heap |
| Pattern | Greedy | Sweep Line |

## Time & Space Complexity Analysis

| Problem | Time | Space | Key Factor |
|---------|------|-------|------------|
| Merge Intervals | O(n log n) | O(n) | Sorting + result array |
| Insert Interval | O(n) | O(n) | Single pass, sorted input |
| Non-overlapping | O(n log n) | O(1) | Sorting + greedy |
| Meeting Rooms II | O(n log n) | O(n) | Sorting + heap |

## Common Pitfalls

### 1. Wrong Sort Key
```python
# ❌ Wrong for activity selection
intervals.sort(key=lambda x: x[0])  # By start

# ✓ Correct for activity selection
intervals.sort(key=lambda x: x[1])  # By end
```

### 2. Off-by-One Errors
```python
# Depends on problem: are endpoints inclusive?
# [1,2] and [2,3] overlap? Depends on definition!

# Exclusive end (like Python ranges)
def overlap_exclusive(a, b):
    return a[0] < b[1] and b[0] < a[1]

# Inclusive end
def overlap_inclusive(a, b):
    return a[0] <= b[1] and b[0] <= a[1]
```

### 3. Not Considering Edge Cases
- Empty intervals list
- Single interval
- All intervals overlap completely
- No intervals overlap
- Intervals with same start or end times

### 4. Inefficient Merging
```python
# ❌ Wrong: Creating new list every time
result = []
for interval in intervals:
    result = merge(result, interval)  # O(n) each time = O(n²) total

# ✓ Correct: Merge in single pass
result = [intervals[0]]
for interval in intervals[1:]:
    if can_merge(result[-1], interval):
        result[-1] = merge_two(result[-1], interval)
    else:
        result.append(interval)
```

## Interview Tips

### Questions to Ask
1. Are interval endpoints inclusive or exclusive?
2. Can intervals have zero length? (e.g., `[5,5]`)
3. Are intervals already sorted?
4. How should we handle invalid inputs?
5. Do intervals represent discrete time slots or continuous time?

### Problem-Solving Steps
1. **Clarify**: Understand interval definition (inclusive/exclusive)
2. **Visualize**: Draw timeline with sample intervals
3. **Sort**: Determine if sorting helps (usually yes)
4. **Choose structure**: Array, heap, or sweep line?
5. **Handle edges**: Empty, single, all overlap, none overlap
6. **Optimize**: Can we reduce space? Early termination?

## Code Templates

### Merge Intervals Template
```python
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]

    for current in intervals[1:]:
        last = result[-1]

        if current[0] <= last[1]:  # Overlap or adjacent
            # Merge: extend the end time
            result[-1] = [last[0], max(last[1], current[1])]
        else:
            # No overlap: add new interval
            result.append(current)

    return result
```

### Insert Interval Template
```python
def insert_interval(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # Merge all overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval = [
            min(new_interval[0], intervals[i][0]),
            max(new_interval[1], intervals[i][1])
        ]
        i += 1

    result.append(new_interval)

    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

### Activity Selection Template
```python
def max_non_overlapping(intervals):
    if not intervals:
        return 0

    # Sort by end time
    intervals.sort(key=lambda x: x[1])

    count = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:
            count += 1
            last_end = end

    return count
```

### Meeting Rooms (Min Heap) Template
```python
import heapq

def min_meeting_rooms(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap = []  # Min heap of end times

    heapq.heappush(heap, intervals[0][1])

    for start, end in intervals[1:]:
        # If earliest ending meeting has ended, reuse room
        if heap[0] <= start:
            heapq.heappop(heap)

        # Allocate room for current meeting
        heapq.heappush(heap, end)

    return len(heap)
```

### Meeting Rooms (Two Pointers) Template
```python
def min_meeting_rooms_two_pointers(intervals):
    if not intervals:
        return 0

    start_times = sorted([i[0] for i in intervals])
    end_times = sorted([i[1] for i in intervals])

    rooms = max_rooms = 0
    start_ptr = end_ptr = 0

    while start_ptr < len(intervals):
        if start_times[start_ptr] < end_times[end_ptr]:
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            start_ptr += 1
        else:
            rooms -= 1
            end_ptr += 1

    return max_rooms
```

## Visual Examples

### Merge Intervals Example
```
Input:   [1,3] [2,6] [8,10] [15,18]
         |-----|
           |-------|
                     |-----|
                                |-----|

After sort: Already sorted

Merge:   [1,3] + [2,6] → [1,6]
         |----------|
                     |-----|
                                |-----|

Result:  [1,6] [8,10] [15,18]
```

### Insert Interval Example
```
Intervals: [1,2] [3,5] [6,7] [8,10] [12,16]
           |--| |---| |--| |----| |------|
New:                    [4,8]
                        |---------|

Phase 1 (before): [1,2]
Phase 2 (merge):  [3,5] [6,7] [8,10] → [3,10]
Phase 3 (after):  [12,16]

Result:  [1,2] [3,10] [12,16]
```

### Non-overlapping Intervals Example
```
Input:   [1,2] [2,3] [3,4] [1,3]
         |--| |--| |--|
         |------|

Sort by end: [1,2] [1,3] [2,3] [3,4]
             |--|
             |------|
                |--|
                   |--|

Greedy:  Keep [1,2], skip [1,3], keep [2,3], keep [3,4]
         |--| X |--| |--|

Remove: 1 interval ([1,3])
```

### Meeting Rooms II Example
```
Meetings: [0,30] [5,10] [15,20]
          |--------------|
              |---|
                   |-----|

Timeline:
0         5   10  15  20     30
|         |   |   |   |      |
[0,30] starts    ●
[5,10] starts       ● (need 2nd room)
[5,10] ends            ✓ (free room)
[15,20] starts            ● (reuse room)
[15,20] ends                  ✓
[0,30] ends                      ✓

Max concurrent: 2 rooms
```

## Practice Strategy

### Progression
1. Start with Merge Intervals (most fundamental)
2. Move to Insert Interval (builds on merging)
3. Try Non-overlapping Intervals (introduces greedy)
4. Finish with Meeting Rooms II (most complex)

### Key Skills to Master
- Sorting with custom comparators
- Greedy algorithm design
- Heap operations (heapq in Python)
- Two-pointer technique
- Sweep line algorithm
- Recognizing when to sort by start vs end time

### Related Problems
- Interval List Intersections
- Employee Free Time
- My Calendar I/II/III
- Car Pooling
- The Skyline Problem (Hard)

## Debugging Checklist
- [ ] Verified correct sort key (start or end?)
- [ ] Checked overlap condition (< or <=?)
- [ ] Handled empty input
- [ ] Handled single interval
- [ ] Tested with all overlapping intervals
- [ ] Tested with no overlapping intervals
- [ ] Checked boundary cases (same start/end times)
- [ ] Verified result array is properly built
- [ ] Checked for off-by-one errors
