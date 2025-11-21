"""
PROBLEM: Design Add and Search Words Data Structure (211)
LeetCode: https://leetcode.com/problems/design-add-and-search-words-data-structure/
Difficulty: Medium
Pattern: Tries/Prefix Trees

Design a data structure that supports adding new words and searching for words
with wildcard support ('.' matches any single character).

Requirements:
- WordDictionary(): Initialize an empty dictionary
- add_word(word): Add a word to the dictionary
- search(word): Search for word with wildcard support
  - '.' can match any single character
  - Regular characters match themselves

Example:
    wd = WordDictionary()
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")
    wd.search("pad")         # returns False
    wd.search("bad")         # returns True
    wd.search(".ad")         # returns True (matches bad, dad, mad)
    wd.search("b..")         # returns True (matches bad)

Time Complexity:
  - addWord: O(m) where m is length of word
  - search: O(N * 26^m) worst case, where N is number of nodes, m is length of word

Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of words, M is avg length
"""


class TrieNode:
    """Node in the Trie structure for word dictionary."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class WordDictionary:
    """Data structure for adding and searching words with wildcard support."""

    def __init__(self):
        """Initialize an empty word dictionary."""
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        """
        Add a word to the dictionary.

        Args:
            word: String to add
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Search for a word with wildcard support.

        Args:
            word: String to search for ('.' can match any single character)

        Returns:
            True if word exists (with wildcards), False otherwise
        """
        def dfs(index: int, node: TrieNode) -> bool:
            # Base case: reached end of word
            if index == len(word):
                return node.is_end_of_word

            char = word[index]

            if char == ".":
                # Wildcard: try all children
                for child in node.children.values():
                    if dfs(index + 1, child):
                        return True
                return False
            else:
                # Regular character: must match exactly
                if char not in node.children:
                    return False
                return dfs(index + 1, node.children[char])

        return dfs(0, self.root)


# Tests
def test():
    wd = WordDictionary()

    # Test basic addWord and search
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")
    assert wd.search("bad") == True
    assert wd.search("dad") == True
    assert wd.search("mad") == True

    # Test non-existent word
    assert wd.search("pad") == False

    # Test wildcard with single dot
    assert wd.search(".ad") == True  # matches bad, dad, mad
    assert wd.search("b.d") == True
    assert wd.search("ba.") == True

    # Test wildcard with multiple dots
    assert wd.search("b..") == True
    assert wd.search("...") == True

    # Test wildcard no match
    assert wd.search(".ba") == False
    assert wd.search("...d") == False

    # Test single character
    wd.add_word("a")
    assert wd.search("a") == True
    assert wd.search(".") == True

    # Test longer words
    wd.add_word("hello")
    assert wd.search("hello") == True
    assert wd.search("h....") == True
    assert wd.search("hell.") == True
    assert wd.search("hel..") == True
    assert wd.search("h.llo") == True

    # Test case sensitivity
    assert wd.search("Hello") == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
