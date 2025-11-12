# Arrays & Hashing - Medium

## Concept/Pattern

Medium-level arrays and hashing problems introduce multi-dimensional thinking and more complex hash table applications. You'll encounter problems requiring grouped data, frequency analysis, or maintaining multiple mappings simultaneously. These challenges often involve nested structures (hash of hashes, hash of lists) or clever encoding schemes. The pattern extends beyond simple lookups to transformations, aggregations, and strategic data organization.

## Key Insights

At this level, the key insight is that the **structure of your hash table matters as much as using one**. You need to choose the right key (which might be derived or composite) and the right value type (might be a list, set, or another hash). Problems often require you to process data in a specific way before or after hashing. Understanding how to normalize data (like sorting characters in an anagram) or use mathematical properties (like product of all except self) becomes essential.

## When to Use This Approach

Medium hashing problems typically involve:
- **Grouping by property**: "Group all anagrams together"
- **Frequency analysis**: "Find k most frequent elements"
- **Multiple relationships**: "Track rows, columns, and boxes in Sudoku"
- **Derived keys**: Using transformations as hash keys
- **Array manipulation**: Problems where hashing supplements array operations
- **Optimization puzzles**: Where naive approaches timeout

Look for problems with words like "group," "frequency," "duplicate in constraints," or "valid configuration."

## Common Pitfalls

1. **Wrong key choice**: Using the raw value when you should use a sorted, encoded, or derived key
2. **Inefficient sorting**: Repeatedly sorting the same data instead of sorting once
3. **Overusing nested loops**: Hash tables should eliminate at least one loop dimension
4. **Mutable keys**: Lists can't be dictionary keys; use tuples or strings instead
5. **Default dict confusion**: Not using `collections.defaultdict` when it would simplify code
6. **Integer overflow**: In problems like "Product Except Self," be mindful of zero handling
7. **Space for time**: Not recognizing when O(n) space is acceptable for O(n) time

## Tips for Solving Problems

- **Identify the grouping criteria**: What makes items "belong together"?
- **Normalize your keys**: Sort strings, convert to tuples, or create canonical representations
- **Use Counter and defaultdict**: Python's `collections` module is your friend
- **Break into steps**: Build the hash structure, then extract/transform the result
- **Think about data flow**: Input → Transformation → Hash Table → Output processing
- **Consider time-space tradeoffs**: Sometimes multiple passes with hashing beats one pass with nested loops
- **Draw examples**: Visualize your hash table structure with sample data
- **Handle duplicates explicitly**: Decide if you need sets (unique) or lists (allow duplicates) as values
