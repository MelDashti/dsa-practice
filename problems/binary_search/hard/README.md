# Binary Search - Hard Problems

## Overview

Hard binary search problems combine multiple advanced concepts: complex search spaces, intricate feasibility functions, mathematical insights, and often require merging multiple algorithms. These problems test deep understanding of binary search principles and creative problem-solving.

## Key Concepts

### Advanced Techniques

1. **Merge of Sorted Arrays**: Binary search to find kth element or median
2. **Complex Search Spaces**: Multi-dimensional or non-obvious search ranges
3. **Mathematical Optimization**: Using binary search for optimization problems
4. **Two-Pointer + Binary Search**: Combining multiple techniques
5. **Partition-based Binary Search**: Finding optimal split points

## Problems in This Section

### 1. Median of Two Sorted Arrays (LC 4)
**Concept**: Binary search for partition point in merged arrays

**Problem**: Find median of two sorted arrays in O(log(min(m,n))) time

**Key Ideas**:
- Median divides array into two equal halves
- Use binary search on the shorter array
- Find partition where left half ≤ right half
- Partition point satisfies: `maxLeft1 ≤ minRight2 AND maxLeft2 ≤ minRight1`
- Handle odd/even total length for median calculation

**Why This Works**:
```
Array1: [1, 3, 8, 9, 15]
Array2: [7, 11, 18, 19, 21, 25]

Partition at:
Array1: [1, 3, 8] | [9, 15]
Array2: [7, 11] | [18, 19, 21, 25]

Merged left half: [1, 3, 7, 8, 11]
Merged right half: [9, 15, 18, 19, 21, 25]

Check: max(left) ≤ min(right)
       11 ≤ 9? No → adjust partition

Correct partition:
Array1: [1, 3] | [8, 9, 15]
Array2: [7, 11, 18, 19] | [21, 25]

Check: max(3, 19) ≤ min(8, 21) → 19 ≤ 8? No

Correct partition:
Array1: [1, 3, 8, 9] | [15]
Array2: [7, 11] | [18, 19, 21, 25]

Check: max(9, 11) ≤ min(15, 18) → 11 ≤ 15? Yes!
Median = (11 + 15) / 2 = 13
```

**Algorithm**:
1. Ensure nums1 is the shorter array (minimize binary search range)
2. Binary search on nums1 for partition point
3. Calculate corresponding partition in nums2: `(m+n+1)//2 - partition1`
4. Get boundary values: `maxLeft1, minRight1, maxLeft2, minRight2`
5. Check if partition is valid: `maxLeft1 ≤ minRight2 AND maxLeft2 ≤ minRight1`
6. If valid, calculate median based on odd/even total length
7. If maxLeft1 > minRight2, move partition left
8. If maxLeft2 > minRight1, move partition right

**Pattern**: Binary search on partition point with validation

**Time Complexity**: O(log(min(m, n)))
**Space Complexity**: O(1)

**Implementation**:
```python
def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is shorter
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1

        # Get boundary values
        maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        minRight1 = float('inf') if partition1 == m else nums1[partition1]

        maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        minRight2 = float('inf') if partition2 == n else nums2[partition2]

        # Check if partition is correct
        if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
            # Found correct partition
            if (m + n) % 2 == 0:
                return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
            else:
                return max(maxLeft1, maxLeft2)
        elif maxLeft1 > minRight2:
            # Partition1 too far right
            right = partition1 - 1
        else:
            # Partition1 too far left
            left = partition1 + 1

    raise ValueError("Input arrays are not sorted")
```

**Detailed Walkthrough**:

Let's trace through an example: `nums1 = [1, 3]`, `nums2 = [2]`

```
m = 2, n = 1, total = 3 (odd)
Target: (m + n + 1) // 2 = 2 elements in left partition

Initial: left = 0, right = 2

Iteration 1:
  partition1 = (0 + 2) // 2 = 1
  partition2 = 2 - 1 = 1

  maxLeft1 = nums1[0] = 1
  minRight1 = nums1[1] = 3
  maxLeft2 = nums2[0] = 2
  minRight2 = inf

  Check: maxLeft1 ≤ minRight2? 1 ≤ inf ✓
         maxLeft2 ≤ minRight1? 2 ≤ 3 ✓

  Valid partition!
  Merged: [1, 2] | [3]
  Median (odd) = max(1, 2) = 2
```

**Edge Cases**:
```python
# One array empty
nums1 = [], nums2 = [1, 2, 3]
# Partition1 = 0, use all of nums2

# No overlap
nums1 = [1, 2], nums2 = [3, 4]

# Complete overlap
nums1 = [1, 5], nums2 = [2, 3, 4]

# Even vs odd total length
nums1 = [1, 2], nums2 = [3, 4]  # Even: avg of two middle
nums1 = [1, 2], nums2 = [3, 4, 5]  # Odd: one middle
```

**Why Use Infinity?**
- When partition is at boundary (0 or m/n), use infinity for comparison
- `-inf` for maxLeft: Ensures left boundary doesn't affect comparison
- `+inf` for minRight: Ensures right boundary doesn't affect comparison

**Common Variations**:
1. Find kth smallest element in two sorted arrays
2. Find kth largest element
3. Merge k sorted arrays
4. Find range of elements in merged array

## Advanced Insights

### Partition-Based Binary Search

The key insight is that we're not searching for a value, but for a **partition point**:

```
Instead of: "Is this value the median?"
Think: "Does this partition divide the arrays correctly?"
```

**Partition Properties**:
1. Left partition has `(m + n + 1) // 2` elements
2. All left elements ≤ all right elements
3. Median is at the boundary of left and right

### Mathematical Elegance

**Why `(m + n + 1) // 2`?**
- Works for both odd and even total lengths
- Odd: Left has one more element (contains median)
- Even: Left and right have equal elements

```
m=2, n=3, total=5 (odd):  (5+1)//2 = 3 → [a,b,c] | [d,e]
m=2, n=2, total=4 (even): (4+1)//2 = 2 → [a,b] | [c,d]
```

### Binary Search Optimization

**Why search on shorter array?**
- Minimizes search space: O(log(min(m,n)))
- Ensures partition2 stays valid: `0 ≤ partition2 ≤ n`
- If partition1 = m, partition2 = (m+n+1)//2 - m
- If m > n, partition2 could be negative!

**Search Space**:
```
left = 0: All elements of nums1 in right partition
right = m: All elements of nums1 in left partition
```

### Related Problems

**Find Kth Element in Two Sorted Arrays**:
```python
def findKthElement(nums1, nums2, k):
    # Similar to median, but partition size = k
    # Use binary search to find partition where left has k elements
    pass
```

**Median of K Sorted Arrays**:
- Can extend to multiple arrays
- Use min heap for efficient merging
- Or generalize partition-based approach

## Learning Path

1. **Understand median concept**: What does median represent?
2. **Study partition idea**: Why partition, not direct search?
3. **Master boundary handling**: Infinity values and edge cases
4. **Trace through examples**: Multiple cases (odd/even, overlapping/non-overlapping)
5. **Implement from scratch**: Without looking at solution
6. **Explain to others**: Can you teach this algorithm?

## Common Mistakes to Avoid

1. **Searching in longer array**: Always binary search on shorter array
2. **Wrong partition formula**: `partition2 = (m+n+1)//2 - partition1`
3. **Boundary handling**: Forgetting infinity values at boundaries
4. **Even/odd confusion**: Different median calculation for even vs odd
5. **Wrong inequality checks**: Must check BOTH cross-comparisons
6. **Integer overflow**: In some languages, `(left + right) // 2` can overflow
7. **Not handling empty arrays**: Edge case when one array is empty

## Debugging Techniques

1. **Draw the partitions**: Visualize where partition cuts each array
2. **Print values at each iteration**:
   ```python
   print(f"partition1={partition1}, partition2={partition2}")
   print(f"maxLeft1={maxLeft1}, minRight1={minRight1}")
   print(f"maxLeft2={maxLeft2}, minRight2={minRight2}")
   ```
3. **Test with simple cases**:
   - `[1], [2]`
   - `[1, 2], [3, 4]`
   - `[1, 3], [2]`
   - `[], [1]`
   - `[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]`

4. **Verify partition properties**:
   - Left partition size: `partition1 + partition2 == (m+n+1)//2`?
   - Cross comparison: `maxLeft1 ≤ minRight2 AND maxLeft2 ≤ minRight1`?
   - Boundaries: `0 ≤ partition1 ≤ m AND 0 ≤ partition2 ≤ n`?

## Interview Tips

1. **Start with brute force**: "We could merge and find median in O(m+n)"
2. **Explain the optimization**: "Binary search can reduce to O(log min(m,n))"
3. **Discuss partition concept**: Draw diagrams to visualize
4. **Handle edge cases explicitly**: Empty arrays, no overlap, equal elements
5. **Walk through a concrete example**: Show the algorithm in action
6. **Discuss complexity**: Why O(log min(m,n))? Why search shorter array?

## Practice Strategy

1. **Understand the problem deeply**: Don't just memorize the solution
2. **Implement brute force first**: Merge and find median
3. **Study the optimal approach**: Understand why partition works
4. **Code without looking**: Can you implement from understanding?
5. **Test extensively**: Many edge cases to consider
6. **Teach someone else**: Best way to solidify understanding
7. **Solve variations**: Kth element, multiple arrays

## Extension Problems

Once you master this problem:
- **Kth Smallest Element in Sorted Matrix (LC 378)**: Similar binary search idea
- **Find K Pairs with Smallest Sums (LC 373)**: Multiple sorted arrays
- **Merge K Sorted Lists (LC 23)**: Related merging problem
- **Count of Smaller Numbers After Self (LC 315)**: Advanced merge concept

## Complexity Analysis

### Time Complexity: O(log(min(m, n)))
- Binary search on shorter array
- Each iteration does O(1) work
- Number of iterations = log(min(m, n))

### Space Complexity: O(1)
- No extra arrays allocated
- Only storing pointers and boundary values
- Recursive approach would be O(log(min(m, n))) for call stack

### Comparison with Alternatives

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Merge arrays | O(m+n) | O(m+n) | Straightforward but slow |
| Two pointers | O(m+n) | O(1) | Better space, still O(m+n) time |
| Binary search | O(log(min(m,n))) | O(1) | Optimal solution |

## Key Takeaways

- Binary search applies to partition points, not just values
- Searching on shorter array is crucial for correctness and efficiency
- Partition satisfies: left side ≤ right side in merged view
- Infinity values elegantly handle boundary cases
- Understanding > memorization: Know WHY each step works
- This technique extends to many "find kth element" problems
- Median is a special case of "find kth element" where k = (m+n)//2

## Advanced Variations

### Weighted Median
Find median where elements have weights:
```python
def weightedMedian(nums1, weights1, nums2, weights2):
    # Partition based on cumulative weights
    # Target weight = (total_weight + 1) / 2
    pass
```

### Online Median
Maintain median as elements arrive:
- Use two heaps (max heap for left, min heap for right)
- Related but different from two sorted arrays
- O(log n) per insertion

### Approximation Algorithms
For very large datasets:
- Sampling-based median finding
- Trade accuracy for speed
- Useful in distributed systems

This problem is considered one of the hardest binary search problems because it requires deep understanding of partitioning, boundary handling, and mathematical reasoning. Master this, and you'll have conquered one of the most elegant algorithms in computer science!
