# Bit Manipulation - Easy

## Overview
Bit manipulation problems leverage binary representation and bitwise operations to solve problems elegantly and efficiently. These problems often have solutions that are faster and use less memory than traditional approaches, making them essential for performance-critical applications.

## Key Concepts

### 1. Binary Representation
- **Bits**: 0 or 1
- **Binary Numbers**: 5 = 101₂ = 1×2² + 0×2¹ + 1×2⁰
- **32-bit Integers**: Range from -2³¹ to 2³¹-1
- **Two's Complement**: Negative numbers in binary

### 2. Bitwise Operators
- **AND (&)**: 1 & 1 = 1, else 0
- **OR (|)**: 0 | 0 = 0, else 1
- **XOR (^)**: Same = 0, Different = 1
- **NOT (~)**: Flip all bits
- **Left Shift (<<)**: Multiply by 2
- **Right Shift (>>)**: Divide by 2

### 3. Common Patterns
- **Set bit**: `num | (1 << i)`
- **Clear bit**: `num & ~(1 << i)`
- **Toggle bit**: `num ^ (1 << i)`
- **Check bit**: `(num >> i) & 1`
- **Clear lowest set bit**: `num & (num - 1)`

### 4. XOR Properties
- **Commutative**: a ^ b = b ^ a
- **Associative**: (a ^ b) ^ c = a ^ (b ^ c)
- **Identity**: a ^ 0 = a
- **Self-inverse**: a ^ a = 0
- **Chain**: a ^ b ^ a = b

## Problems in This Section

### Single Number (LC 136)
**Problem**: Find the element that appears once while others appear twice.

**Key Insight**: XOR all numbers
- a ^ a = 0 (pairs cancel out)
- a ^ 0 = a (single number remains)
- Order doesn't matter (commutative & associative)

**Solution**:
```python
result = 0
for num in nums:
    result ^= num
return result
```

**Complexity**: O(n) time, O(1) space

**Pattern**: XOR properties for cancellation

---

### Number of 1 Bits (LC 191)
**Problem**: Count number of set bits (Hamming weight).

**Approaches**:
1. **Check each bit**: `(n >> i) & 1`
2. **Brian Kernighan's**: `n & (n-1)` clears lowest set bit

**Key Insight**: `n & (n-1)` removes rightmost 1-bit
- 12 = 1100₂
- 11 = 1011₂
- 12 & 11 = 1000₂ (one 1-bit removed)

**Complexity**: O(log n) or O(k) where k = number of 1s

**Pattern**: Bit counting algorithms

---

### Counting Bits (LC 338)
**Problem**: Count 1-bits for all numbers from 0 to n.

**Key Insights**:
1. **DP relation**: `bits[i] = bits[i >> 1] + (i & 1)`
   - Right shift removes last bit
   - Add 1 if last bit is set
2. **Alternative**: `bits[i] = bits[i & (i-1)] + 1`
   - i & (i-1) clears rightmost bit
   - Add 1 for that bit

**Example**: bits[5] = bits[2] + 1
- 5 = 101₂ (2 ones)
- 5 >> 1 = 2 = 10₂ (1 one)
- 5 & 1 = 1 (last bit is 1)

**Complexity**: O(n) time, O(n) space

**Pattern**: Dynamic Programming + Bit Manipulation

---

### Reverse Bits (LC 190)
**Problem**: Reverse bits of a 32-bit unsigned integer.

**Approach**:
1. Extract bits from right of input
2. Place them on left of output
3. Shift both appropriately

**Process**:
```
Input:  00000010100101000001111010011100
Output: 00111001011110000010100101000000

For each bit:
- Take rightmost bit of input: n & 1
- Add to leftmost of result: result << 1
- Shift input right: n >> 1
```

**Complexity**: O(1) time - always 32 iterations

**Pattern**: Bit extraction and reconstruction

---

### Missing Number (LC 268)
**Problem**: Find missing number in array [0, n] with one missing.

**Approaches**:
1. **Sum formula**: `n(n+1)/2 - sum(array)`
2. **XOR**: `0 ^ 1 ^ 2 ^ ... ^ n ^ all_array_elements`
3. **Sort and search**: Less efficient

**XOR Solution**:
```python
result = len(nums)  # n
for i, num in enumerate(nums):
    result ^= i ^ num
return result
```

**Why it works**:
- XOR all indices [0..n-1] and values
- Pairs cancel: 0^0, 1^1, 2^2, etc.
- Missing number has no pair, remains

**Complexity**: O(n) time, O(1) space

**Pattern**: XOR for finding unpaired element

---

### Sum of Two Integers (LC 371)
**Problem**: Add two integers without using + or - operators.

**Key Insights**:
- **Sum without carry**: a ^ b (XOR)
- **Carry**: (a & b) << 1
- **Repeat**: Until carry is 0

**Process**:
```
Add 5 + 3:
  5 = 0101
  3 = 0011

Step 1:
  sum = 5 ^ 3 = 0110 (6)
  carry = (5 & 3) << 1 = 0010 << 1 = 0100 (4)

Step 2:
  sum = 6 ^ 4 = 0010 (2)
  carry = (6 & 4) << 1 = 0100 << 1 = 1000 (8)

Step 3:
  sum = 2 ^ 8 = 1010 (10)
  carry = (2 & 8) << 1 = 0000 << 1 = 0 (0)

Done: carry is 0, return 10 ✗ Wait, 5+3=8!

Let me recalculate:
  5 = 101
  3 = 011

XOR (sum without carry): 101 ^ 011 = 110 (6)
AND then shift (carry): (101 & 011) << 1 = 001 << 1 = 010 (2)

Now add 6 + 2:
XOR: 110 ^ 010 = 100 (4)
Carry: (110 & 010) << 1 = 010 << 1 = 100 (4)

Now add 4 + 4:
XOR: 100 ^ 100 = 000 (0)
Carry: (100 & 100) << 1 = 100 << 1 = 1000 (8)

Now add 0 + 8:
XOR: 000 ^ 1000 = 1000 (8) ✓
Carry: (000 & 1000) << 1 = 0000 << 1 = 0

Result: 8 ✓
```

**Complexity**: O(1) time - at most 32 iterations

**Pattern**: Bitwise arithmetic simulation

---

### Reverse Integer (LC 7)
**Problem**: Reverse digits of an integer, return 0 if overflow.

**Approach**:
```python
result = 0
while x != 0:
    digit = x % 10 if x > 0 else x % -10
    x = x // 10 if x > 0 else -((-x) // 10)

    # Check overflow before updating
    if result > INT_MAX // 10 or result < INT_MIN // 10:
        return 0

    result = result * 10 + digit
```

**Key Points**:
- Handle negative numbers
- Check overflow before it happens
- 32-bit integer limits: -2³¹ to 2³¹-1

**Complexity**: O(log n) time - number of digits

**Pattern**: Digit manipulation + overflow detection

## Bit Manipulation Fundamentals

### Binary Number System
```
Decimal to Binary:
13 = 1101₂
= 1×2³ + 1×2² + 0×2¹ + 1×2⁰
= 8 + 4 + 0 + 1
= 13

Binary to Decimal:
1011₂ = 1×8 + 0×4 + 1×2 + 1×1 = 11
```

### Bitwise Operators

#### AND (&)
```
  1010 (10)
& 1100 (12)
------
  1000 (8)

Use: Check if bit is set, clear bits, masking
```

#### OR (|)
```
  1010 (10)
| 1100 (12)
------
  1110 (14)

Use: Set bits, combine flags
```

#### XOR (^)
```
  1010 (10)
^ 1100 (12)
------
  0110 (6)

Use: Toggle bits, find differences, cancellation
```

#### NOT (~)
```
~1010 = 0101 (for 4-bit)
~10 = -11 (in two's complement)

Use: Flip all bits, create masks
```

#### Left Shift (<<)
```
5 << 1 = 10  (multiply by 2)
5 << 2 = 20  (multiply by 4)
  0101 << 1 = 1010

Use: Multiply by powers of 2, create masks
```

#### Right Shift (>>)
```
10 >> 1 = 5  (divide by 2)
10 >> 2 = 2  (divide by 4)
  1010 >> 1 = 0101

Use: Divide by powers of 2, extract bits
```

### Common Bit Tricks

#### Check if i-th bit is set
```python
def is_bit_set(num, i):
    return (num & (1 << i)) != 0

# Or
def is_bit_set(num, i):
    return (num >> i) & 1 == 1
```

#### Set i-th bit
```python
def set_bit(num, i):
    return num | (1 << i)
```

#### Clear i-th bit
```python
def clear_bit(num, i):
    mask = ~(1 << i)
    return num & mask
```

#### Toggle i-th bit
```python
def toggle_bit(num, i):
    return num ^ (1 << i)
```

#### Clear lowest set bit
```python
def clear_lowest_bit(num):
    return num & (num - 1)

# Example: 12 = 1100
# 12 - 1 = 11 = 1011
# 12 & 11 = 1000 (lowest 1 cleared)
```

#### Check if power of 2
```python
def is_power_of_2(num):
    return num > 0 and (num & (num - 1)) == 0

# Power of 2 has exactly one bit set
# 8 = 1000, 8-1 = 0111, 8 & 7 = 0 ✓
# 7 = 0111, 7-1 = 0110, 7 & 6 = 0110 ≠ 0 ✗
```

#### Get lowest set bit
```python
def lowest_bit(num):
    return num & -num

# -num in two's complement: ~num + 1
# Example: 12 = 1100, -12 = 0100
# 12 & -12 = 0100 (lowest bit isolated)
```

#### Count trailing zeros
```python
def trailing_zeros(num):
    count = 0
    while num > 0 and (num & 1) == 0:
        count += 1
        num >>= 1
    return count

# Or: use num & -num and count position
```

## Code Templates

### Template 1: Single Number (XOR Cancellation)
```python
def singleNumber(nums: List[int]) -> int:
    """Find single element using XOR cancellation."""
    result = 0
    for num in nums:
        result ^= num
    return result
```

### Template 2: Count Bits (Brian Kernighan)
```python
def countBits(n: int) -> int:
    """Count number of 1 bits."""
    count = 0
    while n:
        n &= n - 1  # Clear lowest set bit
        count += 1
    return count
```

### Template 3: Counting Bits (DP)
```python
def countingBits(n: int) -> List[int]:
    """Count bits for 0 to n using DP."""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### Template 4: Reverse Bits
```python
def reverseBits(n: int) -> int:
    """Reverse bits of 32-bit integer."""
    result = 0
    for i in range(32):
        result <<= 1          # Make room for next bit
        result |= (n & 1)     # Add rightmost bit of n
        n >>= 1               # Move to next bit
    return result
```

### Template 5: Missing Number (XOR)
```python
def missingNumber(nums: List[int]) -> int:
    """Find missing number using XOR."""
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

### Template 6: Add Without Operators
```python
def getSum(a: int, b: int) -> int:
    """Add two integers without + or -."""
    # Mask for 32-bit integer
    mask = 0xFFFFFFFF

    while b != 0:
        # Calculate sum and carry
        sum_without_carry = (a ^ b) & mask
        carry = ((a & b) << 1) & mask

        a = sum_without_carry
        b = carry

    # Handle negative numbers (Python specific)
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
```

### Template 7: Reverse Integer
```python
def reverseInteger(x: int) -> int:
    """Reverse integer with overflow check."""
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    result = 0
    sign = 1 if x > 0 else -1
    x = abs(x)

    while x != 0:
        digit = x % 10
        x //= 10

        # Check overflow before updating
        if result > INT_MAX // 10:
            return 0

        result = result * 10 + digit

    result *= sign

    if result < INT_MIN or result > INT_MAX:
        return 0

    return result
```

## Visual Examples

### XOR Cancellation
```
Find single number in [4, 1, 2, 1, 2]:

  0000 (start)
^ 0100 (4)
-------
  0100

^ 0001 (1)
-------
  0101

^ 0010 (2)
-------
  0111

^ 0001 (1)  ← cancels with previous 1
-------
  0110

^ 0010 (2)  ← cancels with previous 2
-------
  0100 (4) ← only unpaired element remains
```

### Count Bits (Brian Kernighan)
```
Count bits in 13 = 1101:

n = 1101
n-1 = 1100
n & (n-1) = 1100 (count = 1)

n = 1100
n-1 = 1011
n & (n-1) = 1000 (count = 2)

n = 1000
n-1 = 0111
n & (n-1) = 0000 (count = 3)

Result: 3 bits
```

### Counting Bits DP
```
i:     0  1  2  3  4  5  6  7  8
bin:   0  1 10 11 100 101 110 111 1000
bits:  0  1  1  2  1  2  2  3  1

Pattern: dp[i] = dp[i>>1] + (i&1)

i=5: 101
i>>1 = 2: 10 (has 1 bit)
i&1 = 1: last bit is 1
dp[5] = dp[2] + 1 = 1 + 1 = 2 ✓
```

### Reverse Bits
```
Input:  00000010100101000001111010011100
        ↓ Extract bits from right

Step by step:
result = 0
Bit 0: 0 → result = 0
Bit 1: 0 → result = 00
Bit 2: 1 → result = 001
...
After 32 bits:
Output: 00111001011110000010100101000000
```

### Add Without Operators
```
Add 5 + 3:

Step 1:
a = 5 = 0101
b = 3 = 0011

sum = a ^ b = 0110 (6)
carry = (a & b) << 1 = (0001) << 1 = 0010 (2)

Step 2:
a = 6 = 0110
b = 2 = 0010

sum = a ^ b = 0100 (4)
carry = (a & b) << 1 = (0010) << 1 = 0100 (4)

Step 3:
a = 4 = 0100
b = 4 = 0100

sum = a ^ b = 0000 (0)
carry = (a & b) << 1 = (0100) << 1 = 1000 (8)

Step 4:
a = 0 = 0000
b = 8 = 1000

sum = a ^ b = 1000 (8)
carry = (a & b) << 1 = 0000 (0)

Done: Result = 8 ✓
```

## Time & Space Complexity Patterns

| Problem | Time | Space | Key Operation |
|---------|------|-------|---------------|
| Single Number | O(n) | O(1) | XOR all elements |
| Number of 1 Bits | O(log n) | O(1) | Clear bits iteratively |
| Counting Bits | O(n) | O(n) | DP with bit shift |
| Reverse Bits | O(1) | O(1) | Fixed 32 iterations |
| Missing Number | O(n) | O(1) | XOR cancellation |
| Sum of Two Integers | O(1) | O(1) | At most 32 iterations |
| Reverse Integer | O(log n) | O(1) | Process each digit |

## Common Pitfalls

### 1. Signed vs Unsigned
```python
# ❌ Python's arbitrary precision can cause issues
n = -1
n >> 1  # May not work as expected for negative

# ✓ Use mask for unsigned behavior
n = n & 0xFFFFFFFF
```

### 2. Infinite Loops in Sum
```python
# ❌ In Python, negative numbers need special handling
while b != 0:
    carry = (a & b) << 1
    a = a ^ b
    b = carry  # Can be infinitely negative in Python!

# ✓ Use mask
mask = 0xFFFFFFFF
while b != 0:
    a, b = (a ^ b) & mask, ((a & b) << 1) & mask
```

### 3. Overflow in Reverse Integer
```python
# ❌ Check after overflow
result = result * 10 + digit
if result > INT_MAX:
    return 0  # Too late!

# ✓ Check before
if result > INT_MAX // 10:
    return 0
result = result * 10 + digit
```

### 4. Wrong Bit Position
```python
# ❌ Off by one
mask = 1 << i
if num & mask:  # Checking bit i+1 if not careful

# ✓ Clear understanding
mask = 1 << i  # This creates: 0...010...0 (1 at position i)
```

## Interview Tips

### Understanding Requirements
1. Are negative numbers involved?
2. What's the integer size? (32-bit, 64-bit)
3. Is overflow a concern?
4. Can I use arithmetic operators?

### Problem-Solving Approach
1. **Write out examples in binary**
2. **Identify patterns** (XOR cancellation, bit counting)
3. **Consider bit properties** (position, value)
4. **Think about edge cases** (0, negative, MAX_INT)

### Communication
- Explain binary representation first
- Walk through bit-by-bit operations
- Mention why bit manipulation is efficient
- Discuss overflow and edge cases

## Practice Progression

### Mastery Path
1. **Single Number**: Learn XOR properties
2. **Number of 1 Bits**: Master bit counting
3. **Counting Bits**: Combine DP with bits
4. **Reverse Bits**: Bit extraction practice
5. **Missing Number**: Apply XOR cancellation
6. **Sum of Integers**: Understand full adder
7. **Reverse Integer**: Handle overflow

### Related Topics
- Two's complement representation
- Bitwise DP problems
- Bit masking in backtracking
- Gray code
- Hamming distance

## Debugging Strategies

### Visualize Bits
```python
def debug_bits(n):
    print(f"{n} = {bin(n)} = {n:032b}")

# Use this to see what's happening
debug_bits(5)   # 5 = 0b101 = 00000000000000000000000000000101
debug_bits(-5)  # Show two's complement
```

### Trace Operations
```python
def trace_xor(nums):
    result = 0
    print(f"Start: {result:08b}")
    for num in nums:
        result ^= num
        print(f"^ {num:08b} = {result:08b}")
    return result
```

### Test Edge Cases
```python
# Always test:
- Zero
- One
- Negative numbers
- MAX_INT and MIN_INT
- All ones (111...1)
- Powers of 2
```

## Key Takeaways

1. **XOR is powerful** for cancellation and difference detection
2. **n & (n-1)** clears the lowest set bit (Brian Kernighan's trick)
3. **Bit shifts** are fast multiplication/division by powers of 2
4. **Masks** help extract and manipulate specific bits
5. **Two's complement** is how negative numbers are represented
6. **DP + bit manipulation** creates elegant solutions
7. **Overflow** must be checked proactively
8. **Binary thinking** leads to O(1) space solutions

## Further Reading

- "Hacker's Delight" by Henry S. Warren
- "Bit Twiddling Hacks" (Stanford)
- Computer Architecture textbooks
- Bitwise operators in different languages
- Hardware-level operations (ALU design)
