"""
PROBLEM: Cheapest Flights Within K Stops (LeetCode 787)
LeetCode: https://leetcode.com/problems/cheapest-flights-within-k-stops/
Difficulty: Medium
Pattern: Advanced Graphs, BFS, Modified Dijkstra, Bellman-Ford
Companies: Amazon, Google, Facebook, Microsoft, Uber

There are n cities connected by some number of flights. You are given an array
flights where flights[i] = [from_i, to_i, price_i] indicates that there is a flight
from city from_i to city to_i with cost price_i.

You are also given three integers src, dst, and k, return the cheapest price from
src to dst with at most k stops. If there is no such route, return -1.

Example 1:
    Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],
           src = 0, dst = 3, k = 1
    Output: 700
    Explanation:
    The graph is shown above.
    The optimal path with at most 1 stop from city 0 to 3 is marked in red and has cost 100 + 600 = 700.
    Note that the path through cities [0,1,2,3] is cheaper but is invalid because it uses 2 stops.

Example 2:
    Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]],
           src = 0, dst = 2, k = 1
    Output: 200
    Explanation:
    The optimal path with at most 1 stop from city 0 to 2 is marked in red and has cost 100 + 100 = 200.

Example 3:
    Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]],
           src = 0, dst = 2, k = 0
    Output: 500
    Explanation:
    The optimal path with no stops from city 0 to 2 is marked in red and has cost 500.

Constraints:
- 1 <= n <= 100
- 0 <= flights.length <= (n * (n - 1) / 2)
- flights[i].length == 3
- 0 <= from_i, to_i < n
- from_i != to_i
- 1 <= price_i <= 10^4
- There will not be any multiple flights between two cities
- 0 <= src, dst, k < n
- src != dst

Approach:
1. Use BFS with level tracking (each level = one stop)
2. Track minimum cost to reach each city
3. Process all nodes at each level before moving to next
4. Only explore paths with at most k stops
5. Keep track of best price seen so far for each city
6. Can't use standard Dijkstra as we need to limit stops, not just minimize cost

Time: O(E * K) where E is number of flights, K is max stops
Space: O(N) for storing prices and graph
"""

from typing import List
from collections import defaultdict, deque


class Solution:
    def find_cheapest_price(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # Build adjacency list
        graph = defaultdict(list)
        for from_city, to_city, price in flights:
            graph[from_city].append((to_city, price))

        # BFS with level tracking
        queue = deque([(src, 0)])  # (city, cost)
        min_cost = [float('inf')] * n
        min_cost[src] = 0
        stops = 0

        while queue and stops <= k:
            size = len(queue)

            for _ in range(size):
                city, cost = queue.popleft()

                # Explore neighbors
                for next_city, price in graph[city]:
                    new_cost = cost + price

                    # Only add to queue if we found a better price
                    if new_cost < min_cost[next_city]:
                        min_cost[next_city] = new_cost
                        queue.append((next_city, new_cost))

            stops += 1

        return min_cost[dst] if min_cost[dst] != float('inf') else -1


# Tests
def test():
    sol = Solution()

    # Test 1: Example with 1 stop
    flights1 = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    assert sol.find_cheapest_price(4, flights1, 0, 3, 1) == 700

    # Test 2: Multiple paths
    flights2 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    assert sol.find_cheapest_price(3, flights2, 0, 2, 1) == 200

    # Test 3: Direct flight only
    flights3 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    assert sol.find_cheapest_price(3, flights3, 0, 2, 0) == 500

    # Test 4: No valid path
    flights4 = [[0, 1, 100], [1, 2, 100]]
    assert sol.find_cheapest_price(3, flights4, 0, 2, 0) == -1

    # Test 5: Direct flight is cheapest
    flights5 = [[0, 1, 100], [1, 2, 100], [0, 2, 150]]
    assert sol.find_cheapest_price(3, flights5, 0, 2, 0) == 150

    # Test 6: Multiple stops allowed
    flights6 = [[0, 1, 100], [1, 2, 100], [2, 3, 100]]
    assert sol.find_cheapest_price(4, flights6, 0, 3, 2) == 300

    # Test 7: Complex graph
    flights7 = [[0, 1, 100], [0, 2, 500], [1, 2, 100], [2, 3, 100]]
    assert sol.find_cheapest_price(4, flights7, 0, 3, 2) == 300

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
