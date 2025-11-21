"""
PROBLEM: Min Stack (LeetCode 155)
Difficulty: Medium
Pattern: Stack, Design
Companies: Amazon, Google, Bloomberg, Microsoft, Apple

Design a stack that supports push, pop, top, and retrieving the minimum element
in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int get_min() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

Example 1:
    Input:
    ["MinStack","push","push","push","getMin","pop","top","getMin"]
    [[],[-2],[0],[-3],[],[],[],[]]

    Output:
    [null,null,null,null,-3,null,0,-2]

    Explanation:
    MinStack minStack = new MinStack();
    minStack.push(-2);
    minStack.push(0);
    minStack.push(-3);
    minStack.get_min(); // return -3
    minStack.pop();
    minStack.top();    // return 0
    minStack.get_min(); // return -2

Constraints:
- -2^31 <= val <= 2^31 - 1
- Methods pop, top and getMin operations will always be called on non-empty stacks.
- At most 3 * 10^4 calls will be made to push, pop, top, and getMin.

Approach:
1. Use two stacks: main stack and min stack
2. Main stack stores all values
3. Min stack stores minimum values at each level
4. Push: add to both stacks (min stack gets min of current and its top)
5. Pop: remove from both stacks
6. GetMin: return top of min stack

Time: O(1) - all operations
Space: O(n) - two stacks
"""


class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Push the minimum value onto min_stack
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]


# Tests
def test():
    minStack = MinStack()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    assert minStack.get_min() == -3
    minStack.pop()
    assert minStack.top() == 0
    assert minStack.get_min() == -2

    # Test 2
    stack2 = MinStack()
    stack2.push(5)
    stack2.push(1)
    stack2.push(3)
    assert stack2.get_min() == 1
    assert stack2.top() == 3
    stack2.pop()
    assert stack2.get_min() == 1
    stack2.pop()
    assert stack2.get_min() == 5

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
