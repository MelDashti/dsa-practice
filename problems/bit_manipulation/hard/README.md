# Bit Manipulation - Hard

## Overview
Hard bit manipulation problems combine advanced bitwise operations with complex algorithms and data structures. These problems often require deep mathematical insights, efficient state representation, and creative applications of bit-level operations to achieve optimal time and space complexity.

## Key Concepts

### 1. Advanced Bitmask Techniques
- Submask enumeration: O(3^n) iteration over all submasks
- Subset Sum Over Subsets (SOS) DP
- Meet-in-the-middle with bitmasks
- Inclusion-Exclusion with bits

### 2. Bit-Level Data Structures
- Bitwise trie with lazy propagation
- Persistent bit vectors
- Binary indexed tree (BIT) with XOR
- Sparse table with bitwise operations

### 3. Number Theory with Bits
- Fast exponentiation with bits
- Computing GCD using bitwise operations
- Prime factorization tricks
- Modular arithmetic optimization

### 4. Advanced XOR Problems
- XOR basis and linear algebra
- Maximum XOR subset
- XOR linked list
- Gaussian elimination with XOR

## Complex Problem Patterns

### 1. Submask Enumeration
Iterate over all submasks of a mask:
```python
def enumerate_submasks(mask):
    """Iterate all submasks in O(3^n) total."""
    submask = mask
    while True:
        # Process submask
        process(submask)

        # Move to next submask
        submask = (submask - 1) & mask
        if submask == mask:
            break
```

### 2. SOS (Sum Over Subsets) DP
```python
def sos_dp(arr):
    """
    For each mask, compute sum of arr[submask] for all submasks.
    Time: O(n * 2^n) instead of O(3^n)
    """
    n = len(bin(len(arr))) - 2
    dp = arr[:]

    for i in range(n):
        for mask in range(1 << n):
            if mask & (1 << i):
                dp[mask] += dp[mask ^ (1 << i)]

    return dp
```

### 3. XOR Basis
Find linearly independent set of XORs:
```python
def xor_basis(nums):
    """Find XOR basis of numbers."""
    basis = []

    for num in nums:
        cur = num
        for b in basis:
            cur = min(cur, cur ^ b)

        if cur != 0:
            basis.append(cur)
            basis.sort(reverse=True)

    return basis
```

### 4. Meet in the Middle
```python
def meet_in_middle(nums, target):
    """
    Find subset with sum = target.
    Time: O(2^(n/2)) instead of O(2^n)
    """
    n = len(nums)
    mid = n // 2

    # Generate all subsets of first half
    first_half = {}
    for mask in range(1 << mid):
        subset_sum = sum(nums[i] for i in range(mid) if mask & (1 << i))
        first_half[subset_sum] = mask

    # Check all subsets of second half
    for mask in range(1 << (n - mid)):
        subset_sum = sum(nums[mid + i] for i in range(n - mid) if mask & (1 << i))
        if target - subset_sum in first_half:
            return True

    return False
```

## Hard LeetCode Problems

### Concatenated Words (LC 472)
Find words formed by concatenating other words using trie + bitmask.

### Maximum Students Taking Exam (LC 1349)
Bitmask DP for valid seating arrangements.

### Minimum Cost to Connect Two Groups (LC 1595)
Bitmask DP with state compression.

### Find Array Given Subset Sums (LC 1982)
Reverse engineering array from subset sums.

### Smallest Sufficient Team (LC 1125)
Minimum people to cover all skills using bitmask DP.

## Advanced Patterns

### 1. Parallel Bit Operations
Process multiple bits simultaneously:
```python
def parallel_count_bits(n):
    """Count bits using parallel computation."""
    # Count pairs
    n = (n & 0x55555555) + ((n >> 1) & 0x55555555)
    # Count nibbles
    n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
    # Count bytes
    n = (n & 0x0F0F0F0F) + ((n >> 4) & 0x0F0F0F0F)
    # Count all
    n = (n & 0x00FF00FF) + ((n >> 8) & 0x00FF00FF)
    n = (n & 0x0000FFFF) + ((n >> 16) & 0x0000FFFF)
    return n
```

### 2. Bitwise Convolution
```python
def xor_convolution(a, b):
    """
    Compute c[k] = sum(a[i] * b[j]) for all i XOR j = k.
    Uses Fast Walsh-Hadamard Transform.
    Time: O(n log n) where n = 2^k
    """
    def fwht(arr):
        n = len(arr)
        h = 1
        while h < n:
            for i in range(0, n, h * 2):
                for j in range(i, i + h):
                    x, y = arr[j], arr[j + h]
                    arr[j], arr[j + h] = x + y, x - y
            h *= 2
        return arr

    n = max(len(a), len(b))
    n = 1 << (n - 1).bit_length()

    a += [0] * (n - len(a))
    b += [0] * (n - len(b))

    a = fwht(a[:])
    b = fwht(b[:])
    c = [a[i] * b[i] for i in range(n)]
    c = fwht(c)

    return [x // n for x in c]
```

### 3. Gray Code Generation
```python
def gray_code(n):
    """Generate n-bit Gray code."""
    result = []
    for i in range(1 << n):
        # Gray code: i XOR (i >> 1)
        result.append(i ^ (i >> 1))
    return result
```

### 4. Bit Tricks for Optimization

#### Isolate rightmost 1-bit
```python
rightmost_one = n & -n
```

#### Isolate rightmost 0-bit
```python
rightmost_zero = ~n & (n + 1)
```

#### Turn off rightmost contiguous 1s
```python
result = n & (n + 1)
```

#### Create mask of trailing zeros
```python
mask = (n & -n) - 1
```

## Complexity Analysis

### Time Complexities
| Technique | Complexity | Use Case |
|-----------|-----------|----------|
| Bitmask DP | O(2^n × n) | Small n (≤ 20) |
| Submask Enumeration | O(3^n) | Iterate submasks |
| SOS DP | O(n × 2^n) | Sum over subsets |
| Meet in Middle | O(2^(n/2)) | Double size limit |
| XOR Basis | O(n × log(max)) | Linear independence |
| Bitwise Trie | O(n × 32) | Maximum XOR queries |

### Space Optimization
- Use rolling array for DP
- Compress states with bitmasks
- Implicit graphs (generate states on-demand)
- Bidirectional search

## Problem-Solving Strategies

### Recognition Patterns
1. **Small n (≤ 20)**: Consider bitmask DP
2. **XOR operations**: Think about XOR basis or trie
3. **Subset problems**: SOS DP or meet-in-middle
4. **State representation**: Use bits for boolean flags
5. **Range operations**: Bit-level parallelism

### Implementation Tips
```python
# Always handle edge cases
if n == 0:
    return base_case

# Use meaningful variable names
used_mask = 0
available_mask = (1 << n) - 1

# Comment bit operations
# Check if i-th bit is set
if mask & (1 << i):
    ...

# Set i-th bit
mask |= (1 << i)

# Clear i-th bit
mask &= ~(1 << i)
```

## Advanced Interview Topics

### Discussion Points
1. **Space-time tradeoffs** in bitmask DP
2. **Why XOR** forms a vector space
3. **Gray code applications** in hardware
4. **Bit parallelism** in modern processors
5. **Cache efficiency** of bit operations

### Follow-up Questions
- Can you optimize space from O(2^n) to O(2^(n-1))?
- How would you parallelize this algorithm?
- What if n is 40? (meet-in-middle)
- Can you use XOR basis to reduce problem size?
- How does this relate to linear algebra?

## Mathematical Foundations

### XOR as Vector Space
- XOR is addition in GF(2)
- Associative and commutative
- Each element is its own inverse
- Basis exists (linearly independent set)

### Gray Code Properties
- Consecutive codes differ by 1 bit
- Useful in error correction
- Hardware state transitions
- Combinatorial generation

### Walsh-Hadamard Transform
- Fast transform for XOR convolution
- Similar to FFT but for XOR
- Applications in coding theory
- Quantum computing connections

## Optimization Techniques

### 1. Precomputation
```python
# Precompute all subset sums
subset_sums = [0] * (1 << n)
for mask in range(1 << n):
    subset_sums[mask] = sum(nums[i] for i in range(n) if mask & (1 << i))
```

### 2. Pruning
```python
# Skip invalid states early
if not is_valid_state(mask):
    continue
```

### 3. Memoization
```python
@lru_cache(maxsize=None)
def dp(mask, index):
    # Recursive DP with memoization
    ...
```

### 4. Bottom-Up Optimization
```python
# Iterate in optimal order
for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            # Current state depends on previous
            dp[mask] = min(dp[mask], dp[mask ^ (1 << i)] + cost[i])
```

## Debugging Hard Problems

### Visualization
```python
def print_mask(mask, n):
    """Visualize bitmask."""
    return ''.join('1' if mask & (1 << i) else '0' for i in range(n-1, -1, -1))

def print_dp_table(dp, n):
    """Visualize DP table."""
    for mask in range(1 << n):
        print(f"{print_mask(mask, n)}: {dp[mask]}")
```

### Testing Strategy
```python
# Test small cases exhaustively
for n in range(1, 6):
    test_all_masks(n)

# Verify properties
assert all(check_submask(mask, submask) for submask in enumerate_submasks(mask))

# Compare with brute force
assert optimized_solution(input) == brute_force(input)
```

## Real-World Applications

### 1. Network Routing
- Shortest path with state (TSP variant)
- Switch configuration optimization
- Packet filtering with bitmasks

### 2. Resource Allocation
- Task assignment with constraints
- Scheduling with dependencies
- Team formation problems

### 3. Cryptography
- XOR-based encryption
- Error detection codes
- Hash function optimization

### 4. Database Systems
- Bitmap indexes
- Query optimization
- Set operations

## Key Takeaways

1. **Bitmask DP** reduces exponential space with clever state encoding
2. **SOS DP** improves O(3^n) to O(n × 2^n)
3. **Meet-in-middle** extends feasible n from 20 to 40
4. **XOR basis** provides linear algebra tools for XOR problems
5. **Bit tricks** can optimize constants significantly
6. **Gray code** minimizes state transitions
7. **Walsh-Hadamard** enables fast XOR convolution

## Further Study

### Books
- "Hacker's Delight" by Henry Warren
- "Concrete Mathematics" by Knuth, Graham, Patashnik
- "The Art of Computer Programming" Volume 4

### Topics
- Fast Walsh-Hadamard Transform
- Linear algebra over GF(2)
- Gaussian elimination for XOR systems
- Advanced DP optimization techniques
- Complexity theory and bitmask algorithms

### Practice Resources
- Codeforces: Bitmask problems
- AtCoder: Bitmask DP contests
- CSES Problem Set: Advanced section
- LeetCode: Hard bit manipulation

## Conclusion

Hard bit manipulation problems require:
- **Deep understanding** of binary representation
- **Mathematical maturity** for proofs and analysis
- **Creative thinking** to spot bit-based solutions
- **Implementation skill** to avoid bugs
- **Optimization mindset** for constant-factor improvements

Master these concepts through deliberate practice, and you'll develop the intuition to recognize when bit manipulation provides elegant solutions to seemingly complex problems.
