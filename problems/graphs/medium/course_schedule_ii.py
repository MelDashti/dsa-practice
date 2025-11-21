"""
PROBLEM: Course Schedule II (LeetCode 210)
LeetCode: https://leetcode.com/problems/course-schedule-ii/
Difficulty: Medium
Pattern: Graphs (Topological Sort)
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg

There are a total of num_courses courses you have to take, labeled from 0 to num_courses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you
must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return the ordering of courses you should take to finish all courses. If there are many valid
answers, return any of them. If it is impossible to finish all courses, return an empty array.

Example 1:
    Input: num_courses = 2, prerequisites = [[1,0]]
    Output: [0,1]
    Explanation: There are a total of 2 courses to take. To take course 1 you should have
    finished course 0. So the correct course order is [0,1].

Example 2:
    Input: num_courses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    Output: [0,2,1,3]
    Explanation: There are a total of 4 courses to take. To take course 3 you should have
    finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished
    course 0. So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].

Example 3:
    Input: num_courses = 1, prerequisites = []
    Output: [0]

Constraints:
- 1 <= num_courses <= 2000
- 0 <= prerequisites.length <= num_courses * (num_courses - 1)
- prerequisites[i].length == 2
- 0 <= ai, bi < num_courses
- ai != bi
- All the pairs [ai, bi] are distinct

Approach:
1. Build adjacency list from prerequisites
2. Use DFS with cycle detection
3. Track visit state and result order
4. Add courses to result in post-order (after visiting prereqs)
5. If cycle detected, return empty array

Time: O(V + E) - visit all vertices and edges
Space: O(V + E) - adjacency list and recursion stack
"""

from typing import List
from collections import defaultdict


class Solution:
    def find_order(self, num_courses: int, prerequisites: List[List[int]]) -> List[int]:
        # Build adjacency list
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[course].append(prereq)

        # 0 = unvisited, 1 = visiting, 2 = visited
        visit_state = [0] * num_courses
        result = []

        def dfs(course):
            if visit_state[course] == 1:  # Cycle detected
                return False
            if visit_state[course] == 2:  # Already visited
                return True

            # Mark as visiting
            visit_state[course] = 1

            # Visit all prerequisites
            for prereq in graph[course]:
                if not dfs(prereq):
                    return False

            # Mark as visited
            visit_state[course] = 2
            result.append(course)
            return True

        # Process all courses
        for course in range(num_courses):
            if not dfs(course):
                return []

        return result


# Tests
def test():
    sol = Solution()

    # Test 1: Simple case
    result1 = sol.find_order(2, [[1,0]])
    assert result1 == [0,1]

    # Test 2: Multiple valid orders
    result2 = sol.find_order(4, [[1,0],[2,0],[3,1],[3,2]])
    # Check that the order is valid (0 before 1 and 2, 1 and 2 before 3)
    assert len(result2) == 4
    idx0 = result2.index(0)
    idx1 = result2.index(1)
    idx2 = result2.index(2)
    idx3 = result2.index(3)
    assert idx0 < idx1 and idx0 < idx2
    assert idx1 < idx3 and idx2 < idx3

    # Test 3: No prerequisites
    result3 = sol.find_order(1, [])
    assert result3 == [0]

    # Test 4: Cycle exists
    result4 = sol.find_order(2, [[1,0],[0,1]])
    assert result4 == []

    # Test 5: Linear chain
    result5 = sol.find_order(3, [[1,0],[2,1]])
    assert result5 == [0,1,2]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
