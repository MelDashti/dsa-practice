# 1D Dynamic Programming - Medium

This folder contains medium-level 1D Dynamic Programming problems. These problems require a deeper understanding of DP patterns and optimization techniques.

## Problems

### 1. House Robber (LeetCode 198)
**File:** `house_robber.py`

**Description:** Rob houses along a street to maximize money without robbing adjacent houses.

**Key Concepts:**
- Decision making: rob or skip current house
- Constraint handling: cannot rob adjacent houses
- Space-optimized DP

**Time:** O(n) | **Space:** O(1)

**Pattern:** Sequential decision with constraints

---

### 2. House Robber II (LeetCode 213)
**File:** `house_robber_ii.py`

**Description:** Same as House Robber but houses are arranged in a circle (first and last are adjacent).

**Key Concepts:**
- Breaking circular dependency
- Running House Robber twice (exclude first OR last house)
- Edge case handling

**Time:** O(n) | **Space:** O(1)

**Pattern:** Circular array DP

---

### 3. Longest Palindromic Substring (LeetCode 5)
**File:** `longest_palindromic_substring.py`

**Description:** Find the longest palindromic substring in a given string.

**Key Concepts:**
- Expand around center technique
- Handling odd and even length palindromes
- Alternative: DP table approach

**Time:** O(n²) | **Space:** O(1) for expand around center

**Pattern:** String DP, palindrome detection

---

### 4. Palindromic Substrings (LeetCode 647)
**File:** `palindromic_substrings.py`

**Description:** Count the number of palindromic substrings in a given string.

**Key Concepts:**
- Similar to Longest Palindromic Substring
- Expand around center and count
- Every single character is a palindrome

**Time:** O(n²) | **Space:** O(1)

**Pattern:** Counting with expand around center

---

### 5. Decode Ways (LeetCode 91)
**File:** `decode_ways.py`

**Description:** A message containing letters A-Z is encoded to numbers 1-26. Count the number of ways to decode a given digit string.

**Key Concepts:**
- Similar to Climbing Stairs with constraints
- Valid single digit: 1-9
- Valid two digits: 10-26
- Handle leading zeros

**Time:** O(n) | **Space:** O(1)

**Pattern:** Fibonacci-like with validation

---

### 6. Coin Change (LeetCode 322)
**File:** `coin_change.py`

**Description:** Find the fewest number of coins needed to make up a given amount.

**Key Concepts:**
- Unbounded knapsack pattern
- Building up from base case (amount 0)
- DP[i] = min number of coins for amount i

**Time:** O(amount × coins) | **Space:** O(amount)

**Pattern:** Unbounded knapsack, minimization

---

### 7. Maximum Product Subarray (LeetCode 152)
**File:** `maximum_product_subarray.py`

**Description:** Find the contiguous subarray with the largest product.

**Key Concepts:**
- Track both max and min (negative × negative = positive)
- Reset on encountering 0
- Similar to Kadane's algorithm

**Time:** O(n) | **Space:** O(1)

**Pattern:** Max/min tracking with state reset

---

### 8. Word Break (LeetCode 139)
**File:** `word_break.py`

**Description:** Determine if a string can be segmented into words from a dictionary.

**Key Concepts:**
- DP[i] = can we segment s[0:i]
- For each position, try all possible words ending there
- Use set for O(1) word lookup

**Time:** O(n² × m) where m = avg word length | **Space:** O(n)

**Pattern:** String segmentation DP

---

### 9. Longest Increasing Subsequence (LeetCode 300)
**File:** `longest_increasing_subsequence.py`

**Description:** Find the length of the longest strictly increasing subsequence.

**Key Concepts:**
- DP[i] = length of LIS ending at index i
- For each element, check all previous elements
- Alternative: Binary search approach O(n log n)

**Time:** O(n²) or O(n log n) | **Space:** O(n)

**Pattern:** Subsequence DP

---

### 10. Partition Equal Subset Sum (LeetCode 416)
**File:** `partition_equal_subset_sum.py`

**Description:** Determine if an array can be partitioned into two subsets with equal sum.

**Key Concepts:**
- Reduce to subset sum problem (target = total_sum / 2)
- 0/1 knapsack pattern
- DP[i] = can we achieve sum i

**Time:** O(n × sum) | **Space:** O(sum)

**Pattern:** 0/1 knapsack, subset sum

---

## Learning Path

### Level 1: Basic Sequential DP
1. House Robber
2. House Robber II
3. Decode Ways

### Level 2: String DP
4. Longest Palindromic Substring
5. Palindromic Substrings
6. Word Break

### Level 3: Optimization Problems
7. Coin Change
8. Maximum Product Subarray
9. Longest Increasing Subsequence

### Level 4: Subset/Knapsack
10. Partition Equal Subset Sum

## Common Patterns

### 1. Sequential Decision Making
**Problems:** House Robber, House Robber II, Decode Ways
```python
dp[i] = f(dp[i-1], dp[i-2], ...)
```

### 2. String Manipulation
**Problems:** Palindromic problems, Word Break
- Often requires checking substrings
- May use expand around center or DP table

### 3. Knapsack Variants
**Problems:** Coin Change, Partition Equal Subset Sum
```python
for amount in range(target + 1):
    for coin in coins:
        dp[amount] = f(dp[amount], dp[amount - coin])
```

### 4. Max/Min Tracking
**Problems:** Maximum Product Subarray, LIS
- Often need to track multiple states (max and min)
- Consider both positive and negative impacts

## Tips for Success

1. **Draw the DP table** - Visualize how values are computed
2. **Write the recurrence relation** - Formalize the relationship between states
3. **Consider edge cases** - Empty arrays, zeros, negatives
4. **Space optimize after solving** - First get it working, then optimize
5. **Practice pattern recognition** - Group similar problems together

## Time Complexity Patterns

- **O(n)**: Sequential scan with O(1) transitions (House Robber, Max Product)
- **O(n²)**: Nested loops or substring checks (LIS, Palindromic Substring)
- **O(n × target)**: Knapsack variants (Coin Change, Partition Equal Subset)

## Companies

Frequently asked by: Amazon, Google, Apple, Microsoft, Facebook, Bloomberg, Adobe, Netflix, Uber, Airbnb

## Next Steps

After mastering these problems, advance to:
- **2D Dynamic Programming** - Problems requiring 2D state space
- **Hard DP Problems** - More complex state transitions and optimizations
