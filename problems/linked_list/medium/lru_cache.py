"""
PROBLEM: LRU Cache (LeetCode 146)
Difficulty: Medium
Pattern: Linked List, Hash Table, Design
Companies: Amazon, Microsoft, Apple, Facebook, Google, Bloomberg

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
- int get(int key) Return the value of the key if the key exists, otherwise return -1.
- void put(int key, int value) Update the value of the key if the key exists.
  Otherwise, add the key-value pair to the cache. If the number of keys exceeds
  the capacity from this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

Example 1:
    Input:
    ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output:
    [null, null, null, 1, null, -1, null, -1, 3, 4]

    Explanation:
    LRUCache lru_cache = new LRUCache(2);
    lru_cache.put(1, 1); // cache is {1=1}
    lru_cache.put(2, 2); // cache is {1=1, 2=2}
    lru_cache.get(1);    // return 1
    lru_cache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    lru_cache.get(2);    // returns -1 (not found)
    lru_cache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    lru_cache.get(1);    // return -1 (not found)
    lru_cache.get(3);    // return 3
    lru_cache.get(4);    // return 4

Constraints:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls will be made to get and put

Approach:
1. Use doubly linked list to maintain order (most recent to least recent)
2. Use hash map for O(1) access to nodes
3. Keep dummy head and tail for easier insertion/removal
4. get: move accessed node to front (most recent)
5. put: add to front, remove from back if over capacity

Time: O(1) - all operations
Space: O(capacity) - store at most capacity items
"""


class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node

        # Dummy head and tail
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Remove node from linked list"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        """Add node right after head (most recently used)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        # Move to front (mark as recently used)
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing key
            self._remove(self.cache[key])

        # Add new node
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)

        # Remove least recently used if over capacity
        if len(self.cache) > self.capacity:
            # Remove from tail (least recently used)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# Tests
def test():
    # Test 1
    lru_cache = LRUCache(2)
    lru_cache.put(1, 1)
    lru_cache.put(2, 2)
    assert lru_cache.get(1) == 1
    lru_cache.put(3, 3)
    assert lru_cache.get(2) == -1
    lru_cache.put(4, 4)
    assert lru_cache.get(1) == -1
    assert lru_cache.get(3) == 3
    assert lru_cache.get(4) == 4

    # Test 2
    cache2 = LRUCache(1)
    cache2.put(2, 1)
    assert cache2.get(2) == 1
    cache2.put(3, 2)
    assert cache2.get(2) == -1
    assert cache2.get(3) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
