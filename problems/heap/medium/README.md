# Heap / Priority Queue - Medium Problems

## Advanced Concepts

### Custom Comparators and Tuples

Heaps can store complex objects with custom ordering:

```python
import heapq

# Tuples: Compare by first element, then second, etc.
heap = []
heapq.heappush(heap, (priority, value))
heapq.heappush(heap, (1, 'high'))
heapq.heappush(heap, (5, 'low'))
heapq.heappush(heap, (1, 'also high'))

# Pop: (1, 'also high') comes first (same priority, alphabetical)

# For objects: Use tuple with key
class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

tasks = []
for task in task_list:
    heapq.heappush(tasks, (task.priority, task.name, task))
```

### Greedy Algorithms with Heaps

Many greedy algorithms use heaps to always process the best option:

**Greedy Pattern**:
1. Add all options to heap
2. Extract best option
3. Process it
4. Add new options if needed
5. Repeat until done

**Why heaps work well**: O(log n) to get next best option vs O(n) to search.

### Multi-Criteria Sorting

When sorting by multiple criteria, use tuples:

```python
# Sort by distance, then by value
heap = []
heapq.heappush(heap, (distance, value, object))

# Python compares tuples element by element
# (1, 100) < (1, 200) < (2, 50)
```

### Lazy Deletion

Instead of deleting from middle of heap (expensive), mark as invalid:

```python
heap = [...]
removed = set()

# "Delete" element
removed.add(element_to_remove)

# When popping
while heap and heap[0] in removed:
    heapq.heappop(heap)

# Now heap[0] is valid
```

## Problems in This Section

### 1. K Closest Points to Origin (LC 973)

**Concept**: Find k points with smallest Euclidean distance from origin

**Pattern**: Max-heap of size k or min-heap with all points

**Time Complexity**: O(n log k) with max-heap, O(n log n) with min-heap
**Space Complexity**: O(k) or O(n)

#### Key Insights

1. **Distance formula**: √(x² + y²), but can use x² + y² (monotonic)
2. **Two approaches**:
   - Min-heap all points, pop k times
   - Max-heap size k, keep k smallest
3. **Max-heap approach is better**: O(n log k) vs O(n log n)

#### Approach 1: Min-Heap (Simpler)

```python
import heapq

def kClosest(points, k):
    # Create heap with distances
    heap = []
    for x, y in points:
        dist = x*x + y*y  # No sqrt needed
        heapq.heappush(heap, (dist, [x, y]))

    # Extract k smallest
    result = []
    for _ in range(k):
        dist, point = heapq.heappop(heap)
        result.append(point)

    return result

# Time: O(n log n) - heap with all points
# Space: O(n)
```

#### Approach 2: Max-Heap Size K (Optimal)

```python
import heapq

def kClosest(points, k):
    # Max-heap of size k (negate distances)
    heap = []

    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, [x, y]))

        # Maintain size k
        if len(heap) > k:
            heapq.heappop(heap)

    # Extract points (ignore distances)
    return [point for dist, point in heap]

# Time: O(n log k) - better for large n, small k
# Space: O(k)
```

#### Approach 3: Quick Select (Optimal for Large K)

```python
def kClosest(points, k):
    # Calculate distances
    dists = [x*x + y*y for x, y in points]

    # Partition around kth smallest distance
    # (Quick select algorithm)

    # Return points with distance <= kth distance

# Time: O(n) average, O(n²) worst case
# Space: O(1)
# Best when k is close to n
```

#### Which Approach to Use?

| Condition | Best Approach | Reason |
|-----------|--------------|---------|
| k << n | Max-heap size k | O(n log k) |
| k ≈ n | Quick select | O(n) average |
| Already have heap | Min-heap | Simpler code |
| Need sorted by distance | Min-heap | Already sorted |

### 2. Kth Largest Element in Array (LC 215)

**Concept**: Find kth largest element in unsorted array

**Pattern**: Min-heap of size k or quick select

**Time Complexity**: O(n log k) heap, O(n) average quick select
**Space Complexity**: O(k) heap, O(1) quick select

#### Approach 1: Min-Heap

```python
import heapq

def findKthLargest(nums, k):
    # Min-heap of k largest elements
    heap = []

    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)

    # Root is kth largest
    return heap[0]

# Time: O(n log k)
# Space: O(k)
```

#### Approach 2: Max-Heap

```python
import heapq

def findKthLargest(nums, k):
    # Heapify all elements
    heap = [-num for num in nums]
    heapq.heapify(heap)

    # Pop k-1 times
    for _ in range(k - 1):
        heapq.heappop(heap)

    return -heap[0]

# Time: O(n + k log n)
# Space: O(n)
```

#### Approach 3: Quick Select (Optimal)

```python
import random

def findKthLargest(nums, k):
    # Convert to finding (n-k)th smallest
    k = len(nums) - k

    def quickSelect(left, right):
        pivot = random.randint(left, right)
        pivot_val = nums[pivot]

        # Move pivot to end
        nums[pivot], nums[right] = nums[right], nums[pivot]

        # Partition
        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_val:
                nums[i], nums[store_index] = nums[store_index], nums[i]
                store_index += 1

        # Move pivot to final position
        nums[right], nums[store_index] = nums[store_index], nums[right]

        # Recurse on correct partition
        if store_index == k:
            return nums[k]
        elif store_index < k:
            return quickSelect(store_index + 1, right)
        else:
            return quickSelect(left, store_index - 1)

    return quickSelect(0, len(nums) - 1)

# Time: O(n) average, O(n²) worst
# Space: O(1)
```

### 3. Task Scheduler (LC 621)

**Concept**: Schedule tasks with cooldown period between same tasks

**Pattern**: Greedy with max-heap + queue for cooldown

**Time Complexity**: O(n log 26) = O(n)
**Space Complexity**: O(26) = O(1)

#### Key Insights

1. **Greedy approach**: Always schedule most frequent task available
2. **Cooldown tracking**: Use queue to track when tasks become available again
3. **Idle time**: When no task available, must idle
4. **Max-heap**: Get most frequent task in O(log n)

#### Algorithm

```python
from collections import Counter, deque
import heapq

def leastInterval(tasks, n):
    # Count frequencies
    counts = Counter(tasks)

    # Max-heap of frequencies
    heap = [-count for count in counts.values()]
    heapq.heapify(heap)

    # Queue: (count, available_time)
    queue = deque()

    time = 0

    while heap or queue:
        time += 1

        # Add back available tasks
        if queue and queue[0][1] == time:
            count = queue.popleft()[0]
            heapq.heappush(heap, count)

        # Schedule most frequent task
        if heap:
            count = heapq.heappop(heap)
            count += 1  # Decrease (it's negative)

            # If task has remaining instances
            if count < 0:
                # Add to queue with cooldown
                queue.append((count, time + n + 1))

    return time
```

#### Alternative: Math Formula

```python
def leastInterval(tasks, n):
    counts = Counter(tasks)
    max_freq = max(counts.values())
    max_count = sum(1 for c in counts.values() if c == max_freq)

    # Minimum time based on most frequent task
    min_time = (max_freq - 1) * (n + 1) + max_count

    # But must process all tasks
    return max(min_time, len(tasks))

# Time: O(n)
# Space: O(1)
```

**Example**:
```
tasks = ['A','A','A','B','B','B'], n = 2

Most frequent: A and B (3 times each)
Pattern: A B _ A B _ A B
Time = (3-1) * (2+1) + 2 = 8

tasks = ['A','A','A','B','B','B'], n = 50
Time = (3-1) * (50+1) + 2 = 104
```

### 4. Design Twitter (LC 355)

**Concept**: Design Twitter-like system with post, follow, unfollow, getNewsFeed

**Pattern**: Heap for k-way merge of timelines

**Time Complexity**:
- Post: O(1)
- Follow/Unfollow: O(1)
- GetNewsFeed: O(k log n) where k = 10, n = number of followees

**Space Complexity**: O(users + tweets)

#### Key Insights

1. **User data**: HashMap of userId → followees set
2. **Tweet data**: HashMap of userId → tweets list
3. **News feed**: Merge timelines of user + followees
4. **Heap for merge**: Keep track of most recent tweet from each timeline

#### Implementation

```python
from collections import defaultdict
import heapq

class Twitter:
    def __init__(self):
        self.timestamp = 0
        self.tweets = defaultdict(list)  # userId -> [(time, tweetId)]
        self.following = defaultdict(set)  # userId -> set of followees

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        # Get all relevant timelines
        users = self.following[userId] | {userId}

        # Max-heap for recent tweets
        heap = []
        for user in users:
            if self.tweets[user]:
                # Add most recent tweet from each user
                time, tweetId = self.tweets[user][-1]
                heapq.heappush(heap, (-time, tweetId, user, len(self.tweets[user]) - 1))

        # Extract 10 most recent
        result = []
        for _ in range(10):
            if not heap:
                break

            time, tweetId, user, index = heapq.heappop(heap)
            result.append(tweetId)

            # Add next tweet from same user
            if index > 0:
                time, tweetId = self.tweets[user][index - 1]
                heapq.heappush(heap, (-time, tweetId, user, index - 1))

        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
```

#### Why K-Way Merge?

Instead of collecting all tweets and sorting (O(n log n)), we use heap to merge k sorted lists (O(k log k)).

**Example**:
```
User 1 tweets: [(10, 'A'), (8, 'B'), (5, 'C')]
User 2 tweets: [(9, 'D'), (7, 'E'), (3, 'F')]
User 3 tweets: [(6, 'G'), (4, 'H')]

Heap merge:
1. Start with most recent from each: [(10,'A',1), (9,'D',2), (6,'G',3)]
2. Pop (10,'A',1), add (8,'B',1): [(9,'D',2), (8,'B',1), (6,'G',3)]
3. Pop (9,'D',2), add (7,'E',2): [(8,'B',1), (7,'E',2), (6,'G',3)]
...
Result: [A, D, B, E, G, H, C, F]
```

## Advanced Patterns

### Pattern 1: Fixed-Size Heap for Top K

```python
def topK(stream, k):
    # Min-heap for k largest (or max-heap for k smallest)
    heap = []

    for item in stream:
        heapq.heappush(heap, item)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap
```

### Pattern 2: Greedy Scheduling with Heap

```python
def schedule_tasks(tasks):
    # Heap of (priority, task)
    heap = [(task.priority, task) for task in tasks]
    heapq.heapify(heap)

    while heap:
        priority, task = heapq.heappop(heap)
        process(task)

        # Add new tasks if needed
        for new_task in task.generates():
            heapq.heappush(heap, (new_task.priority, new_task))
```

### Pattern 3: K-Way Merge

```python
def merge_k_sorted(lists):
    # Heap of (value, list_index, element_index)
    heap = []

    # Initialize with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
```

### Pattern 4: Cooldown/Rate Limiting

```python
def process_with_cooldown(tasks, cooldown):
    from collections import deque

    heap = [...]  # Available tasks
    queue = deque()  # Tasks in cooldown

    time = 0
    while heap or queue:
        # Restore available tasks
        while queue and queue[0][1] <= time:
            task, _ = queue.popleft()
            heapq.heappush(heap, task)

        # Process task
        if heap:
            task = heapq.heappop(heap)
            process(task)
            queue.append((task, time + cooldown))

        time += 1
```

## Complexity Optimization

### When to Use Heap vs Alternatives

| Scenario | Best Choice | Complexity |
|----------|-------------|------------|
| Find kth in unsorted array | Quick select | O(n) avg |
| Stream of data, need kth | Heap | O(n log k) |
| Need all sorted | Sort | O(n log n) |
| Merge k sorted lists | Heap | O(n log k) |
| Top k from sorted data | Just take first k | O(k) |
| Dynamic data, frequent min/max | Heap | O(log n) ops |

### Heap vs Sorting

**Use Heap when**:
- Don't need full sort
- Data arrives over time
- Only need k elements
- Frequent insertions/deletions

**Use Sorting when**:
- Need all elements sorted
- One-time operation
- Small dataset
- k is close to n

## Common Pitfalls

1. **Wrong heap type**: Min when need max (or vice versa)
2. **Forgetting to negate**: For max-heap in Python
3. **Not using tuples**: For multi-criteria sorting
4. **Inefficient approach**: Using O(n log n) when O(n log k) possible
5. **Index errors**: In k-way merge, forgetting to check bounds
6. **Not handling ties**: When multiple elements have same priority

## Tips for Medium Heap Problems

1. **Identify pattern**: Top k? Scheduling? Merging?
2. **Choose heap size**: All elements or just k?
3. **Multi-criteria**: Use tuples for complex sorting
4. **Consider alternatives**: Quick select for one-time kth element
5. **Greedy + heap**: Often work together
6. **Test edge cases**: Empty input, k=0, k=n, all same values

## Practice Progression

1. **K Closest Points**: Basic heap with custom key
2. **Kth Largest**: Compare heap vs quick select
3. **Task Scheduler**: Greedy algorithm with heap
4. **Design Twitter**: K-way merge pattern
5. **Try variants**: Different k values, different orderings

## Beyond These Problems

Master these patterns, then try:
- **Merge K Sorted Lists** (LC 23): Classic k-way merge
- **Top K Frequent Elements** (LC 347): Heap with counter
- **Meeting Rooms II** (LC 253): Greedy scheduling
- **Ugly Number II** (LC 264): Multiple heaps
- **Sliding Window Maximum** (LC 239): Heap or deque

## Real-World Applications

1. **Load Balancing**: Assign tasks to least loaded server
2. **Event Processing**: Process events by priority/time
3. **Recommendation Systems**: Top k recommendations
4. **Social Media Feeds**: Merge timelines by timestamp
5. **CPU Scheduling**: Schedule processes by priority
6. **Network Routing**: Find shortest paths (Dijkstra)

## Key Takeaways

1. **Fixed-size heap**: Essential for "top k" problems
2. **Greedy + heap**: Natural combination for optimization
3. **K-way merge**: Heap beats sorting when k << n
4. **Tuples for sorting**: Python's natural multi-criteria sort
5. **Consider alternatives**: Quick select can be better
6. **Max-heap in Python**: Remember to negate values

## Interview Tips

- Explain time/space complexity trade-offs
- Mention alternative approaches (quick select, sorting)
- Discuss why heap is better for your use case
- Consider follow-up: What if k changes? Stream of data?
- Optimize: Can you use O(k) space instead of O(n)?
