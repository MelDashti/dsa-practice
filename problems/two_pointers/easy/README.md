# Two Pointers - Easy

## Concept/Pattern

The two pointers technique uses two indices that traverse an array or string, typically from opposite ends moving toward each other, or both starting from one end moving in the same direction at different speeds. At the easy level, this pattern shines in problems involving palindrome checking, removing duplicates, or finding pairs. The fundamental concept is reducing nested loops by having pointers move intelligently based on problem conditions, turning O(n²) problems into O(n) solutions.

## Key Insights

The key insight with two pointers is that **you can make progress from both ends simultaneously** or **maintain a sliding relationship between pointers**. For palindromes, comparing from both ends lets you fail fast when characters don't match. For sorted arrays, moving pointers based on comparison results eliminates the need for nested loops. The pattern works because you can definitively rule out possibilities with each pointer movement, ensuring you don't need to revisit elements. Understanding when to move which pointer is the core skill.

## When to Use This Approach

Use two pointers when you see:
- **Palindrome problems**: Checking if strings read the same forwards and backwards
- **Sorted array operations**: Finding pairs, removing duplicates, or merging
- **String manipulation**: Reversing, comparing, or cleaning strings in-place
- **Meeting in the middle**: Where processing from both ends makes sense
- **Opposite direction traversal**: Left pointer moves right, right pointer moves left
- **Skip or ignore conditions**: Filtering out characters (like non-alphanumeric in palindromes)

If the problem involves symmetry, sorted data, or mentions "in-place" with O(1) space, consider two pointers.

## Common Pitfalls

1. **Off-by-one errors**: Forgetting whether to use `<` or `<=` in while conditions
2. **Not handling edge cases**: Empty strings, single characters, or all spaces
3. **Case sensitivity**: Forgetting to normalize case in string comparisons
4. **Invalid character skipping**: Not properly skipping non-alphanumeric characters in palindromes
5. **Pointer crossing**: Not checking if left pointer has passed right pointer
6. **In-place confusion**: Trying to modify strings (which are immutable in Python)
7. **Overthinking**: Using extra space when pointers alone would suffice

## Tips for Solving Problems

- **Draw it out**: Visualize pointers moving with a small example
- **Start with boundaries**: Initialize left at 0 and right at len-1 for opposite direction
- **Define movement rules**: Clearly decide when to move each pointer
- **Handle invalid data**: Skip characters that don't match your criteria (spaces, punctuation)
- **Normalize input**: Convert to lowercase, filter characters, or clean data first
- **Check termination**: Ensure your loop ends when pointers meet or cross
- **Test edge cases**: Empty input, single element, all same characters, all invalid characters
- **Consider helper functions**: For character validation or comparison logic
- **Think about returns**: What happens if you exit the loop? That's usually your answer
- **Compare with brute force**: Convince yourself two pointers visits fewer combinations than nested loops
