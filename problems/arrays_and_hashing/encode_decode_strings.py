"""
PROBLEM: Encode and Decode Strings (LeetCode 271)
Difficulty: Medium
Pattern: Arrays & Hashing, String
Companies: Google, Facebook, Amazon

Design an algorithm to encode a list of strings to a string. The encoded string
is then sent over the network and is decoded back to the original list of strings.

Please implement encode and decode methods.

Example 1:
    Input: ["lint","code","love","you"]
    Output: ["lint","code","love","you"]
    Explanation:
    One possible encode method is: "lint:;code:;love:;you"

Example 2:
    Input: ["we", "say", ":", "yes"]
    Output: ["we", "say", ":", "yes"]
    Explanation: Need to handle special characters

Constraints:
- 0 <= strs.length < 200
- 0 <= strs[i].length < 200
- strs[i] contains any possible characters out of 256 valid ASCII characters

Approach:
1. For encoding: Use length prefix - "length#string"
2. For example: ["we","say",":","yes"] -> "2#we3#say1#:3#yes"
3. For decoding: Read length, then read that many characters
4. This handles any special characters including delimiters

Time: O(n) where n is total characters in all strings
Space: O(n) for the encoded string
"""

from typing import List


class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        encoded = ""
        for s in strs:
            encoded += str(len(s)) + "#" + s
        return encoded

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result = []
        i = 0

        while i < len(s):
            # Find the delimiter
            j = i
            while s[j] != '#':
                j += 1

            # Get the length
            length = int(s[i:j])

            # Extract the string
            i = j + 1
            result.append(s[i:i + length])

            # Move to next string
            i += length

        return result


# Tests
def test():
    codec = Codec()

    # Test 1
    strs1 = ["lint","code","love","you"]
    encoded1 = codec.encode(strs1)
    decoded1 = codec.decode(encoded1)
    assert decoded1 == strs1

    # Test 2: With special characters
    strs2 = ["we", "say", ":", "yes"]
    encoded2 = codec.encode(strs2)
    decoded2 = codec.decode(encoded2)
    assert decoded2 == strs2

    # Test 3: Empty strings
    strs3 = ["", "hello", "", "world"]
    encoded3 = codec.encode(strs3)
    decoded3 = codec.decode(encoded3)
    assert decoded3 == strs3

    # Test 4: Empty list
    strs4 = []
    encoded4 = codec.encode(strs4)
    decoded4 = codec.decode(encoded4)
    assert decoded4 == strs4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
