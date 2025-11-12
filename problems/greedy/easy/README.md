# Greedy - Easy

This folder contains easy-level Greedy algorithm problems. These problems are excellent for understanding the greedy approach and when it produces optimal solutions.

## Problems

### 1. Maximum Subarray (LeetCode 53)
**File:** `maximum_subarray.py`

**Description:** Find the contiguous subarray with the largest sum.

**Key Concepts:**
- Kadane's Algorithm
- Greedy choice: at each position, decide to extend current subarray or start fresh
- If current sum becomes negative, reset to 0
- Track maximum sum seen so far
- Can also be solved with DP

**Time:** O(n) | **Space:** O(1)

**Pattern:** Kadane's Algorithm / Greedy subarray

---

## The Greedy Approach

### What is a Greedy Algorithm?

A greedy algorithm makes the locally optimal choice at each step with the hope of finding a global optimum.

**Key characteristics:**
1. Makes the best choice at the current moment
2. Never reconsiders previous choices
3. Usually fast (often O(n) or O(n log n))
4. Doesn't always produce optimal solution (need to prove correctness)

### When to Use Greedy

Greedy works when:
1. **Greedy choice property** - Local optimum leads to global optimum
2. **Optimal substructure** - Optimal solution contains optimal solutions to subproblems
3. The problem asks for maximum/minimum of something
4. You can prove making the greedy choice leaves you in a state where you can still reach optimal solution

### Maximum Subarray - Why Greedy Works

**Intuition:**
- At each position, we decide: extend current subarray or start new one
- If current sum is negative, it will only decrease future sums, so reset
- This greedy choice guarantees we find the maximum sum

**Proof sketch:**
- Any optimal subarray doesn't include a negative prefix
- If it did, removing that prefix would give a larger sum
- Therefore, resetting when sum becomes negative is optimal

## Algorithm Deep Dive

### Kadane's Algorithm

```python
def maxSubArray(nums):
    max_sum = nums[0]
    current_sum = 0

    for num in nums:
        # Greedy choice: start fresh if current_sum is negative
        current_sum = max(0, current_sum)
        current_sum += num
        max_sum = max(max_sum, current_sum)

    return max_sum
```

**Step-by-step process:**
1. Keep running sum of current subarray
2. If sum becomes negative, reset to 0 (start fresh)
3. Track maximum sum encountered
4. Return maximum

**Example:** `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

```
Position:  -2   1  -3   4  -1   2   1  -5   4
Current:   -2   1  -2   4   3   5   6   1   5
Max:       -2   1   1   4   4   5   6   6   6
```

Answer: 6 (subarray [4, -1, 2, 1])

## Variations

### Return the Subarray (not just sum)

Track start and end indices:

```python
def maxSubArrayWithIndices(nums):
    max_sum = float('-inf')
    current_sum = 0
    start = end = temp_start = 0

    for i, num in enumerate(nums):
        if current_sum < 0:
            current_sum = 0
            temp_start = i

        current_sum += num

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return max_sum, nums[start:end+1]
```

### Handle All Negative Numbers

The basic algorithm handles this correctly - it returns the least negative number.

## Common Patterns

### 1. Running Sum with Reset
- Keep running calculation
- Reset when condition met (e.g., sum < 0)
- Track global optimum

### 2. Greedy Decision Point
- At each element: extend or restart
- Make choice based on current state
- Don't look back

## Alternative Approaches

### 1. Dynamic Programming
```python
# dp[i] = max sum ending at index i
dp[i] = max(nums[i], dp[i-1] + nums[i])
```
Same time/space complexity, but Kadane's is more elegant.

### 2. Divide and Conquer
- Split array in half
- Max subarray is either:
  - Entirely in left half
  - Entirely in right half
  - Crosses the middle
- O(n log n) time - less efficient than greedy

## Practice Tips

1. **Understand the invariant** - What stays true after each iteration?
2. **Trace through examples** - Work through arrays by hand
3. **Consider edge cases**:
   - All negative numbers
   - All positive numbers
   - Single element
   - Empty array (if allowed)
4. **Prove correctness** - Why does greedy work here?

## Interview Insights

**Common questions:**
- "Why does this greedy approach work?"
  - Negative prefix never helps future sums

- "Can you solve it with O(1) space?"
  - Yes, Kadane's algorithm uses O(1) space

- "What if we need the actual subarray?"
  - Track start/end indices during iteration

- "What's the difference between greedy and DP here?"
  - Same logic, DP explicitly stores subproblems
  - Greedy just tracks what's needed

## Related Problems

After mastering Maximum Subarray, you'll be ready for:

**Medium Greedy:**
- Jump Game (55)
- Jump Game II (45)
- Gas Station (134)

**Similar Pattern:**
- Maximum Product Subarray (152) - More complex, needs to track min/max
- Best Time to Buy and Sell Stock (121) - Similar one-pass greedy

## Real-World Applications

1. **Stock Trading** - Finding best period for investment
2. **Performance Analysis** - Identifying peak performance periods
3. **Signal Processing** - Finding strongest signal segments
4. **Resource Allocation** - Maximizing resource usage in time periods

## Companies

Frequently asked by: Amazon, Google, Microsoft, Apple, Facebook, Bloomberg, LinkedIn

## Time Complexity Analysis

- **Kadane's Algorithm**: O(n) time, O(1) space - Optimal
- **Brute Force**: O(n²) or O(n³) - Check all subarrays
- **Divide and Conquer**: O(n log n) - Recursive split

## Key Takeaways

1. **Greedy works when local optimum → global optimum**
2. **Kadane's algorithm is the canonical greedy solution**
3. **Negative prefix never helps** - this is the greedy insight
4. **O(n) time and O(1) space is achievable**
5. **Can track indices with minor modifications**

## Next Steps

1. **Master this problem thoroughly** - It appears frequently in interviews
2. **Understand why greedy works** - Practice explaining the proof
3. **Try variations** - Return subarray, handle edge cases
4. **Move to medium greedy** - Jump Game, Gas Station, etc.
5. **Compare with DP** - Understand the relationship between approaches

---

This is a fundamental problem that teaches core greedy principles. Understanding it deeply will help you recognize when greedy approaches work in other problems.
