# Sliding Window - Easy

## Concept/Pattern

The sliding window technique maintains a dynamic range (window) of elements in an array or string, expanding or contracting as you iterate. At the easy level, this typically involves fixed-size windows or simple conditions for window boundaries. The classic example is finding maximum profit in stock prices by maintaining the minimum price seen so far (left boundary) while checking each current price (right boundary). The pattern transforms problems that seem to require checking all subarrays into single-pass O(n) solutions by intelligently moving window boundaries.

## Key Insights

The fundamental insight is that **you don't need to recalculate everything when the window moves—you can update incrementally**. For stock prices, you only need to track the lowest price encountered so far and compare each new price against it. The window concept is implicit: your "window" is from the minimum price point to the current price. This eliminates redundant calculations that a brute force nested loop would perform. Understanding that maintaining state (like min/max/sum) as you slide is more efficient than recalculating is the key breakthrough.

## When to Use This Approach

Use sliding window for:
- **Contiguous subarray problems**: Finding max sum, min length, or optimal subarray
- **Maximum/minimum in range**: Best profit, largest value in a window
- **String problems**: Longest substring without repeating characters (medium), patterns
- **Running calculations**: Sum, average, or product over a moving range
- **Sequential optimization**: Where you process elements in order and maintain state
- **Single pass requirements**: When O(n) time is needed and you can't sort or use extra passes

If you see "subarray," "substring," "contiguous," or "window of size k," think sliding window.

## Common Pitfalls

1. **Forgetting to update state**: Not maintaining min/max/sum as the window moves
2. **Fixed vs variable window confusion**: Not recognizing whether window size changes
3. **Off-by-one errors**: Incorrect window size calculations or boundary checks
4. **Recalculating unnecessarily**: Computing window properties from scratch instead of updating
5. **Initial window setup**: Not properly initializing the first window before sliding
6. **Edge cases**: Arrays smaller than window size, all same values, single element
7. **Return value mistakes**: Returning index vs value, or forgetting to handle "no solution"
8. **Integer overflow**: With sum or product calculations on large numbers

## Tips for Solving Problems

- **Identify what to track**: What value needs to be maintained as you scan? (min, max, sum, etc.)
- **Start simple**: For fixed windows, process first k elements, then slide one at a time
- **Update incrementally**: Add new element, remove old element, update calculation
- **Use variables not arrays**: Often you only need one or two variables, not a full window storage
- **Think about boundaries**: What marks the left edge? What marks the right edge?
- **One pass mindset**: How can you solve this while only looking at each element once?
- **Simulate with examples**: Trace through a small example and watch your tracking variables change
- **Consider deque for advanced cases**: For problems needing to track window contents (not in easy typically)
- **Handle impossible cases**: What if no valid window exists?
- **Compare with brute force**: Nested loop checking all subarrays vs single pass with state
- **Test edge cases**: Empty array, array smaller than required window, all same values
