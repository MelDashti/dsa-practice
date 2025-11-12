# Arrays & Hashing - Easy

## Concept/Pattern

Arrays and hashing at the easy level focus on fundamental data structure operations and understanding how to leverage hash tables (dictionaries/sets in Python) for constant-time lookups. These problems typically involve checking existence, finding duplicates, or mapping relationships between elements. The key insight is recognizing when O(1) lookup time can replace O(n) search operations.

## Key Insights

The most important realization in this category is that hash tables trade space for time complexity. When you need to check if an element exists, count occurrences, or maintain a mapping, a hash table is often your best friend. For arrays, you'll frequently iterate once while building your hash structure, then use it to answer questions in constant or linear time. Understanding that "seen before" or "find pair" problems almost always benefit from hashing is crucial.

## When to Use This Approach

Use arrays and hashing when you encounter problems asking about:
- **Duplicate detection**: "Does this array contain duplicates?"
- **Pair finding**: "Find two numbers that sum to a target"
- **Frequency counting**: "How many times does each element appear?"
- **Mapping relationships**: "Are these two strings anagrams?"
- **Set operations**: "What elements appear in both arrays?"

If the problem involves searching, matching, or tracking what you've seen, hashing is likely the solution.

## Common Pitfalls

1. **Over-complicating with sorting**: Many beginners sort first when hashing would be simpler and more efficient
2. **Forgetting edge cases**: Empty arrays, single elements, or all duplicates need special handling
3. **Hash collisions concern**: Python's dictionaries handle this internally; don't overthink it
4. **Space complexity oversight**: Remember you're using O(n) extra space with hash tables
5. **Modifying while iterating**: Be careful when adding to a hash table during iteration

## Tips for Solving Problems

- **Read carefully**: Determine if you need to return indices, values, or boolean results
- **Think hash first**: Ask yourself, "Could a hash table make this O(1) lookup?"
- **Consider multiple passes**: Sometimes two passes (one to build hash, one to query) is cleaner than one complex pass
- **Use appropriate structures**: Sets for existence checks, dictionaries for counts/mappings
- **Test edge cases**: Always check empty input, single element, and all same elements
- **Optimize later**: Get a working hash solution first, then consider if you need better space complexity
