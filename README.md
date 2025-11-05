# DSA Practice

[![Tests](https://github.com/user/dsa-practice/workflows/Tests/badge.svg)](https://github.com/user/dsa-practice/actions)
[![Code Quality](https://github.com/user/dsa-practice/workflows/Code%20Quality/badge.svg)](https://github.com/user/dsa-practice/actions)

Interview prep - organized, simple, effective.

## Quick Start

```bash
# Install dependencies
make install

# Run all tests
make test

# Run tests with coverage
make test-coverage

# Format and lint code
make format
make lint
```

## Progress Overview

**Current Focus:** Week 2 - Hashing + Strings (50% complete)

**Total Solved:** 2 / TBD problems

| Category | Solved | Total | Progress |
|----------|--------|-------|----------|
| Arrays | 1 | TBD | ▓░░░░░░░░░ 10% |
| Strings | 1 | TBD | ▓░░░░░░░░░ 10% |
| Linked Lists | 0 | TBD | ░░░░░░░░░░ 0% |
| Trees | 0 | TBD | ░░░░░░░░░░ 0% |
| Graphs | 0 | TBD | ░░░░░░░░░░ 0% |
| Dynamic Programming | 0 | TBD | ░░░░░░░░░░ 0% |

### Difficulty Breakdown

- **Easy:** 1 ✓
- **Medium:** 0
- **Hard:** 1 ✓

## Problems

### Arrays (1/TBD)
- [x] [Dynamic Array](problems/arrays/dynamic_array.py) - Easy
  - Pattern: Arrays & Memory Management
  - Time: O(1) amortized
  - Space: O(n)

### Strings (1/TBD)
- [x] [Minimum Window Substring](problems/strings/min_window.py) - Hard
  - Pattern: Sliding Window + Hash Map
  - Companies: Amazon, Facebook, Google, Microsoft
  - Time: O(m + n)
  - Space: O(k)

### Linked Lists (0/TBD)
See [problems/linked_lists/README.md](problems/linked_lists/README.md) for planned problems.

### Trees (0/TBD)
See [problems/trees/README.md](problems/trees/README.md) for planned problems.

### Graphs (0/TBD)
See [problems/graphs/README.md](problems/graphs/README.md) for planned problems.

### Dynamic Programming (0/TBD)
See [problems/dp/README.md](problems/dp/README.md) for planned problems.

---

## Repository Structure

```
dsa-practice/
├── problems/           # Solutions organized by category
│   ├── arrays/
│   ├── strings/
│   ├── linked_lists/
│   ├── trees/
│   ├── graphs/
│   └── dp/
├── tests/             # Pytest test suite
├── templates/         # Templates for new problems
├── .github/           # CI/CD workflows
│   └── workflows/
├── requirements.txt   # Python dependencies
├── pyproject.toml    # Project configuration
└── Makefile          # Development commands
```

## Features

- **Comprehensive Test Suite**: pytest with coverage reporting
- **Code Quality**: Black formatting, flake8 linting, mypy type checking
- **CI/CD**: Automated testing via GitHub Actions
- **Solution Templates**: Consistent structure for all problems
- **Documentation**: Each problem includes description, examples, complexity analysis

## Development Workflow

### Adding a New Problem

1. **Copy the template:**
   ```bash
   cp templates/solution_template.py problems/[category]/[problem_name].py
   cp templates/test_template.py tests/test_[problem_name].py
   ```

2. **Implement the solution:**
   - Fill in problem description
   - Implement the algorithm
   - Add time/space complexity

3. **Write tests:**
   - Add test cases covering edge cases
   - Run tests: `make test`

4. **Verify quality:**
   ```bash
   make run-all-checks  # Runs format, lint, type-check, and tests
   ```

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific test file
pytest tests/test_dynamic_array.py -v
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Run all checks
make run-all-checks
```

## Problem-Solving Patterns

Common patterns used in this repository:

| Pattern | Problems | Description |
|---------|----------|-------------|
| Two Pointers | - | Use two pointers to traverse data structure |
| Sliding Window | Min Window Substring | Maintain a window of elements |
| Hash Map | Min Window Substring | Use hash table for O(1) lookups |
| Arrays & Memory | Dynamic Array | Manual memory management |
| DFS/BFS | - | Tree/graph traversal |
| Dynamic Programming | - | Break down into subproblems |

## Contributing

This is a personal practice repository, but feel free to:
- Open issues for bugs or suggestions
- Submit PRs for improvements
- Use as a template for your own practice

## Resources

- [LeetCode](https://leetcode.com/)
- [NeetCode Roadmap](https://neetcode.io/roadmap)
- [AlgoExpert](https://www.algoexpert.io/)

---

**Last Updated:** 2025-11-05
