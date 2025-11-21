"""
PROBLEM: Time Based Key-Value Store (LeetCode 981)
LeetCode: https://leetcode.com/problems/time-based-key-value-store/
Difficulty: Medium
Pattern: Binary Search
Companies: Amazon, Google, Facebook, Bloomberg, Microsoft

Design a time-based key-value data structure that can store multiple values
for the same key at different time stamps and retrieve the key's value at a
certain timestamp.

Implement the TimeMap class:
- TimeMap() Initializes the object of the data structure
- void set(String key, String value, int timestamp) Stores the key with the
  value at the given time timestamp
- String get(String key, int timestamp) Returns a value such that set was
  called previously, with timestamp_prev <= timestamp. If there are multiple
  such values, it returns the value associated with the largest timestamp_prev.
  If there are no values, it returns ""

Example 1:
    Input:
    ["TimeMap", "set", "get", "get", "set", "get", "get"]
    [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
    Output:
    [null, null, "bar", "bar", null, "bar2", "bar2"]

    Explanation:
    TimeMap time_map = new TimeMap();
    time_map.set("foo", "bar", 1);  // store key "foo" and value "bar" with timestamp = 1
    time_map.get("foo", 1);         // return "bar"
    time_map.get("foo", 3);         // return "bar", no value at 3, return value at 1
    time_map.set("foo", "bar2", 4); // store key "foo" and value "bar2" with timestamp = 4
    time_map.get("foo", 4);         // return "bar2"
    time_map.get("foo", 5);         // return "bar2"

Constraints:
- 1 <= key.length, value.length <= 100
- key and value consist of lowercase English letters and digits
- 1 <= timestamp <= 10^7
- All the timestamps of set are strictly increasing
- At most 2 * 10^5 calls will be made to set and get

Approach:
1. Use a dictionary to map keys to list of (timestamp, value) pairs
2. For set: append (timestamp, value) to the list for the given key
3. For get: use binary search to find the largest timestamp <= given timestamp
4. Since timestamps are strictly increasing, the list is already sorted

Time:
- set: O(1) - append to list
- get: O(log n) - binary search where n is number of timestamps for the key
Space: O(n) - storing all key-value-timestamp tuples
"""

from typing import List
from collections import defaultdict


class TimeMap:
    def __init__(self):
        # key -> list of (timestamp, value) tuples
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        values = self.store[key]
        left, right = 0, len(values) - 1
        result = ""

        # Binary search for largest timestamp <= given timestamp
        while left <= right:
            mid = left + (right - left) // 2

            if values[mid][0] <= timestamp:
                result = values[mid][1]
                left = mid + 1  # Try to find a larger valid timestamp
            else:
                right = mid - 1

        return result


# Tests
def test():
    time_map = TimeMap()

    time_map.set("foo", "bar", 1)
    assert time_map.get("foo", 1) == "bar"
    assert time_map.get("foo", 3) == "bar"

    time_map.set("foo", "bar2", 4)
    assert time_map.get("foo", 4) == "bar2"
    assert time_map.get("foo", 5) == "bar2"

    # Additional tests
    time_map2 = TimeMap()
    time_map2.set("love", "high", 10)
    time_map2.set("love", "low", 20)
    assert time_map2.get("love", 5) == ""
    assert time_map2.get("love", 10) == "high"
    assert time_map2.get("love", 15) == "high"
    assert time_map2.get("love", 20) == "low"
    assert time_map2.get("love", 25) == "low"

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
