# Web Crawler Basics

## 1. Problem Statement

Design a basic web crawler that can systematically browse the web and download web pages for indexing or archiving purposes. The crawler should visit web pages, extract links, and follow those links to discover new pages while avoiding infinite loops and respecting politeness policies.

## 2. Requirements

### Functional Requirements
- Start from a set of seed URLs
- Extract and parse HTML content from web pages
- Extract hyperlinks from downloaded pages
- Follow discovered links to crawl new pages
- Store downloaded content for later processing
- Avoid revisiting the same URL (deduplication)
- Support basic robot.txt compliance

### Non-Functional Requirements
- Handle up to 1000 pages per crawl session
- Respect rate limiting (1 request per second per domain)
- Handle basic error cases (404, timeouts, malformed HTML)
- Simple sequential crawling (single-threaded)
- Basic storage mechanism (files or simple database)

### Out of Scope
- Distributed crawling
- JavaScript rendering
- Complex politeness policies
- Advanced content parsing
- Scale beyond thousands of pages

## 3. Capacity Estimation

### Scale Assumptions
- Target: 1000 pages per crawl session
- Average page size: 100 KB
- Average links per page: 50
- Crawl duration: ~17 minutes (1 req/sec, 1000 pages)

### Storage Estimation
- Content storage: 1000 pages × 100 KB = 100 MB
- URL metadata: ~10 KB for tracking visited URLs
- Total storage: ~110 MB per crawl session

### Bandwidth Estimation
- Download rate: 100 KB/sec (1 page per second)
- Session bandwidth: 100 MB per session
- Minimal bandwidth requirements for basic crawler

## 4. High-Level Design

```
┌─────────────┐
│  Seed URLs  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   URL Frontier      │ (Queue of URLs to visit)
│   (Queue/List)      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  URL Deduplicator   │ (Check if URL visited)
│   (Set/HashTable)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   HTTP Fetcher      │ (Download page)
│                     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   HTML Parser       │ (Extract links & content)
│                     │
└──────┬──────────────┘
       │
       ├─────────────────► Store Content
       │
       └─────────────────► Extract Links → URL Frontier
```

### Core Components
1. **URL Frontier**: Queue/list of URLs to be crawled
2. **URL Deduplicator**: Tracks visited URLs to prevent cycles
3. **HTTP Fetcher**: Downloads web pages
4. **HTML Parser**: Extracts links and content
5. **Content Storage**: Stores downloaded pages
6. **Politeness Manager**: Enforces rate limiting

## 5. API Design

### Core Crawler Interface

```python
class WebCrawler:
    def __init__(self, config: CrawlerConfig):
        """
        Initialize crawler with configuration
        config: max_pages, rate_limit, storage_path, etc.
        """
        pass

    def add_seed_url(self, url: str) -> None:
        """Add a starting URL to begin crawling"""
        pass

    def crawl(self) -> CrawlResult:
        """
        Start the crawling process
        Returns: Statistics about the crawl
        """
        pass

    def stop(self) -> None:
        """Stop the crawling process"""
        pass
```

### Supporting Interfaces

```python
class URLFrontier:
    def add_url(self, url: str, depth: int) -> None:
        """Add URL to the frontier"""
        pass

    def get_next_url(self) -> Optional[str]:
        """Get next URL to crawl"""
        pass

    def is_empty(self) -> bool:
        """Check if frontier is empty"""
        pass

class HTMLParser:
    def parse(self, html: str, base_url: str) -> ParseResult:
        """
        Parse HTML and extract links
        Returns: list of absolute URLs and cleaned content
        """
        pass

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from HTML"""
        pass
```

## 6. Component Design

### URL Frontier (BFS Queue)

**Algorithm**: Breadth-First Search traversal
```python
class URLFrontier:
    def __init__(self):
        self.queue = deque()  # FIFO queue
        self.url_depth = {}   # Track depth of each URL

    def add_url(self, url: str, depth: int):
        if depth <= MAX_DEPTH:
            self.queue.append(url)
            self.url_depth[url] = depth

    def get_next_url(self) -> Optional[str]:
        if self.queue:
            return self.queue.popleft()
        return None
```

**Time Complexity**: O(1) for enqueue/dequeue
**Space Complexity**: O(n) where n is number of URLs in queue

### URL Deduplicator

**Algorithm**: Hash-based set membership check
```python
class URLDeduplicator:
    def __init__(self):
        self.visited_urls = set()  # Hash set for O(1) lookup

    def is_visited(self, url: str) -> bool:
        normalized_url = self.normalize_url(url)
        return normalized_url in self.visited_urls

    def mark_visited(self, url: str):
        normalized_url = self.normalize_url(url)
        self.visited_urls.add(normalized_url)

    def normalize_url(self, url: str) -> str:
        # Remove trailing slash, convert to lowercase, remove fragments
        parsed = urlparse(url.lower().rstrip('/'))
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
```

**Time Complexity**: O(1) average for lookup and insert
**Space Complexity**: O(n) where n is number of unique URLs

### HTTP Fetcher

**Algorithm**: Sequential HTTP requests with error handling
```python
class HTTPFetcher:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def fetch(self, url: str) -> FetchResult:
        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
                headers={'User-Agent': 'BasicCrawler/1.0'}
            )

            if response.status_code == 200:
                return FetchResult(
                    success=True,
                    content=response.text,
                    content_type=response.headers.get('Content-Type')
                )
            else:
                return FetchResult(
                    success=False,
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            return FetchResult(success=False, error=str(e))
```

### HTML Parser

**Algorithm**: DOM parsing with link extraction
```python
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class HTMLParser:
    def parse(self, html: str, base_url: str) -> ParseResult:
        soup = BeautifulSoup(html, 'html.parser')

        # Extract all links
        links = []
        for anchor in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, anchor['href'])
            if self.is_valid_url(absolute_url):
                links.append(absolute_url)

        # Extract text content
        text = soup.get_text(separator=' ', strip=True)

        return ParseResult(links=links, text=text, title=soup.title.string)

    def is_valid_url(self, url: str) -> bool:
        # Filter out non-http URLs, fragments, etc.
        return url.startswith('http://') or url.startswith('https://')
```

### Politeness Manager

**Algorithm**: Rate limiting with sleep intervals
```python
import time

class PolitenessManager:
    def __init__(self, delay_seconds: float = 1.0):
        self.delay = delay_seconds
        self.last_request_time = {}  # domain -> timestamp

    def wait_if_needed(self, url: str):
        domain = urlparse(url).netloc

        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

        self.last_request_time[domain] = time.time()
```

### Main Crawl Loop

```python
class WebCrawler:
    def crawl(self) -> CrawlResult:
        pages_crawled = 0

        while not self.frontier.is_empty() and pages_crawled < self.max_pages:
            url = self.frontier.get_next_url()

            # Skip if already visited
            if self.deduplicator.is_visited(url):
                continue

            # Mark as visited
            self.deduplicator.mark_visited(url)

            # Respect politeness
            self.politeness.wait_if_needed(url)

            # Fetch page
            result = self.fetcher.fetch(url)
            if not result.success:
                continue

            # Parse HTML
            parsed = self.parser.parse(result.content, url)

            # Store content
            self.storage.save(url, parsed)

            # Add discovered links to frontier
            current_depth = self.frontier.url_depth.get(url, 0)
            for link in parsed.links:
                self.frontier.add_url(link, current_depth + 1)

            pages_crawled += 1

        return CrawlResult(pages_crawled=pages_crawled)
```

## 7. Data Structures & Storage

### In-Memory Data Structures

```python
# URL Frontier
frontier_queue: Deque[str]              # O(1) append/popleft
url_depth_map: Dict[str, int]           # Track crawl depth

# Visited URLs
visited_urls: Set[str]                  # O(1) membership check

# Domain timing (for politeness)
last_request_time: Dict[str, float]     # domain -> timestamp
```

### Persistent Storage

**Simple File-Based Storage**
```
storage/
├── pages/
│   ├── page_001.html
│   ├── page_002.html
│   └── ...
├── metadata/
│   ├── page_001.json  # {url, timestamp, title, links_count}
│   └── page_002.json
└── crawl_stats.json   # Overall statistics
```

**Alternative: SQLite Database**
```sql
CREATE TABLE crawled_pages (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    content TEXT,
    crawled_at TIMESTAMP,
    depth INTEGER,
    status_code INTEGER
);

CREATE TABLE extracted_links (
    id INTEGER PRIMARY KEY,
    source_page_id INTEGER,
    target_url TEXT,
    FOREIGN KEY (source_page_id) REFERENCES crawled_pages(id)
);

CREATE INDEX idx_url ON crawled_pages(url);
```

## 8. Fault Tolerance & High Availability

### Error Handling Strategies

**Network Failures**
```python
def fetch_with_retry(self, url: str, max_retries: int = 3) -> FetchResult:
    for attempt in range(max_retries):
        try:
            result = self.fetch(url)
            if result.success:
                return result
        except (Timeout, ConnectionError) as e:
            if attempt == max_retries - 1:
                return FetchResult(success=False, error=str(e))
            time.sleep(2 ** attempt)  # Exponential backoff
```

**Malformed HTML**
```python
try:
    parsed = self.parser.parse(html, url)
except HTMLParseError as e:
    logger.warning(f"Failed to parse {url}: {e}")
    continue  # Skip to next URL
```

### State Persistence

**Checkpoint Mechanism**
```python
def save_checkpoint(self):
    checkpoint = {
        'frontier_urls': list(self.frontier.queue),
        'visited_urls': list(self.deduplicator.visited_urls),
        'pages_crawled': self.pages_crawled
    }
    with open('checkpoint.json', 'w') as f:
        json.dump(checkpoint, f)

def restore_from_checkpoint(self):
    if os.path.exists('checkpoint.json'):
        with open('checkpoint.json', 'r') as f:
            checkpoint = json.load(f)
            self.frontier.queue = deque(checkpoint['frontier_urls'])
            self.deduplicator.visited_urls = set(checkpoint['visited_urls'])
            self.pages_crawled = checkpoint['pages_crawled']
```

### Graceful Shutdown

```python
def handle_shutdown(self, signum, frame):
    logger.info("Shutdown signal received, saving state...")
    self.save_checkpoint()
    self.stop()
    sys.exit(0)
```

## 9. Monitoring & Observability

### Key Metrics to Track

```python
class CrawlMetrics:
    def __init__(self):
        self.pages_crawled = 0
        self.pages_failed = 0
        self.bytes_downloaded = 0
        self.links_discovered = 0
        self.start_time = time.time()
        self.error_counts = defaultdict(int)  # error_type -> count

    def record_success(self, page_size: int, links_count: int):
        self.pages_crawled += 1
        self.bytes_downloaded += page_size
        self.links_discovered += links_count

    def record_failure(self, error_type: str):
        self.pages_failed += 1
        self.error_counts[error_type] += 1

    def get_stats(self) -> Dict:
        elapsed = time.time() - self.start_time
        return {
            'pages_crawled': self.pages_crawled,
            'pages_failed': self.pages_failed,
            'success_rate': self.pages_crawled / (self.pages_crawled + self.pages_failed),
            'bytes_downloaded': self.bytes_downloaded,
            'links_discovered': self.links_discovered,
            'crawl_rate': self.pages_crawled / elapsed,  # pages/sec
            'elapsed_time': elapsed,
            'errors': dict(self.error_counts)
        }
```

### Logging Strategy

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('WebCrawler')

# Log key events
logger.info(f"Starting crawl with {len(seed_urls)} seed URLs")
logger.debug(f"Fetching URL: {url}")
logger.warning(f"Failed to fetch {url}: {error}")
logger.error(f"Critical error in crawler: {exception}")
```

### Progress Reporting

```python
def crawl_with_progress(self):
    with tqdm(total=self.max_pages, desc="Crawling") as pbar:
        while not self.frontier.is_empty() and self.pages_crawled < self.max_pages:
            # ... crawl logic ...
            pbar.update(1)
            pbar.set_postfix({
                'queue_size': len(self.frontier.queue),
                'visited': len(self.deduplicator.visited_urls)
            })
```

## 10. Scalability

### Current Limitations
- **Single-threaded**: Sequential processing limits throughput
- **In-memory storage**: Visited URLs limited by RAM
- **No prioritization**: BFS treats all URLs equally
- **Simple deduplication**: Doesn't handle URL variations well

### Scaling to Medium Scale (10K-100K pages)

**Multi-threading**
```python
from concurrent.futures import ThreadPoolExecutor

class ParallelCrawler:
    def __init__(self, num_threads: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        self.lock = threading.Lock()  # Protect shared data structures

    def crawl_parallel(self):
        futures = []
        while not self.frontier.is_empty():
            # Submit multiple fetch tasks
            for _ in range(self.num_threads):
                url = self.frontier.get_next_url()
                if url:
                    future = self.executor.submit(self.crawl_single_url, url)
                    futures.append(future)

            # Wait for completion
            for future in futures:
                future.result()
```

**Persistent Deduplication**
```python
# Use bloom filter for memory-efficient deduplication
from pybloom_live import BloomFilter

class ScalableDeduplicator:
    def __init__(self, capacity: int = 100000):
        self.bloom = BloomFilter(capacity=capacity, error_rate=0.001)
        # Bloom filter uses ~1.2MB for 100K URLs

    def is_visited(self, url: str) -> bool:
        return url in self.bloom

    def mark_visited(self, url: str):
        self.bloom.add(url)
```

**URL Prioritization**
```python
import heapq

class PriorityURLFrontier:
    def __init__(self):
        self.heap = []  # Min heap
        self.counter = 0

    def add_url(self, url: str, priority: int):
        # Lower priority number = higher priority
        heapq.heappush(self.heap, (priority, self.counter, url))
        self.counter += 1

    def get_next_url(self) -> Optional[str]:
        if self.heap:
            return heapq.heappop(self.heap)[2]
        return None
```

### Path to Distributed Crawling
- Use message queue (RabbitMQ) for distributed URL frontier
- Implement distributed hash table for URL deduplication
- Store content in distributed storage (S3)
- Use distributed coordination (ZooKeeper) for crawler instances
- Implement consistent hashing for domain partitioning

## 11. Trade-offs

### BFS vs DFS Traversal
**BFS (Current)**
- Pros: Discovers important pages quickly, balanced crawl
- Cons: Higher memory usage (large frontier queue)

**DFS Alternative**
- Pros: Lower memory (stack-based), deeper exploration
- Cons: May get stuck in deep paths, miss important pages

### Politeness vs Speed
**Conservative (1 req/sec)**
- Pros: Respectful to servers, lower ban risk
- Cons: Slower crawling

**Aggressive (10 req/sec)**
- Pros: Faster crawling
- Cons: May overload servers, risk of IP blocking

### Storage: Files vs Database
**Files**
- Pros: Simple, no dependencies, easy to inspect
- Cons: Slower queries, no indexing, harder to manage at scale

**SQLite**
- Pros: Indexed queries, ACID properties, relational data
- Cons: Added complexity, locking issues with concurrent writes

### URL Normalization Strictness
**Strict**
- Pros: Better deduplication, fewer duplicate pages
- Cons: May miss legitimate variations

**Lenient**
- Pros: Captures more content variations
- Cons: More duplicate content, larger storage

### Synchronous vs Asynchronous I/O
**Synchronous (Current)**
- Pros: Simpler code, easier debugging
- Cons: Blocked on I/O, lower throughput

**Async Alternative**
```python
import asyncio
import aiohttp

async def fetch_async(self, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```
- Pros: Higher throughput, better resource utilization
- Cons: More complex code, harder debugging

## 12. Follow-up Questions

### Design & Requirements
1. How would you handle robots.txt parsing and compliance?
2. How would you detect and handle crawler traps (infinite URL spaces)?
3. How would you prioritize URLs (PageRank-style vs recrawl frequency)?
4. How would you handle different content types (PDF, images, videos)?

### Scalability
5. How would you scale this to crawl millions of pages?
6. How would you distribute the crawler across multiple machines?
7. How would you partition the URL space for parallel crawling?
8. How would you handle domain-specific rate limiting in a distributed system?

### Quality & Reliability
9. How would you detect duplicate content (not just duplicate URLs)?
10. How would you handle URL redirects and canonicalization?
11. How would you deal with dynamic content loaded via JavaScript?
12. How would you validate and sanitize downloaded content?

### Politeness & Ethics
13. How would you implement adaptive rate limiting based on server response times?
14. How would you handle websites that explicitly block crawlers?
15. How would you respect different crawl-delay directives for different user agents?

### Advanced Features
16. How would you implement focused crawling for specific topics?
17. How would you add support for incremental crawling (recrawl only changed pages)?
18. How would you implement URL frontier prioritization based on page importance?
19. How would you extract structured data from crawled pages?
20. How would you build a crawler that respects user privacy and GDPR?

### Implementation
21. What data structure would you use for efficient URL deduplication at 100M scale?
22. How would you implement a distributed URL frontier?
23. How would you handle time zones and timestamps for scheduling recrawls?
24. How would you monitor crawler health and performance in production?
