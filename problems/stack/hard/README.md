# Stack - Hard Problems

## Overview

Hard stack problems require mastery of advanced techniques, particularly monotonic stacks combined with dynamic programming concepts. These problems often involve optimizing brute force O(n²) or O(n³) solutions down to O(n) using clever stack manipulation.

## Key Concepts

### Advanced Techniques

1. **Monotonic Stack with DP**: Combining state tracking with monotonic properties
2. **Multi-dimensional Optimization**: Optimizing both width and height calculations
3. **Area/Volume Calculations**: Using stack to efficiently compute 2D areas
4. **Boundary Detection**: Finding left and right boundaries efficiently

## Problems in This Section

### 1. Largest Rectangle in Histogram (LC 84)
**Concept**: Monotonic stack for 2D area optimization

**Problem**: Given array of bar heights, find largest rectangle area that can be formed.

**Key Ideas**:
- For each bar, need to know how far left and right it can extend
- A bar can extend while heights are greater than or equal to it
- Monotonic increasing stack to find boundaries efficiently
- Area = height[i] × (right_boundary - left_boundary - 1)
- Stack stores indices for width calculation

**Brute Force**: O(n²) - for each bar, scan left and right
**Optimized**: O(n) - each element pushed and popped once

**Algorithm**:
1. Use monotonic increasing stack (stores indices)
2. When current height < stack top, we found right boundary
3. Pop and calculate area using popped element's height
4. Left boundary is the element below in stack (or -1)
5. Width = current_index - left_boundary - 1
6. Process remaining stack elements at the end

**Pattern**: Monotonic stack with boundary detection

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Example Walkthrough**:
```
heights = [2, 1, 5, 6, 2, 3]

Index:     0  1  2  3  4  5
Heights:  [2, 1, 5, 6, 2, 3]

Step-by-step:
i=0: heights[0]=2, stack=[] → push 0 → stack=[0]
i=1: heights[1]=1 < heights[0]=2
     Pop 0: area = 2 × (1-(-1)-1) = 2 × 1 = 2
     Push 1 → stack=[1]

i=2: heights[2]=5 > heights[1]=1 → push 2 → stack=[1,2]
i=3: heights[3]=6 > heights[2]=5 → push 3 → stack=[1,2,3]

i=4: heights[4]=2 < heights[3]=6
     Pop 3: area = 6 × (4-2-1) = 6 × 1 = 6
     heights[4]=2 < heights[2]=5
     Pop 2: area = 5 × (4-1-1) = 5 × 2 = 10 ← Maximum!
     Push 4 → stack=[1,4]

i=5: heights[5]=3 > heights[4]=2 → push 5 → stack=[1,4,5]

Process remaining stack:
Pop 5: area = 3 × (6-4-1) = 3 × 1 = 3
Pop 4: area = 2 × (6-1-1) = 2 × 4 = 8
Pop 1: area = 1 × (6-(-1)-1) = 1 × 6 = 6

Maximum area = 10
```

**Why This Works**:
- **Monotonic property**: Stack maintains increasing heights
- **Right boundary**: When we pop, current index is the right limit
- **Left boundary**: Element below in stack is the left limit
- **Each bar processed once**: Push once, pop once = O(n)

**Common Implementation Pattern**:
```python
def largestRectangleArea(heights):
    stack = []
    max_area = 0

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height_idx = stack.pop()
            height = heights[height_idx]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    # Process remaining elements
    while stack:
        height_idx = stack.pop()
        height = heights[height_idx]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, height * width)

    return max_area
```

**Alternative Approach - Sentinel Values**:
Add 0 at the end to force processing all elements:
```python
def largestRectangleArea(heights):
    stack = [-1]  # Sentinel for left boundary
    heights.append(0)  # Sentinel to flush stack
    max_area = 0

    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
```

## Advanced Insights

### Why Monotonic Increasing Stack?

1. **Efficiency**: Each element touched exactly twice (push and pop)
2. **Boundary detection**: Stack top always provides left boundary
3. **Automatic processing**: Smaller element triggers calculation
4. **Implicit state**: Stack stores all information needed

### Width Calculation Trick

```
Left boundary = stack[-1] (or -1 if stack empty)
Right boundary = current index
Width = right - left - 1

Why -1? Because boundaries are exclusive:
    [X, X, X, bar, X, X]
     left      i    right
Width doesn't include the boundary bars
```

### Related Hard Problems

This technique extends to:
- **Maximal Rectangle (LC 85)**: Apply histogram technique to each row
- **Trapping Rain Water 2D (LC 407)**: Similar boundary concept
- **Maximum Score of a Good Subarray (LC 1793)**: Variant with conditions

## Learning Path

1. **Master Daily Temperatures**: Understand basic monotonic stack
2. **Study the algorithm**: Understand why monotonic increasing
3. **Practice width calculation**: This is the tricky part
4. **Trace through examples**: Draw the stack state
5. **Try variants**: Maximal Rectangle, Trapping Rain Water

## Common Mistakes to Avoid

1. **Wrong width calculation**: Forgetting the -1 in (right - left - 1)
2. **Not handling remaining stack**: Missing potential maximum at the end
3. **Using decreasing stack**: Should be increasing for this problem
4. **Integer overflow**: In some languages, need to use long
5. **Off-by-one errors**: Careful with boundary indices

## Debugging Techniques

1. **Print stack state**: At each iteration, print stack contents
2. **Trace small example**: Use [2,1,5,6,2,3] to verify logic
3. **Check boundary cases**:
   - All increasing: [1,2,3,4,5]
   - All decreasing: [5,4,3,2,1]
   - All same: [3,3,3,3,3]
   - Single element: [5]
   - Empty: []

## Optimization Variations

### Space Optimization
Can solve with O(1) extra space using divide and conquer, but O(n log n) time:
- Find minimum height
- Max area = max(min_height × length, left_half, right_half)
- Recursively solve left and right of minimum

### Time Optimization
Stack approach is already optimal O(n), but can optimize constants:
- Use array instead of stack (slightly faster)
- Avoid redundant calculations
- Early termination in some cases

## Interview Tips

1. **Explain the pattern first**: "This uses a monotonic stack"
2. **Start with brute force**: Show you understand O(n²) solution
3. **Explain the optimization**: Why stack reduces complexity
4. **Handle edge cases**: Empty array, single element, all same
5. **Trace through example**: Show your understanding
6. **Discuss related problems**: Maximal Rectangle, Rain Water

## Practice Strategy

1. Implement brute force O(n²) solution first
2. Understand why it's slow (redundant boundary checks)
3. Learn the monotonic stack pattern
4. Implement O(n) solution
5. Test with various inputs
6. Explain the solution to someone else
7. Solve related problems to reinforce the pattern

## Extension Problems

Once you master this problem:
- **Maximal Rectangle (LC 85)**: 2D version using this algorithm
- **Trapping Rain Water (LC 42)**: Similar monotonic stack concept
- **Sum of Subarray Minimums (LC 907)**: Monotonic stack with DP
- **Maximum Score from Good Subarray (LC 1793)**: Histogram variant

## Key Takeaways

- Monotonic stack can reduce O(n²) to O(n) for boundary problems
- Store indices, not values, for width calculations
- Each element is pushed and popped exactly once
- Sentinel values can simplify code
- This pattern appears in many hard problems
- Understanding width calculation is crucial: (right - left - 1)
