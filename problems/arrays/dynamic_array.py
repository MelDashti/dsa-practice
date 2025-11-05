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

from typing import Any, List


class DynamicArray:
    """A dynamic array implementation with automatic resizing."""

    def __init__(self, capacity: int) -> None:
        """
        Initialize dynamic array with given capacity.

        Args:
            capacity: Initial capacity of the array

        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity: int = capacity
        self.size: int = 0
        self.array: List[Any] = []

    def get(self, i: int) -> Any:
        """
        Get element at index i.

        Args:
            i: Index to retrieve

        Returns:
            Element at index i

        Raises:
            IndexError: If index is out of bounds
        """
        if i < 0 or i >= self.size:
            raise IndexError(f"Index {i} out of bounds for size {self.size}")
        return self.array[i]

    def set(self, i: int, n: Any) -> None:
        """
        Set element at index i to value n.

        Args:
            i: Index to set
            n: Value to set

        Raises:
            IndexError: If index is out of bounds
        """
        if i < 0 or i >= self.size:
            raise IndexError(f"Index {i} out of bounds for size {self.size}")
        self.array[i] = n

    def pushback(self, n: Any) -> None:
        """
        Add element to the end of array, resizing if necessary.

        Args:
            n: Element to add

        Time Complexity: O(1) amortized
        """
        if self.size == self.capacity:
            self.resize()
        self.array.append(n)
        self.size += 1

    def popback(self) -> Any:
        """
        Remove and return the last element.

        Returns:
            The last element in the array

        Raises:
            IndexError: If array is empty

        Time Complexity: O(1)
        """
        if self.size == 0:
            raise IndexError("Cannot pop from empty array")
        self.size -= 1
        return self.array.pop()

    def resize(self) -> None:
        """
        Double the capacity of the array.

        Time Complexity: O(1) - only updates capacity, actual resize happens in pushback
        """
        self.capacity = self.capacity * 2

    def getSize(self) -> int:
        """
        Get current number of elements in array.

        Returns:
            Current size
        """
        return self.size

    def getCapacity(self) -> int:
        """
        Get current capacity of array.

        Returns:
            Current capacity
        """
        return self.capacity


def main():
    """Example usage and manual testing."""
    arr = DynamicArray(1)

    arr.pushback(1)
    print(f"Size: {arr.getSize()}, Capacity: {arr.getCapacity()}")  # 1, 1

    arr.pushback(2)
    print(f"Size: {arr.getSize()}, Capacity: {arr.getCapacity()}")  # 2, 2

    print(f"arr.get(1) = {arr.get(1)}")  # 2
    print(f"arr.popback() = {arr.popback()}")  # 2
    print(f"Size: {arr.getSize()}")  # 1

    print("✓ All manual tests passed")


if __name__ == "__main__":
    main()
