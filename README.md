# DSA Practice - NeetCode 150

A comprehensive collection of 150 curated coding interview problems from [NeetCode.io](https://neetcode.io/), organized by topic and difficulty level. Each problem includes detailed explanations, optimal solutions, and test cases.

## 📊 Progress

**Total Problems:** 150/150 ✅ (100% Complete)

### By Difficulty
- 🟢 **Easy:** 36 problems
- 🟡 **Medium:** 92 problems
- 🔴 **Hard:** 22 problems

## 📚 Problem Categories

Each category is organized into `easy/`, `medium/`, and `hard/` subdirectories with detailed README explanations.

| Category | Easy | Medium | Hard | Total |
|----------|------|--------|------|-------|
| [Arrays & Hashing](#arrays--hashing) | 4 | 4 | 1 | 9 |
| [Two Pointers](#two-pointers) | 1 | 3 | 1 | 5 |
| [Sliding Window](#sliding-window) | 1 | 4 | 1 | 6 |
| [Stack](#stack) | 2 | 4 | 1 | 7 |
| [Binary Search](#binary-search) | 1 | 5 | 1 | 7 |
| [Linked List](#linked-list) | 3 | 5 | 3 | 11 |
| [Trees](#trees) | 6 | 8 | 2 | 16 |
| [Tries](#tries) | 0 | 2 | 1 | 3 |
| [Heap / Priority Queue](#heap--priority-queue) | 2 | 4 | 1 | 7 |
| [Backtracking](#backtracking) | 0 | 8 | 1 | 9 |
| [Graphs](#graphs) | 1 | 10 | 2 | 13 |
| [Advanced Graphs](#advanced-graphs) | 0 | 3 | 3 | 6 |
| [1-D Dynamic Programming](#1-d-dynamic-programming) | 2 | 10 | 0 | 12 |
| [2-D Dynamic Programming](#2-d-dynamic-programming) | 0 | 8 | 3 | 11 |
| [Greedy](#greedy) | 1 | 7 | 0 | 8 |
| [Intervals](#intervals) | 1 | 4 | 1 | 6 |
| [Math & Geometry](#math--geometry) | 3 | 4 | 1 | 8 |
| [Bit Manipulation](#bit-manipulation) | 8 | 0 | 0 | 8 |

## 🗂️ Repository Structure

```
dsa-practice/
├── README.md
└── problems/
    ├── arrays_and_hashing/
    │   ├── easy/
    │   │   ├── problem_name.py
    │   │   └── README.md
    │   ├── medium/
    │   └── hard/
    ├── two_pointers/
    ├── sliding_window/
    ├── stack/
    ├── binary_search/
    ├── linked_list/
    ├── trees/
    ├── tries/
    ├── heap/
    ├── backtracking/
    ├── graphs/
    ├── advanced_graphs/
    ├── 1d_dynamic_programming/
    ├── 2d_dynamic_programming/
    ├── greedy/
    ├── intervals/
    ├── math_geometry/
    └── bit_manipulation/
```

## 📖 Problem Format

Each problem includes:

1. **Solution File (.py)**
   - Comprehensive problem description
   - LeetCode problem number
   - Difficulty level
   - Pattern classification
   - Top companies that ask this question
   - Multiple examples with explanations
   - Constraints
   - Detailed approach explanation
   - Time and space complexity analysis
   - Working solution with type hints
   - Comprehensive test cases

2. **README.md**
   - Concept explanation
   - Key insights and intuition
   - Pattern identification
   - Common pitfalls
   - Related problems
   - Visual explanations where applicable

## 🎯 How to Use This Repository

### Practice by Topic
```bash
# Navigate to a specific topic
cd problems/arrays_and_hashing/medium/

# Run a solution
python two_sum.py
```

### Practice by Difficulty
```bash
# Find all easy problems
find problems -type d -name "easy"

# Run all tests in medium problems
find problems/*/medium -name "*.py" -exec python {} \;
```

### Study a Concept
Each problem directory contains a README.md explaining:
- The core concept and pattern
- When to apply this technique
- Common variations
- Tips and tricks

## 🏆 Problem Categories

### Arrays & Hashing
Master fundamental array operations and hash table usage for O(1) lookups.
- **Key Patterns:** Frequency counting, two pointers, prefix sums
- **Path:** `problems/arrays_and_hashing/`

### Two Pointers
Optimize array/string problems using left and right pointer technique.
- **Key Patterns:** Opposite direction, same direction, fast-slow
- **Path:** `problems/two_pointers/`

### Sliding Window
Efficiently solve subarray/substring problems with dynamic window sizes.
- **Key Patterns:** Fixed window, variable window, substring matching
- **Path:** `problems/sliding_window/`

### Stack
Utilize LIFO structure for parsing, monotonic sequences, and nested problems.
- **Key Patterns:** Monotonic stack, expression evaluation, nested structures
- **Path:** `problems/stack/`

### Binary Search
Achieve O(log n) search in sorted or rotated arrays.
- **Key Patterns:** Search space reduction, finding boundaries, rotated arrays
- **Path:** `problems/binary_search/`

### Linked List
Manipulate pointer-based data structures with in-place operations.
- **Key Patterns:** Fast-slow pointers, reversal, dummy nodes
- **Path:** `problems/linked_list/`

### Trees
Traverse and manipulate binary trees and binary search trees.
- **Key Patterns:** DFS (preorder, inorder, postorder), BFS, recursion
- **Path:** `problems/trees/`

### Tries
Build prefix trees for efficient string operations and autocomplete.
- **Key Patterns:** Prefix matching, word search, dictionary operations
- **Path:** `problems/tries/`

### Heap / Priority Queue
Manage dynamic datasets with O(log n) insertions and O(1) access to min/max.
- **Key Patterns:** K-th element, median finding, merge operations
- **Path:** `problems/heap/`

### Backtracking
Generate all possible solutions through recursive exploration.
- **Key Patterns:** Subsets, permutations, combinations, constraint satisfaction
- **Path:** `problems/backtracking/`

### Graphs
Traverse and analyze graph structures with DFS, BFS, and Union Find.
- **Key Patterns:** Connected components, cycle detection, topological sort
- **Path:** `problems/graphs/`

### Advanced Graphs
Implement sophisticated graph algorithms for weighted graphs and networks.
- **Key Patterns:** Dijkstra's, MST, shortest paths, network flow
- **Path:** `problems/advanced_graphs/`

### 1-D Dynamic Programming
Solve optimization problems with one-dimensional state transitions.
- **Key Patterns:** Fibonacci-style, house robber, subsequences
- **Path:** `problems/1d_dynamic_programming/`

### 2-D Dynamic Programming
Handle complex state spaces with two-dimensional DP tables.
- **Key Patterns:** Grid problems, string matching, game theory
- **Path:** `problems/2d_dynamic_programming/`

### Greedy
Make locally optimal choices to find global optimums.
- **Key Patterns:** Interval scheduling, jump game, partitioning
- **Path:** `problems/greedy/`

### Intervals
Manage and merge time intervals efficiently.
- **Key Patterns:** Merge intervals, meeting rooms, sweep line
- **Path:** `problems/intervals/`

### Math & Geometry
Apply mathematical concepts and geometric algorithms.
- **Key Patterns:** Matrix manipulation, number theory, coordinate geometry
- **Path:** `problems/math_geometry/`

### Bit Manipulation
Optimize solutions using bitwise operations.
- **Key Patterns:** XOR tricks, bit masking, counting bits
- **Path:** `problems/bit_manipulation/`

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dsa-practice.git
   cd dsa-practice
   ```

2. **Choose your learning path**
   - Start with easy problems in each category
   - Follow the NeetCode roadmap order
   - Focus on weak areas

3. **Practice methodology**
   - Read the problem statement
   - Attempt to solve independently (20-30 min)
   - Review the solution and README
   - Implement from scratch
   - Solve related problems

## 📈 Study Plan Suggestions

### Beginner (4-6 weeks)
- Focus on Easy problems
- Complete Arrays & Hashing, Two Pointers, Sliding Window
- Build strong foundations in fundamental patterns

### Intermediate (8-12 weeks)
- Complete all Medium problems
- Master Trees, Graphs, and 1-D DP
- Practice pattern recognition

### Advanced (12-16 weeks)
- Tackle all Hard problems
- Focus on Advanced Graphs and 2-D DP
- Optimize solutions and reduce complexity

## 🎓 Additional Resources

- [NeetCode.io](https://neetcode.io/) - Video explanations for all problems
- [LeetCode](https://leetcode.com/) - Practice platform
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) - Time complexity reference

## 📝 Notes

- All solutions are tested and verified
- Problems are selected for maximum interview preparation value
- Each problem maps to actual interview questions from top tech companies
- Solutions prioritize clarity and optimal time/space complexity

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest improvements to explanations
- Add alternative solutions
- Improve test coverage

## 📄 License

This repository is for educational purposes. All problem statements are property of their respective owners (LeetCode, NeetCode).

---

**Last Updated:** November 12, 2025
**Status:** ✅ All 150 problems complete with explanations
