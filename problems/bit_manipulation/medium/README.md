# Bit Manipulation - Medium

## Overview
Medium bit manipulation problems involve more complex patterns, multiple bit operations combined, and often integrate with other data structures or algorithms. These problems require deeper understanding of binary representations and creative application of bitwise operations.

## Key Concepts

### 1. Bit Masking
- Creating and applying masks for specific bit patterns
- Extracting ranges of bits
- Setting/clearing multiple bits at once
- Using masks for state representation

### 2. Advanced XOR Patterns
- Finding two unique numbers
- Finding three unique numbers
- XOR with prefix/suffix combinations
- Bitwise trie structures

### 3. Bit DP and State Compression
- Using bitmasks to represent states
- Traveling Salesman Problem (TSP)
- Subset enumeration
- Assignment problems

### 4. Mathematical Properties
- Modular arithmetic with bits
- Prime number operations
- Greatest common divisor (GCD) with bits
- Fast multiplication/division

## Common Medium Problems

### Single Number II (LC 137)
Find the element appearing once when others appear three times.

### Single Number III (LC 260)
Find two elements appearing once when others appear twice.

### Bitwise AND of Numbers Range (LC 201)
Find bitwise AND of all numbers in range [m, n].

### Maximum XOR of Two Numbers (LC 421)
Find maximum XOR of two numbers in an array.

### UTF-8 Validation (LC 393)
Validate if data represents valid UTF-8 encoding.

## Patterns to Master

### 1. Finding Two Unique Numbers
When all others appear twice:
```python
def singleNumberIII(nums):
    # XOR all numbers - result is xor of two unique numbers
    xor = 0
    for num in nums:
        xor ^= num

    # Find rightmost set bit (where two numbers differ)
    rightmost_bit = xor & -xor

    # Partition numbers into two groups
    a, b = 0, 0
    for num in nums:
        if num & rightmost_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

### 2. Bitmask DP
```python
# Example: TSP or subset problems
dp = [float('inf')] * (1 << n)
dp[0] = 0

for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            prev_mask = mask ^ (1 << i)
            dp[mask] = min(dp[mask], dp[prev_mask] + cost[i])
```

### 3. Bitwise Trie
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = 0

def insert_trie(root, num):
    node = root
    for i in range(31, -1, -1):
        bit = (num >> i) & 1
        if bit not in node.children:
            node.children[bit] = TrieNode()
        node = node.children[bit]
    node.value = num
```

## Complexity Patterns

| Pattern | Time | Space | Use Case |
|---------|------|-------|----------|
| Bitmask DP | O(2^n × n) | O(2^n) | State compression |
| Bitwise Trie | O(n × 32) | O(n × 32) | Maximum XOR |
| Bit Grouping | O(n) | O(1) | Multiple unique numbers |
| Range AND | O(log n) | O(1) | Range operations |

## Practice Strategy

### Prerequisites
- Master all easy bit manipulation problems
- Understand XOR properties deeply
- Comfortable with binary representation
- Know basic DP concepts

### Progression
1. Single Number variations (II, III)
2. Bitwise operations on ranges
3. Bitmask DP problems
4. Bitwise trie problems

### Related Topics
- Dynamic Programming with bitmasks
- Trie data structures
- Number theory
- Computational geometry (XOR in coordinates)

## Interview Tips

### Key Questions to Ask
1. What's the range of numbers? (affects bit count)
2. Can numbers be negative?
3. Are there memory constraints? (affects DP approach)
4. What's the expected time complexity?

### Problem-Solving Framework
1. Identify if XOR properties apply
2. Consider grouping or partitioning numbers
3. Think about bit positions independently
4. Explore trie for maximum/minimum XOR
5. Consider bitmask for state representation

## Next Steps

After mastering medium problems:
- Explore hard bit manipulation challenges
- Study advanced number theory
- Learn about Gray codes and error correction
- Practice competitive programming bit tricks

## Additional Resources

- Competitive Programming 3: Section on Bitmasks
- "Hacker's Delight": Advanced bit tricks
- Codeforces: Bit manipulation tutorials
- LeetCode: Practice problems tagged "Bit Manipulation"
