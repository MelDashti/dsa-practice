# Stack - Medium Problems

## Overview

Medium stack problems introduce more complex patterns including monotonic stacks, expression evaluation, and multi-step state tracking. These problems require a deeper understanding of when and how stacks can optimize solutions.

## Key Concepts

### Advanced Stack Patterns

1. **Monotonic Stack**: Stack maintaining elements in increasing or decreasing order
2. **Expression Evaluation**: Processing mathematical or logical expressions
3. **Backtracking with Stack**: Exploring multiple possibilities
4. **State Tracking**: Maintaining and comparing states across iterations

### When to Use Advanced Stack Techniques

- Finding next greater/smaller elements
- Evaluating postfix/prefix expressions
- Generating all valid combinations
- Processing elements with dependencies on previous elements

## Problems in This Section

### 1. Evaluate Reverse Polish Notation (LC 150)
**Concept**: Stack-based expression evaluation

**Key Ideas**:
- Process tokens from left to right
- Push numbers onto stack
- Pop two operands when encountering an operator
- Push result back onto stack
- Final stack contains one element: the result

**Pattern**: Postfix expression evaluation

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Example**:
```
["2", "1", "+", "3", "*"] → ((2 + 1) * 3) = 9
Stack evolution: [2] → [2,1] → [3] → [3,3] → [9]
```

---

### 2. Generate Parentheses (LC 22)
**Concept**: Backtracking with stack or recursion

**Key Ideas**:
- Track open and close bracket counts
- Only add opening bracket if count < n
- Only add closing bracket if it won't exceed opening brackets
- Backtrack to explore all valid combinations
- Result when both counts equal n

**Pattern**: Constraint-based generation with backtracking

**Time Complexity**: O(4^n / √n) - Catalan number
**Space Complexity**: O(n) for recursion depth

---

### 3. Daily Temperatures (LC 739)
**Concept**: Monotonic decreasing stack

**Key Ideas**:
- Stack stores indices of temperatures
- Maintain decreasing order in stack
- When finding a warmer day, pop all cooler days
- Calculate days difference using indices
- Unprocessed indices get default value 0

**Pattern**: Next greater element using monotonic stack

**Time Complexity**: O(n) - each element pushed and popped once
**Space Complexity**: O(n)

**Why Monotonic Stack?**
- Naive approach: O(n²) checking each future day
- Monotonic stack: O(n) by processing each element once

---

### 4. Car Fleet (LC 853)
**Concept**: Stack with sorted data and time calculations

**Key Ideas**:
- Sort cars by starting position (closest to target first)
- Calculate time to reach target for each car
- Use stack to track fleet formation
- Cars form fleet if faster car catches slower car ahead
- Stack size represents number of fleets

**Pattern**: State tracking with preprocessing

**Time Complexity**: O(n log n) - dominated by sorting
**Space Complexity**: O(n)

## Common Patterns for Medium Stack Problems

### 1. Monotonic Stack Pattern
```python
def nextGreaterElements(nums):
    result = [-1] * len(nums)
    stack = []  # Store indices

    for i, num in enumerate(nums):
        # Pop all smaller elements - found their next greater
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num
        stack.append(i)

    return result
```

### 2. Expression Evaluation Pattern
```python
def evalRPN(tokens):
    stack = []
    operators = {'+', '-', '*', '/'}

    for token in tokens:
        if token in operators:
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            else: stack.append(int(a / b))  # Truncate toward zero
        else:
            stack.append(int(token))

    return stack[0]
```

### 3. Backtracking Pattern
```python
def generateParenthesis(n):
    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return

        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result
```

### 4. Preprocessing with Stack Pattern
```python
def carFleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    stack = []

    for pos, spd in cars:
        time = (target - pos) / spd
        # If this car is slower, it forms a new fleet
        if not stack or time > stack[-1]:
            stack.append(time)

    return len(stack)
```

## Key Insights

### Monotonic Stack
- **Use case**: Find next greater/smaller element
- **Benefit**: Reduces O(n²) to O(n)
- **Maintenance**: Pop elements that violate monotonic property
- **Trick**: Store indices instead of values for result tracking

### Expression Evaluation
- **Postfix notation**: No parentheses needed, no operator precedence
- **Stack depth**: Maximum depth equals max nested operations
- **Operand order**: Watch out! Pop order matters (a - b vs b - a)

### Backtracking
- **Constraint tracking**: Use counters to enforce validity
- **Early termination**: Stop invalid paths immediately
- **State restoration**: Implicit in recursion, explicit if using loops

## Learning Path

1. **Start with Evaluate RPN**: Master expression evaluation
2. **Practice Generate Parentheses**: Understand backtracking
3. **Master Daily Temperatures**: Learn monotonic stack pattern
4. **Tackle Car Fleet**: Combine multiple concepts

## Tips for Success

1. **Identify the pattern early**: Is it monotonic? Expression? Backtracking?
2. **Draw the stack state**: Visualize what happens at each step
3. **Consider sorting**: Sometimes preprocessing makes the problem easier
4. **Use indices in stack**: Often more useful than values
5. **Think about time saved**: How does stack avoid redundant work?

## Common Mistakes to Avoid

- Confusing operand order in expression evaluation (a - b vs b - a)
- Not maintaining monotonic property correctly
- Forgetting to handle remaining stack elements
- Incorrect backtracking constraints (allowing invalid states)
- Not sorting when problem requires position-based processing

## Optimization Techniques

1. **Space optimization**: Sometimes can avoid stack with smart iteration
2. **Early termination**: In backtracking, prune invalid branches quickly
3. **Index vs Value**: Storing indices often provides more information
4. **Single pass**: Many stack problems can be solved in one iteration

## Next Steps

Once comfortable with medium problems:
- **Hard stack problems**: More complex optimizations
- **Segment trees**: Advanced range query data structures
- **Expression parsing**: Infix to postfix conversion
- **Advanced monotonic stack**: Handling circular arrays, multiple passes
