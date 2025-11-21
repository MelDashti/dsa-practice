"""
PROBLEM: Walls and Gates (LeetCode 286)
LeetCode: https://leetcode.com/problems/walls-and-gates/
Difficulty: Medium
Pattern: Graphs (BFS)
Companies: Google, Facebook, Amazon, Microsoft

You are given an m x n grid rooms initialized with these three possible values:
- -1 A wall or an obstacle.
- 0 A gate.
- INF Infinity means an empty room. We use the value 2^31 - 1 = 2147483647 to
  represent INF as you may assume that the distance to a gate is less than 2147483647.

Fill each empty room with the distance to its nearest gate. If it is impossible to
reach a gate, it should be filled with INF.

Example 1:
    Input: rooms = [
        [2147483647,-1,0,2147483647],
        [2147483647,2147483647,2147483647,-1],
        [2147483647,-1,2147483647,-1],
        [0,-1,2147483647,2147483647]
    ]
    Output: [
        [3,-1,0,1],
        [2,2,1,-1],
        [1,-1,2,-1],
        [0,-1,3,4]
    ]

Example 2:
    Input: rooms = [[-1]]
    Output: [[-1]]

Constraints:
- m == rooms.length
- n == rooms[i].length
- 1 <= m, n <= 250
- rooms[i][j] is -1, 0, or 2^31 - 1

Approach:
1. Use multi-source BFS starting from all gates simultaneously
2. Add all gates (value 0) to queue
3. Process level by level, updating distances
4. Only visit empty rooms (INF values)
5. Each level represents distance from nearest gate

Time: O(m * n) - visit each cell once
Space: O(m * n) - queue in worst case
"""

from typing import List
from collections import deque


class Solution:
    def walls_and_gates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        if not rooms or not rooms[0]:
            return

        rows, cols = len(rooms), len(rooms[0])
        INF = 2147483647
        queue = deque()

        # Add all gates to queue
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    queue.append((r, c))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # BFS from all gates
        while queue:
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check bounds and if it's an empty room
                if (0 <= nr < rows and 0 <= nc < cols and
                    rooms[nr][nc] == INF):
                    rooms[nr][nc] = rooms[r][c] + 1
                    queue.append((nr, nc))


# Tests
def test():
    sol = Solution()
    INF = 2147483647

    # Test 1: Standard case
    rooms1 = [
        [INF,-1,0,INF],
        [INF,INF,INF,-1],
        [INF,-1,INF,-1],
        [0,-1,INF,INF]
    ]
    sol.walls_and_gates(rooms1)
    expected1 = [
        [3,-1,0,1],
        [2,2,1,-1],
        [1,-1,2,-1],
        [0,-1,3,4]
    ]
    assert rooms1 == expected1

    # Test 2: Only walls
    rooms2 = [[-1]]
    sol.walls_and_gates(rooms2)
    assert rooms2 == [[-1]]

    # Test 3: Only gates
    rooms3 = [[0,0],[0,0]]
    sol.walls_and_gates(rooms3)
    assert rooms3 == [[0,0],[0,0]]

    # Test 4: Unreachable rooms
    rooms4 = [
        [INF,-1,-1],
        [-1,-1,-1],
        [-1,-1,0]
    ]
    sol.walls_and_gates(rooms4)
    expected4 = [
        [INF,-1,-1],
        [-1,-1,-1],
        [-1,-1,0]
    ]
    assert rooms4 == expected4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
