# Sliding Window - Hard

## Concept/Pattern

Hard sliding window problems demand sophisticated state management and often combine sliding window with advanced data structures like deques, heaps, or monotonic stacks. Minimum Window Substring requires tracking two different frequency maps and determining smallest valid window. Sliding Window Maximum needs maintaining maximums efficiently as window slides, using a monotonic deque. These problems test your ability to maintain complex invariants across window movements and choose optimal data structures for O(n) or O(n log n) solutions instead of O(n²).

## Key Insights

The breakthrough insight is that **efficient window state updates require choosing the right data structure for the specific query you're answering**. For minimum window containing all characters, you need two hash maps (target frequencies and current window frequencies) and a "formed" counter tracking how many unique characters meet their requirement. For sliding window maximum, a deque maintaining decreasing order lets you access maximum in O(1) while discarding irrelevant smaller elements. Understanding what makes an element "irrelevant" or "expired" and removing it efficiently is crucial.

## When to Use This Approach

Hard sliding window problems involve:
- **Complex validity conditions**: Multiple constraints that must all be satisfied
- **Range queries with updates**: Finding min/max/median in sliding windows
- **Optimization across constraints**: Smallest window containing all required elements
- **Monotonic structures**: Maintaining increasing/decreasing order within window
- **Multiple tracking requirements**: Frequency matching plus size minimization
- **Efficient maximum/minimum**: Needing O(1) or O(log n) access to extremes
- **Substring matching with flexibility**: Permutations, character inclusion, pattern matching

These problems often appear in interviews for senior positions and require deep data structure knowledge.

## Common Pitfalls

1. **Wrong data structure choice**: Using simple hash map when you need deque/heap for efficiency
2. **State management complexity**: Not clearly tracking all necessary invariants
3. **Deque manipulation errors**: Not properly maintaining monotonic property or removing expired elements
4. **Window validity logic**: Complex conditions with && and || that are hard to get right
5. **Update ordering**: Adding/removing from structures in wrong sequence breaks invariants
6. **Index vs value tracking**: Storing wrong information in deque (indices vs values)
7. **Formed/matched counting**: Incorrectly tracking when frequency requirements are met
8. **Early optimization**: Trying to optimize before getting correct solution
9. **Edge cases**: Empty input, window size larger than array, no valid window exists
10. **Space complexity**: Using more space than necessary with redundant structures

## Tips for Solving Problems

- **Break down requirements**: List all conditions that must be true for valid window
- **Choose structure carefully**:
  - Hash map for frequencies
  - Deque for maintaining max/min in window
  - Heap for kth largest/smallest
  - Set for uniqueness checks
- **Maintain invariants**: Write out what must be true after each operation
- **Use helper functions**: Validate window, update structures, check completeness
- **Start with working solution**: Get O(n²) working, then optimize to O(n) or O(n log n)
- **Understand monotonic deque**: Front has maximum, remove smaller elements from back, remove expired from front
- **Track both frequency and completeness**: Often need to know "how many chars satisfied" not just counts
- **Test thoroughly**: Test minimum cases, maximum cases, no solution, entire array is answer
- **Trace data structures**: Draw out deque/heap/map state at each step for small example
- **Optimize incrementally**: First correctness, then time complexity, then space
- **Learn patterns**: Study classic problems (Min Window, Sliding Max) deeply—they're templates
- **Handle duplicates carefully**: In frequency matching, duplicates in target vs window behave differently
- **Consider two-pass**: Sometimes preprocessing helps; don't assume single pass is always best
