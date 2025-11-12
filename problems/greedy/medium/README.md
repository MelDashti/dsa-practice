# Greedy - Medium

This folder contains medium-level Greedy algorithm problems. These problems require deeper insight into when and why greedy approaches work.

## Problems

### 1. Jump Game (LeetCode 55)
**File:** `jump_game.py`

**Description:** Given an array where each element represents max jump length from that position, determine if you can reach the last index.

**Key Concepts:**
- Track furthest reachable position
- Greedy: always try to reach as far as possible
- If current position > furthest, return false
- Update furthest at each step

**Time:** O(n) | **Space:** O(1)

**Pattern:** Greedy reachability

---

### 2. Jump Game II (LeetCode 45)
**File:** `jump_game_ii.py`

**Description:** Find minimum number of jumps to reach the last index (guaranteed reachable).

**Key Concepts:**
- Track current jump's reach and next jump's reach
- Increment jumps when reaching end of current range
- Greedy: within each jump, find furthest next position
- BFS-like level traversal

**Time:** O(n) | **Space:** O(1)

**Pattern:** Greedy jump optimization

---

### 3. Gas Station (LeetCode 134)
**File:** `gas_station.py`

**Description:** Given gas and cost arrays for circular route, find starting gas station to complete circuit (or -1 if impossible).

**Key Concepts:**
- If total gas < total cost, impossible
- Track running tank balance
- If tank goes negative at position i, start must be after i
- Greedy: reset start position when tank becomes negative
- Key insight: if solution exists, greedy choice finds it

**Time:** O(n) | **Space:** O(1)

**Pattern:** Greedy circular array

---

### 4. Hand of Straights (LeetCode 846)
**File:** `hand_of_straights.py`

**Description:** Determine if array can be divided into groups of consecutive cards of size groupSize.

**Key Concepts:**
- Sort and use frequency map
- Greedy: always try to form group starting with smallest available card
- For each card, try to form complete consecutive sequence
- Use counter/hashmap to track available cards

**Time:** O(n log n) | **Space:** O(n)

**Pattern:** Greedy grouping with sorting

---

### 5. Merge Triplets to Form Target (LeetCode 1899)
**File:** `merge_triplets.py`

**Description:** Given array of triplets and target triplet, determine if target can be formed by max-merging some triplets.

**Key Concepts:**
- Greedy: only consider triplets where no element exceeds target
- Track which target positions we've achieved
- A triplet is useful if all elements ≤ target and at least one equals target
- Check if we can achieve all three target values

**Time:** O(n) | **Space:** O(1)

**Pattern:** Greedy selection with constraints

---

### 6. Partition Labels (LeetCode 763)
**File:** `partition_labels.py`

**Description:** Partition string into as many parts as possible where each letter appears in at most one part.

**Key Concepts:**
- Find last occurrence of each character
- Greedy: extend current partition to include last occurrence of all chars seen
- When current position reaches partition end, finalize partition
- Two-pass: first get last positions, then partition

**Time:** O(n) | **Space:** O(1) - fixed alphabet size

**Pattern:** Greedy partitioning

---

### 7. Valid Parenthesis String (LeetCode 678)
**File:** `valid_parenthesis_string.py`

**Description:** Validate parenthesis string where '*' can be '(', ')', or empty.

**Key Concepts:**
- Track range of possible open parentheses count [min, max]
- '(': increment both min and max
- ')': decrement both min and max
- '*': decrement min, increment max (most flexible)
- min = max(0, min) to handle negatives
- Valid if max ≥ 0 throughout and min ≤ 0 at end

**Time:** O(n) | **Space:** O(1)

**Pattern:** Greedy range tracking

---

## Learning Path

### Level 1: Basic Greedy
1. **Jump Game** - Fundamental greedy reachability concept
2. **Gas Station** - Understanding when greedy finds optimal

### Level 2: Greedy with Data Structures
3. **Hand of Straights** - Greedy with sorting and counting
4. **Partition Labels** - Greedy with preprocessing

### Level 3: Greedy with Constraints
5. **Jump Game II** - Minimization with greedy
6. **Merge Triplets** - Greedy selection under constraints

### Level 4: Advanced Greedy
7. **Valid Parenthesis String** - Range-based greedy thinking

## Common Greedy Patterns

### 1. Reachability/Range Extension
**Problems:** Jump Game, Partition Labels
```python
furthest = 0
for i in range(len(arr)):
    if i > furthest:
        return False
    furthest = max(furthest, i + arr[i])
return True
```

### 2. Reset Point Strategy
**Problems:** Gas Station, Jump Game II
```python
# When condition fails, reset start point
if current_sum < 0:
    start = i + 1
    current_sum = 0
```

### 3. Greedy with Sorting
**Problems:** Hand of Straights
```python
# Sort first, then greedily process smallest elements
items.sort()
for item in items:
    # Greedy choice based on smallest available
```

### 4. Range Tracking
**Problems:** Valid Parenthesis String
```python
# Track min and max possible values
min_count, max_count = 0, 0
# Update ranges based on choices
```

### 5. Two-Pass Greedy
**Problems:** Partition Labels
```python
# Pass 1: Gather information (last positions)
# Pass 2: Make greedy decisions based on info
```

## Proving Greedy Correctness

### Framework for Proof:

1. **Greedy Choice Property**
   - Show that a greedy choice at each step is safe
   - Prove it doesn't prevent reaching optimal solution

2. **Optimal Substructure**
   - After greedy choice, remaining problem has same form
   - Optimal solution to original = greedy choice + optimal solution to subproblem

### Example: Gas Station

**Claim:** If we can't complete circuit starting at i, then we can't start at any station between start and i.

**Proof:**
- If we fail at position i starting from j, our tank went negative
- Starting from any k between j and i gives us less gas (we had positive balance reaching k from j)
- Therefore, we can skip all positions j to i

## Common Greedy Strategies

### 1. Always Pick Smallest/Largest
- Sort first, then process in order
- Example: Hand of Straights

### 2. Extend Until Forced to Stop
- Keep expanding range/window
- Stop when condition violated
- Example: Jump Game, Partition Labels

### 3. Track Best Alternative
- Maintain information about best choice seen
- Example: Jump Game II (track furthest in current level)

### 4. Reset on Failure
- When greedy choice fails, start fresh
- Example: Gas Station

### 5. Process by Constraint
- Handle most constrained elements first
- Example: Merge Triplets

## Time Complexity Patterns

- **O(n)**: Single pass or two-pass (Jump Game, Gas Station, Partition Labels)
- **O(n log n)**: Sorting required (Hand of Straights)
- **O(n)** with preprocessing: Two passes (Partition Labels)

## Space Complexity Patterns

- **O(1)**: Only track few variables (Jump Game, Gas Station)
- **O(n)**: Need hash map or counter (Hand of Straights)
- **O(26) = O(1)**: Fixed alphabet (Partition Labels)

## Common Mistakes

1. **Assuming greedy works without proof**
   - Not all optimization problems have greedy solutions
   - Always verify greedy choice property

2. **Incorrect greedy choice**
   - Choosing wrong local optimum
   - Example: In Gas Station, starting from highest gas is wrong

3. **Missing edge cases**
   - Empty arrays
   - Single elements
   - All elements same

4. **Not considering counterexamples**
   - Try to break your greedy approach
   - If you can, it's not correct

5. **Overcomplicating**
   - Greedy should be simple
   - If solution is complex, reconsider approach

## Greedy vs Other Approaches

| Approach | When to Use | Trade-offs |
|----------|-------------|------------|
| Greedy | Local optimum → global optimum | Fast but need proof |
| DP | Overlapping subproblems | Slower but more general |
| Backtracking | Need all solutions | Can be exponential |
| Divide & Conquer | Problem splits nicely | Often O(n log n) |

## Interview Strategies

### Recognizing Greedy Problems

Look for:
1. **Optimization** - maximize/minimize something
2. **Simple decision** - at each step, obvious choice
3. **No backtracking** - don't need to reconsider
4. **Linear/sorted processing** - natural order

### Explaining Your Approach

1. **State the greedy choice** - "At each step, I..."
2. **Explain why it works** - "This is safe because..."
3. **Handle edge cases** - "When X happens, I..."
4. **Analyze complexity** - "This runs in O(n) because..."

### If Greedy Doesn't Work

Signs greedy might be wrong:
- Can construct counterexample
- Need to reconsider previous choices
- Multiple competing greedy strategies

Try:
- Dynamic Programming
- Graph algorithms (BFS/DFS)
- Backtracking

## Debugging Greedy Solutions

1. **Test small cases by hand** - Verify logic
2. **Check edge cases** - Empty, single element, all same
3. **Try counterexamples** - Can you break it?
4. **Compare with brute force** - On small inputs
5. **Verify invariants** - What should be true at each step?

## Real-World Applications

- **Jump Games**: Network routing, game AI
- **Gas Station**: Resource allocation, supply chain
- **Hand of Straights**: Scheduling, resource grouping
- **Partition Labels**: Data compression, string processing
- **Valid Parenthesis**: Parser design, syntax validation

## Companies

Frequently asked by: Amazon, Google, Microsoft, Facebook, Apple, Bloomberg, Adobe, Uber, LinkedIn, Airbnb

## Tips for Success

1. **Master the proof** - Understand why greedy works
2. **Practice pattern recognition** - Similar problems use similar greedy choices
3. **Start simple** - Get O(n²) greedy working, then optimize
4. **Draw it out** - Visualize the greedy choices
5. **Consider alternatives** - What if greedy doesn't work?

## Next Steps

After mastering these problems:

1. **More Greedy Problems**:
   - Meeting Rooms II
   - Non-overlapping Intervals
   - Minimum Number of Arrows

2. **Advanced Topics**:
   - Interval scheduling
   - Huffman coding
   - Activity selection

3. **Related Patterns**:
   - Two pointers with greedy
   - Sliding window with greedy
   - Greedy + data structures (heaps, stacks)

## Key Takeaways

1. **Greedy works when local optimum = global optimum**
2. **Always prove correctness** - counterexamples are crucial
3. **Simple is better** - greedy should be elegant
4. **Sorting often helps** - creates natural greedy order
5. **Track what matters** - min/max, ranges, counts
6. **Reset strategies** - when greedy fails, start fresh
7. **Two-pass common** - preprocess then decide

---

Greedy algorithms are powerful when applicable. Master these patterns, and you'll quickly recognize when greedy is the right approach in new problems.
