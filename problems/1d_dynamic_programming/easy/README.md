# 1D Dynamic Programming - Easy

This folder contains easy-level 1D Dynamic Programming problems. These problems are great for beginners learning dynamic programming concepts.

## Problems

### 1. Climbing Stairs (LeetCode 70)
**File:** `climbing_stairs.py`

**Description:** Given n steps, find how many distinct ways you can climb to the top if you can climb 1 or 2 steps at a time.

**Key Concepts:**
- Fibonacci sequence pattern
- Bottom-up dynamic programming
- Space optimization (O(1) space)

**Time Complexity:** O(n)
**Space Complexity:** O(1)

**Pattern Recognition:** When you see problems asking for "number of ways" with limited choices at each step, think Fibonacci/DP.

---

### 2. Min Cost Climbing Stairs (LeetCode 746)
**File:** `min_cost_climbing_stairs.py`

**Description:** Given an array of costs where cost[i] is the cost of stepping on the ith step, find the minimum cost to reach the top. You can start from index 0 or 1.

**Key Concepts:**
- Decision-making at each step (min cost path)
- Bottom-up dynamic programming
- Space optimization

**Time Complexity:** O(n)
**Space Complexity:** O(1)

**Pattern Recognition:** When optimizing cost/value while making sequential decisions, consider DP. Similar to Climbing Stairs but with costs.

---

## Learning Path

1. **Start with Climbing Stairs** - This is the classic introduction to 1D DP and the Fibonacci pattern.
2. **Then tackle Min Cost Climbing Stairs** - Builds on the same pattern but adds an optimization element.

## Common Patterns

### Pattern: Sequential Decision Making
Both problems follow this pattern:
- Make decisions step by step
- Current state depends on previous states
- Optimize by only keeping necessary previous states

### Optimization Technique
Instead of storing entire DP array:
```python
# Space: O(n)
dp = [0] * n

# Space: O(1) - Only keep what you need
prev1, prev2 = 0, 0
```

## Tips for Success

1. **Identify the recurrence relation** - How does the current step relate to previous steps?
2. **Define base cases clearly** - What are the simplest cases you can solve directly?
3. **Consider space optimization** - Can you solve it with O(1) space instead of O(n)?
4. **Trace through examples** - Work through small examples by hand to verify your logic.

## Companies

These problems are frequently asked by: Amazon, Google, Adobe, Apple, Microsoft, Facebook

## Related Medium Problems

After mastering these, try:
- House Robber (198)
- House Robber II (213)
- Decode Ways (91)
