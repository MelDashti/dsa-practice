# Complete FAANG Interview Preparation

A comprehensive collection of **159 DSA problems** and **50+ System Design problems** for FAANG/MAANG interviews. Everything you need to ace coding and system design interviews at top tech companies.

##  📦 What's Inside

1. **[DSA Problems](#-dsa-problems-neetcode-150)** - 150 NeetCode problems + 9 bonus highly-asked FAANG problems
2. **[System Design](#-system-design)** - 50+ comprehensive system design documents

---

# 💻 DSA Problems - NeetCode 150 + Bonus

A complete collection of 150 curated coding interview problems from [NeetCode.io](https://neetcode.io/), organized by topic and difficulty level, **PLUS 9 additional highly-asked FAANG problems** to fill pattern gaps. Each problem includes detailed explanations, optimal solutions, and test cases.

## 📊 Progress

**Total Problems:** 159/159 ✅ (100% Complete)
- **NeetCode 150:** 150/150 ✅
- **Bonus FAANG Problems:** 9/9 ✅

### By Difficulty
- 🟢 **Easy:** 36 problems
- 🟡 **Medium:** 92 problems
- 🔴 **Hard:** 22 problems

## 📚 Problem Categories

Each category is organized into `easy/`, `medium/`, and `hard/` subdirectories with detailed README explanations.

| Category | Easy | Medium | Hard | Total | Bonus |
|----------|------|--------|------|-------|-------|
| [Arrays & Hashing](#arrays--hashing) | 4 | 4 | 2 | 10 | +1 |
| [Two Pointers](#two-pointers) | 1 | 3 | 1 | 5 | - |
| [Sliding Window](#sliding-window) | 1 | 4 | 1 | 6 | - |
| [Stack](#stack) | 2 | 5 | 2 | 9 | +2 |
| [Binary Search](#binary-search) | 1 | 6 | 1 | 8 | +1 |
| [Linked List](#linked-list) | 3 | 5 | 3 | 11 | - |
| [Trees](#trees) | 6 | 8 | 1 | 15 | - |
| [Tries](#tries) | 0 | 2 | 1 | 3 | - |
| [Heap / Priority Queue](#heap--priority-queue) | 2 | 5 | 2 | 9 | +2 |
| [Backtracking](#backtracking) | 0 | 8 | 1 | 9 | - |
| [Graphs](#graphs) | 1 | 11 | 2 | 14 | +1 |
| [Advanced Graphs](#advanced-graphs) | 0 | 3 | 3 | 6 | - |
| [1-D Dynamic Programming](#1-d-dynamic-programming) | 2 | 10 | 0 | 12 | - |
| [2-D Dynamic Programming](#2-d-dynamic-programming) | 0 | 8 | 4 | 12 | +1 |
| [Greedy](#greedy) | 1 | 8 | 0 | 9 | +1 |
| [Intervals](#intervals) | 1 | 4 | 1 | 6 | - |
| [Math & Geometry](#math--geometry) | 3 | 4 | 1 | 8 | - |
| [Bit Manipulation](#bit-manipulation) | 8 | 0 | 0 | 8 | - |

## 🗂️ Repository Structure

```
dsa-practice/
├── README.md
├── problems/                    # 150 DSA Problems
│   ├── arrays_and_hashing/
│   │   ├── easy/
│   │   │   ├── problem_name.py
│   │   │   └── README.md
│   │   ├── medium/
│   │   └── hard/
│   ├── two_pointers/
│   ├── sliding_window/
│   ├── stack/
│   ├── binary_search/
│   ├── linked_list/
│   ├── trees/
│   ├── tries/
│   ├── heap/
│   ├── backtracking/
│   ├── graphs/
│   ├── advanced_graphs/
│   ├── 1d_dynamic_programming/
│   ├── 2d_dynamic_programming/
│   ├── greedy/
│   ├── intervals/
│   ├── math_geometry/
│   └── bit_manipulation/
└── system_design/              # 50+ System Design Documents
    ├── README.md
    ├── fundamentals/
    ├── core_components/
    ├── social_media/
    ├── messaging/
    ├── location_based/
    ├── ecommerce_payments/
    ├── infrastructure/
    └── storage_data/
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

## 🎁 Bonus FAANG Problems

In addition to the complete NeetCode 150, we've added **9 highly-asked FAANG problems** that fill important pattern gaps:

### Pattern Gaps Filled
1. **Cyclic Sort** - First Missing Positive (Hard)
2. **Binary Search Boundaries** - Find First and Last Position (Medium)
3. **Expression Parsing** - Basic Calculator I & II (Hard & Medium)
4. **Two Heaps Pattern** - Sliding Window Median (Hard)
5. **K-way Merge** - K Pairs with Smallest Sums (Medium)
6. **Greedy + Heap** - Reorganize String (Medium)
7. **8-Directional BFS** - Shortest Path in Binary Matrix (Medium)
8. **2-D DP + Monotonic Stack** - Maximal Rectangle (Hard)

### Why These Problems?
- **High Interview Frequency**: Top 20 most asked at Amazon, Google, Meta
- **Pattern Diversity**: Cover patterns underrepresented in NeetCode 150
- **Difficulty Progression**: Mix of Medium and Hard to challenge advanced learners
- **Real Interview Questions**: All from actual 2024-2025 FAANG interviews

These bonus problems ensure you're prepared for **any** pattern that might appear in your interview!

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

---

# 🏗️ System Design

A comprehensive collection of 50+ system design problems covering all major areas asked in FAANG interviews. From fundamentals to complex distributed systems.

## 📊 Overview

**Total Designs:** 50+ comprehensive system design documents
**Categories:** 8 major topics
**Focus:** FAANG interview preparation

### By Difficulty
- 🟢 **Easy:** 8 problems (Fundamentals and simple systems)
- 🟡 **Medium:** 25+ problems (Production-scale systems)
- 🔴 **Hard:** 17+ problems (Complex distributed systems)

## 📚 System Design Categories

| Category | Easy | Medium | Hard | Total | Focus Area |
|----------|------|--------|------|-------|------------|
| **Fundamentals** | 3 | 3 | 3 | 9 | Core concepts |
| **Core Components** | 3 | 4 | 3 | 10 | Building blocks |
| **Social Media** | 1 | 4 | 2 | 7 | User content platforms |
| **Messaging** | 1 | 3 | 2 | 6 | Real-time communication |
| **Location-Based** | 1 | 3 | 2 | 6 | Geospatial services |
| **E-commerce & Payments** | 1 | 3 | 4 | 8 | Transactions |
| **Infrastructure** | 1 | 4 | 4 | 9 | Distributed systems |
| **Storage & Data** | 1 | 5 | 4 | 10 | Data management |

## 🗂️ System Design Structure

```
system_design/
├── README.md (comprehensive guide)
├── fundamentals/         (Scaling, Caching, Load Balancing, CAP, Consensus)
├── core_components/      (URL Shortener, Rate Limiter, Auth, ID Generator)
├── social_media/         (Instagram, Twitter, Reddit, TikTok, News Feed)
├── messaging/            (WhatsApp, Slack, Discord, Messenger)
├── location_based/       (Uber, Google Maps, Yelp, Proximity Service)
├── ecommerce_payments/   (Amazon, Payment System, UPI, Stock Exchange)
├── infrastructure/       (Kafka, Web Crawler, Metrics, Distributed Cache)
└── storage_data/         (Dropbox, YouTube, Netflix, S3, Zoom)
```

## 🎯 Top 15 Must-Know System Designs

1. **URL Shortener** - Classic entry-level problem
2. **Rate Limiter** - Appears in 80% of interviews
3. **Design Instagram** - Social media fundamentals
4. **Design Twitter** - Real-time feeds
5. **Design YouTube** - Video streaming
6. **Design WhatsApp** - Real-time messaging
7. **Design Uber** - Location-based services
8. **Design Amazon** - E-commerce at scale
9. **News Feed Algorithm** - Ranking systems
10. **Payment System** - Transaction consistency
11. **Consistent Hashing** - Distributed systems
12. **Design Kafka** - Message queues
13. **Design Dropbox** - File sync
14. **Web Crawler** - Data ingestion
15. **Unique ID Generator** - Distributed coordination

## 📖 Each Design Document Includes

1. Problem Statement & Requirements
2. Capacity Estimation (Traffic, Storage, Bandwidth)
3. High-Level Architecture with diagrams
4. API Design (REST/WebSocket)
5. Database Schema & justification
6. Detailed Component Design
7. Scalability & Performance considerations
8. Trade-offs & Alternatives
9. Monitoring & Operations
10. 15-30 Follow-up Questions

## 🚀 Quick Start - System Design

```bash
# Navigate to system design
cd system_design/

# Read the main guide
cat README.md

# Start with fundamentals
cd fundamentals/easy/
ls  # See all easy topics

# Study a specific design
cat scaling_basics.md
```

## 📈 System Design Study Plans

### 1-Week Crash Course
- Days 1-2: All Fundamentals
- Days 3-4: Top 5 must-know problems
- Days 5-6: Company-specific domains
- Day 7: Mock interviews

### 1-Month Comprehensive
- Week 1: Fundamentals + Core Components
- Week 2: Social Media + Messaging
- Week 3: Location + E-commerce
- Week 4: Infrastructure + Storage + Practice

### Interview-Ready Checklist
- ✅ Understand CAP theorem
- ✅ Know database scaling strategies
- ✅ Master caching patterns
- ✅ Can explain load balancing
- ✅ Understand distributed systems concepts
- ✅ Practiced top 15 designs
- ✅ Can do capacity estimation
- ✅ Know trade-offs for each design choice

---

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

**Last Updated:** November 15, 2025
**Status:**
- ✅ All 150 NeetCode problems complete with explanations
- ✅ 9 bonus highly-asked FAANG problems added
- ✅ All 50+ System Design documents complete
- ✅ **159 total DSA problems** - Ready for FAANG interviews!
