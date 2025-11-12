# 2D Dynamic Programming - Hard

This folder contains hard-level 2D Dynamic Programming problems. These problems require advanced DP techniques, complex state transitions, and deep problem-solving skills.

## Problems

### 1. Distinct Subsequences (LeetCode 115)
**File:** `distinct_subsequences.py`

**Description:** Given strings s and t, count the number of distinct subsequences of s that equal t.

**Key Concepts:**
- dp[i][j] = number of ways to form t[0:j] from s[0:i]
- If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
  - Either use current char or skip it
- If not equal: dp[i][j] = dp[i-1][j]
- Similar to LCS but counting ways instead of length
- Handle large numbers (might need modulo)

**Time:** O(m × n) | **Space:** O(m × n) or O(n) optimized

**Pattern:** Subsequence counting with 2D DP

**Why Hard:**
- Subtle state transitions (use char vs skip)
- Easy to confuse with other string DP problems
- Requires careful base case initialization

---

### 2. Edit Distance (LeetCode 72)
**File:** `edit_distance.py`

**Description:** Find minimum operations (insert, delete, replace) to convert word1 to word2.

**Key Concepts:**
- dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
- If chars match: dp[i][j] = dp[i-1][j-1]
- If not: dp[i][j] = 1 + min(insert, delete, replace)
  - Insert: dp[i][j-1]
  - Delete: dp[i-1][j]
  - Replace: dp[i-1][j-1]
- Classic algorithm (Levenshtein distance)

**Time:** O(m × n) | **Space:** O(m × n) or O(n) optimized

**Pattern:** String transformation DP

**Why Hard:**
- Three different operations to consider
- Understanding which operation corresponds to which state
- Conceptually challenging to visualize

---

### 3. Burst Balloons (LeetCode 312)
**File:** `burst_balloons.py`

**Description:** Given n balloons with coins, maximize coins gained by bursting them. Bursting balloon i gives coins[i-1] × coins[i] × coins[i+1] coins.

**Key Concepts:**
- **Key insight:** Think about which balloon to burst LAST, not first
- dp[i][j] = max coins from bursting all balloons in range (i, j)
- For each k in (i, j), assume k is burst last
- dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]×nums[k]×nums[j])
- Add boundary balloons with value 1
- Requires reverse thinking

**Time:** O(n³) | **Space:** O(n²)

**Pattern:** Interval DP with reverse thinking

**Why Hard:**
- Non-intuitive: must think about last balloon, not first
- Order-dependent operations
- Requires adding boundaries
- Three nested loops

---

### 4. Regular Expression Matching (LeetCode 10)
**File:** `regular_expression_matching.py`

**Description:** Implement regex matching with '.' (any char) and '*' (zero or more of previous char).

**Key Concepts:**
- dp[i][j] = does s[0:i] match p[0:j]
- If p[j-1] == s[i-1] or p[j-1] == '.': dp[i][j] = dp[i-1][j-1]
- If p[j-1] == '*':
  - '*' represents zero: dp[i][j] = dp[i][j-2]
  - '*' represents one+: dp[i][j] = dp[i-1][j] (if prev char matches)
- Complex base cases and edge cases
- Recursive solution also possible with memoization

**Time:** O(m × n) | **Space:** O(m × n)

**Pattern:** Pattern matching DP with wildcards

**Why Hard:**
- '*' has two meanings (zero or more)
- Interaction between current char and '*'
- Many edge cases to handle
- Understanding what each state transition means

---

## Problem Comparison

| Problem | Core Challenge | Key Insight |
|---------|---------------|-------------|
| Distinct Subsequences | Count ways instead of length | Track both "use" and "skip" transitions |
| Edit Distance | Three operations | Each operation maps to a DP cell |
| Burst Balloons | Order-dependent operations | Think last balloon, not first |
| Regular Expression | Wildcard handling | '*' affects previous character |

## Learning Path

### Recommended Order:

1. **Edit Distance** (Start here)
   - Most straightforward of the hard problems
   - Clear state transitions
   - Builds on LCS knowledge

2. **Distinct Subsequences**
   - Similar to LCS but with counting
   - Helps understand multiple transition paths

3. **Regular Expression Matching**
   - More complex pattern matching
   - Multiple cases to handle

4. **Burst Balloons** (Most challenging)
   - Requires paradigm shift in thinking
   - Non-obvious approach

## Advanced Patterns

### 1. String Transformation
**Problems:** Edit Distance, Regular Expression Matching
```python
# Multiple operations to consider
if condition:
    dp[i][j] = dp[i-1][j-1]  # Match/Replace
else:
    dp[i][j] = min(
        dp[i-1][j] + 1,    # Delete
        dp[i][j-1] + 1,    # Insert
        dp[i-1][j-1] + 1   # Replace
    )
```

### 2. Subsequence Counting
**Problem:** Distinct Subsequences
```python
# Count both using and skipping current element
dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
```

### 3. Interval DP
**Problem:** Burst Balloons
```python
# Try each element as last operation in range
for k in range(i+1, j):
    dp[i][j] = max(dp[i][j],
        dp[i][k] + dp[k][j] + operation(i, k, j))
```

### 4. Pattern Matching with Wildcards
**Problem:** Regular Expression Matching
```python
# Handle special characters with multiple meanings
if pattern[j-1] == '*':
    # Zero occurrences OR one+ occurrences
    dp[i][j] = dp[i][j-2] or (match and dp[i-1][j])
```

## Space Optimization

Most of these problems can be optimized:

1. **1D Array Optimization**: Edit Distance, Distinct Subsequences
   - Only need previous row
   - Can reduce O(m×n) to O(n)

2. **Rolling Array**: When accessing multiple previous states
   - Keep 2 rows instead of full table

3. **In-place**: Some problems allow modifying input

## Common Techniques

### 1. Base Case Initialization
Critical in hard problems - spend time getting these right:
```python
# Edit Distance
dp[0][j] = j  # Insert j characters
dp[i][0] = i  # Delete i characters

# Regular Expression
dp[0][0] = True  # Empty matches empty
# Handle patterns like a*b*c* matching empty
```

### 2. State Definition
Be precise about what each state represents:
- **Edit Distance**: dp[i][j] = min ops for word1[0:i] → word2[0:j]
- **Burst Balloons**: dp[i][j] = max coins from range (i, j) exclusive
- **Distinct Subsequences**: dp[i][j] = count of t[0:j] in s[0:i]

### 3. Boundary Handling
Some problems require adding boundaries:
- **Burst Balloons**: Add 1s at both ends
- Simplifies edge cases and calculations

## Debugging Tips

1. **Test small examples** - Work through by hand first
2. **Print the DP table** - Visualize what's being computed
3. **Check base cases** - Often the source of bugs
4. **Verify state transitions** - Make sure each case is correct
5. **Test edge cases** - Empty strings, single elements

## Time Complexity Analysis

- **O(m × n)**: Edit Distance, Distinct Subsequences, Regular Expression
  - Two nested loops over string lengths

- **O(n³)**: Burst Balloons
  - Three nested loops for interval DP
  - Still polynomial time

## Common Mistakes

1. **Index confusion** - 0-indexed arrays vs 1-indexed DP table
2. **Wrong base cases** - Causes cascading errors
3. **Missing edge cases** - Empty strings, single characters
4. **State transition errors** - Not considering all cases
5. **Integer overflow** - Use modulo in counting problems

## Interview Tips

1. **Clarify problem** - Understand all constraints and operations
2. **Start with brute force** - Identify overlapping subproblems
3. **Define state clearly** - What does dp[i][j] mean?
4. **Work through example** - Fill small DP table by hand
5. **Optimize after solving** - Get correct solution first
6. **Discuss tradeoffs** - Time vs space optimization

## Real-World Applications

- **Edit Distance**: Spell checkers, DNA sequence alignment, version control
- **Regular Expression**: Text search, input validation, parsers
- **Burst Balloons**: Resource optimization, game AI
- **Distinct Subsequences**: Bioinformatics, pattern recognition

## Companies

These problems are frequently asked by top tech companies:
- **FAANG**: Amazon, Google, Microsoft, Facebook, Apple
- **Others**: Bloomberg, Adobe, Uber, Airbnb, Netflix, LinkedIn

## Prerequisites

Before attempting these problems, make sure you're comfortable with:
- 1D Dynamic Programming patterns
- Medium 2D DP problems (LCS, Unique Paths, etc.)
- String manipulation
- Recursion and memoization

## Next Steps

After mastering these:
1. **Study variations** - Wildcard matching, different edit operations
2. **Optimize further** - Practice space optimization
3. **Learn advanced DP** - Bitmask DP, tree DP, digit DP
4. **System design** - How to scale these algorithms
