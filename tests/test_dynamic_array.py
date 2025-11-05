"""Tests for Dynamic Array implementation."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from problems.arrays.dynamic_array import DynamicArray


class TestDynamicArray:
    """Test suite for DynamicArray class."""

    def test_initialization(self):
        """Test array initialization with given capacity."""
        arr = DynamicArray(5)
        assert arr.getSize() == 0
        assert arr.getCapacity() == 5

    def test_pushback_and_get(self):
        """Test adding elements and retrieving them."""
        arr = DynamicArray(2)
        arr.pushback(10)
        arr.pushback(20)
        assert arr.get(0) == 10
        assert arr.get(1) == 20
        assert arr.getSize() == 2

    def test_auto_resize(self):
        """Test automatic resizing when capacity is reached."""
        arr = DynamicArray(1)
        arr.pushback(1)
        assert arr.getCapacity() == 1

        arr.pushback(2)  # Should trigger resize
        assert arr.getCapacity() == 2
        assert arr.getSize() == 2

        arr.pushback(3)  # Should trigger another resize
        assert arr.getCapacity() == 4
        assert arr.getSize() == 3

    def test_set_and_get(self):
        """Test setting and getting elements."""
        arr = DynamicArray(3)
        arr.pushback(1)
        arr.pushback(2)
        arr.pushback(3)

        arr.set(1, 99)
        assert arr.get(1) == 99

    def test_popback(self):
        """Test removing elements from the end."""
        arr = DynamicArray(2)
        arr.pushback(10)
        arr.pushback(20)

        assert arr.popback() == 20
        assert arr.getSize() == 1
        assert arr.popback() == 10
        assert arr.getSize() == 0

    def test_popback_empty_array(self):
        """Test popback on empty array raises IndexError."""
        arr = DynamicArray(1)
        with pytest.raises(IndexError):
            arr.popback()

    def test_get_out_of_bounds(self):
        """Test that get raises IndexError for invalid index."""
        arr = DynamicArray(2)
        arr.pushback(1)

        with pytest.raises(IndexError):
            arr.get(5)

    def test_set_out_of_bounds(self):
        """Test that set raises IndexError for invalid index."""
        arr = DynamicArray(2)
        arr.pushback(1)

        with pytest.raises(IndexError):
            arr.set(5, 99)

    def test_multiple_resizes(self):
        """Test multiple automatic resizes."""
        arr = DynamicArray(1)
        for i in range(10):
            arr.pushback(i)

        assert arr.getSize() == 10
        assert arr.getCapacity() == 16  # 1 -> 2 -> 4 -> 8 -> 16

        # Verify all elements are preserved
        for i in range(10):
            assert arr.get(i) == i
