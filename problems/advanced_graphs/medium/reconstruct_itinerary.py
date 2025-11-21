"""
PROBLEM: Reconstruct Itinerary (LeetCode 332)
Difficulty: Hard
Pattern: Advanced Graphs, DFS, Eulerian Path
Companies: Amazon, Google, Facebook, Uber, Apple

You are given a list of airline tickets where tickets[i] = [from_i, to_i] represent
the departure and the arrival airports of one flight. Reconstruct the itinerary in
order and return it.

All of the tickets belong to a man who departs from "JFK", thus, the itinerary must
begin with "JFK". If there are multiple valid itineraries, you should return the
itinerary that has the smallest lexical order when read as a single string.

For example, the itinerary ["JFK", "LGA"] has a smaller lexical order than ["JFK", "LGB"].

You may assume all tickets form at least one valid itinerary. You must use all the
tickets once and only once.

Example 1:
    Input: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
    Output: ["JFK","MUC","LHR","SFO","SJC"]

Example 2:
    Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
    Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
    Explanation: Another possible reconstruction is ["JFK","SFO","ATL","JFK","ATL","SFO"]
    but it is larger in lexical order.

Constraints:
- 1 <= tickets.length <= 300
- tickets[i].length == 2
- from_i.length == 3
- to_i.length == 3
- from_i and to_i consist of uppercase English letters
- from_i != to_i

Approach:
1. Build adjacency list graph with sorted destinations (for lexical order)
2. Use Hierholzer's algorithm to find Eulerian path
3. Start DFS from "JFK", always choose smallest lexical destination
4. Use backtracking to explore all tickets
5. Add nodes to result in post-order (reverse at end)

Time: O(E log E) where E is number of edges (tickets), for sorting destinations
Space: O(E) for the graph and recursion stack
"""

from typing import List
from collections import defaultdict


class Solution:
    def find_itinerary(self, tickets: List[List[str]]) -> List[str]:
        # Build graph with sorted destinations
        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)

        route = []

        def dfs(airport):
            while graph[airport]:
                next_dest = graph[airport].pop()
                dfs(next_dest)
            route.append(airport)

        dfs("JFK")
        return route[::-1]


# Tests
def test():
    sol = Solution()

    # Test 1: Basic itinerary
    tickets1 = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    assert sol.find_itinerary(tickets1) == ["JFK", "MUC", "LHR", "SFO", "SJC"]

    # Test 2: Multiple valid paths, return lexically smallest
    tickets2 = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    assert sol.find_itinerary(tickets2) == ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]

    # Test 3: Simple round trip
    tickets3 = [["JFK", "KUL"], ["KUL", "JFK"]]
    assert sol.find_itinerary(tickets3) == ["JFK", "KUL", "JFK"]

    # Test 4: Single ticket
    tickets4 = [["JFK", "SFO"]]
    assert sol.find_itinerary(tickets4) == ["JFK", "SFO"]

    # Test 5: Complex cycle
    tickets5 = [["JFK", "ATL"], ["ATL", "JFK"], ["JFK", "ATL"], ["ATL", "AAA"]]
    assert sol.find_itinerary(tickets5) == ["JFK", "ATL", "JFK", "ATL", "AAA"]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
