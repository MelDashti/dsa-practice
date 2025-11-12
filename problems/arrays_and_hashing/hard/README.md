# Arrays & Hashing - Hard

## Concept/Pattern

Hard-level arrays and hashing problems demand sophisticated algorithmic thinking that combines hashing with other techniques like union-find, dynamic programming, or mathematical insights. The Longest Consecutive Sequence problem exemplifies this: while it uses a hash set, the real challenge is recognizing how to avoid unnecessary work by only starting sequences from their true beginning. These problems test your ability to see beyond the obvious hash table application to find the optimal algorithm.

## Key Insights

The critical insight at this level is that **hashing enables O(1) queries, but algorithm design determines overall complexity**. You must combine efficient lookups with smart traversal strategies. For consecutive sequences, the breakthrough is recognizing that checking if `num-1` exists prevents redundant work—you only start counting from actual sequence starts. Hard problems often require you to maintain state, track boundaries, or use the hash table in unexpected ways. The hash table is a tool, not the solution itself.

## When to Use This Approach

Hard hashing problems appear when:
- **Sequence detection**: Finding longest consecutive, increasing, or pattern-matching sequences
- **Range queries**: Determining if numbers form continuous ranges
- **Set-based optimization**: Where membership testing is critical but not sufficient alone
- **Constraint satisfaction**: Complex rules requiring fast validation
- **Graph-like relationships**: Where elements connect based on properties
- **Avoiding nested iterations**: Where brute force is O(n²) or worse

These problems often have multiple valid approaches, but hashing provides the optimal time complexity.

## Common Pitfalls

1. **Missing the optimization**: Using hash set but still having O(n²) algorithm from poor logic
2. **Redundant checking**: Not filtering out non-starting points in sequence problems
3. **Overcomplicating**: Trying to sort or use complex data structures when simple set operations suffice
4. **Edge case blindness**: Empty arrays, single elements, all consecutive, or large gaps
5. **Integer assumptions**: Not handling negative numbers, duplicates, or non-consecutive ranges
6. **Memory limits**: Not considering if O(n) space is acceptable for the problem constraints
7. **Premature optimization**: Trying to be too clever before getting a working solution

## Tips for Solving Problems

- **Start with brute force**: Understand the O(n²) or O(n³) solution first, then optimize
- **Identify redundant work**: What are you checking repeatedly? Can a hash set eliminate it?
- **Look for sequence patterns**: If problem mentions "consecutive" or "longest," think about starting points
- **Use sets for membership**: When you only need "is this present?" not "how many?"
- **Analyze each iteration**: Is every loop iteration necessary? Can you skip some?
- **Think about boundaries**: In sequences, you often only need to process endpoints
- **Combine techniques**: Hard problems rarely use just one pattern—maybe hash + greedy, or hash + DP
- **Test thoroughly**: Hard problems have tricky edge cases; test empty, single, all-same, reversed, and large inputs
- **Prove correctness**: Convince yourself why your approach works for all cases, not just examples
