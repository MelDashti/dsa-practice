# Tries - Medium Problems

## Core Concepts

### What is a Trie?

A **Trie** (pronounced "try") or **Prefix Tree** is a specialized tree data structure used to store and retrieve strings efficiently.

**Key Properties**:
- Each node represents a character
- Root represents empty string
- Path from root to node represents a string prefix
- Nodes can be marked as end of valid words

**Why Use Tries?**
- Fast prefix-based operations: O(m) where m is string length
- Space-efficient for storing many strings with common prefixes
- Excellent for autocomplete, spell check, IP routing

### Trie vs Other Data Structures

| Operation | Trie | Hash Set | Sorted Array |
|-----------|------|----------|--------------|
| Insert word | O(m) | O(m) | O(n log n) |
| Search word | O(m) | O(m) | O(log n) |
| Search prefix | O(m) | O(n*m) | O(log n + k) |
| Space | O(ALPHABET * N * M) | O(N*M) | O(N*M) |

Where:
- m = length of word
- n = number of words
- N = total number of nodes
- M = average string length

**Trie Advantage**: Prefix operations are extremely efficient!

### Basic Trie Structure

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # Maps character to TrieNode
        self.is_end_of_word = False  # Marks if word ends here

class Trie:
    def __init__(self):
        self.root = TrieNode()
```

### Visual Example

After inserting "cat", "car", "card", "dog":

```
         root
        /    \
       c      d
       |      |
       a      o
      / \     |
     t   r    g
         |    [end]
         d
         [end]
    [end]
```

**Key Observations**:
- "ca" is a common prefix for cat, car, card
- Each path from root represents a prefix
- Marked nodes indicate complete words

## Problems in This Section

### 1. Implement Trie (Prefix Tree) (LC 208)

**Concept**: Design and implement a trie with insert, search, and startsWith operations

**Required Operations**:
1. `insert(word)`: Add word to trie
2. `search(word)`: Return true if word exists
3. `startsWith(prefix)`: Return true if any word has this prefix

**Pattern**: Basic trie implementation

**Time Complexity**:
- Insert: O(m) where m is word length
- Search: O(m)
- StartsWith: O(m)

**Space Complexity**: O(N * M * ALPHABET_SIZE) where N is number of words

#### Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie"""
        node = self.root

        for char in word:
            # Create new node if character doesn't exist
            if char not in node.children:
                node.children[char] = TrieNode()

            # Move to child node
            node = node.children[char]

        # Mark end of word
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Return True if word is in trie"""
        node = self.root

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]

        # Word must end at a marked node
        return node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """Return True if any word starts with prefix"""
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        # Any node reached means prefix exists
        return True
```

#### Key Insights

1. **Children Storage**: Use dictionary for flexible alphabet (could use array for fixed alphabet)
2. **Word End Marker**: Essential to distinguish "car" from "card" prefix
3. **Node Traversal**: Follow character path, create nodes as needed
4. **Prefix Check**: Don't need to check `is_end_of_word` for startsWith

#### Common Pitfalls

1. **Forgetting is_end_of_word**: "card" contains "car" but they're different words
2. **Not creating nodes during insert**: Must build path for new characters
3. **Returning wrong value in startsWith**: Any reached node is valid prefix

#### Optimizations

```python
# Using defaultdict for cleaner code
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end = False

# For lowercase letters only (space optimization)
class TrieNode:
    def __init__(self):
        self.children = [None] * 26  # Only a-z
        self.is_end = False

    def _index(self, char):
        return ord(char) - ord('a')
```

### 2. Design Add and Search Words Data Structure (LC 211)

**Concept**: Extend trie to support wildcard search with '.' matching any character

**Required Operations**:
1. `addWord(word)`: Add word to data structure
2. `search(word)`: Search with '.' as wildcard for any character

**Pattern**: Trie with DFS for wildcard matching

**Time Complexity**:
- Add: O(m)
- Search without wildcards: O(m)
- Search with wildcards: O(n) worst case, where n is total nodes

**Space Complexity**: O(N * M)

#### Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """Standard trie insertion"""
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Search with '.' as wildcard"""
        def dfs(node, index):
            # Base case: reached end of word
            if index == len(word):
                return node.is_end_of_word

            char = word[index]

            if char == '.':
                # Try all possible children
                for child in node.children.values():
                    if dfs(child, index + 1):
                        return True
                return False
            else:
                # Regular character match
                if char not in node.children:
                    return False
                return dfs(node.children[char], index + 1)

        return dfs(self.root, 0)
```

#### Key Insights

1. **Wildcard Handling**: Must explore all branches when encountering '.'
2. **DFS Approach**: Recursively explore possible paths
3. **Early Termination**: Return True immediately when match found
4. **Regular Characters**: Follow single path like normal search

#### Algorithm Walkthrough

Example: Search ".ad" in trie containing ["bad", "dad", "mad"]

```
         root
        / | \
       b  d  m
       |  |  |
       a  a  a
       |  |  |
       d  d  d

Step 1: '.' at root -> explore all children (b, d, m)
Step 2: 'a' -> check if each has 'a' child
Step 3: 'd' -> check if 'a' child has 'd' child
Result: Found matches through all paths
```

#### Edge Cases

```python
# Word with multiple wildcards
search("a.d.e")  # Must handle multiple branches

# All wildcards
search("....")  # Match any 4-letter word

# Empty string
search("")  # Should return False

# Prefix vs full word
addWord("bad")
search("b")  # Should return False (not marked as end)
search("bad")  # Should return True
```

#### Common Pitfalls

1. **Not using recursion for wildcards**: Iterative approach very complex
2. **Checking all children**: When '.' encountered, must try all branches
3. **Forgetting base case**: Must check is_end_of_word when index reaches end
4. **Not handling edge cases**: Empty string, all wildcards, no matches

#### Optimization Techniques

```python
# Optimization 1: Length-based grouping
class WordDictionary:
    def __init__(self):
        self.words_by_length = defaultdict(set)

    def addWord(self, word):
        self.words_by_length[len(word)].add(word)

    def search(self, word):
        # Only check words of same length
        for w in self.words_by_length[len(word)]:
            if self._matches(word, w):
                return True
        return False

# Optimization 2: Early termination with length check
def search(self, word):
    if '.' not in word:
        # No wildcard, use regular search
        return self._regular_search(word)
    else:
        return self._wildcard_search(word)
```

## Advanced Patterns

### Pattern 1: Basic Trie Template

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        # Add extra fields as needed:
        # self.count = 0  # For counting
        # self.word = None  # For storing word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
```

### Pattern 2: DFS on Trie for Wildcard

```python
def wildcard_search(word):
    def dfs(node, index):
        if index == len(word):
            return node.is_end

        if word[index] == '.':
            # Branch on all children
            return any(dfs(child, index + 1)
                      for child in node.children.values())
        else:
            # Follow specific path
            if word[index] not in node.children:
                return False
            return dfs(node.children[word[index]], index + 1)

    return dfs(root, 0)
```

### Pattern 3: Collecting Results from Trie

```python
def get_all_words_with_prefix(prefix):
    """Get all words starting with prefix"""
    # Navigate to prefix node
    node = root
    for char in prefix:
        if char not in node.children:
            return []
        node = node.children[char]

    # DFS to collect all words from this node
    results = []

    def dfs(node, path):
        if node.is_end:
            results.append(prefix + path)

        for char, child in node.children.items():
            dfs(child, path + char)

    dfs(node, "")
    return results
```

## Space Optimization Techniques

### 1. Array vs Dictionary for Children

```python
# Dictionary (flexible, sparse)
children = {}  # Only store existing characters

# Array (fast, dense)
children = [None] * 26  # Pre-allocate for a-z

# Choose based on:
# - Alphabet size (small = array, large = dict)
# - Density of children (sparse = dict, dense = array)
```

### 2. Compressed Tries (Radix Trees)

For memory efficiency, compress chains of single-child nodes:

```
# Standard Trie:
a -> b -> c -> d -> e

# Compressed:
"abcde"
```

### 3. Storing Words vs Just Markers

```python
# Approach 1: Store word at end node
node.word = "complete_word"  # Uses more space but convenient

# Approach 2: Just mark end
node.is_end = True  # Less space, need to reconstruct word
```

## Common Use Cases

### 1. Autocomplete
```python
def autocomplete(prefix):
    # Find prefix node
    # DFS to collect all completions
    # Return top k most frequent
    pass
```

### 2. Spell Checker
```python
def spell_check(word):
    # Search exact match
    # If not found, find similar words (edit distance)
    pass
```

### 3. IP Routing
```python
# Store IP prefixes
# Find longest matching prefix for routing
```

### 4. Dictionary with Prefix Count
```python
class PrefixCount:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1  # Track words with this prefix
        node.is_end = True
```

## Complexity Analysis

### Time Complexity

| Operation | Best Case | Worst Case | Average |
|-----------|-----------|------------|---------|
| Insert | O(m) | O(m) | O(m) |
| Search | O(1) | O(m) | O(m) |
| Prefix | O(1) | O(m) | O(m) |
| Wildcard | O(m) | O(n) | O(m * b^w) |

Where:
- m = word length
- n = total nodes in trie
- b = branching factor
- w = number of wildcards

### Space Complexity

**Per Node**: O(ALPHABET_SIZE)
- Dictionary: O(k) where k is number of actual children
- Array: O(ALPHABET_SIZE) always

**Total**: O(N * M * ALPHABET_SIZE)
- N = number of words
- M = average word length
- Can be less with shared prefixes

## Tips for Trie Problems

1. **Understand Operations**: Insert is straightforward; search variations are key
2. **Choose Data Structure**: Dict for flexibility, array for speed (if fixed alphabet)
3. **Mark Word Ends**: Essential for distinguishing words from prefixes
4. **Use DFS for Wildcards**: Recursion handles branching naturally
5. **Optimize for Use Case**: Consider space vs. time trade-offs
6. **Test Edge Cases**: Empty strings, single character, all same character

## Common Mistakes

1. **Not marking word end**: Can't distinguish "car" from "care" prefix
2. **Incorrect wildcard handling**: Must explore all branches
3. **Memory issues**: Using arrays for large alphabets wastes space
4. **Not handling empty input**: Edge case in most operations
5. **Confusing search vs startsWith**: Different return conditions

## Practice Strategy

1. **Master basic implementation**: Insert, search, startsWith
2. **Add wildcard search**: Understand DFS on trie
3. **Extend functionality**: Count words, find all words with prefix
4. **Optimize**: Try both dict and array implementations
5. **Real applications**: Implement autocomplete, spell checker

## Beyond These Problems

Once comfortable with these, explore:
- **Prefix and Suffix Search** (LC 745): Combine prefix and suffix tries
- **Replace Words** (LC 648): Trie for word replacement
- **Map Sum Pairs** (LC 677): Trie with value aggregation
- **Maximum XOR** (LC 421): Binary trie for XOR problems
- **Palindrome Pairs** (LC 336): Trie with reverse strings
