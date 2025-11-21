"""
PROBLEM: Implement Trie (208)
LeetCode: https://leetcode.com/problems/implement-trie-prefix-tree/
Difficulty: Medium
Pattern: Tries/Prefix Trees

Implement a Trie (prefix tree) data structure.

A Trie is a tree-based data structure that efficiently stores and retrieves strings.
Each node represents a character, and paths from root to nodes form words.

Requirements:
- Trie(): Initialize an empty trie
- insert(word): Insert a word into the trie
- search(word): Return True if word exists in trie
- starts_with(prefix): Return True if any word starts with prefix

Example:
    trie = Trie()
    trie.insert("apple")
    trie.search("apple")      # returns True
    trie.search("app")        # returns False
    trie.starts_with("app")    # returns True
    trie.insert("app")
    trie.search("app")        # returns True

Time Complexity:
  - insert: O(m) where m is length of word
  - search: O(m) where m is length of word
  - startsWith: O(m) where m is length of prefix

Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of words, M is avg length
"""


class TrieNode:
    """Node in the Trie structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """Trie data structure for efficient string storage and retrieval."""

    def __init__(self):
        """Initialize an empty trie with root node."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Args:
            word: String to insert
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Search for an exact word in the trie.

        Args:
            word: String to search for

        Returns:
            True if word exists, False otherwise
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.

        Args:
            prefix: String prefix to search for

        Returns:
            True if any word starts with prefix, False otherwise
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


# Tests
def test():
    trie = Trie()

    # Test insertion and search
    trie.insert("apple")
    assert trie.search("apple") == True
    assert trie.search("app") == False
    assert trie.starts_with("app") == True

    # Test after inserting prefix
    trie.insert("app")
    assert trie.search("app") == True

    # Test multiple words
    trie.insert("application")
    assert trie.search("application") == True
    assert trie.starts_with("appl") == True
    assert trie.search("appl") == False

    # Test non-existent word
    assert trie.search("orange") == False
    assert trie.starts_with("orange") == False

    # Test single character
    trie.insert("a")
    assert trie.search("a") == True
    assert trie.starts_with("a") == True

    # Test case sensitivity
    assert trie.search("Apple") == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
