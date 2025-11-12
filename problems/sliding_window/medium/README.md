# Sliding Window - Medium

## Concept/Pattern

Medium sliding window problems introduce variable-size windows that expand and contract based on conditions, and often require additional data structures like hash maps or sets to track window contents. Unlike easy problems with implicit or fixed windows, here you actively manage both left and right pointers to maintain valid windows. Problems involve finding longest valid substrings, checking for permutations, or optimizing under constraints. The window "slides" by expanding right to explore possibilities and contracting left to maintain validity.

## Key Insights

The key insight is the **expand-contract paradigm**: expand the window by moving right to include new elements, then contract from the left to restore validity when constraints are violated. For "longest substring without repeating characters," you expand right to add characters and contract left when you hit a duplicate. For "permutation in string," you expand to size k, check if it matches, then slide by removing leftmost and adding next. Understanding when to expand (always or conditionally?) and when to contract (restore validity?) is crucial. Hash maps track frequencies or positions, enabling O(1) validity checks.

## When to Use This Approach

Medium sliding window problems involve:
- **Variable-length windows**: Finding longest/shortest subarray meeting criteria
- **Frequency constraints**: Matching character counts, k distinct elements
- **Permutation/anagram checks**: Substring contains all characters of another
- **Character replacement**: Longest substring with at most k replacements
- **Distinct elements**: Subarrays with exactly or at most k distinct values
- **Optimization with constraints**: Maximize/minimize while maintaining validity
- **Pattern matching**: Finding substrings matching patterns or rules

If you see "longest substring," "at most k," "contains all," or "valid subarray," think variable sliding window.

## Common Pitfalls

1. **Not using hash maps**: Trying to track frequencies or validity without proper data structures
2. **Expanding without contracting**: Growing window but not shrinking when invalid
3. **Contracting too much**: Shrinking beyond what's necessary to restore validity
4. **Wrong validity check**: Not correctly determining when window is valid/invalid
5. **Update order**: Updating window state before/after moving pointers in wrong order
6. **Missing while loops**: Needing `while invalid: contract` but using `if` instead
7. **Character set assumptions**: Assuming only lowercase letters when input can be broader
8. **Maximum tracking**: Forgetting to update max length or best solution found
9. **Initial state**: Not properly initializing hash map or window state
10. **Early termination**: Stopping when you should continue exploring

## Tips for Solving Problems

- **Use the template**: Start with expand-contract structure and customize
- **Define validity clearly**: Write out exactly what makes a window valid/invalid
- **Choose right structure**: Hash map for frequencies, set for uniqueness, deque for max/min tracking
- **Track window state**: What information about current window do you need?
- **Update in correct order**: Typically expand right, check validity, contract left, update result
- **Use while for contracting**: You might need multiple left movements to restore validity
- **Handle edge cases**: Empty string, single character, entire string is answer
- **Optimize hash operations**: Use `collections.defaultdict` or `Counter`
- **Test incrementally**: Verify expansion logic works, then contraction, then together
- **Trace through examples**: Step through with small inputs watching window and state change
- **Compare window sizes**: Often need right - left + 1 for current window length
- **Consider all valid windows**: Don't stop at first valid window; keep sliding for optimal
