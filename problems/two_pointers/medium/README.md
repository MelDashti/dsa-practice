# Two Pointers - Medium

## Concept/Pattern

Medium two pointer problems extend the basic pattern to more complex scenarios: finding triplets instead of pairs, maximizing area between boundaries, or solving on sorted arrays with constraints. These problems require strategic pointer movement based on multiple conditions and often involve nested loops where two pointers optimize the inner loop. You'll make decisions about which pointer to move based on comparisons, sums, or geometric properties, turning O(n³) brute force into O(n²) or better solutions.

## Key Insights

The breakthrough at this level is understanding that **pointer movement should be guided by problem-specific logic that eliminates impossible solutions**. In 3Sum, after fixing one number, you use two pointers to find pairs that complete the triplet—moving based on whether the sum is too large or small. In Container With Most Water, you move the pointer at the shorter height because moving the taller one can only decrease area. The pattern requires analyzing why certain combinations can't produce better results, allowing you to skip them confidently.

## When to Use This Approach

Medium two pointer problems involve:
- **Multiple element combinations**: Finding triplets, quadruplets, or k-sums
- **Optimization problems**: Maximizing or minimizing some quantity (area, volume, sum)
- **Sorted array exploitation**: Using order to prune search space
- **Fixing and searching**: Fix one element, use pointers to find complementary elements
- **Geometry and bounds**: Problems with visual interpretations like water containers
- **Avoiding duplicates**: Skipping over repeated values in sorted arrays
- **Range operations**: Finding subarrays or subsequences meeting criteria

If you see "sum of three," "maximum area," or "in sorted array," think two pointers.

## Common Pitfalls

1. **Duplicate handling**: Not properly skipping duplicate elements in 3Sum-style problems
2. **Pointer movement logic**: Moving the wrong pointer or both when you should move one
3. **Sort forgetting**: Not sorting first when the problem requires it
4. **Greedy assumptions**: Moving pointers without understanding why it's optimal
5. **Integer overflow**: Large sums might overflow; use appropriate data types
6. **Time complexity miscount**: Thinking it's O(n²) when inner loop doesn't always complete
7. **Boundary conditions**: Not handling cases where pointers meet immediately or can't move
8. **Modification issues**: Trying to modify sorted array while iterating

## Tips for Solving Problems

- **Sort if needed**: Many two pointer solutions start with sorting O(n log n)
- **Fix then search**: In k-sum problems, fix k-2 elements and use pointers for the rest
- **Understand the decision**: Why do you move left vs right? Write out the reasoning
- **Skip duplicates carefully**: After finding a solution, skip all copies of that value
- **Draw the scenario**: For geometric problems, sketch what pointers represent
- **Analyze greedy choice**: Prove to yourself why moving a pointer can't miss optimal solution
- **Use while loops**: Inner pointer logic often needs while loops for skipping or searching
- **Track previous values**: Sometimes you need to remember what you just processed
- **Consider edge cases**: All same values, no solution exists, multiple solutions
- **Optimize incrementally**: Get correct solution first, then optimize pointer movement
- **Compare approaches**: Could hashing work? Is two pointers actually better here?
