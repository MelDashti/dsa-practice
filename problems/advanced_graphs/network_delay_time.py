"""
PROBLEM: Network Delay Time (LeetCode 743)
Difficulty: Medium
Pattern: Advanced Graphs, Dijkstra's Algorithm, Shortest Path
Companies: Amazon, Google, Microsoft, Facebook, Bloomberg

You are given a network of n nodes, labeled from 1 to n. You are also given times,
a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the
source node, vi is the target node, and wi is the time it takes for a signal to
travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all
the n nodes to receive the signal. If it is impossible for all the n nodes to receive
the signal, return -1.

Example 1:
    Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
    Output: 2

Example 2:
    Input: times = [[1,2,1]], n = 2, k = 1
    Output: 1

Example 3:
    Input: times = [[1,2,1]], n = 2, k = 2
    Output: -1

Constraints:
- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- times[i].length == 3
- 1 <= ui, vi <= n
- ui != vi
- 0 <= wi <= 100
- All the pairs (ui, vi) are unique (i.e., no multiple edges)

Approach:
1. Build adjacency list graph from times
2. Use Dijkstra's algorithm to find shortest path from k to all nodes
3. Use min heap to always process node with minimum distance first
4. Track minimum distance to reach each node
5. Return maximum distance among all reachable nodes
6. If not all nodes reachable, return -1

Time: O((V + E) log V) where V is number of nodes, E is number of edges
Space: O(V + E) for graph and distances
"""

from typing import List
import heapq
from collections import defaultdict


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Build adjacency list
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        # Dijkstra's algorithm
        min_heap = [(0, k)]  # (time, node)
        distances = {}

        while min_heap:
            time, node = heapq.heappop(min_heap)

            if node in distances:
                continue

            distances[node] = time

            # Explore neighbors
            for neighbor, weight in graph[node]:
                if neighbor not in distances:
                    heapq.heappush(min_heap, (time + weight, neighbor))

        # Check if all nodes are reachable
        if len(distances) != n:
            return -1

        return max(distances.values())


# Tests
def test():
    sol = Solution()

    # Test 1: Basic network
    times1 = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert sol.networkDelayTime(times1, 4, 2) == 2

    # Test 2: Simple two-node network
    times2 = [[1, 2, 1]]
    assert sol.networkDelayTime(times2, 2, 1) == 1

    # Test 3: Unreachable nodes
    times3 = [[1, 2, 1]]
    assert sol.networkDelayTime(times3, 2, 2) == -1

    # Test 4: Single node
    times4 = []
    assert sol.networkDelayTime(times4, 1, 1) == 0

    # Test 5: All nodes directly connected from source
    times5 = [[1, 2, 1], [1, 3, 2], [1, 4, 3]]
    assert sol.networkDelayTime(times5, 4, 1) == 3

    # Test 6: Multiple paths to same node
    times6 = [[1, 2, 1], [2, 3, 2], [1, 3, 4]]
    assert sol.networkDelayTime(times6, 3, 1) == 3

    # Test 7: Complex network - shortest path wins
    times7 = [[1, 2, 1], [2, 3, 2], [1, 3, 1]]
    assert sol.networkDelayTime(times7, 3, 1) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
