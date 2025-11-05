"""
PROBLEM: Dynamic Array
Difficulty: Easy
Pattern: Arrays & Memory Management

Design a DynamicArray class (like C++ vector or Java ArrayList) that manages
its own capacity and resizes when full.

Requirements:
- __init__(capacity): Initialize with given capacity
- get(i): Return element at index i
- set(i, n): Set element at index i to n
- pushback(n): Add element to end (resize if needed)
- popback(): Remove and return last element
- resize(): Double the capacity
- getSize(): Return current size
- getCapacity(): Return current capacity

Example:
    arr = DynamicArray(1)
    arr.pushback(1)    # [1], size=1, capacity=1
    arr.pushback(2)    # [1,2], size=2, capacity=2 (resized)
    arr.get(1)         # returns 2
    arr.popback()      # returns 2, size=1

Time Complexity: O(1) amortized for pushback, O(1) for others
Space Complexity: O(n)
"""


class DynamicArray:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.array = []

    def get(self, i: int) -> int:
        if i >= self.size:
            raise IndexError("Index out of bounds")
        return self.array[i]

    def set(self, i: int, n: int) -> None:
        if i >= self.size:
            raise IndexError("Index out of bounds")
        self.array[i] = n

    def pushback(self, n: int) -> None:
        if self.size == self.capacity:
            self.resize()
        self.array.append(n)
        self.size += 1

    def popback(self) -> int:
        if self.size == 0:
            return None
        self.size -= 1
        return self.array.pop()

    def resize(self) -> None:
        self.capacity = self.capacity * 2

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity


# Tests
def test():
    arr = DynamicArray(1)

    arr.pushback(1)
    assert arr.getSize() == 1
    assert arr.getCapacity() == 1

    arr.pushback(2)
    assert arr.getSize() == 2
    assert arr.getCapacity() == 2

    assert arr.get(1) == 2
    assert arr.popback() == 2
    assert arr.getSize() == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
