"""
PROBLEM: Design Twitter (LeetCode 355)
LeetCode: https://leetcode.com/problems/design-twitter/
Difficulty: Medium
Pattern: Heap, Hash Table, Design
Companies: Amazon, Twitter, Google, Facebook

Design a simplified version of Twitter where users can post tweets, follow/unfollow
another user, and is able to see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:
- Twitter() Initializes your twitter object.
- void post_tweet(int user_id, int tweet_id) Composes a new tweet with ID tweet_id by
  the user user_id. Each call to this function will be made with a unique tweet_id.
- List<Integer> get_news_feed(int user_id) Retrieves the 10 most recent tweet IDs in
  the user's news feed. Each item in the news feed must be posted by users who the
  user followed or by the user themself. Tweets must be ordered from most recent
  to least recent.
- void follow(int follower_id, int followee_id) The user with ID follower_id started
  following the user with ID followee_id.
- void unfollow(int follower_id, int followee_id) The user with ID follower_id started
  unfollowing the user with ID followee_id.

Example 1:
    Input:
    ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
    [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
    Output:
    [null, null, [5], null, null, [6, 5], null, [5]]

    Explanation:
    Twitter twitter = new Twitter();
    twitter.post_tweet(1, 5); // User 1 posts a new tweet (id = 5).
    twitter.get_news_feed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
    twitter.follow(1, 2);    // User 1 follows user 2.
    twitter.post_tweet(2, 6); // User 2 posts a new tweet (id = 6).
    twitter.get_news_feed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
    twitter.unfollow(1, 2);  // User 1 unfollows user 2.
    twitter.get_news_feed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.

Constraints:
- 1 <= user_id, follower_id, followee_id <= 500
- 0 <= tweet_id <= 10^4
- All the tweets have unique IDs.
- At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow.

Approach:
1. Store tweets for each user with timestamp
2. Store followee set for each user
3. For getNewsFeed, merge tweets from user and all followees
4. Use max heap to get 10 most recent tweets
5. Use global counter for timestamps

Time:
- postTweet: O(1)
- follow/unfollow: O(1)
- getNewsFeed: O(n log k) where n is total tweets, k is 10
Space: O(users + tweets)
"""

import heapq
from collections import defaultdict


class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)  # user_id -> list of (time, tweet_id)
        self.following = defaultdict(set)  # user_id -> set of followeeIds

    def post_tweet(self, user_id: int, tweet_id: int) -> None:
        self.tweets[user_id].append((self.time, tweet_id))
        self.time += 1

    def get_news_feed(self, user_id: int) -> list[int]:
        # Get tweets from user and all followees
        min_heap = []

        # Add user's own tweets
        for time, tweet_id in self.tweets[user_id]:
            heapq.heappush(min_heap, (time, tweet_id))
            if len(min_heap) > 10:
                heapq.heappop(min_heap)

        # Add followees' tweets
        for followee_id in self.following[user_id]:
            for time, tweet_id in self.tweets[followee_id]:
                heapq.heappush(min_heap, (time, tweet_id))
                if len(min_heap) > 10:
                    heapq.heappop(min_heap)

        # Extract and reverse to get most recent first
        result = []
        while min_heap:
            result.append(heapq.heappop(min_heap)[1])

        return result[::-1]

    def follow(self, follower_id: int, followee_id: int) -> None:
        if follower_id != followee_id:
            self.following[follower_id].add(followee_id)

    def unfollow(self, follower_id: int, followee_id: int) -> None:
        self.following[follower_id].discard(followee_id)


# Tests
def test():
    # Test 1
    twitter = Twitter()
    twitter.post_tweet(1, 5)
    assert twitter.get_news_feed(1) == [5]
    twitter.follow(1, 2)
    twitter.post_tweet(2, 6)
    assert twitter.get_news_feed(1) == [6, 5]
    twitter.unfollow(1, 2)
    assert twitter.get_news_feed(1) == [5]

    # Test 2
    twitter2 = Twitter()
    twitter2.post_tweet(1, 1)
    twitter2.post_tweet(1, 2)
    twitter2.post_tweet(1, 3)
    assert twitter2.get_news_feed(1) == [3, 2, 1]

    # Test 3
    twitter3 = Twitter()
    twitter3.post_tweet(1, 5)
    twitter3.follow(1, 1)  # User follows themselves
    assert twitter3.get_news_feed(1) == [5]

    # Test 4
    twitter4 = Twitter()
    twitter4.post_tweet(2, 5)
    twitter4.follow(1, 2)
    twitter4.follow(1, 2)  # Duplicate follow
    assert twitter4.get_news_feed(1) == [5]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
