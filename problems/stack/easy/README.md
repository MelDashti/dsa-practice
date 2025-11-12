# Stack - Easy Problems

## Overview

Easy stack problems introduce you to the fundamental concepts of the Last-In-First-Out (LIFO) data structure. These problems help you understand when and how to use stacks effectively.

## Key Concepts

### What is a Stack?

A stack is a linear data structure that follows the LIFO principle:
- **Push**: Add an element to the top of the stack
- **Pop**: Remove the element from the top of the stack
- **Peek/Top**: View the top element without removing it
- **isEmpty**: Check if the stack is empty

### When to Use a Stack

Stacks are perfect for:
1. **Matching pairs**: Parentheses, brackets, or tags
2. **Reversing sequences**: Undo operations, backtracking
3. **Tracking most recent items**: Browser history, function calls
4. **Nested structures**: Parsing expressions, validating syntax

## Problems in This Section

### 1. Valid Parentheses (LC 20)
**Concept**: String validation using matching pairs

**Key Ideas**:
- Use stack to track opening brackets
- Pop from stack when encountering closing bracket
- Stack must be empty at the end for valid string
- Each closing bracket must match the most recent opening bracket

**Pattern**: Character matching and validation

**Time Complexity**: O(n)
**Space Complexity**: O(n)

---

### 2. Min Stack (LC 155)
**Concept**: Stack with constant-time minimum retrieval

**Key Ideas**:
- Maintain two stacks: one for values, one for minimums
- Alternative: Store (value, current_min) pairs in a single stack
- Each operation must remain O(1)
- The min stack tracks the minimum value at each level

**Pattern**: Auxiliary data structure for enhanced functionality

**Time Complexity**: O(1) for all operations
**Space Complexity**: O(n)

## Common Patterns for Easy Stack Problems

### 1. Matching Pattern
```python
def isValid(s: str) -> bool:
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in pairs:  # Closing bracket
            if not stack or stack.pop() != pairs[char]:
                return False
        else:  # Opening bracket
            stack.append(char)

    return len(stack) == 0
```

### 2. Auxiliary Stack Pattern
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)
```

## Learning Path

1. **Start with Valid Parentheses**: Master the basic matching pattern
2. **Move to Min Stack**: Learn how to extend stack functionality
3. **Practice variations**: Try with different types of brackets or constraints

## Tips for Success

1. **Always check if stack is empty before popping**: Prevents errors
2. **Use a dictionary for mappings**: Makes code cleaner and more maintainable
3. **Think about edge cases**: Empty strings, single characters, unmatched brackets
4. **Consider using lists in Python**: They have built-in append() and pop() methods
5. **Draw the stack state**: Visualize what's happening at each step

## Common Mistakes to Avoid

- Forgetting to check if stack is empty before pop()
- Not returning the correct value (stack should be empty for valid parentheses)
- Using the wrong data structure (queue instead of stack)
- Not handling edge cases (empty input, single character)

## Next Steps

Once you're comfortable with these problems, move on to:
- **Medium stack problems**: Multiple operations, complex state tracking
- **Monotonic stacks**: A special pattern for optimization problems
- **Stack-based algorithms**: Expression evaluation, DFS implementations
