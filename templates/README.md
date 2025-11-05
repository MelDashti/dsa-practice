# Solution Templates

This directory contains templates to maintain consistency across all DSA problems.

## Files

### `solution_template.py`
Template for implementing new DSA problems. Includes:
- Structured problem description
- Type hints
- Docstrings
- Time/space complexity
- Example usage

### `test_template.py`
Template for creating test files. Includes:
- pytest class structure
- Common edge cases
- Setup method for fixtures

## Usage

### Creating a New Problem

1. Copy the solution template:
   ```bash
   cp templates/solution_template.py problems/[category]/[problem_name].py
   ```

2. Copy the test template:
   ```bash
   cp templates/test_template.py tests/test_[problem_name].py
   ```

3. Fill in the placeholders:
   - Replace `[Problem Name]`, `[Difficulty]`, `[Pattern]`
   - Add problem description and examples
   - Implement the solution
   - Update test cases

4. Run tests:
   ```bash
   pytest tests/test_[problem_name].py -v
   ```

## Template Guidelines

- **Type Hints**: Always include type hints for parameters and return values
- **Docstrings**: Document the purpose, args, and return values
- **Complexity**: Always specify time and space complexity
- **Tests**: Include at least 5 test cases covering edge cases
- **Naming**: Use snake_case for functions and methods
