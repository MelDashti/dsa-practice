# Math & Geometry - Easy

## Overview
Easy math and geometry problems introduce fundamental mathematical operations, number properties, and basic geometric concepts. These problems build intuition for mathematical problem-solving and often appear as building blocks in more complex algorithms.

## Key Concepts

### 1. Number Properties
- **Even vs Odd**: n % 2 == 0
- **Divisibility**: a % b == 0
- **Prime Numbers**: Only divisible by 1 and itself
- **Perfect Squares**: n = k² for some integer k

### 2. Mathematical Operations
- **Modular Arithmetic**: (a + b) % m = ((a % m) + (b % m)) % m
- **Integer Division**: a // b in Python
- **Overflow Handling**: Important in languages like C++/Java
- **Digit Manipulation**: Extract digits using % 10 and // 10

### 3. Data Structure Design
- **Class Design**: Creating custom data structures
- **API Design**: Defining clear interfaces
- **State Management**: Maintaining internal state
- **Operation Efficiency**: Optimizing method calls

### 4. Space-Time Tradeoffs
- **Precomputation**: Trading space for time
- **Lazy Evaluation**: Computing only when needed
- **Caching**: Storing results for reuse
- **Hash Tables**: O(1) average case lookups

## Problems in This Section

### Happy Number (LC 202)
**Problem**: Determine if a number is "happy" (repeatedly replacing it with sum of squares of digits eventually reaches 1).

**Key Insights**:
- Use Floyd's cycle detection (fast/slow pointers)
- Or use a hash set to detect cycles
- If we reach 1, it's happy
- If we see a repeated number, we're in a cycle (not happy)

**Approach**:
```python
# Compute next number: O(log n) - number of digits
# Cycle detection with set: O(1) per check
# Total: O(log n) time, O(log n) space
```

**Pattern**: Cycle Detection + Digit Manipulation

**Common Pitfalls**:
- Not detecting cycles (infinite loop)
- Computing sum of digits incorrectly
- Not handling single digit inputs

---

### Plus One (LC 66)
**Problem**: Given array representing a large number, add 1 to it.

**Key Insights**:
- Start from the least significant digit (end of array)
- Handle carry propagation
- Edge case: All 9's (e.g., [9,9,9] → [1,0,0,0])
- Think like manual addition

**Approach**:
```python
# Iterate from right to left: O(n)
# Add carry and update digits
# Prepend 1 if final carry exists
# Time: O(n), Space: O(1) or O(n) for result
```

**Pattern**: Array Manipulation + Carry Propagation

**Common Pitfalls**:
- Not handling all 9's case
- Modifying array during iteration incorrectly
- Forgetting to add leading 1 when needed

---

### Detect Squares (LC 2013)
**Problem**: Design a data structure to add points and count axis-aligned squares.

**Key Insights**:
- Store points with their frequencies (same point can appear multiple times)
- To count squares: fix diagonal, find other two corners
- For square with corners (x1,y1) and (x2,y2): other corners are (x1,y2) and (x2,y1)
- Side length must match: |x2-x1| == |y2-y1|

**Approach**:
```python
# Store points: O(1) per add
# Count squares: O(n) where n = unique points
# Use dictionary for O(1) lookups
# Space: O(n)
```

**Pattern**: Hash Table + Geometry + Combinatorics

**Common Pitfalls**:
- Not handling duplicate points
- Incorrect square validation (must be axis-aligned)
- Missing diagonal relationship
- Not considering all possible diagonals

## Fundamental Techniques

### 1. Digit Manipulation
```python
def sum_of_digit_squares(n):
    """Calculate sum of squares of digits."""
    total = 0
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total

# Alternative: using string
def sum_of_digit_squares_alt(n):
    return sum(int(d) ** 2 for d in str(n))
```

### 2. Cycle Detection (Floyd's Algorithm)
```python
def detect_cycle(start, next_func):
    """Detect cycle using slow/fast pointers."""
    slow = fast = start

    while True:
        slow = next_func(slow)
        fast = next_func(next_func(fast))

        if fast == target:
            return True  # Found target

        if slow == fast:
            return False  # Cycle detected without target
```

### 3. Hash Set for Cycle Detection
```python
def detect_cycle_with_set(start, next_func, target):
    """Detect cycle using hash set."""
    seen = set()

    current = start
    while current not in seen:
        if current == target:
            return True

        seen.add(current)
        current = next_func(current)

    return False  # Cycle detected
```

### 4. Carry Propagation
```python
def add_one_digit_array(digits):
    """Add 1 to number represented as digit array."""
    carry = 1

    for i in range(len(digits) - 1, -1, -1):
        total = digits[i] + carry
        digits[i] = total % 10
        carry = total // 10

        if carry == 0:
            break  # Early termination

    if carry:
        digits.insert(0, 1)

    return digits
```

### 5. Point-Based Hash Table
```python
def store_points():
    """Store 2D points with frequencies."""
    from collections import defaultdict

    points = defaultdict(int)

    # Add point
    points[(x, y)] += 1

    # Check if point exists
    if (x, y) in points:
        count = points[(x, y)]

    return points
```

## Code Templates

### Template 1: Happy Number
```python
def isHappy(n: int) -> bool:
    """Determine if number is happy using cycle detection."""

    def sum_of_squares(num):
        total = 0
        while num:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    seen = set()

    while n != 1 and n not in seen:
        seen.add(n)
        n = sum_of_squares(n)

    return n == 1
```

### Template 2: Plus One
```python
def plusOne(digits: List[int]) -> List[int]:
    """Add one to number represented as digit array."""
    n = len(digits)

    # Traverse from right to left
    for i in range(n - 1, -1, -1):
        # If digit is less than 9, just add 1 and return
        if digits[i] < 9:
            digits[i] += 1
            return digits

        # Otherwise, set to 0 and continue (carry over)
        digits[i] = 0

    # If we're here, all digits were 9
    # e.g., [9,9,9] becomes [0,0,0], need to prepend 1
    return [1] + digits
```

### Template 3: Detect Squares
```python
from collections import defaultdict
from typing import List

class DetectSquares:
    """Data structure to add points and count squares."""

    def __init__(self):
        # Store points with their counts
        self.points = defaultdict(int)

    def add(self, point: List[int]) -> None:
        """Add a point to the data structure."""
        self.points[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        """Count squares with one corner at point."""
        x1, y1 = point
        total = 0

        # Try all other points as potential diagonal corners
        for (x2, y2), count2 in self.points.items():
            # Skip same point or non-diagonal points
            if x1 == x2 or y1 == y2:
                continue

            # Check if it forms a square (equal side lengths)
            if abs(x2 - x1) != abs(y2 - y1):
                continue

            # Count the square by checking other two corners
            # The other two corners are (x1, y2) and (x2, y1)
            count_a = self.points[(x1, y2)]
            count_b = self.points[(x2, y1)]

            # Multiply counts (combinatorics)
            total += count2 * count_a * count_b

        return total
```

## Visual Examples

### Happy Number Flow
```
Example: n = 19

19 → 1² + 9² = 1 + 81 = 82
82 → 8² + 2² = 64 + 4 = 68
68 → 6² + 8² = 36 + 64 = 100
100 → 1² + 0² + 0² = 1 ✓ Happy!

Example: n = 2

2 → 2² = 4
4 → 4² = 16
16 → 1² + 6² = 1 + 36 = 37
37 → 3² + 7² = 9 + 49 = 58
58 → 5² + 8² = 25 + 64 = 89
89 → 8² + 9² = 64 + 81 = 145
145 → 1² + 4² + 5² = 1 + 16 + 25 = 42
42 → 4² + 2² = 16 + 4 = 20
20 → 2² + 0² = 4 ← Cycle detected! Not happy.
```

### Plus One Visualization
```
Example: [1, 2, 3]
         [1, 2, 3] + 1 = [1, 2, 4]
            ↑ add 1

Example: [1, 2, 9]
         [1, 2, 9] + 1
            ↑ becomes 0, carry 1
         [1, 3, 0]

Example: [9, 9, 9]
         [9, 9, 9] + 1
         ↓  ↓  ↓  all become 0, carry propagates
         [0, 0, 0] → [1, 0, 0, 0]
         prepend 1
```

### Detect Squares Example
```
Points: (0,0), (0,1), (1,0), (1,1)

         (0,1) ●━━━━━● (1,1)
           ┃         ┃
           ┃         ┃
         (0,0) ●━━━━━● (1,0)

Query: count((0,0))

Fix diagonal to (1,1):
- Distance: |1-0| = 1 (x), |1-0| = 1 (y) ✓ Equal
- Other corners: (0,1) and (1,0)
- Check if both exist: Yes!
- This forms 1 square

Another example with diagonal to (0,1):
- Not diagonal (x coordinates same)
- Skip

Result: 1 square
```

## Time & Space Complexity Patterns

| Problem | Time (per operation) | Space | Notes |
|---------|---------------------|-------|-------|
| Happy Number | O(log n) | O(log n) | Digits in n |
| Plus One | O(n) | O(1) | n = array length |
| Detect Squares (add) | O(1) | O(n) | n = total points |
| Detect Squares (count) | O(n) | O(n) | Check all points |

## Common Interview Questions

### Mathematical Understanding
1. Why does the happy number algorithm always terminate?
2. What's the maximum cycle length for happy numbers?
3. How do you handle integer overflow in other languages?

### Implementation Details
1. Why use tuple instead of list for dictionary keys?
2. How does carry propagation work?
3. What's the difference between `//` and `/` in Python?

### Design Questions
1. How would you extend DetectSquares to detect rectangles?
2. Could you optimize the count operation?
3. What if coordinates can be negative?

## Edge Cases to Consider

### Happy Number
```python
# Single digit happy numbers: 1, 7
# Single digit unhappy numbers: 2-6, 8-9
# Powers of 10: 10, 100, 1000
# Large numbers: test cycle detection
```

### Plus One
```python
# All 9's: [9], [9,9,9]
# No carry: [1,2,3]
# Partial carry: [1,9,9]
# Single digit: [0], [5]
```

### Detect Squares
```python
# No points: count should return 0
# Single point: no squares possible
# Same point multiple times: multiplicative counting
# Rectangle (not square): should not count
# Negative coordinates: should work
# Large coordinates: test hash efficiency
```

## Practice Tips

### Understanding the Problem
1. Work through examples manually
2. Draw diagrams for geometric problems
3. Identify the core mathematical operation
4. Consider edge cases early

### Implementation Strategy
1. Start with brute force if needed
2. Identify bottlenecks
3. Apply appropriate data structures
4. Test with edge cases

### Optimization
1. Can you precompute anything?
2. Is there a mathematical property to exploit?
3. Can hash tables speed up lookups?
4. Is early termination possible?

## Debugging Strategies

### Happy Number
```python
# Print the sequence
def debug_happy(n):
    seen = set()
    path = [n]

    while n != 1 and n not in seen:
        seen.add(n)
        n = sum_of_squares(n)
        path.append(n)

    print(f"Path: {' → '.join(map(str, path))}")
    return n == 1
```

### Plus One
```python
# Visualize carry
def debug_plus_one(digits):
    print(f"Input: {digits}")

    carry = 1
    for i in range(len(digits)-1, -1, -1):
        old = digits[i]
        digits[i] = (digits[i] + carry) % 10
        carry = (old + carry) // 10
        print(f"Position {i}: {old} → {digits[i]}, carry={carry}")

    if carry:
        digits.insert(0, 1)

    return digits
```

### Detect Squares
```python
# Visualize point storage
def debug_add_point(self, point):
    print(f"Adding point: {point}")
    self.points[tuple(point)] += 1
    print(f"Current points: {dict(self.points)}")

def debug_count(self, point):
    print(f"Counting squares with corner at {point}")

    # Add detailed logging for each diagonal check
    ...
```

## Related Concepts

### Mathematical
- **Number Theory**: Prime factorization, GCD, LCM
- **Combinatorics**: Counting principles, permutations
- **Geometry**: Distance formulas, area calculations
- **Modular Arithmetic**: Useful for large number operations

### Programming
- **Hash Tables**: Efficient key-value storage
- **Two Pointers**: Slow/fast for cycle detection
- **Array Manipulation**: In-place modifications
- **Object-Oriented Design**: Class and method design

## Next Steps

After mastering easy problems:
1. **Medium**: More complex geometry (matrix rotations, spirals)
2. **Advanced Math**: Implement pow(x,n), multiply large numbers
3. **Bit Manipulation**: Often combined with math problems
4. **Dynamic Programming**: Math problems with optimal substructure

## Additional Resources

### Online Resources
- Visualgo: Interactive algorithm visualizations
- Khan Academy: Mathematical foundations
- Python Docs: Numeric operations and data structures

### Books
- "Concrete Mathematics" by Knuth
- "Introduction to Algorithms" (CLRS)
- "Elements of Programming Interviews"

### Practice Platforms
- LeetCode: More math problems (tagged "Math")
- HackerRank: Mathematical challenges
- Project Euler: Pure math problems
