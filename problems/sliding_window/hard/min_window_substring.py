"""
PROBLEM: Minimum Window Substring (LeetCode 76)
LeetCode: https://leetcode.com/problems/minimum-window-substring/
Difficulty: Hard
Pattern: Sliding Window + Hash Map
Companies: Amazon, Facebook, Google, Microsoft

Given two strings s and t, find the smallest substring in s that contains
all characters of t (including duplicates). Return "" if none exists.

Example 1:
    s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"

Example 2:
    s = "a", t = "a"
    Output: "a"

Example 3:
    s = "a", t = "aa"
    Output: ""  (need two 'a's)

Constraints:
- 1 <= s.length, t.length <= 10^5
- Consists of English letters

Approach:
1. Create frequency map for t
2. Use sliding window (left, right pointers)
3. Expand right: add chars to window
4. Contract left: when valid, try to minimize
5. Track minimum window found

Time: O(m + n) where m=len(s), n=len(t)
Space: O(k) where k=unique chars
"""

from collections import Counter


class Solution:
    def min_window(self, s: str, t: str) -> str:
        if not s or not t: 
            return ""
        
        freq_t = Counter(t) 
        required = len(freq_t)
        
        # sliding window variables 
        left = 0 
        formed = 0 # tracks how many unique chars in window meet the req
        window = {} # Freq map of current window 
        
        # Result: (window_length, left, right)
        min_len = float('inf')
        min_left = 0 
        min_right = 0 
        
        for right, letter in enumerate(s): 
            window[letter] = window.get(letter, 0) + 1
            
            if letter in freq_t and window[letter] == freq_t[letter]: 
                formed +=1 
            
            # try to contract window while it's valid 
            while formed == required and left <= right: 
                
                window_len = right - left + 1
                if window_len < min_len: 
                    min_len = window_len 
                    min_left = left
                    min_right = right
                    
                # remove leftmost character from window
                left_char = s[left]
                window[left_char] -= 1
                
                # check if removing left_char makes window invalid
                if left_char in freq_t and window[left_char] < freq_t[left_char]:
                    formed -= 1

                left += 1
            
        return "" if min_len == float('inf') else s[min_left:min_right + 1]

# Tests
def test():
    sol = Solution()

    assert sol.min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert sol.min_window("a", "a") == "a"
    assert sol.min_window("a", "aa") == ""

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
