# 2D Dynamic Programming - Medium

This folder contains medium-level 2D Dynamic Programming problems. These problems require building and manipulating 2D state spaces.

## Problems

### 1. Unique Paths (LeetCode 62)
**File:** `unique_paths.py`

**Description:** Find the number of unique paths from top-left to bottom-right in an m×n grid, moving only right or down.

**Key Concepts:**
- 2D DP table: dp[i][j] = number of ways to reach cell (i,j)
- dp[i][j] = dp[i-1][j] + dp[i][j-1]
- Base case: first row and column all have 1 path
- Space optimization: can use 1D array

**Time:** O(m × n) | **Space:** O(m × n) or O(n) optimized

**Pattern:** Grid path counting

---

### 2. Longest Common Subsequence (LeetCode 1143)
**File:** `longest_common_subsequence.py`

**Description:** Find the length of the longest subsequence common to two strings.

**Key Concepts:**
- dp[i][j] = LCS of text1[0:i] and text2[0:j]
- If chars match: dp[i][j] = dp[i-1][j-1] + 1
- If not: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
- Classic 2D string DP

**Time:** O(m × n) | **Space:** O(m × n)

**Pattern:** String comparison DP

---

### 3. Best Time to Buy and Sell Stock with Cooldown (LeetCode 309)
**File:** `stock_cooldown.py`

**Description:** Maximize profit from stock trading with cooldown (must wait 1 day after selling before buying again).

**Key Concepts:**
- State machine: held, sold, cooldown
- Track max profit in each state
- Transitions between states
- Similar to House Robber with states

**Time:** O(n) | **Space:** O(1) with state variables

**Pattern:** State machine DP

---

### 4. Coin Change II (LeetCode 518)
**File:** `coin_change_ii.py`

**Description:** Count the number of combinations that make up a given amount using unlimited coins.

**Key Concepts:**
- Unbounded knapsack counting
- dp[i] = number of ways to make amount i
- Order matters: iterate coins in outer loop to avoid duplicates
- Different from Coin Change (min coins)

**Time:** O(amount × coins) | **Space:** O(amount)

**Pattern:** Unbounded knapsack, counting combinations

---

### 5. Target Sum (LeetCode 494)
**File:** `target_sum.py`

**Description:** Assign + or - to each number to reach a target sum. Count number of ways.

**Key Concepts:**
- Convert to subset sum problem
- (sum + target) / 2 = subset sum to find
- dp[i] = ways to achieve sum i
- Similar to Partition Equal Subset Sum

**Time:** O(n × sum) | **Space:** O(sum)

**Pattern:** Subset sum with twist

---

### 6. Interleaving String (LeetCode 97)
**File:** `interleaving_string.py`

**Description:** Determine if s3 is formed by interleaving s1 and s2 while maintaining relative order.

**Key Concepts:**
- dp[i][j] = can s3[0:i+j] be formed from s1[0:i] and s2[0:j]
- Check if current char of s3 matches s1[i-1] or s2[j-1]
- 2D table representing both string positions
- Can optimize to 1D

**Time:** O(m × n) | **Space:** O(m × n)

**Pattern:** String interleaving DP

---

### 7. Longest Increasing Path in a Matrix (LeetCode 329)
**File:** `longest_increasing_path_matrix.py`

**Description:** Find the length of the longest increasing path in a matrix (can move in 4 directions).

**Key Concepts:**
- DFS + memoization (2D DP)
- Cache results for each cell
- No need for visited array (strictly increasing prevents cycles)
- Try all 4 directions from each cell

**Time:** O(m × n) | **Space:** O(m × n)

**Pattern:** Matrix DFS with memoization

---

## Learning Path

### Level 1: Grid-Based DP
1. **Unique Paths** - Simplest 2D DP, understand the grid traversal pattern

### Level 2: String Matching
2. **Longest Common Subsequence** - Classic 2D string DP
3. **Interleaving String** - More complex string relationship

### Level 3: State Management
4. **Stock with Cooldown** - Understanding state transitions
5. **Target Sum** - Converting problem to standard DP pattern

### Level 4: Advanced Techniques
6. **Coin Change II** - Combination counting with proper ordering
7. **Longest Increasing Path Matrix** - DFS + memoization on 2D grid

## Common Patterns

### 1. Grid Traversal
**Problem:** Unique Paths
```python
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```
- Build table row by row or column by column
- Base cases: edges of grid

### 2. String Comparison
**Problems:** LCS, Interleaving String
```python
# When characters match
dp[i][j] = dp[i-1][j-1] + value
# When they don't
dp[i][j] = max/or(dp[i-1][j], dp[i][j-1])
```

### 3. Knapsack with Combinations
**Problems:** Coin Change II, Target Sum
```python
for coin in coins:  # Outer loop for combinations
    for amount in range(coin, target + 1):
        dp[amount] += dp[amount - coin]
```

### 4. State Machine
**Problem:** Stock Cooldown
```python
# Define states and transitions
held = max(held, cooldown - price)
sold = held + price
cooldown = max(cooldown, sold)
```

### 5. DFS + Memoization
**Problem:** Longest Increasing Path
```python
def dfs(i, j):
    if memo[i][j]:
        return memo[i][j]
    # Try all directions
    result = 1 + max(dfs(ni, nj) for all valid neighbors)
    memo[i][j] = result
    return result
```

## Space Optimization Techniques

Many 2D DP problems can be optimized:

1. **1D Array**: When current row only depends on previous row
   - Unique Paths: O(m×n) → O(n)
   - LCS: O(m×n) → O(min(m,n))

2. **State Variables**: When tracking fixed number of states
   - Stock Cooldown: O(n) → O(1)

3. **In-place DP**: When input can be modified
   - Some matrix problems can reuse input array

## Tips for Success

1. **Draw the DP table** - Visualize dependencies between cells
2. **Identify dimensions** - What do rows and columns represent?
3. **Define state clearly** - What does dp[i][j] mean?
4. **Initialize base cases** - Often first row/column
5. **Check dependencies** - Make sure you compute in right order
6. **Consider space optimization** - After solving with 2D table

## Time Complexity Patterns

- **O(m × n)**: Most grid/string problems with nested loops
- **O(n × sum)**: Knapsack variants where sum is the target
- **O(m × n) with DFS**: Matrix problems with memoization

## Common Mistakes to Avoid

1. **Off-by-one errors** - Be careful with indices (0-indexed vs 1-indexed)
2. **Wrong initialization** - Base cases must be correct
3. **Order of iteration** - In knapsack problems, order matters for combinations vs permutations
4. **Integer overflow** - In counting problems, might need modulo
5. **Space confusion** - Understand what you're optimizing to 1D

## Companies

Frequently asked by: Amazon, Google, Microsoft, Facebook, Apple, Bloomberg, Adobe, Uber, Airbnb, Netflix

## Next Steps

After mastering these, advance to:
- **Hard 2D DP Problems** - More complex state transitions
- **3D DP Problems** - Additional dimensions for more complex states
- **DP Optimization Techniques** - Monotonic queue, divide and conquer DP
