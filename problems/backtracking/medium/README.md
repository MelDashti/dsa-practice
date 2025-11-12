# Backtracking - Medium Problems

## Overview

This directory contains medium-level backtracking problems. These problems introduce core backtracking concepts including state exploration, pruning, and systematic search through solution spaces.

## What is Backtracking?

Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally. When the algorithm determines that a partial solution cannot possibly lead to a valid complete solution, it abandons (backtracks from) that path and tries another.

### Key Characteristics:
- **Recursive exploration**: Systematically explores all possible candidates
- **State management**: Maintains current state and modifies it during exploration
- **Pruning**: Eliminates invalid paths early to improve efficiency
- **Backtracking**: Undoes choices when they lead to invalid solutions

## Core Patterns

### 1. Subsets Pattern
Used when you need to generate all possible combinations of elements.

```python
def backtrack(start, path):
    result.append(path[:])  # Add current subset

    for i in range(start, len(nums)):
        path.append(nums[i])  # Choose
        backtrack(i + 1, path)  # Explore
        path.pop()  # Unchoose (backtrack)
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n) for recursion depth

### 2. Combination Pattern
Similar to subsets but with target sum or specific conditions.

```python
def backtrack(start, target, path):
    if target == 0:
        result.append(path[:])
        return
    if target < 0:
        return  # Prune invalid paths

    for i in range(start, len(candidates)):
        path.append(candidates[i])
        backtrack(i, target - candidates[i], path)  # i for reuse, i+1 for no reuse
        path.pop()
```

### 3. Permutation Pattern
Generates all possible orderings of elements.

```python
def backtrack(path, used):
    if len(path) == len(nums):
        result.append(path[:])
        return

    for i in range(len(nums)):
        if used[i]:
            continue  # Skip already used elements

        used[i] = True
        path.append(nums[i])
        backtrack(path, used)
        path.pop()
        used[i] = False
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n)

### 4. Grid Exploration Pattern
Used for word search and path-finding problems.

```python
def backtrack(row, col, index):
    if index == len(word):
        return True

    if (row < 0 or row >= rows or col < 0 or col >= cols or
        board[row][col] != word[index] or visited[row][col]):
        return False

    visited[row][col] = True  # Mark as visited

    # Explore all 4 directions
    found = (backtrack(row+1, col, index+1) or
             backtrack(row-1, col, index+1) or
             backtrack(row, col+1, index+1) or
             backtrack(row, col-1, index+1))

    visited[row][col] = False  # Backtrack
    return found
```

## Problems in This Directory

### 1. Subsets (78)
**Concept**: Generate all possible subsets of a set
**Pattern**: Subsets pattern
**Key Insight**: Each element has 2 choices - include or exclude
**Variations**: Can be solved iteratively or recursively

### 2. Combination Sum (39)
**Concept**: Find all unique combinations that sum to target
**Pattern**: Combination pattern with element reuse
**Key Insight**: Start index allows element reuse; pruning on negative target
**Edge Cases**: Empty candidates, no valid combinations

### 3. Permutations (46)
**Concept**: Generate all possible orderings
**Pattern**: Permutation pattern
**Key Insight**: Track used elements with boolean array or set
**Variations**: Can use swapping technique to avoid extra space

### 4. Subsets II (90)
**Concept**: Generate subsets with duplicate elements
**Pattern**: Subsets pattern with duplicate handling
**Key Insight**: Sort first, skip duplicates at same level
**Important**: Only skip duplicates at same recursive level, not different levels

### 5. Combination Sum II (40)
**Concept**: Find combinations with each element used once
**Pattern**: Combination pattern without reuse
**Key Insight**: Sort and skip duplicates; increment start index
**Difference from I**: No element reuse, must handle duplicates

### 6. Word Search (79)
**Concept**: Find if word exists in 2D grid
**Pattern**: Grid exploration with backtracking
**Key Insight**: Mark cells as visited, backtrack to unmark
**Optimization**: Can modify board instead of using visited array

### 7. Palindrome Partitioning (131)
**Concept**: Partition string into palindrome substrings
**Pattern**: String partitioning with validation
**Key Insight**: Check palindrome before recursing; partition at each position
**Optimization**: Can precompute palindrome checks with DP

### 8. Letter Combinations of a Phone Number (17)
**Concept**: Generate all letter combinations from digit string
**Pattern**: Multi-choice backtracking
**Key Insight**: Each digit maps to multiple letters
**Implementation**: Can use iterative approach with queue

## Common Pitfalls

1. **Forgetting to backtrack**: Always undo state changes
2. **Wrong base case**: Ensure termination conditions are correct
3. **Modifying vs. Copying**: Be careful when adding paths to results (use `path[:]` or `path.copy()`)
4. **Duplicate handling**: Sort first and skip duplicates correctly
5. **Index management**: Be careful with start indices in loops

## Optimization Techniques

1. **Early Pruning**: Eliminate invalid paths as early as possible
2. **Sorting**: Can help with pruning and duplicate handling
3. **Memoization**: Cache results for overlapping subproblems
4. **Iterative Solutions**: Some problems can be solved iteratively (e.g., subsets)
5. **In-place Modification**: Modify input instead of using extra visited array

## Practice Strategy

1. **Start with Subsets**: Understand the basic pattern
2. **Move to Combinations**: Learn about pruning and conditions
3. **Practice Permutations**: Master state management with used elements
4. **Tackle Grid Problems**: Combine backtracking with graph traversal
5. **Study Duplicates**: Learn proper duplicate handling techniques

## Time Complexity Summary

| Problem | Time Complexity | Space Complexity | Reason |
|---------|----------------|------------------|---------|
| Subsets | O(2^n) | O(n) | 2 choices per element |
| Combination Sum | O(2^n) | O(target/min) | Exponential branches |
| Permutations | O(n!) | O(n) | n! permutations |
| Word Search | O(m*n*4^L) | O(L) | 4 directions, L = word length |
| Palindrome Partition | O(2^n) | O(n) | Partition at each position |

## Additional Resources

- **Backtracking Template**: Study the three-step pattern (choose, explore, unchoose)
- **Decision Trees**: Draw decision trees to visualize the search space
- **State Space Trees**: Understand how backtracking explores the solution space
- **Pruning Strategies**: Learn when and how to prune invalid branches

## Next Steps

After mastering these problems, you should:
1. Move on to Hard backtracking problems (N-Queens, etc.)
2. Study constraint satisfaction problems
3. Learn about branch and bound techniques
4. Explore dynamic programming as an optimization for overlapping subproblems
