# Binary Search - Easy Problems

## Overview

Easy binary search problems introduce the fundamental divide-and-conquer technique for searching in sorted data. Understanding binary search is crucial as it reduces search time from O(n) to O(log n).

## Key Concepts

### What is Binary Search?

Binary search is an efficient algorithm for finding a target value in a **sorted** array:
1. Compare target with middle element
2. If equal, return the index
3. If target is smaller, search left half
4. If target is larger, search right half
5. Repeat until found or search space is empty

### Why Binary Search?

- **Time Complexity**: O(log n) vs O(n) for linear search
- **Efficiency**: For 1 million elements, linear = 1M operations, binary = 20 operations
- **Foundation**: Basis for many optimization algorithms

### Binary Search Template

There are several valid templates. Here's the most common:

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # Not found
```

### Critical Details

1. **Initialization**: `left = 0, right = len(nums) - 1` (inclusive on both ends)
2. **Loop condition**: `while left <= right` (use <= for inclusive bounds)
3. **Mid calculation**: `mid = left + (right - left) // 2` (avoids overflow)
4. **Update pointers**: `left = mid + 1` or `right = mid - 1` (exclude mid)

## Problems in This Section

### 1. Binary Search (LC 704)
**Concept**: Classic binary search implementation

**Problem**: Find target in sorted array, return index or -1

**Key Ideas**:
- Array is sorted in ascending order
- Use standard binary search template
- Target either exists once or not at all
- Search space halves each iteration

**Edge Cases**:
- Empty array
- Single element
- Target at boundaries
- Target not in array

**Pattern**: Classic binary search

**Time Complexity**: O(log n)
**Space Complexity**: O(1) iterative, O(log n) recursive

**Implementation Notes**:
```python
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Why This Works**:
- Sorted array guarantees: if nums[mid] < target, target must be in right half
- Each iteration eliminates half the search space
- Loop terminates when left > right (search space exhausted)

## Common Patterns

### 1. Standard Binary Search
Finding exact target in sorted array
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### 2. Recursive Binary Search
Same algorithm, recursive approach
```python
def binary_search_recursive(nums, target, left, right):
    if left > right:
        return -1

    mid = left + (right - left) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search_recursive(nums, target, mid + 1, right)
    else:
        return binary_search_recursive(nums, target, left, mid - 1)
```

## Important Variations

### Finding Left Boundary
First occurrence of target in array with duplicates:
```python
def find_left(nums, target):
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### Finding Right Boundary
Last occurrence of target:
```python
def find_right(nums, target):
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

## Learning Path

1. **Understand the algorithm**: Study how search space reduces
2. **Implement iterative version**: Start with the standard template
3. **Practice recursive version**: Understand the base case and recursion
4. **Try variations**: Left boundary, right boundary, insertion point
5. **Visualize the process**: Draw the array and pointer movements

## Tips for Success

1. **Always check if array is sorted**: Binary search requires sorted data
2. **Use the correct loop condition**: `left <= right` for inclusive bounds
3. **Avoid integer overflow**: Use `left + (right - left) // 2` instead of `(left + right) // 2`
4. **Update pointers correctly**: `left = mid + 1` or `right = mid - 1` (exclude mid)
5. **Handle edge cases**: Empty array, single element, target at boundaries

## Common Mistakes to Avoid

1. **Wrong loop condition**: Using `left < right` with inclusive bounds (misses cases)
2. **Off-by-one errors**: Not updating `left = mid + 1` or `right = mid - 1`
3. **Integer overflow**: In some languages, `(left + right) / 2` can overflow
4. **Forgetting sorted requirement**: Binary search only works on sorted data
5. **Infinite loops**: Occurs when not excluding mid in pointer updates

## Debugging Tips

1. **Print the search space**: Log left, right, mid at each iteration
2. **Trace small examples**: Use [1,2,3,4,5] and trace the algorithm
3. **Test edge cases**:
   - Empty array: []
   - Single element: [1]
   - Two elements: [1,2]
   - Target at start: [1,2,3,4,5], target=1
   - Target at end: [1,2,3,4,5], target=5
   - Target not present: [1,2,3,4,5], target=6
4. **Check invariants**: After each iteration, is target in [left, right]?

## Time Complexity Analysis

Why is binary search O(log n)?

```
n = 16:
Iteration 1: 16 elements
Iteration 2: 8 elements
Iteration 3: 4 elements
Iteration 4: 2 elements
Iteration 5: 1 element

Number of iterations = log₂(16) = 4

General: After k iterations, n/(2^k) elements remain
When n/(2^k) = 1, we're done
k = log₂(n)
```

## Comparison with Linear Search

| Aspect | Linear Search | Binary Search |
|--------|--------------|---------------|
| Time Complexity | O(n) | O(log n) |
| Space Complexity | O(1) | O(1) iterative |
| Requirement | None | Sorted array |
| Use Case | Small arrays, unsorted | Large arrays, sorted |
| Example (n=1M) | 1M operations | 20 operations |

## Next Steps

Once comfortable with basic binary search:
- **Medium problems**: Binary search on answer, rotated arrays
- **Search variations**: Finding boundaries, insertion points
- **Binary search on functions**: Finding minimum/maximum
- **Advanced applications**: Optimization problems, space reduction

## Practice Exercises

To solidify understanding:
1. Implement both iterative and recursive versions
2. Implement finding left and right boundaries
3. Find insertion position for target in sorted array
4. Count occurrences of target (using left and right boundaries)
5. Search in infinite sorted array (without knowing the size)

## Key Takeaways

- Binary search reduces O(n) to O(log n) for sorted arrays
- Must exclude mid when updating pointers to avoid infinite loops
- Use `left + (right - left) // 2` to avoid overflow
- Loop condition `left <= right` for inclusive bounds
- Foundation for many advanced algorithms and optimization problems
