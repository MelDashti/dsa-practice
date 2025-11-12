"""
PROBLEM: Task Scheduler (LeetCode 621)
Difficulty: Medium
Pattern: Heap, Greedy, Queue
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg

Given a characters array tasks, representing the tasks a CPU needs to do, where
each letter represents a different task. Tasks could be done in any order. Each
task is done in one unit of time. For each unit of time, the CPU could complete
either one task or just be idle.

However, there is a non-negative integer n that represents the cooldown period
between two same tasks (the same letter in the array), that is that there must
be at least n units of time between any two same tasks.

Return the least number of units of times that the CPU will take to finish all
the given tasks.

Example 1:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation:
    A -> B -> idle -> A -> B -> idle -> A -> B
    There is at least 2 units of time between any two same tasks.

Example 2:
    Input: tasks = ["A","A","A","B","B","B"], n = 0
    Output: 6
    Explanation: On this case any permutation of size 6 would work since n = 0.
    ["A","A","A","B","B","B"]
    ["A","B","A","B","A","B"]
    ["B","B","B","A","A","A"]
    ...
    And so on.

Example 3:
    Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
    Output: 16
    Explanation:
    One possible solution is
    A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A

Constraints:
- 1 <= tasks.length <= 10^4
- tasks[i] is an uppercase English letter
- 0 <= n <= 100

Approach:
1. Count frequency of each task
2. Use max heap to always process most frequent task
3. Use queue to track tasks in cooldown with their available time
4. At each time unit:
   - Move tasks from cooldown queue back to heap if ready
   - Process most frequent task from heap
   - Add processed task to cooldown queue
5. Continue until all tasks processed

Time: O(n * m) where n is total tasks and m is cooldown period
Space: O(1) - at most 26 unique tasks
"""

import heapq
from collections import Counter, deque


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        # Count frequency of each task
        count = Counter(tasks)

        # Max heap (use negative values for max heap in Python)
        max_heap = [-freq for freq in count.values()]
        heapq.heapify(max_heap)

        time = 0
        queue = deque()  # pairs of (count, idle_time)

        while max_heap or queue:
            time += 1

            if max_heap:
                # Process most frequent task
                freq = heapq.heappop(max_heap) + 1  # Decrement count
                if freq:  # If still has remaining tasks
                    queue.append((freq, time + n))  # Add to cooldown

            # Check if any task is ready from cooldown
            if queue and queue[0][1] == time:
                heapq.heappush(max_heap, queue.popleft()[0])

        return time


# Tests
def test():
    sol = Solution()

    # Test 1
    assert sol.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8

    # Test 2
    assert sol.leastInterval(["A", "A", "A", "B", "B", "B"], 0) == 6

    # Test 3
    assert sol.leastInterval(["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2) == 16

    # Test 4
    assert sol.leastInterval(["A", "A", "A", "B", "B", "B"], 3) == 10

    # Test 5
    assert sol.leastInterval(["A", "B", "C", "D", "E", "F"], 2) == 6

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
