# Design News Feed Generation Algorithm (Facebook-style)

## 1. Problem Statement & Scope

Design the core news feed generation and ranking algorithm that powers a social media platform like Facebook. This is a deep-dive into the specific component responsible for determining what content users see in their feed.

### In Scope:
- Feed ranking algorithm (EdgeRank and modern ML-based)
- Fanout architecture (write vs. read)
- Real-time feed updates
- Personalization and relevance scoring
- Feed diversity and quality
- Story bumping (showing older high-engagement posts)
- A/B testing infrastructure
- Multi-format content (text, photos, videos, links, polls)
- Engagement prediction
- Spam and clickbait detection

### Out of Scope:
- Full social media platform design (focus on feed only)
- Content moderation details
- Ads placement algorithm (separate system)
- Messenger/chat features
- Groups/Events/Pages (mention but don't design)

### Scale:
- 3 billion daily active users (Facebook scale)
- Each user sees ~30-50 posts per session
- 100 billion feed loads per day
- 5 billion new posts/day
- 500 million concurrent users during peak
- Feed load latency requirement: < 500ms (p95)

## 2. Functional Requirements

**FR1: Feed Generation**
- Generate personalized feed for each user
- Rank posts by relevance and engagement potential
- Mix content types (friend posts, page posts, groups, videos)
- Support pagination and infinite scroll

**FR2: Personalization**
- Score based on user-content affinity
- Consider user's engagement history
- Adapt to changing interests over time
- Factor in real-time signals

**FR3: Real-Time Updates**
- Show new posts from friends in near real-time
- Update engagement counts (likes, comments)
- Handle viral posts efficiently

**FR4: Feed Quality**
- Diversity: Don't show 10 posts from same person
- Freshness: Balance new vs. older high-quality content
- Quality signals: Penalize clickbait, spam
- Content-type balance: Mix photos, videos, text

**FR5: Engagement Optimization**
- Predict probability of engagement (like, comment, share)
- Optimize for meaningful interactions
- Down-rank passive consumption
- Reward high-quality content

## 3. Non-Functional Requirements (Scale, Performance, Availability)

### Scale:
- **Users:** 3 billion DAU
- **Feed loads:** 100 billion/day = 1.15M feeds/second
- **New posts:** 5 billion/day = 57K posts/second
- **Fanout writes:** Assume avg 200 friends per user: 5B × 200 = 1 trillion writes/day
- **Ranking operations:** 1.15M feeds × 1000 candidates = 1.15B rankings/second

### Performance:
- **Feed generation:** < 500ms (p95)
- **Candidate retrieval:** < 100ms
- **Ranking (ML inference):** < 200ms for 1000 posts
- **Real-time updates:** < 5 seconds from post creation to feed appearance

### Availability:
- **Service availability:** 99.99%
- **Feed freshness:** No more than 5 minutes stale during outages

### Consistency:
- **Eventual consistency:** Acceptable for most feed updates
- **Strong consistency:** For user's own posts

## 4. Back-of-envelope Calculations

### Feed Generation Load:

```
Feed requests: 100B/day
Average candidates per feed: 1000 posts
Total ranking operations: 100B × 1000 = 100 trillion/day

Per second: 100T ÷ 86,400 = 1.15B operations/second

ML model inference time: 0.2ms per post
Total compute time: 1.15B × 0.2ms = 230K CPU-seconds/second
CPU cores needed: 230K cores (at 100% utilization)

With 20% average utilization: ~1.15M cores
EC2 c5.9xlarge (36 cores): ~32,000 instances
Cost: $1.53/hour × 32,000 = $48,960/hour = ~$35M/month

This is just for ranking! Hence the need for optimization.
```

### Storage for Feed Cache:

```
Active users: 500M concurrent
Cached feed per user: 100 post IDs × 8 bytes = 800 bytes
Total cache: 500M × 800 bytes = 400 GB

Post metadata cache:
Hot posts: 100M posts
Metadata per post: 5 KB
Total: 100M × 5 KB = 500 GB

Total cache needed: ~1 TB (easily fits in Redis cluster)
```

### Fanout Writes:

```
Using fanout-on-write:
Posts per day: 5B
Average friends per user: 200
Total writes: 5B × 200 = 1 trillion writes/day
Per second: 1T ÷ 86,400 = 11.5M writes/second

This is massive! Hence hybrid fanout strategy.
```

## 5. High-Level Architecture

```
[User Requests Feed]
       |
       v
[API Gateway]
       |
       v
[Feed Service] ---> [Cache] (Check if feed cached)
       |                |
       |           [Cache Hit]
       |                |
       v                v
[Cache Miss]      [Return Feed]
       |
       v
[Candidate Generation Service]
       |
       +-----------+----------+-----------+
       |           |          |           |
       v           v          v           v
[Friend     [Page      [Group     [Trending
 Posts]      Posts]     Posts]     Content]
       |           |          |           |
       +-----------+----------+-----------+
                   |
                   v
        [~1000 candidate posts]
                   |
                   v
         [Ranking Service]
                   |
       +-----------+-----------+
       |                       |
       v                       v
[Feature          [ML Model
 Extraction]       Serving]
       |                       |
       +-----------+-----------+
                   |
                   v
         [Ranked Feed (top 20)]
                   |
                   v
          [Post-Processing]
          (Diversity, Story Bumping)
                   |
                   v
         [Cache Result]
                   |
                   v
          [Return to User]


[Post Creation Flow]
       |
       v
[New Post Created]
       |
       v
[Fanout Service]
       |
   +---+---+
   |       |
   v       v
[Celebrity?]
   |       |
  No      Yes
   |       |
   v       v
[Fanout  [Skip Fanout]
 on Write]  (Pull on Read)
   |       |
   +--->---+
       |
       v
[Update Caches/Invalidate]
```

## 6. Core Algorithm Components

### A. EdgeRank (Facebook's Original Algorithm)

```python
def calculate_edge_rank(user_id, post):
    """
    Original Facebook EdgeRank formula:
    EdgeRank = Affinity × Weight × Time Decay
    """

    # 1. Affinity Score: How close is user to content creator?
    affinity = calculate_affinity(user_id, post.author_id)

    # 2. Weight: Type of post and interaction
    weight = calculate_weight(post.type, post.engagement_type)

    # 3. Time Decay: How old is the post?
    time_decay = calculate_time_decay(post.created_at)

    edge_rank = affinity * weight * time_decay

    return edge_rank


def calculate_affinity(user_id, author_id):
    """
    Affinity = how often user interacts with author
    Range: 0-1
    """

    # Get interaction history (last 30 days)
    interactions = get_interactions(user_id, author_id, days=30)

    # Different interaction types have different values
    score = 0
    score += interactions.comments * 10  # Commenting is strongest signal
    score += interactions.likes * 5
    score += interactions.shares * 15
    score += interactions.clicks * 1
    score += interactions.profile_visits * 8

    # Normalize to 0-1 range
    max_score = 500  # Assumed maximum for very active interaction
    affinity = min(score / max_score, 1.0)

    # If they're tagged as "close friends": boost
    if is_close_friend(user_id, author_id):
        affinity *= 1.5
        affinity = min(affinity, 1.0)

    return affinity


def calculate_weight(post_type, engagement_type=None):
    """
    Weight based on post type and engagement
    """

    base_weights = {
        'status': 1.0,
        'photo': 1.5,
        'video': 2.0,
        'link': 0.8,
        'shared_post': 1.2
    }

    engagement_multipliers = {
        'comment': 3.0,
        'like': 1.0,
        'share': 2.5,
        'click': 0.5
    }

    weight = base_weights.get(post_type, 1.0)

    if engagement_type:
        weight *= engagement_multipliers.get(engagement_type, 1.0)

    return weight


def calculate_time_decay(created_at):
    """
    Time decay: exponential decay based on age
    Recent posts get higher scores
    """

    age_hours = (datetime.now() - created_at).total_seconds() / 3600

    # Exponential decay with half-life of 24 hours
    # After 24 hours, score is reduced by 50%
    decay = math.exp(-0.693 * age_hours / 24)

    return decay
```

### B. Modern ML-Based Ranking

```python
class FeedRankingEngine:
    """
    Modern machine learning based feed ranking
    Predicts P(meaningful interaction | user, post)
    """

    def __init__(self):
        self.model = load_ml_model("feed_ranking_v5")
        self.feature_store = FeatureStore()

    def rank_posts(self, user_id, candidate_posts):
        """
        Rank candidate posts for a user
        Returns sorted list of posts
        """

        # Extract features for all candidates in batch
        features = self.extract_features_batch(user_id, candidate_posts)

        # Predict engagement probabilities
        scores = self.model.predict(features)

        # Create (post, score) pairs
        scored_posts = list(zip(candidate_posts, scores))

        # Sort by score descending
        ranked = sorted(scored_posts, key=lambda x: x[1], reverse=True)

        return [post for post, score in ranked]

    def extract_features_batch(self, user_id, posts):
        """
        Extract features for ML model
        Returns matrix of features [num_posts × num_features]
        """

        all_features = []

        # Get user features once (same for all posts)
        user_features = self.get_user_features(user_id)

        for post in posts:
            # Get post features
            post_features = self.get_post_features(post)

            # Get interaction features
            interaction_features = self.get_interaction_features(
                user_id, post)

            # Combine all features
            combined = {
                **user_features,
                **post_features,
                **interaction_features
            }

            all_features.append(combined)

        return all_features

    def get_user_features(self, user_id):
        """
        User features (demographic, behavioral)
        """

        # Fetch from feature store (cached)
        user = self.feature_store.get_user(user_id)

        return {
            # Demographics
            'user_age_group': user.age_group,  # 18-24, 25-34, etc.
            'user_gender': user.gender,
            'user_location_country': user.country,

            # Behavioral
            'user_avg_session_length': user.avg_session_length_minutes,
            'user_posts_per_week': user.posts_per_week,
            'user_likes_per_week': user.likes_per_week,
            'user_comments_per_week': user.comments_per_week,
            'user_shares_per_week': user.shares_per_week,

            # Preferences (learned)
            'user_prefers_video': user.video_engagement_rate,
            'user_prefers_photos': user.photo_engagement_rate,
            'user_avg_watch_time': user.avg_video_watch_time_seconds,

            # Recency
            'user_last_active_hours_ago': (
                datetime.now() - user.last_active_at).total_seconds() / 3600,

            # Network
            'user_friend_count': user.friend_count,
            'user_page_likes_count': user.page_likes_count,
            'user_groups_count': user.groups_count
        }

    def get_post_features(self, post):
        """
        Post features (content, creator, engagement)
        """

        return {
            # Content type
            'post_type_status': 1 if post.type == 'status' else 0,
            'post_type_photo': 1 if post.type == 'photo' else 0,
            'post_type_video': 1 if post.type == 'video' else 0,
            'post_type_link': 1 if post.type == 'link' else 0,

            # Post attributes
            'post_has_text': 1 if post.text else 0,
            'post_text_length': len(post.text) if post.text else 0,
            'post_has_media': 1 if post.media_count > 0 else 0,
            'post_media_count': post.media_count,
            'post_video_duration': post.video_duration or 0,

            # Timing
            'post_age_hours': (
                datetime.now() - post.created_at).total_seconds() / 3600,
            'post_hour_of_day': post.created_at.hour,
            'post_day_of_week': post.created_at.weekday(),

            # Creator features
            'creator_friend_count': post.author.friend_count,
            'creator_posts_per_week': post.author.posts_per_week,
            'creator_is_verified': 1 if post.author.is_verified else 0,

            # Early engagement (first hour)
            'post_early_likes': post.likes_in_first_hour,
            'post_early_comments': post.comments_in_first_hour,
            'post_early_shares': post.shares_in_first_hour,
            'post_early_ctr': post.click_through_rate_first_hour,

            # Current engagement
            'post_total_likes': post.likes_count,
            'post_total_comments': post.comments_count,
            'post_total_shares': post.shares_count,
            'post_engagement_rate': (
                post.likes_count + post.comments_count + post.shares_count
            ) / max(post.reach, 1),

            # Quality signals
            'post_avg_watch_time': post.avg_watch_time_seconds or 0,
            'post_completion_rate': post.video_completion_rate or 0,
            'post_is_clickbait': self.detect_clickbait(post.text)
        }

    def get_interaction_features(self, user_id, post):
        """
        User-Post interaction features
        """

        # Check relationship with author
        is_friend = self.check_friendship(user_id, post.author_id)
        is_close_friend = self.check_close_friend(user_id, post.author_id)

        # Historical interaction with author
        author_interactions = self.get_author_interaction_history(
            user_id, post.author_id, days=30)

        # Similarity
        common_friends = self.get_mutual_friends_count(
            user_id, post.author_id)
        common_interests = self.calculate_interest_overlap(
            user_id, post.author_id)

        return {
            # Relationship
            'is_friend': 1 if is_friend else 0,
            'is_close_friend': 1 if is_close_friend else 0,
            'is_family': 1 if self.check_family(user_id, post.author_id) else 0,

            # Interaction history with author
            'author_interaction_likes_30d': author_interactions['likes'],
            'author_interaction_comments_30d': author_interactions['comments'],
            'author_interaction_shares_30d': author_interactions['shares'],
            'author_profile_visits_30d': author_interactions['profile_visits'],
            'days_since_last_interaction': author_interactions['days_since_last'],

            # Network
            'common_friends_count': common_friends,
            'common_interests_score': common_interests,

            # Content affinity
            'user_engaged_similar_posts': self.count_similar_engaged_posts(
                user_id, post, days=7)
        }

    def detect_clickbait(self, text):
        """
        Simple clickbait detection
        Production would use ML model
        """

        if not text:
            return 0

        clickbait_phrases = [
            "you won't believe",
            "shocking",
            "number 7 will",
            "what happened next",
            "doctors hate",
            "this one trick"
        ]

        text_lower = text.lower()

        for phrase in clickbait_phrases:
            if phrase in text_lower:
                return 1

        # Check for excessive caps and exclamation marks
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
        exclamation_count = text.count('!')

        if caps_ratio > 0.5 or exclamation_count > 3:
            return 1

        return 0
```

### C. Candidate Generation

```python
class CandidateGenerator:
    """
    Generate ~1000 candidate posts for ranking
    Multi-source funnel
    """

    def generate_candidates(self, user_id, limit=1000):
        """
        Pull candidates from multiple sources
        """

        candidates = []

        # Source 1: Friends' posts (60% of candidates)
        friends_posts = self.get_friends_posts(user_id, limit=600)
        candidates.extend(friends_posts)

        # Source 2: Pages user follows (20% of candidates)
        page_posts = self.get_page_posts(user_id, limit=200)
        candidates.extend(page_posts)

        # Source 3: Groups (10% of candidates)
        group_posts = self.get_group_posts(user_id, limit=100)
        candidates.extend(group_posts)

        # Source 4: Trending/viral content (5% of candidates)
        trending_posts = self.get_trending_posts(user_id, limit=50)
        candidates.extend(trending_posts)

        # Source 5: Friend-of-friend posts (5% of candidates)
        fof_posts = self.get_friend_of_friend_posts(user_id, limit=50)
        candidates.extend(fof_posts)

        # Deduplicate
        candidates = self.deduplicate(candidates)

        # Filter already seen
        candidates = self.filter_seen(user_id, candidates)

        # Filter privacy (user blocked, private posts, etc.)
        candidates = self.filter_by_privacy(user_id, candidates)

        return candidates[:limit]

    def get_friends_posts(self, user_id, limit):
        """
        Get recent posts from friends
        Mix of fanout inbox + pull from active friends
        """

        # Check fanout inbox (pre-populated)
        inbox_posts = self.get_inbox_posts(user_id, limit=limit * 0.8)

        # Pull from highly active friends (not in inbox)
        active_friends = self.get_active_friends_not_in_inbox(user_id)
        pull_posts = []

        for friend_id in active_friends:
            recent = self.get_recent_posts(friend_id, limit=5)
            pull_posts.extend(recent)

        # Combine
        all_posts = inbox_posts + pull_posts

        # Sort by recency
        all_posts.sort(key=lambda p: p.created_at, reverse=True)

        return all_posts[:limit]

    def get_inbox_posts(self, user_id, limit):
        """
        Get posts from fanout inbox
        """

        # Posts are fanned out to inbox on creation
        # Stored as sorted set in Redis (score = timestamp)

        post_ids = redis.zrevrange(
            f"inbox:{user_id}",
            0,
            limit - 1
        )

        # Batch fetch post details
        posts = self.batch_get_posts(post_ids)

        return posts
```

### D. Feed Diversity and Post-Processing

```python
class FeedPostProcessor:
    """
    Apply business rules and diversity constraints
    After ML ranking
    """

    def post_process(self, user_id, ranked_posts):
        """
        Apply post-processing to improve feed quality
        """

        final_feed = []
        seen_authors = {}
        seen_post_types = {}
        consecutive_videos = 0

        for post in ranked_posts:
            # Rule 1: Don't show more than 2 consecutive posts from same author
            if post.author_id in seen_authors:
                recent_count = seen_authors[post.author_id]
                if recent_count >= 2:
                    # Skip this post, come back to it later
                    continue

            # Rule 2: Don't show more than 3 videos in a row
            if post.type == 'video':
                consecutive_videos += 1
                if consecutive_videos > 3:
                    continue
            else:
                consecutive_videos = 0

            # Rule 3: Ensure content type diversity (every 10 posts)
            if len(final_feed) > 0 and len(final_feed) % 10 == 0:
                # Reset type counts
                seen_post_types = {}

            # Rule 4: Story bumping - resurface older high-engagement posts
            if self.should_bump_story(post, user_id):
                # Insert at top even if it's older
                final_feed.insert(0, post)
            else:
                final_feed.append(post)

            # Update tracking
            seen_authors[post.author_id] = seen_authors.get(
                post.author_id, 0) + 1
            seen_post_types[post.type] = seen_post_types.get(post.type, 0) + 1

            # Every 5 posts, reset author tracking (allow same author again)
            if len(final_feed) % 5 == 0:
                seen_authors = {}

            # Stop once we have enough
            if len(final_feed) >= 20:
                break

        return final_feed

    def should_bump_story(self, post, user_id):
        """
        Story bumping: bring back older posts with new engagement
        """

        # Post must be at least 1 hour old
        age_hours = (datetime.now() - post.created_at).total_seconds() / 3600
        if age_hours < 1:
            return False

        # Check if post has new engagement since user last saw it
        last_feed_load = self.get_last_feed_load_time(user_id)

        new_engagement = self.get_engagement_since(post.id, last_feed_load)

        # Bump if significant new engagement
        if new_engagement['comments'] >= 5 or new_engagement['likes'] >= 20:
            return True

        # Bump if friend commented
        if self.friend_commented_since(user_id, post.id, last_feed_load):
            return True

        return False
```

## 7. Fanout Architecture

```python
class FanoutService:
    """
    Handle fanout of posts to followers
    Hybrid approach: fanout-on-write for normal users, fanout-on-read for celebrities
    """

    CELEBRITY_THRESHOLD = 1_000_000  # 1M followers

    def on_post_created(self, post):
        """
        Called when user creates a new post
        """

        # Determine fanout strategy
        follower_count = self.get_follower_count(post.author_id)

        if follower_count > self.CELEBRITY_THRESHOLD:
            # Celebrity: fanout on read
            self.fanout_on_read_strategy(post)
        else:
            # Normal user: fanout on write
            self.fanout_on_write_strategy(post)

    def fanout_on_write_strategy(self, post):
        """
        Push model: write to all followers' inboxes immediately
        """

        # Get all followers
        followers = self.get_followers(post.author_id)

        # Filter to active users only (logged in last 7 days)
        active_followers = [
            f for f in followers
            if self.is_active_user(f)
        ]

        # Fanout to active followers
        # Use batch writes for efficiency
        batch_size = 1000

        for i in range(0, len(active_followers), batch_size):
            batch = active_followers[i:i + batch_size]

            # Write to Redis inbox (sorted set)
            pipeline = redis.pipeline()

            for follower_id in batch:
                pipeline.zadd(
                    f"inbox:{follower_id}",
                    {post.id: post.created_at.timestamp()}
                )

                # Trim to keep only latest 1000 posts
                pipeline.zremrangebyrank(
                    f"inbox:{follower_id}",
                    0, -1001
                )

            pipeline.execute()

        # Also persist to database (async)
        self.persist_fanout_to_db_async(post.id, active_followers)

    def fanout_on_read_strategy(self, post):
        """
        Pull model: mark post as from celebrity, pull during feed generation
        """

        # Just mark the post as from celebrity
        redis.sadd("celebrity_posts", post.id)
        redis.zadd("celebrity_posts_timeline", {
            post.id: post.created_at.timestamp()
        })

        # Set expiry (remove after 7 days)
        redis.expire("celebrity_posts_timeline", 604800)

    def get_feed_hybrid(self, user_id):
        """
        Generate feed using hybrid approach
        """

        # Get posts from inbox (fanout-on-write)
        inbox_posts = self.get_inbox_posts(user_id, limit=500)

        # Get posts from celebrities user follows (fanout-on-read)
        celebrity_posts = []

        # Get celebrities this user follows
        following = self.get_following(user_id)
        celebrities = [
            f for f in following
            if self.is_celebrity(f)
        ]

        # Pull recent posts from each celebrity
        for celeb_id in celebrities:
            recent = self.get_recent_posts(celeb_id, limit=10)
            celebrity_posts.extend(recent)

        # Merge both sources
        all_candidates = inbox_posts + celebrity_posts

        # Remove duplicates
        all_candidates = list({p.id: p for p in all_candidates}.values())

        return all_candidates
```

## 8. Real-Time Updates

```python
class RealtimeFeedService:
    """
    Handle real-time feed updates using WebSockets
    """

    def on_post_created(self, post):
        """
        Notify online followers of new post
        """

        # Get online followers
        followers = self.get_followers(post.author_id)
        online_followers = [
            f for f in followers
            if self.is_user_online(f)
        ]

        # Send WebSocket notification
        for follower_id in online_followers:
            self.send_ws_notification(follower_id, {
                "type": "new_post",
                "post_id": post.id,
                "author_id": post.author_id,
                "author_name": post.author.name,
                "preview": post.text[:100]
            })

        # Update feed cache
        for follower_id in online_followers:
            # Prepend to cached feed
            self.prepend_to_feed_cache(follower_id, post.id)

    def send_ws_notification(self, user_id, notification):
        """
        Send WebSocket message to user
        """

        # Find WebSocket connection for user
        ws_connection = self.get_ws_connection(user_id)

        if ws_connection:
            ws_connection.send(json.dumps(notification))

    def is_user_online(self, user_id):
        """
        Check if user is currently online
        """

        # Check Redis (presence tracking)
        last_active = redis.get(f"user:last_active:{user_id}")

        if last_active:
            last_active_time = float(last_active)
            now = time.time()

            # Consider online if active in last 5 minutes
            return (now - last_active_time) < 300

        return False
```

## 9. A/B Testing Infrastructure

```python
class FeedExperimentService:
    """
    A/B testing framework for feed ranking
    """

    def get_feed_with_experiment(self, user_id):
        """
        Get feed, applying A/B test if user is in experiment
        """

        # Determine which experiment bucket user is in
        experiment_id = "feed_ranking_v6_test"
        bucket = self.assign_experiment_bucket(user_id, experiment_id)

        if bucket == "control":
            # Use current production model
            ranker = FeedRankingEngine()
        elif bucket == "treatment_a":
            # Test new model variant A
            ranker = FeedRankingEngineV6A()
        elif bucket == "treatment_b":
            # Test new model variant B
            ranker = FeedRankingEngineV6B()
        else:
            # Default to control
            ranker = FeedRankingEngine()

        # Generate candidates
        candidates = self.generate_candidates(user_id)

        # Rank using assigned ranker
        ranked_feed = ranker.rank_posts(user_id, candidates)

        # Log for analysis
        self.log_experiment_impression(
            user_id, experiment_id, bucket, ranked_feed)

        return ranked_feed

    def assign_experiment_bucket(self, user_id, experiment_id):
        """
        Assign user to experiment bucket (deterministic based on user_id)
        """

        # Hash user_id + experiment_id to get consistent bucket
        hash_input = f"{user_id}:{experiment_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)

        # Split: 50% control, 25% treatment_a, 25% treatment_b
        bucket_value = hash_value % 100

        if bucket_value < 50:
            return "control"
        elif bucket_value < 75:
            return "treatment_a"
        else:
            return "treatment_b"

    def log_experiment_impression(self, user_id, experiment_id, bucket, feed):
        """
        Log impression for later analysis
        """

        kafka.publish("experiment_impressions", {
            "user_id": user_id,
            "experiment_id": experiment_id,
            "bucket": bucket,
            "post_ids": [p.id for p in feed],
            "timestamp": time.time()
        })

    def track_engagement(self, user_id, post_id, engagement_type):
        """
        Track user engagement for A/B test analysis
        """

        # Find which experiment user is in
        experiment_id = "feed_ranking_v6_test"
        bucket = self.assign_experiment_bucket(user_id, experiment_id)

        # Log engagement
        kafka.publish("experiment_engagements", {
            "user_id": user_id,
            "experiment_id": experiment_id,
            "bucket": bucket,
            "post_id": post_id,
            "engagement_type": engagement_type,
            "timestamp": time.time()
        })
```

## 10. Trade-offs

### 1. Fanout on Write vs. Fanout on Read

**Decision: Hybrid**

| Aspect | Fanout on Write | Fanout on Read | Hybrid (Our Choice) |
|--------|----------------|----------------|---------------------|
| Write Latency | Slow (write to millions) | Fast | Medium |
| Read Latency | Fast (pre-computed) | Slow (compute on-demand) | Fast |
| Storage | High (duplicate data) | Low | Medium |
| Celebrity Problem | Doesn't scale | Scales perfectly | Best of both |
| Freshness | Stale until fanout completes | Always fresh | Fresh for active users |

### 2. ML Model Complexity vs. Latency

**Decision: Two-stage ranking**

Stage 1: Simple model on 1000 candidates (fast)
Stage 2: Complex model on top 100 (slower but acceptable)

### 3. Personalization vs. Diversity

**Decision: Post-processing rules**

Use ML for personalization, then apply diversity constraints

### 4. Real-time vs. Eventual Consistency

**Decision: Eventual consistency with real-time updates for online users**

Most users see updates within 5 seconds, acceptable trade-off

## 11. Monitoring and Metrics

### Key Metrics:

**Feed Quality:**
- Click-through rate (CTR)
- Time spent on feed
- Engagement rate (likes, comments, shares)
- Negative feedback rate (hide post, report)

**Performance:**
- Feed generation latency (p50, p95, p99)
- Cache hit rate
- ML inference latency

**Business Metrics:**
- Daily active users (DAU)
- Session length
- Posts per user per day
- Viral coefficient

## 12. Follow-up Questions

**Q1: How do you prevent filter bubbles?**
A: Inject diverse content periodically, show posts from outside network, mix trending posts

**Q2: How to handle spam and fake news?**
A: ML classifiers for spam/fake news, user reporting, trusted source boost, fact-checking partnerships

**Q3: How to optimize for meaningful interactions vs. passive consumption?**
A: Weight comments/shares higher than likes, down-rank clickbait, reward long-form discussions

**Q4: How do you handle user privacy in ranking?**
A: Respect privacy settings, don't use private info in features, anonymize training data

**Q5: How to make feed generation cost-effective?**
A: Cache aggressively, use simpler models for inactive users, batch processing, spot instances

---

**Interview Time:** 75-90 minutes

**Difficulty:** Hard (requires deep algorithm knowledge and ML systems understanding)
