"""
PROBLEM: Course Schedule (LeetCode 207)
LeetCode: https://leetcode.com/problems/course-schedule/
Difficulty: Medium
Pattern: Graphs (Topological Sort, Cycle Detection)
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg

There are a total of num_courses courses you have to take, labeled from 0 to num_courses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you
must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

Example 1:
    Input: num_courses = 2, prerequisites = [[1,0]]
    Output: true
    Explanation: There are a total of 2 courses to take.
    To take course 1 you should have finished course 0. So it is possible.

Example 2:
    Input: num_courses = 2, prerequisites = [[1,0],[0,1]]
    Output: false
    Explanation: There are a total of 2 courses to take.
    To take course 1 you should have finished course 0, and to take course 0 you should
    also have finished course 1. So it is impossible.

Constraints:
- 1 <= num_courses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < num_courses
- All the pairs prerequisites[i] are unique

Approach:
1. Build adjacency list from prerequisites
2. Use DFS to detect cycles
3. Track visit state: unvisited (0), visiting (1), visited (2)
4. If we encounter a node in "visiting" state, there's a cycle
5. Return false if cycle found, true otherwise

Time: O(V + E) - visit all vertices and edges
Space: O(V + E) - adjacency list and recursion stack
"""

from typing import List
from collections import defaultdict


class Solution:
    def can_finish(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        # Build adjacency list
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[course].append(prereq)

        # 0 = unvisited, 1 = visiting, 2 = visited
        visit_state = [0] * num_courses

        def has_cycle(course):
            if visit_state[course] == 1:  # Currently visiting - cycle detected
                return True
            if visit_state[course] == 2:  # Already visited
                return False

            # Mark as visiting
            visit_state[course] = 1

            # Check all prerequisites
            for prereq in graph[course]:
                if has_cycle(prereq):
                    return True

            # Mark as visited
            visit_state[course] = 2
            return False

        # Check each course
        for course in range(num_courses):
            if has_cycle(course):
                return False

        return True


# Tests
def test():
    sol = Solution()

    # Test 1: Possible to finish
    assert sol.can_finish(2, [[1,0]]) == True

    # Test 2: Cycle exists
    assert sol.can_finish(2, [[1,0],[0,1]]) == False

    # Test 3: Multiple prerequisites
    assert sol.can_finish(4, [[1,0],[2,0],[3,1],[3,2]]) == True

    # Test 4: No prerequisites
    assert sol.can_finish(3, []) == True

    # Test 5: Complex cycle
    assert sol.can_finish(3, [[0,1],[1,2],[2,0]]) == False

    # Test 6: Linear dependencies
    assert sol.can_finish(5, [[1,0],[2,1],[3,2],[4,3]]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
