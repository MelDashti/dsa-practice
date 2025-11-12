# Math & Geometry - Hard

## Overview
Hard math and geometry problems require implementing complex mathematical algorithms that aren't typically provided by standard libraries. These problems test deep understanding of algorithms, number theory, and string manipulation for representing arbitrarily large numbers.

## Key Concepts

### 1. Arbitrary Precision Arithmetic
- **Beyond Integer Limits**: Handling numbers larger than 64-bit integers
- **String Representation**: Using strings to store digits
- **Digit-by-Digit Operations**: Manual implementation of arithmetic
- **Carry Management**: Propagating carries across digits

### 2. Grade School Algorithms
- **Long Multiplication**: Multiplying each digit with entire number
- **Long Division**: Not often needed but conceptually similar
- **Position Values**: Understanding place value (ones, tens, hundreds...)
- **Result Size Estimation**: Predicting output length

### 3. String Manipulation for Math
- **Reverse Processing**: Often easier to work right-to-left
- **Leading Zeros**: Handling and removing them appropriately
- **Sign Handling**: Negative numbers in string form
- **Immutable Strings**: Building results efficiently

### 4. Optimization Techniques
- **Early Termination**: Skipping unnecessary operations
- **Zero Handling**: Special cases for zero operands
- **StringBuilder/List**: Avoiding repeated string concatenation
- **Space Reuse**: In-place operations where possible

## Problems in This Section

### Multiply Strings (LC 43)
**Problem**: Multiply two non-negative integers represented as strings, return result as string.

**Why It's Hard**:
- Cannot use built-in big integer libraries (that's cheating!)
- Must implement multiplication from scratch
- Handle arbitrarily large numbers (e.g., 1000-digit numbers)
- Manage carry propagation correctly
- Edge cases: zeros, leading zeros, different lengths

**Key Insights**:
1. **Grade School Multiplication**:
   ```
       123
     ×  45
     -----
       615  (123 × 5)
      492   (123 × 4, shifted left once)
     -----
      5535
   ```

2. **Position-Based Approach**:
   - Product of digit at position i and j goes to position i+j and i+j+1
   - `num1[i] × num2[j]` contributes to result[i+j] and result[i+j+1]

3. **Result Length**:
   - Maximum length: len(num1) + len(num2)
   - May have leading zero if result is smaller

**Complexity**:
- Time: O(m × n) where m, n are lengths
- Space: O(m + n) for result

**Pattern**: Simulation + Carry Propagation + String Manipulation

---

## Deep Dive: Multiply Strings

### Approach 1: Grade School Algorithm

#### Conceptual Understanding
```
Multiply: 123 × 456

Step 1: 123 × 6 = 738
Step 2: 123 × 5 = 615 (shift left 1)
Step 3: 123 × 4 = 492 (shift left 2)

Add all:
      738
     6150  (+)
    49200  (+)
   -------
    56088
```

#### Implementation Strategy
```python
def multiply(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"

    m, n = len(num1), len(num2)
    result = [0] * (m + n)

    # Multiply each digit
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # Multiply digits
            mul = int(num1[i]) * int(num2[j])

            # Add to existing value at this position
            p1, p2 = i + j, i + j + 1
            total = mul + result[p2]

            result[p2] = total % 10  # Current digit
            result[p1] += total // 10  # Carry

    # Convert to string, skip leading zeros
    result_str = ''.join(map(str, result))
    return result_str.lstrip('0') or '0'
```

### Why Position-Based Works

**Key Insight**: When multiplying digit at position i by digit at position j, the result affects positions i+j and i+j+1.

**Example**: 123 × 45

```
Index:     0  1  2    (num1 = "123")
          ×  0  1     (num2 = "45")
          ---------
Result:    0  1  2  3  4

Multiplication table:
num1[0] × num2[0] = 1 × 4 = 4  → pos [0+0, 0+0+1] = [0, 1]
num1[0] × num2[1] = 1 × 5 = 5  → pos [0+1, 0+1+1] = [1, 2]
num1[1] × num2[0] = 2 × 4 = 8  → pos [1+0, 1+0+1] = [1, 2]
num1[1] × num2[1] = 2 × 5 = 10 → pos [1+1, 1+1+1] = [2, 3]
num1[2] × num2[0] = 3 × 4 = 12 → pos [2+0, 2+0+1] = [2, 3]
num1[2] × num2[1] = 3 × 5 = 15 → pos [2+1, 2+1+1] = [3, 4]

Position-wise addition with carry:
Pos 4: 15 % 10 = 5, carry 1
Pos 3: 12 + 10 + 1 = 23 → 3, carry 2
Pos 2: 8 + 5 + 2 = 15 → 5, carry 1
Pos 1: 4 + 1 = 5
Pos 0: 0

Result: 05535 → 5535
```

### Step-by-Step Trace

**Input**: num1 = "123", num2 = "45"

```
Initial: result = [0, 0, 0, 0, 0]
                   0  1  2  3  4

Step 1: i=2 (digit 3), j=1 (digit 5)
  mul = 3 × 5 = 15
  p1=3, p2=4
  result[4] = 15 % 10 = 5
  result[3] = 15 // 10 = 1
  result = [0, 0, 0, 1, 5]

Step 2: i=2, j=0 (digit 4)
  mul = 3 × 4 = 12
  p1=2, p2=3
  total = 12 + result[3] = 12 + 1 = 13
  result[3] = 13 % 10 = 3
  result[2] = 13 // 10 = 1
  result = [0, 0, 1, 3, 5]

Step 3: i=1 (digit 2), j=1 (digit 5)
  mul = 2 × 5 = 10
  p1=2, p2=3
  total = 10 + result[3] = 10 + 3 = 13
  result[3] = 13 % 10 = 3
  result[2] += 13 // 10 = 1 + 1 = 2
  result = [0, 0, 2, 3, 5]

Step 4: i=1, j=0 (digit 4)
  mul = 2 × 4 = 8
  p1=1, p2=2
  total = 8 + result[2] = 8 + 2 = 10
  result[2] = 10 % 10 = 0
  result[1] += 10 // 10 = 0 + 1 = 1
  result = [0, 1, 0, 3, 5]

Step 5: i=0 (digit 1), j=1 (digit 5)
  mul = 1 × 5 = 5
  p1=1, p2=2
  total = 5 + result[2] = 5 + 0 = 5
  result[2] = 5 % 10 = 5
  result[1] += 5 // 10 = 1 + 0 = 1
  result = [0, 1, 5, 3, 5]

Step 6: i=0, j=0 (digit 4)
  mul = 1 × 4 = 4
  p1=0, p2=1
  total = 4 + result[1] = 4 + 1 = 5
  result[1] = 5 % 10 = 5
  result[0] += 5 // 10 = 0 + 0 = 0
  result = [0, 5, 5, 3, 5]

Final: "05535" → strip leading zero → "5535"
```

### Approach 2: Karatsuba Algorithm

For very large numbers (1000+ digits), Karatsuba multiplication is faster than grade school.

**Idea**: Divide and conquer
- Split each number into two halves
- Use formula: (a×10^m + b) × (c×10^m + d) = ac×10^(2m) + ((a+b)×(c+d) - ac - bd)×10^m + bd
- Reduces multiplications from 4 to 3

**Complexity**: O(n^log₂3) ≈ O(n^1.585) vs O(n²) for grade school

**Implementation** (conceptual):
```python
def karatsuba(x, y):
    # Base case
    if x < 10 or y < 10:
        return x * y

    # Split numbers
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    x1, x0 = divmod(x, 10**m)
    y1, y0 = divmod(y, 10**m)

    # Three multiplications instead of four
    z0 = karatsuba(x0, y0)
    z2 = karatsuba(x1, y1)
    z1 = karatsuba(x0 + x1, y0 + y1) - z0 - z2

    return z2 * 10**(2*m) + z1 * 10**m + z0
```

**Note**: For LeetCode problems, grade school is sufficient and easier to implement correctly.

### Edge Cases and Special Handling

#### 1. Zero Handling
```python
# Special case: if either is zero
if num1 == "0" or num2 == "0":
    return "0"

# After computation, handle leading zeros
result_str.lstrip('0') or '0'  # '0' if empty after lstrip
```

#### 2. Leading Zeros
```python
# Input might have leading zeros (though usually not in valid test cases)
num1 = num1.lstrip('0') or '0'
num2 = num2.lstrip('0') or '0'
```

#### 3. Different Lengths
```python
# Works naturally with position-based approach
# No need for special handling
```

#### 4. Single Digit
```python
# "3" × "4" = "12"
# Works with same algorithm
```

#### 5. Large Numbers
```python
# "999" × "999" = "998001"
# "12345678901234567890" × "98765432109876543210"
# Algorithm handles any size (limited by memory)
```

## Complete Implementation with Comments

```python
def multiply(num1: str, num2: str) -> str:
    """
    Multiply two non-negative integers represented as strings.

    Time Complexity: O(m × n) where m, n are lengths
    Space Complexity: O(m + n) for result array

    Args:
        num1: First number as string
        num2: Second number as string

    Returns:
        Product as string
    """
    # Edge case: either number is zero
    if num1 == "0" or num2 == "0":
        return "0"

    m, n = len(num1), len(num2)

    # Result can have at most m + n digits
    # Example: 99 × 99 = 9801 (2 + 2 = 4 digits)
    result = [0] * (m + n)

    # Multiply each digit of num1 with each digit of num2
    # Process from right to left (least significant to most significant)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # Multiply current digits
            mul = int(num1[i]) * int(num2[j])

            # Positions in result array
            p1 = i + j      # Position for tens digit (carry)
            p2 = i + j + 1  # Position for ones digit

            # Add multiplication result to existing value
            total = mul + result[p2]

            # Update positions with new digit and carry
            result[p2] = total % 10      # Ones place
            result[p1] += total // 10     # Tens place (carry)

    # Convert result array to string
    result_str = ''.join(map(str, result))

    # Remove leading zeros (if any) but keep at least one '0'
    return result_str.lstrip('0') or '0'
```

## Alternative Implementations

### Using Single Loop with Offset
```python
def multiply_v2(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"

    result = "0"

    # Multiply num1 by each digit of num2
    for i, digit2 in enumerate(reversed(num2)):
        # Multiply num1 by single digit
        temp = multiply_by_digit(num1, int(digit2))
        # Add appropriate zeros (shift left)
        temp += "0" * i
        # Add to result
        result = add_strings(result, temp)

    return result

def multiply_by_digit(num: str, digit: int) -> str:
    """Multiply string number by single digit."""
    carry = 0
    result = []

    for i in range(len(num) - 1, -1, -1):
        prod = int(num[i]) * digit + carry
        result.append(str(prod % 10))
        carry = prod // 10

    if carry:
        result.append(str(carry))

    return ''.join(reversed(result))

def add_strings(num1: str, num2: str) -> str:
    """Add two string numbers."""
    # Implementation of string addition
    ...
```

### Recursive Approach
```python
def multiply_recursive(num1: str, num2: str) -> str:
    # Base cases
    if num1 == "0" or num2 == "0":
        return "0"
    if num1 == "1":
        return num2
    if num2 == "1":
        return num1

    # Split numbers in half
    n = max(len(num1), len(num2))
    mid = n // 2

    # Pad with zeros if needed
    num1 = num1.zfill(n)
    num2 = num2.zfill(n)

    # Divide
    a, b = num1[:-mid] or "0", num1[-mid:] or "0"
    c, d = num2[:-mid] or "0", num2[-mid:] or "0"

    # Recursive multiplications (can optimize with Karatsuba)
    ac = multiply_recursive(a, c)
    bd = multiply_recursive(b, d)
    ad_bc = add_strings(
        multiply_recursive(a, d),
        multiply_recursive(b, c)
    )

    # Combine: ac × 10^(2m) + (ad+bc) × 10^m + bd
    return add_strings(
        add_strings(ac + "0" * (2 * mid), ad_bc + "0" * mid),
        bd
    )
```

## Testing Strategy

### Test Cases
```python
# Basic cases
assert multiply("2", "3") == "6"
assert multiply("123", "456") == "56088"

# Zero cases
assert multiply("0", "123") == "0"
assert multiply("456", "0") == "0"
assert multiply("0", "0") == "0"

# Single digit
assert multiply("9", "9") == "81"
assert multiply("5", "7") == "35"

# Different lengths
assert multiply("999", "1") == "999"
assert multiply("123", "45") == "5535"

# Large numbers
assert multiply("123456789", "987654321") == "121932631112635269"

# Edge cases
assert multiply("1", "1") == "1"
assert multiply("999", "999") == "998001"

# Very large (stress test)
big1 = "12345678901234567890"
big2 = "98765432109876543210"
result = multiply(big1, big2)
# Verify with Python's built-in: int(big1) * int(big2)
```

### Performance Testing
```python
import time

def benchmark():
    # Test increasing sizes
    for length in [10, 100, 1000]:
        num1 = "9" * length
        num2 = "9" * length

        start = time.time()
        result = multiply(num1, num2)
        elapsed = time.time() - start

        print(f"Length {length}: {elapsed:.4f}s")
        print(f"Result length: {len(result)}")

# Expected: O(n²) growth in time
```

## Common Mistakes

### 1. Incorrect Position Calculation
```python
# ❌ Wrong
p1, p2 = i + j, i + j + 2  # Off by one!

# ✓ Correct
p1, p2 = i + j, i + j + 1
```

### 2. Forgetting Carry Addition
```python
# ❌ Wrong
result[p2] = total % 10
result[p1] = total // 10  # Should be +=

# ✓ Correct
result[p2] = total % 10
result[p1] += total // 10
```

### 3. Not Handling Leading Zeros
```python
# ❌ Wrong
return ''.join(map(str, result))  # Might have leading 0

# ✓ Correct
return ''.join(map(str, result)).lstrip('0') or '0'
```

### 4. Wrong Loop Direction
```python
# ❌ Wrong: Processing left to right makes carry harder
for i in range(m):
    for j in range(n):
        ...

# ✓ Correct: Right to left (least to most significant)
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
        ...
```

### 5. Missing Zero Check
```python
# ❌ Wrong: Might return "0000"
if num1 == "0" or num2 == "0":
    return "0"
# ... rest of code ...
return ''.join(map(str, result)).lstrip('0')  # Empty string!

# ✓ Correct
return ''.join(map(str, result)).lstrip('0') or '0'
```

## Interview Tips

### Problem-Solving Approach
1. **Clarify**: Can we use built-in BigInteger? (Usually no)
2. **Example**: Work through "23" × "45" by hand
3. **Pattern**: Identify it's grade school multiplication
4. **Data Structure**: Array to accumulate results
5. **Implementation**: Position-based approach
6. **Test**: Edge cases (zero, single digit, large)

### What Interviewers Look For
- Understanding of elementary algorithms
- Careful handling of carries
- Attention to edge cases
- Clean, readable code
- Proper complexity analysis

### Follow-up Questions
- How would you implement addition/subtraction?
- What about division?
- Can you optimize for very large numbers? (Karatsuba)
- How would you handle negative numbers?
- What about floating point multiplication?

## Related Problems

### String Arithmetic Series
- Add Strings (LC 415)
- Add Binary (LC 67)
- Plus One (LC 66)
- Multiply Strings (LC 43)
- Divide Two Integers (LC 29)

### Advanced
- Implement BigInteger class
- Arbitrary precision calculator
- Scientific notation handling
- Fraction arithmetic

## Key Takeaways

1. **Position-based multiplication** is key insight: `num1[i] × num2[j]` affects positions `i+j` and `i+j+1`
2. **Carry propagation** must be handled correctly with `+=`
3. **Right-to-left processing** is natural for arithmetic
4. **Leading zeros** must be removed from result
5. **Zero is special case** requiring early return
6. **O(m × n) complexity** is optimal for grade school algorithm
7. **Karatsuba exists** but rarely needed in interviews
8. **String manipulation** skills are essential for arbitrary precision

## Further Reading

- CLRS Chapter 30: Polynomials and FFT (advanced multiplication)
- Knuth's "The Art of Computer Programming" Volume 2
- GMP library source code (real-world implementation)
- "Hacker's Delight" for bit-level optimizations
