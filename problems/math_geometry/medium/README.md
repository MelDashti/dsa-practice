# Math & Geometry - Medium

## Overview
Medium math and geometry problems involve matrix manipulations, advanced algorithms (like fast exponentiation), and 2D geometry transformations. These problems require understanding of both mathematical principles and efficient algorithmic implementations.

## Key Concepts

### 1. Matrix Operations
- **In-place Rotation**: Transforming matrix without extra space
- **Layer-by-layer Processing**: Working from outside to inside
- **Transpose + Reverse**: Alternative rotation method
- **Matrix Traversal Patterns**: Row, column, spiral, diagonal

### 2. Mathematical Algorithms
- **Fast Exponentiation**: Computing x^n in O(log n) time
- **Bit Manipulation for Math**: Using binary representation
- **Overflow Handling**: Especially important for exponentiation
- **Sign Handling**: Negative bases and exponents

### 3. Space Optimization
- **In-place Algorithms**: O(1) space instead of O(n²)
- **Sentinel Values**: Using special markers for state
- **Bit Flags**: Compact state representation
- **Two-Pass vs One-Pass**: Trade-offs

### 4. 2D Geometry
- **Coordinate Transformations**: Rotation, reflection, translation
- **Boundary Handling**: Edge and corner cases in matrices
- **Pattern Recognition**: Identifying geometric patterns

## Problems in This Section

### Rotate Image (LC 48)
**Problem**: Rotate n×n matrix 90 degrees clockwise in-place.

**Key Insights**:
- **Approach 1**: Transpose + Reverse each row
  - Transpose: `matrix[i][j] ↔ matrix[j][i]`
  - Reverse: `reverse each row`
- **Approach 2**: Rotate layer by layer
  - Process from outermost to innermost layer
  - Rotate 4 elements at a time in a cycle

**Mathematical Foundation**:
```
90° clockwise rotation:
(i, j) → (j, n-1-i)

Transpose:
(i, j) → (j, i)

Reverse rows:
(i, j) → (i, n-1-j)

Combined: (i, j) → (j, i) → (j, n-1-i) ✓
```

**Complexity**:
- Time: O(n²) - must touch every element
- Space: O(1) - in-place rotation

**Pattern**: Matrix Manipulation + Layer Processing

---

### Spiral Matrix (LC 54)
**Problem**: Return elements of matrix in spiral order.

**Key Insights**:
- Process matrix layer by layer (outside to inside)
- Four directions: right → down → left → up
- Track boundaries: top, bottom, left, right
- Shrink boundaries after each direction
- Handle single row/column edge cases

**Approach**:
```python
# Initialize boundaries
# While boundaries valid:
#   - Traverse right (top row)
#   - Traverse down (right column)
#   - Traverse left (bottom row) if still valid
#   - Traverse up (left column) if still valid
#   - Shrink boundaries
# Time: O(m×n), Space: O(1) excluding output
```

**Pattern**: Boundary Simulation + Direction Control

---

### Set Matrix Zeroes (LC 73)
**Problem**: If element is 0, set entire row and column to 0. Do it in-place.

**Key Insights**:
- **Naive**: O(m×n) space - use extra matrix
- **Better**: O(m+n) space - track zero rows and columns
- **Optimal**: O(1) space - use first row/column as markers
  - Use first row to mark zero columns
  - Use first column to mark zero rows
  - Need separate flag for first row/column themselves

**Approach (O(1) space)**:
```python
1. Check if first row/column have zeros
2. Use first row/column as markers for other rows/columns
3. Set zeros based on markers (skip first row/column)
4. Set first row/column to zero if they had zeros
# Time: O(m×n), Space: O(1)
```

**Pattern**: In-place Marking + Two-Pass Algorithm

---

### Pow(x, n) (LC 50)
**Problem**: Implement pow(x, n) - calculate x raised to power n.

**Key Insights**:
- **Naive**: O(n) - multiply x by itself n times (too slow)
- **Fast Exponentiation**: O(log n) - use binary exponentiation
  - x^8 = (x^4)^2 = ((x^2)^2)^2
  - If n is odd: x^n = x × x^(n-1)
  - If n is even: x^n = (x^(n/2))^2

**Edge Cases**:
- Negative exponent: x^(-n) = 1 / x^n
- Zero base: 0^n = 0 (except 0^0)
- Zero exponent: x^0 = 1
- Negative base with even/odd exponent

**Complexity**:
- Time: O(log n)
- Space: O(1) iterative, O(log n) recursive

**Pattern**: Divide and Conquer + Bit Manipulation

---

## Detailed Problem Analysis

### Rotate Image - Deep Dive

#### Approach 1: Transpose + Reverse
```python
def rotate(matrix):
    n = len(matrix)

    # Step 1: Transpose (flip along main diagonal)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
```

**Visualization**:
```
Original:          Transpose:         Reverse rows:
[1, 2, 3]         [1, 4, 7]          [7, 4, 1]
[4, 5, 6]    →    [2, 5, 8]    →     [8, 5, 2]
[7, 8, 9]         [3, 6, 9]          [9, 6, 3]
```

#### Approach 2: Layer-by-Layer Rotation
```python
def rotate_layers(matrix):
    n = len(matrix)

    for layer in range(n // 2):
        first, last = layer, n - 1 - layer

        for i in range(first, last):
            offset = i - first

            # Save top
            top = matrix[first][i]

            # left → top
            matrix[first][i] = matrix[last-offset][first]

            # bottom → left
            matrix[last-offset][first] = matrix[last][last-offset]

            # right → bottom
            matrix[last][last-offset] = matrix[i][last]

            # top → right
            matrix[i][last] = top
```

**Visualization of 4-element cycle**:
```
Layer 0:
  top    (0,0) → (0,1) → (0,2)
         ↑                  ↓
  left (1,0)              (1,2) right
         ↑                  ↓
bottom (2,0) ← (2,1) ← (2,2)

Rotate cycle:
top → right → bottom → left → top
```

---

### Spiral Matrix - Deep Dive

#### Step-by-Step Simulation
```python
def spiralOrder(matrix):
    if not matrix:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Move right along top row
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Move down along right column
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Move left along bottom row (if still valid)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Move up along left column (if still valid)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result
```

**Visualization**:
```
Matrix:
 1  2  3  4
 5  6  7  8
 9 10 11 12

Step 1: Right (top=0)
→ → → →
1  2  3  4

Step 2: Down (right=3)
           ↓
        8  ↓
       12  ↓

Step 3: Left (bottom=2)
← ← ←
9 10 11

Step 4: Up (left=0)
↑
5
↑

Step 5: Right (top=1)
→ →
6  7

Result: [1,2,3,4,8,12,11,10,9,5,6,7]
```

---

### Set Matrix Zeroes - Deep Dive

#### O(1) Space Solution
```python
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])

    # Check if first row has zero
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))

    # Check if first column has zero
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))

    # Use first row and column as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0  # Mark row
                matrix[0][j] = 0  # Mark column

    # Set zeros based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Handle first row
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0

    # Handle first column
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0
```

**Why this works**:
```
Original matrix with zeros marked:
[1, 1, 1]
[1, 0, 1]  ← Zero found at (1,1)
[1, 1, 1]

After marking (use first row/col):
[1, 0, 1]  ← Marked column 1
     ↑
[0, 0, 1]  ← Marked row 1
[1, 1, 1]

After setting zeros:
[1, 0, 1]
[0, 0, 0]
[1, 0, 1]
```

---

### Pow(x, n) - Deep Dive

#### Fast Exponentiation (Iterative)
```python
def myPow(x, n):
    if n < 0:
        x = 1 / x
        n = -n

    result = 1
    current_product = x

    while n > 0:
        if n % 2 == 1:  # Odd exponent
            result *= current_product

        current_product *= current_product  # Square the base
        n //= 2

    return result
```

**How it works**:
```
Example: 2^10

Binary representation of 10: 1010

10 = 8 + 2 = 2^3 + 2^1

So: 2^10 = 2^8 × 2^2

Step-by-step:
n=10 (1010):  result=1,    current=2
n=5  (101):   result=1,    current=4      (n is even, square base)
n=5  (101):   result=1,    current=4      (n is odd, use current)
n=2  (10):    result=4,    current=16     (square base)
n=1  (1):     result=4,    current=256    (n is even, square base)
n=1  (1):     result=4,    current=256    (n is odd, use current)
n=0:          result=1024, done

Result: 2^10 = 1024
```

#### Fast Exponentiation (Recursive)
```python
def myPow_recursive(x, n):
    if n == 0:
        return 1
    if n < 0:
        return 1 / myPow_recursive(x, -n)

    if n % 2 == 0:  # Even
        half = myPow_recursive(x, n // 2)
        return half * half
    else:  # Odd
        return x * myPow_recursive(x, n - 1)
```

**Recursion tree for 2^10**:
```
                2^10
               /    \
           2^5 × 2^5
           /  \
       2×2^4  (expand one side)
          /  \
      2^2×2^2
       / \
    2^1×2^1
```

## Advanced Techniques

### 1. Matrix Rotation Formulas
```python
# 90° clockwise:  (i,j) → (j, n-1-i)
# 90° counter:    (i,j) → (n-1-j, i)
# 180°:           (i,j) → (n-1-i, n-1-j)
# 270° clockwise: (i,j) → (n-1-j, i)
```

### 2. Spiral Traversal Variations
```python
# Spiral from outside-in (given above)
# Spiral from inside-out (reverse)
# Zigzag traversal
# Diagonal traversal
```

### 3. Binary Exponentiation Properties
```python
# a^(b+c) = a^b × a^c
# (a^b)^c = a^(b×c)
# (a×b)^c = a^c × b^c

# For modular arithmetic:
# (a^b) % m = ((a % m)^b) % m
```

### 4. Space Optimization Patterns
```python
# Use existing space as markers
# Two-pass algorithms to avoid conflicts
# Bit manipulation for flags
# Coordinate compression
```

## Complexity Analysis Summary

| Problem | Time | Space | Optimization Key |
|---------|------|-------|------------------|
| Rotate Image | O(n²) | O(1) | In-place swap |
| Spiral Matrix | O(m×n) | O(1)* | Boundary tracking |
| Set Matrix Zeroes | O(m×n) | O(1) | First row/col as markers |
| Pow(x, n) | O(log n) | O(1) | Binary exponentiation |

*O(1) excluding output array

## Common Pitfalls

### 1. Rotate Image
```python
# ❌ Wrong: Not truly in-place
rotated = [[matrix[n-1-j][i] for j in range(n)] for i in range(n)]
matrix[:] = rotated

# ✓ Correct: In-place with transpose + reverse
for i in range(n):
    for j in range(i+1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
for i in range(n):
    matrix[i].reverse()
```

### 2. Spiral Matrix
```python
# ❌ Wrong: Missing boundary checks
if top <= bottom:  # Need this check!
    for col in range(right, left-1, -1):
        result.append(matrix[bottom][col])

# Edge case: single row or column
```

### 3. Set Matrix Zeroes
```python
# ❌ Wrong: Setting zeros while scanning
for i in range(m):
    for j in range(n):
        if matrix[i][j] == 0:
            set_row_zero(i)  # Affects future scans!
            set_col_zero(j)

# ✓ Correct: Mark first, then set
```

### 4. Pow(x, n)
```python
# ❌ Wrong: Integer overflow (in some languages)
result = 1
for _ in range(n):
    result *= x  # Can overflow

# ❌ Wrong: Not handling negative exponents
if n < 0:
    return -myPow(x, -n)  # Should be 1/myPow, not negative

# ✓ Correct: Binary exponentiation + proper negatives
```

## Interview Tips

### Problem-Solving Framework
1. **Clarify Requirements**:
   - Matrix dimensions (square? rectangular?)
   - In-place or extra space allowed?
   - Input constraints (overflow possible?)

2. **Start Simple**:
   - Solve for small examples (2×2, 3×3)
   - Identify pattern
   - Generalize to n×n

3. **Optimize Iteratively**:
   - Brute force → Optimized space → Optimized time
   - Consider trade-offs

4. **Test Edge Cases**:
   - Empty matrix
   - 1×1 matrix
   - Single row/column
   - All zeros (for Set Matrix Zeroes)
   - Negative numbers (for Pow)

### Communication
```python
# Good interview response structure:
1. "Let me clarify the requirements..."
2. "I'll start with a simple approach..."
3. "The time complexity is... because..."
4. "I can optimize this by..."
5. "Let me trace through an example..."
6. "Edge cases to consider are..."
```

## Code Templates

### Matrix Rotation Template
```python
def rotate90clockwise(matrix):
    """Rotate n×n matrix 90° clockwise in-place."""
    n = len(matrix)

    # Transpose
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
```

### Spiral Traversal Template
```python
def spiral_order(matrix):
    """Return elements in spiral order."""
    if not matrix or not matrix[0]:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Down
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Left (check bounds)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Up (check bounds)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result
```

### Fast Exponentiation Template
```python
def fast_pow(x, n):
    """Calculate x^n in O(log n) time."""
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n

    result = 1
    current = x

    while n > 0:
        if n % 2 == 1:
            result *= current
        current *= current
        n //= 2

    return result
```

## Practice Strategy

### Progression
1. **Rotate Image**: Master in-place matrix operations
2. **Spiral Matrix**: Learn boundary management
3. **Set Matrix Zeroes**: Understand space optimization
4. **Pow(x, n)**: Study divide-and-conquer

### Related Problems
- Spiral Matrix II (generation instead of traversal)
- Rotate Array
- Matrix Diagonal Sum
- Implement Sqrt(x) (similar binary search/math)

## Key Takeaways

1. **Matrix problems** often benefit from in-place algorithms
2. **Transpose operations** are fundamental for rotations
3. **Boundary tracking** is crucial for traversal problems
4. **First row/column** can serve as auxiliary space
5. **Binary exponentiation** reduces O(n) to O(log n)
6. **Two-pass algorithms** prevent conflicts in in-place operations
