# Intervals - Easy

## Overview
Easy interval problems introduce the fundamental concepts of working with time ranges, intervals, and overlapping periods. These problems help build intuition about interval manipulation, which is crucial for more complex scheduling and range-based algorithms.

## Key Concepts

### 1. Interval Representation
- Intervals are typically represented as pairs: `[start, end]`
- Can be implemented as lists, tuples, or custom objects
- Start is usually inclusive, end can be inclusive or exclusive (problem-dependent)

### 2. Interval Relationships
Two intervals can have several relationships:
- **Overlap**: `[1, 5]` and `[3, 7]` overlap at `[3, 5]`
- **Non-overlapping**: `[1, 3]` and `[4, 6]` don't overlap
- **Contained**: `[2, 4]` is contained in `[1, 5]`
- **Adjacent**: `[1, 3]` and `[3, 5]` are adjacent (touching)

### 3. Common Patterns
- **Sorting**: Most interval problems benefit from sorting by start time
- **Sweep Line**: Process events in chronological order
- **Greedy Approach**: Make locally optimal choices

## Problems in This Section

### Meeting Rooms (LC 252)
**Problem**: Determine if a person can attend all meetings given their time intervals.

**Key Insights**:
- Sort intervals by start time
- Check if any consecutive meetings overlap
- Two meetings overlap if: `meeting1.end > meeting2.start`

**Approach**:
```python
# Sort by start time: O(n log n)
# Check consecutive pairs: O(n)
# Total: O(n log n)
```

**Common Pitfalls**:
- Forgetting to sort first
- Using `>=` instead of `>` for overlap check (depends on problem definition)
- Not handling edge cases (0 or 1 meeting)

**Related Patterns**:
- Array traversal after sorting
- Two-pointer technique (implicit)

## Learning Path

### Prerequisites
- Basic understanding of arrays and sorting
- Familiarity with comparison operations
- Understanding of time complexity

### Practice Tips
1. **Draw it out**: Visualize intervals on a timeline
2. **Sort first**: Most interval problems become easier after sorting
3. **Check boundaries**: Pay attention to inclusive/exclusive endpoints
4. **Edge cases**: Empty arrays, single intervals, identical intervals

### Next Steps
After mastering easy interval problems, move to:
- Medium: Multiple interval operations (merge, insert, remove)
- Learn about interval trees and segment trees for advanced problems

## Time & Space Complexity Patterns

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Sorting intervals | O(n log n) | O(1) - O(n) | Depends on sorting algorithm |
| Checking overlap | O(n) | O(1) | After sorting |
| Merging intervals | O(n) | O(n) | Building result array |

## Common Interview Questions
1. How do you determine if two intervals overlap?
2. Why is sorting usually the first step in interval problems?
3. What's the difference between `[1,3]` and `[3,5]` - do they overlap?
4. How would you handle intervals with the same start time?

## Additional Resources
- **Sorting Algorithms**: Understanding merge sort and quicksort
- **Comparators**: Custom sorting logic in Python
- **Lambda Functions**: For concise sorting keys
- **Two-Pointer Technique**: For checking consecutive elements

## Code Templates

### Basic Interval Overlap Check
```python
def intervals_overlap(a, b):
    """Check if two intervals [start, end] overlap."""
    return a[0] < b[1] and b[0] < a[1]
```

### Sorting Intervals
```python
def sort_intervals(intervals):
    """Sort intervals by start time, then by end time."""
    return sorted(intervals, key=lambda x: (x[0], x[1]))
```

### Checking All Meetings
```python
def can_attend_all(intervals):
    """Template for checking if all meetings can be attended."""
    if not intervals:
        return True

    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i-1][1] > intervals[i][0]:
            return False

    return True
```

## Visual Examples

### Non-overlapping Intervals
```
Meeting 1: [----]
Meeting 2:       [----]
Meeting 3:             [----]
Timeline: |-----|-----|-----|
Result: Can attend all ✓
```

### Overlapping Intervals
```
Meeting 1: [--------]
Meeting 2:     [--------]
Meeting 3:          [----]
Timeline: |-----|-----|-----|
Result: Cannot attend all ✗
```

## Debugging Tips
1. Print intervals after sorting to verify order
2. Draw the timeline on paper for small test cases
3. Check boundary conditions (equal start/end times)
4. Test with: empty array, single interval, all overlapping, none overlapping

## Performance Optimization
- **Early termination**: Return false as soon as overlap is found
- **In-place operations**: Avoid creating new arrays when possible
- **Custom comparators**: Use efficient comparison logic
- **Input validation**: Check for invalid intervals upfront
