# Problem: Design a Dynamic Array

Design a `DynamicArray` class that simulates a dynamic array (like a C++ vector or Java ArrayList). It should manage its own capacity and resize itself when it becomes full.

**Class Requirements:**

- `__init__(self, capacity: int)`: Initializes the array with a given initial capacity.
- `get(self, i: int) -> int`: Returns the value at the ith index.
- `set(self, i: int, n: int) -> None`: Sets the value at the ith index to n.
- `pushback(self, n: int) -> None`: Adds an element n to the end of the array. If the array is at capacity, it should trigger a resize.
- `popback(self) -> int`: Removes and returns the last element.
- `resize(self) -> None`: Doubles the capacity of the array.
- `getSize(self) -> int`: Returns the current number of elements in the array.
- `getCapacity(self) -> int`: Returns the current maximum capacity of the array.
