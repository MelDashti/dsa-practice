# Binary Search - Medium Problems

## Overview

Medium binary search problems extend beyond searching for a target value. They introduce concepts like binary search on answer space, handling rotated/modified arrays, and optimizing solutions through intelligent search space reduction.

## Key Concepts

### Advanced Binary Search Patterns

1. **Binary Search on Answer**: Search the solution space, not the array
2. **Modified Binary Search**: Handling rotated, pivoted, or modified arrays
3. **2D Binary Search**: Applying binary search to matrices
4. **Feasibility Function**: Check if a value is valid as an answer
5. **Minimizing/Maximizing**: Finding optimal values using binary search

### When to Use Binary Search

Look for these clues:
- "Find minimum/maximum value such that..."
- "Find the smallest/largest value where condition holds"
- Sorted or partially sorted data
- Search space has monotonic property
- Can validate a solution in O(n) or less

## Problems in This Section

### 1. Search in 2D Matrix (LC 74)
**Concept**: Treat 2D matrix as 1D sorted array

**Key Ideas**:
- Matrix sorted row-wise and column-wise
- Can be viewed as flattened sorted array
- Convert 2D index to 1D: `index = row × cols + col`
- Convert 1D to 2D: `row = mid // cols`, `col = mid % cols`
- Standard binary search on virtual 1D array

**Pattern**: Binary search with index conversion

**Time Complexity**: O(log(m × n))
**Space Complexity**: O(1)

**Implementation**:
```python
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        mid_value = matrix[mid // n][mid % n]

        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

---

### 2. Koko Eating Bananas (LC 875)
**Concept**: Binary search on answer space

**Problem**: Find minimum eating speed k such that Koko can eat all bananas in h hours

**Key Ideas**:
- Search space: [1, max(piles)] (possible eating speeds)
- Feasibility check: Can finish all piles in h hours at speed k?
- Want minimum k where feasibility is true
- Monotonic property: if speed k works, k+1 also works
- Binary search for smallest valid k

**Pattern**: Binary search on answer with feasibility function

**Time Complexity**: O(n log m) where m = max(piles)
**Space Complexity**: O(1)

**Template for Binary Search on Answer**:
```python
def minEatingSpeed(piles, h):
    def canFinish(k):
        hours = sum((pile - 1) // k + 1 for pile in piles)
        return hours <= h

    left, right = 1, max(piles)

    while left < right:
        mid = left + (right - left) // 2
        if canFinish(mid):
            right = mid  # Can finish, try slower
        else:
            left = mid + 1  # Too slow, must eat faster

    return left
```

---

### 3. Search in Rotated Sorted Array (LC 33)
**Concept**: Modified binary search on rotated array

**Key Ideas**:
- Array was sorted, then rotated at some pivot
- One half is always properly sorted
- Determine which half is sorted
- Check if target is in sorted half
- Adjust search space accordingly

**Pattern**: Modified binary search with additional logic

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Algorithm**:
```python
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        if nums[left] <= nums[mid]:  # Left half sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

---

### 4. Find Minimum in Rotated Sorted Array (LC 153)
**Concept**: Finding pivot point using binary search

**Key Ideas**:
- Minimum is at the rotation point
- Compare mid with rightmost element
- If nums[mid] > nums[right], minimum is in right half
- If nums[mid] < nums[right], minimum is in left half (including mid)
- No duplicates makes this straightforward

**Pattern**: Binary search for inflection point

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Implementation**:
```python
def findMin(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1  # Minimum in right half
        else:
            right = mid  # Minimum in left half or at mid

    return nums[left]
```

---

### 5. Time Based Key-Value Store (LC 981)
**Concept**: Binary search for timestamp lookup

**Key Ideas**:
- Store (timestamp, value) pairs for each key
- Timestamps are strictly increasing
- Binary search to find largest timestamp ≤ target
- Use right boundary binary search variation

**Pattern**: Binary search for boundary value

**Time Complexity**: O(log n) per get operation
**Space Complexity**: O(n) for storage

**Implementation**:
```python
class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key, value, timestamp):
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        if key not in self.store:
            return ""

        values = self.store[key]
        left, right = 0, len(values) - 1
        result = ""

        while left <= right:
            mid = left + (right - left) // 2
            if values[mid][0] <= timestamp:
                result = values[mid][1]
                left = mid + 1  # Try to find larger timestamp
            else:
                right = mid - 1

        return result
```

## Common Patterns

### Pattern 1: Binary Search on Answer
When to use: "Find minimum/maximum value such that..."

**Template**:
```python
def binary_search_answer(arr, condition):
    def is_feasible(mid):
        # Check if mid satisfies the condition
        pass

    left, right = min_possible, max_possible

    while left < right:
        mid = left + (right - left) // 2
        if is_feasible(mid):
            right = mid  # For minimization
            # left = mid + 1  # For maximization
        else:
            left = mid + 1  # For minimization
            # right = mid  # For maximization

    return left
```

### Pattern 2: Search in Rotated Array
**Key insight**: One half is always sorted

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Check which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

### Pattern 3: Finding Boundaries
**Left boundary** (smallest index where condition is true):
```python
def find_left_boundary(arr, target):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] >= target:
            result = mid
            right = mid - 1  # Keep searching left
        else:
            left = mid + 1

    return result
```

**Right boundary** (largest index where condition is true):
```python
def find_right_boundary(arr, target):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            result = mid
            left = mid + 1  # Keep searching right
        else:
            right = mid - 1

    return result
```

## Key Insights

### Binary Search on Answer
1. **Identify search space**: What are min and max possible answers?
2. **Monotonic property**: If x works, does x+1 or x-1 also work?
3. **Feasibility function**: Can you check if a value is valid in O(n)?
4. **Minimize or maximize**: Are you finding minimum or maximum?

**Example Problems**:
- Minimum eating speed (Koko Bananas)
- Minimum capacity to ship packages
- Split array largest sum
- Minimum time to complete tasks

### Rotated Array Tricks
1. **One half is always sorted**: Use this to determine search direction
2. **Compare with boundaries**: `nums[left]` vs `nums[mid]` determines which half
3. **Target in sorted half**: Use normal range check
4. **Target in rotated half**: Must be in other half

### Index Conversion (2D to 1D)
For m×n matrix:
- **1D to 2D**: `row = index // n`, `col = index % n`
- **2D to 1D**: `index = row * n + col`
- **Total elements**: `m * n`
- **Last index**: `m * n - 1`

## Learning Path

1. **Master 2D Matrix**: Understand index conversion
2. **Practice Koko Bananas**: Learn binary search on answer
3. **Tackle Rotated Array**: Handle modified binary search
4. **Solve Find Minimum**: Find inflection points
5. **Implement TimeMap**: Boundary finding with timestamps

## Tips for Success

1. **Identify the pattern**: Is it search on answer? Rotated array? Boundary finding?
2. **Define search space clearly**: What are left and right initially?
3. **Write feasibility function**: For search on answer, separate the check
4. **Draw the array**: Visualize rotations and sorted portions
5. **Test edge cases**: Single element, no rotation, target at boundaries

## Common Mistakes to Avoid

1. **Wrong loop condition**: `left < right` vs `left <= right` depends on pattern
2. **Incorrect mid update**: When to use `left = mid + 1` vs `left = mid`
3. **Overlooking edge cases**: Empty array, single element, no rotation
4. **Feasibility function errors**: Off-by-one in capacity/speed calculations
5. **Not checking sorted half**: In rotated array, must determine which half

## Optimization Techniques

1. **Early termination**: Check boundaries before binary search
2. **Smart initialization**: Use better bounds if possible (e.g., not 1 to 10^9)
3. **Avoid redundant calculations**: Cache values if used multiple times
4. **Mathematical simplification**: `(pile - 1) // k + 1` instead of `ceil(pile / k)`

## Advanced Applications

### Binary Search on Answer - More Examples

**Split Array Largest Sum**:
```python
def splitArray(nums, m):
    def can_split(max_sum):
        count, curr_sum = 1, 0
        for num in nums:
            if curr_sum + num > max_sum:
                count += 1
                curr_sum = num
            else:
                curr_sum += num
        return count <= m

    left, right = max(nums), sum(nums)
    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## Next Steps

Once comfortable with medium problems:
- **Hard problems**: Multiple constraints, complex feasibility functions
- **Multi-dimensional search**: Binary search in multiple dimensions
- **Advanced optimization**: Ternary search, exponential search
- **Combined techniques**: Binary search + sliding window, + two pointers

## Key Takeaways

- Binary search applies beyond sorted arrays
- "Find minimum/maximum such that..." often means binary search on answer
- Rotated arrays need special handling but remain O(log n)
- Feasibility function is key to binary search on answer
- One half of rotated array is always properly sorted
- Index conversion enables binary search on 2D structures
