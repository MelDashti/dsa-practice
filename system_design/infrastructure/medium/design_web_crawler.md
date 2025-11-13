# Design Web Crawler - Large-Scale (Google-style)

## 1. Problem Statement

Design a large-scale distributed web crawler similar to what Google or Bing uses to index the web. The system should crawl billions of web pages efficiently, respect politeness policies, handle diverse content types, detect duplicate content, and continuously update its index with fresh content.

## 2. Requirements

### Functional Requirements
- Crawl billions of web pages across millions of domains
- Extract and parse HTML, JavaScript-rendered content
- Follow links and discover new pages
- Handle different content types (HTML, PDF, images, videos)
- Detect and filter duplicate content
- Support prioritized crawling (important pages first)
- Respect robots.txt and rate limiting per domain
- Support recrawling for freshness
- Extract structured data and metadata

### Non-Functional Requirements
- **Scale**: Crawl 10 billion pages per month (3,850 pages/second)
- **Latency**: Process and store page within 1 second of fetch
- **Throughput**: Handle 50,000 concurrent fetches
- **Storage**: Store 10 PB of content
- **Politeness**: Maximum 1 request per second per domain
- **Availability**: 99.9% uptime
- **Freshness**: Recrawl important pages every 1-7 days

### Out of Scope
- Content indexing and search (separate component)
- Natural language processing
- Deep learning for content understanding
- Ad crawling and click fraud detection

## 3. Capacity Estimation

### Scale Assumptions
- Total pages to crawl: 10 billion/month
- Average page size: 100 KB (HTML + assets)
- Average links per page: 100
- Crawl rate: 3,850 pages/second
- Recrawl frequency: 30 days average
- Number of domains: 50 million
- Active URLs in frontier: 100 million

### Storage Estimation
```
New content per month:
10B pages × 100 KB = 1 PB/month

Total storage (with history):
- Current content: 1 PB
- Historical snapshots (3 months): 3 PB
- Metadata and indexes: 500 TB
- URL frontier and dedup: 200 TB
Total: ~4.7 PB

With 3x replication: 14 PB
```

### Memory Estimation
```
URL Frontier:
- 100M URLs × 200 bytes = 20 GB

URL Deduplication (Bloom Filter):
- 10B URLs with 1% false positive rate
- Required bits: 10B × 10 = 100 billion bits
- Memory: 12.5 GB

Domain State (politeness):
- 50M domains × 100 bytes = 5 GB

Total memory per crawler node: ~40 GB
Crawler nodes: 1,000 nodes
Total memory: 40 TB
```

### Network Bandwidth
```
Download bandwidth:
3,850 pages/sec × 100 KB = 385 MB/sec = 3 Gbps

Upload bandwidth (to storage):
Same as download: 3 Gbps

DNS queries:
3,850 pages/sec / 100 pages per domain = 38.5 domains/sec
Negligible bandwidth

Total bandwidth: ~10 Gbps (with headroom)
```

### Compute Estimation
```
Crawler workers: 1,000 nodes
Each node: 50 concurrent fetches
Total concurrent fetches: 50,000

CPU per node:
- URL processing: 10%
- HTML parsing: 30%
- Deduplication: 20%
- Content extraction: 40%

Total CPU: 16 cores × 1,000 nodes = 16,000 cores
```

## 4. High-Level Design

```
                    ┌─────────────────┐
                    │  Seed URLs &    │
                    │  Sitemap Seeds  │
                    └────────┬─────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │        URL Frontier Service            │
        │  (Distributed Priority Queue)          │
        │  - Prioritization                      │
        │  - Domain partitioning                 │
        └────────┬────────────────────────────────┘
                 │
                 │ URLs to crawl
                 ▼
    ┌────────────────────────────────────────┐
    │         Crawler Cluster                │
    │    (1000 worker nodes)                 │
    │                                        │
    │  ┌──────────────────────────────┐    │
    │  │   Crawler Worker             │    │
    │  │  - DNS Resolution            │    │
    │  │  - HTTP Fetch                │    │
    │  │  - Politeness Check          │    │
    │  │  - Content Download          │    │
    │  └──────┬───────────────────────┘    │
    └─────────┼──────────────────────────────┘
              │
              ▼
    ┌─────────────────────────┐
    │    Content Processor    │
    │  - HTML Parser          │
    │  - Link Extractor       │
    │  - Content Extractor    │
    │  - JS Renderer          │
    └──────┬──────────────────┘
           │
           ├─────────────────────────────────┐
           │                                 │
           ▼                                 ▼
    ┌──────────────┐              ┌──────────────────┐
    │  Dedup       │              │  Content Store   │
    │  Service     │              │  (S3/GCS/HDFS)   │
    │              │              │  - HTML          │
    │ - Bloom      │              │  - Extracted     │
    │   Filter     │              │    Text          │
    │ - Content    │              │  - Metadata      │
    │   Hash       │              └──────────────────┘
    └──────┬───────┘
           │
           │ New URLs
           ▼
    ┌──────────────────┐
    │  URL Frontier    │
    │  (Priority Queue)│
    └──────────────────┘

Supporting Services:
┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ DNS Cache   │  │ robots.txt  │  │ Scheduler    │  │ Monitoring   │
│ Service     │  │ Service     │  │ (Recrawl)    │  │ & Metrics    │
└─────────────┘  └─────────────┘  └──────────────┘  └──────────────┘
```

### Core Components
1. **URL Frontier**: Distributed priority queue of URLs to crawl
2. **Crawler Workers**: Distributed workers that fetch web pages
3. **Content Processor**: Parses HTML, extracts links and content
4. **Deduplication Service**: Detects duplicate URLs and content
5. **Content Store**: Distributed storage for crawled content
6. **DNS Cache**: Caches DNS resolutions
7. **Robots.txt Service**: Caches and serves robots.txt rules
8. **Scheduler**: Manages recrawl schedules
9. **Monitoring**: Tracks crawler health and metrics

## 5. API Design

### URL Frontier API

```python
class URLFrontierService:
    def add_urls(self, urls: List[URLItem], priority: int) -> bool:
        """
        Add URLs to frontier with priority
        URLItem: {url, source_url, depth, timestamp}
        priority: 0 (highest) to 100 (lowest)
        """
        pass

    def get_next_batch(self, worker_id: str, batch_size: int) -> List[URLItem]:
        """
        Get next batch of URLs for worker to crawl
        Returns URLs from different domains for politeness
        """
        pass

    def mark_completed(self, urls: List[str]) -> bool:
        """Mark URLs as successfully crawled"""
        pass

    def mark_failed(self, urls: List[str], error: str) -> bool:
        """Mark URLs as failed with error reason"""
        pass

    def get_stats(self) -> FrontierStats:
        """
        Get frontier statistics
        Returns: queue_size, domains_count, avg_priority
        """
        pass
```

### Crawler Worker API

```python
class CrawlerWorker:
    def crawl_url(self, url: str) -> CrawlResult:
        """
        Crawl a single URL
        Returns: content, links, metadata, status
        """
        pass

    def set_politeness_delay(self, domain: str, delay_ms: int):
        """Set politeness delay for domain"""
        pass

    def get_status(self) -> WorkerStatus:
        """
        Get worker status
        Returns: active_fetches, pages_crawled, errors
        """
        pass
```

### Content Processor API

```python
class ContentProcessor:
    def process_page(self, html: str, url: str) -> ProcessedPage:
        """
        Process HTML page
        Returns: extracted_text, links, metadata, language
        """
        pass

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract and normalize all links"""
        pass

    def detect_content_type(self, response: HTTPResponse) -> str:
        """Detect content type (HTML, PDF, image, etc.)"""
        pass

    def render_javascript(self, url: str) -> str:
        """Render JavaScript-heavy page (headless browser)"""
        pass
```

### Deduplication API

```python
class DeduplicationService:
    def is_url_seen(self, url: str) -> bool:
        """Check if URL has been crawled"""
        pass

    def mark_url_seen(self, url: str, timestamp: int):
        """Mark URL as crawled"""
        pass

    def is_content_duplicate(self, content_hash: str) -> bool:
        """Check if content is duplicate (SimHash)"""
        pass

    def add_content_fingerprint(self, content_hash: str, url: str):
        """Add content fingerprint"""
        pass
```

## 6. Component Design

### URL Frontier

**Multi-Level Priority Queue with Domain Partitioning**

```python
class DistributedURLFrontier:
    """
    Priority queue partitioned by domain for politeness
    Uses consistent hashing for distribution
    """

    def __init__(self):
        # Priority queues (0 = highest priority)
        self.priority_queues = {
            0: deque(),   # Critical (homepage, sitemaps)
            1: deque(),   # High (popular sites)
            2: deque(),   # Medium (normal sites)
            3: deque()    # Low (deep pages, discovered links)
        }

        # Domain-specific queues for politeness
        self.domain_queues = {}  # domain -> queue of URLs

        # Domain last access time (for rate limiting)
        self.domain_last_access = {}  # domain -> timestamp

        # Domain crawl delay from robots.txt
        self.domain_delays = {}  # domain -> delay_seconds

        self.lock = threading.Lock()

    def add_url(self, url: str, priority: int, depth: int):
        domain = self.extract_domain(url)

        # Add to priority queue
        item = URLItem(url=url, priority=priority, depth=depth, domain=domain)
        self.priority_queues[priority].append(item)

        # Add to domain queue
        if domain not in self.domain_queues:
            self.domain_queues[domain] = deque()
        self.domain_queues[domain].append(item)

    def get_next_batch(self, batch_size: int) -> List[URLItem]:
        """
        Get next batch of URLs respecting politeness
        Returns URLs from different domains
        """
        batch = []
        current_time = time.time()

        with self.lock:
            # Iterate through priority levels
            for priority in sorted(self.priority_queues.keys()):
                queue = self.priority_queues[priority]

                while len(batch) < batch_size and queue:
                    item = queue.popleft()
                    domain = item.domain

                    # Check politeness
                    if self.can_crawl_domain(domain, current_time):
                        batch.append(item)
                        self.domain_last_access[domain] = current_time

                        # Remove from domain queue
                        if domain in self.domain_queues:
                            self.domain_queues[domain].remove(item)
                    else:
                        # Put back in queue
                        queue.append(item)

                if len(batch) >= batch_size:
                    break

        return batch

    def can_crawl_domain(self, domain: str, current_time: float) -> bool:
        """Check if we can crawl domain based on politeness rules"""
        if domain not in self.domain_last_access:
            return True

        last_access = self.domain_last_access[domain]
        delay = self.domain_delays.get(domain, 1.0)  # Default 1 second

        return (current_time - last_access) >= delay
```

**Algorithm Complexity**:
- Add URL: O(1)
- Get next batch: O(batch_size × priority_levels)
- Space: O(n) where n is number of URLs

### URL Prioritization

**PageRank-based Priority Scoring**

```python
class URLPrioritizer:
    def __init__(self):
        self.pagerank_cache = {}  # URL -> PageRank score
        self.domain_authority = {}  # domain -> authority score

    def calculate_priority(self, url: str, source_url: str, depth: int) -> int:
        """
        Calculate priority score (0-3)
        0 = highest priority, 3 = lowest
        """
        score = 0

        # Factor 1: Domain authority
        domain = extract_domain(url)
        domain_score = self.domain_authority.get(domain, 0.5)
        score += domain_score * 40  # 0-40 points

        # Factor 2: Depth (shallower = better)
        depth_penalty = min(depth * 5, 30)
        score += depth_penalty  # 0-30 points

        # Factor 3: PageRank of source page
        source_pagerank = self.pagerank_cache.get(source_url, 0.1)
        score += (1 - source_pagerank) * 20  # 0-20 points

        # Factor 4: URL signals
        if self.is_homepage(url):
            score -= 20
        elif self.is_sitemap(url):
            score -= 15
        elif self.has_query_params(url):
            score += 10

        # Map to priority levels
        if score < 25:
            return 0  # Critical
        elif score < 50:
            return 1  # High
        elif score < 75:
            return 2  # Medium
        else:
            return 3  # Low

    def is_homepage(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.path in ['/', '/index.html', '/index.htm']

    def is_sitemap(self, url: str) -> bool:
        return 'sitemap' in url.lower() and url.endswith('.xml')
```

### Crawler Worker

**Parallel Fetching with Politeness**

```python
class CrawlerWorker:
    def __init__(self, worker_id: str, concurrency: int = 50):
        self.worker_id = worker_id
        self.concurrency = concurrency
        self.session = requests.Session()

        # Connection pooling
        adapter = HTTPAdapter(
            pool_connections=concurrency,
            pool_maxsize=concurrency * 2,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # Per-domain rate limiters
        self.domain_limiters = {}  # domain -> RateLimiter

    async def crawl_batch(self, urls: List[str]):
        """Crawl batch of URLs concurrently"""
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.crawl_url(url))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def crawl_url(self, url: str) -> CrawlResult:
        """Crawl single URL"""
        domain = extract_domain(url)

        try:
            # 1. Check robots.txt
            if not await self.is_allowed(url):
                return CrawlResult(url, status='blocked', reason='robots.txt')

            # 2. Rate limit per domain
            await self.wait_for_rate_limit(domain)

            # 3. DNS resolution (with caching)
            ip_address = await self.resolve_dns(domain)

            # 4. Fetch page
            start_time = time.time()
            response = await self.fetch_page(url)
            fetch_latency = time.time() - start_time

            # 5. Validate response
            if response.status_code != 200:
                return CrawlResult(url, status='error',
                                 error=f"HTTP {response.status_code}")

            # 6. Check content type
            content_type = response.headers.get('Content-Type', '')
            if not self.is_crawlable_content(content_type):
                return CrawlResult(url, status='skipped',
                                 reason=f"Unsupported type: {content_type}")

            # 7. Download content
            content = response.text

            # 8. Return result
            return CrawlResult(
                url=url,
                status='success',
                content=content,
                status_code=response.status_code,
                headers=dict(response.headers),
                fetch_latency=fetch_latency,
                timestamp=time.time()
            )

        except Exception as e:
            return CrawlResult(url, status='error', error=str(e))

    async def wait_for_rate_limit(self, domain: str):
        """Enforce rate limit per domain"""
        if domain not in self.domain_limiters:
            # Get crawl delay from robots.txt (default 1 second)
            delay = await self.get_crawl_delay(domain)
            self.domain_limiters[domain] = RateLimiter(delay)

        await self.domain_limiters[domain].wait()

    async def resolve_dns(self, domain: str) -> str:
        """Resolve DNS with caching"""
        # Check local cache
        if domain in self.dns_cache:
            return self.dns_cache[domain]

        # Query DNS cache service
        ip = await self.dns_service.resolve(domain)
        self.dns_cache[domain] = ip
        return ip
```

### Content Processor

**HTML Parsing and Link Extraction**

```python
class ContentProcessor:
    def __init__(self):
        self.parser = BeautifulSoup
        self.js_renderer = None  # Headless Chrome for JS rendering

    def process_page(self, html: str, url: str) -> ProcessedPage:
        """Process HTML and extract data"""
        soup = BeautifulSoup(html, 'lxml')

        # Extract links
        links = self.extract_links(soup, url)

        # Extract text content
        text = self.extract_text(soup)

        # Extract metadata
        metadata = self.extract_metadata(soup, url)

        # Detect language
        language = self.detect_language(text)

        # Extract structured data (JSON-LD, microdata)
        structured_data = self.extract_structured_data(soup)

        return ProcessedPage(
            url=url,
            links=links,
            text=text,
            metadata=metadata,
            language=language,
            structured_data=structured_data
        )

    def extract_links(self, soup, base_url: str) -> List[str]:
        """Extract and normalize all links"""
        links = []

        # Extract from <a> tags
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            absolute_url = urljoin(base_url, href)

            # Normalize URL
            normalized = self.normalize_url(absolute_url)

            if self.is_valid_url(normalized):
                links.append(normalized)

        # Extract from <link> tags (canonicals, alternates)
        for link in soup.find_all('link', href=True):
            if link.get('rel') in [['canonical'], ['alternate']]:
                href = link['href']
                absolute_url = urljoin(base_url, href)
                normalized = self.normalize_url(absolute_url)
                if self.is_valid_url(normalized):
                    links.append(normalized)

        # Deduplicate
        return list(set(links))

    def normalize_url(self, url: str) -> str:
        """
        Normalize URL for deduplication
        - Convert to lowercase (domain part)
        - Remove trailing slash
        - Remove default ports (80, 443)
        - Remove fragments (#)
        - Sort query parameters
        - Remove session IDs
        """
        parsed = urlparse(url)

        # Normalize domain
        domain = parsed.netloc.lower()

        # Remove default ports
        if domain.endswith(':80') or domain.endswith(':443'):
            domain = domain.rsplit(':', 1)[0]

        # Normalize path
        path = parsed.path.rstrip('/') or '/'

        # Sort query parameters
        query_params = parse_qs(parsed.query)
        # Remove common session parameters
        session_params = ['sessionid', 'sid', 'jsessionid', 'phpsessid']
        for param in session_params:
            query_params.pop(param, None)

        sorted_query = urlencode(sorted(query_params.items()))

        # Reconstruct URL
        normalized = f"{parsed.scheme}://{domain}{path}"
        if sorted_query:
            normalized += f"?{sorted_query}"

        return normalized

    def extract_text(self, soup) -> str:
        """Extract visible text from HTML"""
        # Remove script and style tags
        for script in soup(['script', 'style', 'noscript']):
            script.decompose()

        # Get text
        text = soup.get_text(separator=' ', strip=True)

        # Clean whitespace
        text = ' '.join(text.split())

        return text

    def extract_metadata(self, soup, url: str) -> Dict:
        """Extract page metadata"""
        metadata = {
            'url': url,
            'title': None,
            'description': None,
            'keywords': None,
            'author': None,
            'published_date': None,
            'canonical_url': None
        }

        # Title
        if soup.title:
            metadata['title'] = soup.title.string

        # Meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property_attr = meta.get('property', '').lower()
            content = meta.get('content', '')

            if name == 'description' or property_attr == 'og:description':
                metadata['description'] = content
            elif name == 'keywords':
                metadata['keywords'] = content
            elif name == 'author':
                metadata['author'] = content
            elif property_attr == 'article:published_time':
                metadata['published_date'] = content

        # Canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            metadata['canonical_url'] = canonical['href']

        return metadata

    def render_javascript(self, url: str) -> str:
        """Render JavaScript-heavy page using headless browser"""
        if self.js_renderer is None:
            self.js_renderer = HeadlessChrome()

        html = self.js_renderer.render(url, wait_time=3)
        return html
```

### Deduplication Service

**Bloom Filter + Content Hashing**

```python
class DeduplicationService:
    def __init__(self):
        # URL deduplication - Bloom filter
        self.url_bloom = BloomFilter(
            capacity=10_000_000_000,  # 10 billion URLs
            error_rate=0.01  # 1% false positive
        )

        # Content deduplication - SimHash
        self.content_hashes = {}  # simhash -> URL
        self.simhash_bits = 64

    def is_url_seen(self, url: str) -> bool:
        """Check if URL has been crawled (probabilistic)"""
        normalized = self.normalize_url(url)
        return normalized in self.url_bloom

    def mark_url_seen(self, url: str):
        """Mark URL as seen"""
        normalized = self.normalize_url(url)
        self.url_bloom.add(normalized)

        # Also store in persistent storage
        self.store_url(normalized, timestamp=time.time())

    def is_content_duplicate(self, content: str) -> Tuple[bool, str]:
        """
        Check if content is duplicate using SimHash
        Returns (is_duplicate, original_url)
        """
        # Calculate SimHash
        content_hash = self.simhash(content)

        # Check for near-duplicates (Hamming distance <= 3)
        for stored_hash, url in self.content_hashes.items():
            hamming_dist = self.hamming_distance(content_hash, stored_hash)
            if hamming_dist <= 3:
                return True, url

        # Not a duplicate, store this hash
        self.content_hashes[content_hash] = url
        return False, None

    def simhash(self, content: str) -> int:
        """
        Calculate SimHash for content
        SimHash is a locality-sensitive hash for near-duplicate detection
        """
        # Tokenize content
        tokens = self.tokenize(content)

        # Initialize bit vector
        v = [0] * self.simhash_bits

        # For each token
        for token in tokens:
            # Hash token to get bit vector
            token_hash = hash(token) % (2 ** self.simhash_bits)

            # Update vector
            for i in range(self.simhash_bits):
                if token_hash & (1 << i):
                    v[i] += 1
                else:
                    v[i] -= 1

        # Generate final hash
        fingerprint = 0
        for i in range(self.simhash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)

        return fingerprint

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """Calculate Hamming distance between two hashes"""
        xor = hash1 ^ hash2
        return bin(xor).count('1')

    def tokenize(self, content: str) -> List[str]:
        """Tokenize content into shingles"""
        # Use 3-grams (shingles of 3 words)
        words = content.lower().split()
        shingles = []

        for i in range(len(words) - 2):
            shingle = ' '.join(words[i:i+3])
            shingles.append(shingle)

        return shingles
```

### Robots.txt Service

**Caching and Parsing robots.txt**

```python
class RobotsTxtService:
    def __init__(self):
        self.cache = {}  # domain -> RobotsTxtRules
        self.cache_ttl = 86400  # 24 hours
        self.user_agent = 'MyBot/1.0'

    async def is_allowed(self, url: str) -> bool:
        """Check if URL is allowed to crawl"""
        domain = extract_domain(url)

        # Get rules from cache or fetch
        rules = await self.get_rules(domain)

        # Check if URL is allowed
        return rules.is_allowed(url, self.user_agent)

    async def get_rules(self, domain: str) -> RobotsTxtRules:
        """Get robots.txt rules for domain"""
        # Check cache
        if domain in self.cache:
            rules, timestamp = self.cache[domain]
            if time.time() - timestamp < self.cache_ttl:
                return rules

        # Fetch robots.txt
        robots_url = f"https://{domain}/robots.txt"
        try:
            response = await self.fetch(robots_url)
            if response.status_code == 200:
                rules = self.parse_robots_txt(response.text)
            else:
                # No robots.txt, allow all
                rules = RobotsTxtRules(allow_all=True)
        except Exception:
            # Error fetching, allow all
            rules = RobotsTxtRules(allow_all=True)

        # Cache rules
        self.cache[domain] = (rules, time.time())
        return rules

    def parse_robots_txt(self, content: str) -> RobotsTxtRules:
        """Parse robots.txt content"""
        rules = RobotsTxtRules()

        current_user_agent = None
        for line in content.split('\n'):
            line = line.strip()

            if line.startswith('#') or not line:
                continue

            if line.lower().startswith('user-agent:'):
                current_user_agent = line.split(':', 1)[1].strip()
            elif line.lower().startswith('disallow:'):
                if current_user_agent == '*' or current_user_agent == self.user_agent:
                    path = line.split(':', 1)[1].strip()
                    rules.add_disallow(path)
            elif line.lower().startswith('allow:'):
                if current_user_agent == '*' or current_user_agent == self.user_agent:
                    path = line.split(':', 1)[1].strip()
                    rules.add_allow(path)
            elif line.lower().startswith('crawl-delay:'):
                delay = float(line.split(':', 1)[1].strip())
                rules.set_crawl_delay(delay)
            elif line.lower().startswith('sitemap:'):
                sitemap_url = line.split(':', 1)[1].strip()
                rules.add_sitemap(sitemap_url)

        return rules

class RobotsTxtRules:
    def __init__(self, allow_all=False):
        self.allow_all = allow_all
        self.disallow_paths = []
        self.allow_paths = []
        self.crawl_delay = 1.0  # Default 1 second
        self.sitemaps = []

    def is_allowed(self, url: str, user_agent: str) -> bool:
        if self.allow_all:
            return True

        parsed = urlparse(url)
        path = parsed.path

        # Check allow rules (more specific)
        for allow_path in self.allow_paths:
            if path.startswith(allow_path):
                return True

        # Check disallow rules
        for disallow_path in self.disallow_paths:
            if path.startswith(disallow_path):
                return False

        # Default: allowed
        return True
```

### Scheduler for Recrawling

**Priority-based Recrawl Scheduling**

```python
class RecrawlScheduler:
    def __init__(self):
        self.schedule_queue = []  # Min heap of (next_crawl_time, url)
        self.crawl_history = {}  # url -> CrawlHistory

    def schedule_recrawl(self, url: str, priority: int):
        """Schedule URL for recrawling"""
        # Calculate next crawl time based on priority
        interval = self.get_recrawl_interval(priority)
        next_crawl_time = time.time() + interval

        # Add to schedule
        heapq.heappush(self.schedule_queue, (next_crawl_time, url))

    def get_recrawl_interval(self, priority: int) -> int:
        """
        Get recrawl interval based on priority
        0 (critical): 1 day
        1 (high): 7 days
        2 (medium): 30 days
        3 (low): 90 days
        """
        intervals = {
            0: 86400,      # 1 day
            1: 604800,     # 7 days
            2: 2592000,    # 30 days
            3: 7776000     # 90 days
        }
        return intervals.get(priority, 2592000)

    def get_urls_to_recrawl(self, batch_size: int) -> List[str]:
        """Get URLs that are due for recrawling"""
        current_time = time.time()
        urls_to_crawl = []

        while len(urls_to_crawl) < batch_size and self.schedule_queue:
            next_time, url = heapq.heappop(self.schedule_queue)

            if next_time <= current_time:
                urls_to_crawl.append(url)
            else:
                # Put back in queue (not due yet)
                heapq.heappush(self.schedule_queue, (next_time, url))
                break

        return urls_to_crawl

    def update_crawl_history(self, url: str, status: str, content_hash: str):
        """Update crawl history for URL"""
        if url not in self.crawl_history:
            self.crawl_history[url] = CrawlHistory(url)

        history = self.crawl_history[url]
        history.add_crawl(
            timestamp=time.time(),
            status=status,
            content_hash=content_hash
        )

        # Adjust recrawl frequency if content hasn't changed
        if history.is_stable():
            # Content stable, reduce crawl frequency
            self.increase_recrawl_interval(url)
        else:
            # Content changing frequently, increase crawl frequency
            self.decrease_recrawl_interval(url)
```

## 7. Data Structures & Storage

### URL Storage

**Distributed Hash Table for URL Metadata**

```python
# URL metadata stored in distributed key-value store (e.g., Cassandra)

CREATE TABLE urls (
    url_hash TEXT PRIMARY KEY,      # MD5 hash of normalized URL
    url TEXT,                        # Original URL
    domain TEXT,                     # Extracted domain
    priority INT,                    # Priority level (0-3)
    depth INT,                       # Crawl depth
    last_crawled TIMESTAMP,          # Last crawl time
    next_crawl TIMESTAMP,            # Scheduled next crawl
    crawl_count INT,                 # Number of times crawled
    content_hash TEXT,               # SimHash of content
    status TEXT,                     # last, success, error, blocked
    error_message TEXT,              # Error if failed
    page_rank DOUBLE,                # PageRank score
    inbound_links INT,               # Number of inbound links
    outbound_links INT               # Number of outbound links
);

CREATE INDEX ON urls (domain);
CREATE INDEX ON urls (next_crawl);
CREATE INDEX ON urls (priority);
```

### Content Storage

**Distributed Object Storage (S3/GCS/HDFS)**

```
Storage Structure:
s3://crawler-content/
├── raw/
│   ├── 2025/01/12/
│   │   ├── domain1/
│   │   │   ├── page1_hash.html.gz
│   │   │   └── page2_hash.html.gz
│   │   └── domain2/
│   │       └── page1_hash.html.gz
│   └── ...
├── processed/
│   ├── 2025/01/12/
│   │   ├── domain1/
│   │   │   ├── page1_hash.json  # {url, text, links, metadata}
│   │   │   └── page2_hash.json
│   │   └── ...
└── snapshots/
    ├── 2025/01/12/
    │   └── urls_snapshot.parquet  # Bulk URL metadata
    └── ...

File naming: {md5_hash}.{extension}.gz
Compression: gzip for HTML, snappy for JSON
Partitioning: By date and domain for efficient access
```

### Bloom Filter for URL Dedup

```python
# In-memory Bloom filter with persistent backup

class PersistentBloomFilter:
    def __init__(self, capacity: int, error_rate: float):
        self.bloom = BloomFilter(capacity, error_rate)
        self.backup_file = 'url_bloom_filter.bin'

    def add(self, url: str):
        self.bloom.add(url)
        # Periodically persist to disk
        if self.should_persist():
            self.persist()

    def persist(self):
        with open(self.backup_file, 'wb') as f:
            pickle.dump(self.bloom, f)

    def load(self):
        if os.path.exists(self.backup_file):
            with open(self.backup_file, 'rb') as f:
                self.bloom = pickle.load(f)

# Memory usage: ~1.2GB for 1B URLs at 1% error rate
```

## 8. Fault Tolerance & High Availability

### Crawler Worker Failures

```python
class WorkerHealthMonitor:
    def __init__(self):
        self.workers = {}  # worker_id -> WorkerState
        self.heartbeat_timeout = 60  # seconds

    def handle_worker_failure(self, worker_id: str):
        """Reassign URLs from failed worker"""
        # 1. Get URLs assigned to failed worker
        assigned_urls = self.get_assigned_urls(worker_id)

        # 2. Mark worker as failed
        self.workers[worker_id].status = 'failed'

        # 3. Return URLs to frontier
        for url in assigned_urls:
            self.url_frontier.add_url(url, priority=1)

        # 4. Start new worker to replace failed one
        self.start_new_worker()

    def check_heartbeats(self):
        """Periodically check worker heartbeats"""
        while True:
            time.sleep(10)
            current_time = time.time()

            for worker_id, state in self.workers.items():
                if state.status == 'active':
                    time_since_heartbeat = current_time - state.last_heartbeat

                    if time_since_heartbeat > self.heartbeat_timeout:
                        self.handle_worker_failure(worker_id)
```

### URL Frontier Failures

```python
# Replicate frontier across multiple nodes
class ReplicatedURLFrontier:
    def __init__(self):
        self.primary = URLFrontierNode('primary')
        self.replicas = [
            URLFrontierNode('replica1'),
            URLFrontierNode('replica2')
        ]

    def add_url(self, url: str, priority: int):
        # Write to primary
        self.primary.add_url(url, priority)

        # Asynchronously replicate to replicas
        for replica in self.replicas:
            asyncio.create_task(replica.add_url(url, priority))

    def get_next_batch(self, batch_size: int):
        try:
            return self.primary.get_next_batch(batch_size)
        except Exception:
            # Primary failed, use replica
            return self.replicas[0].get_next_batch(batch_size)
```

### Data Loss Prevention

```python
# Checkpointing for recovery
class CrawlerCheckpoint:
    def __init__(self):
        self.checkpoint_interval = 3600  # 1 hour

    def create_checkpoint(self):
        """Save crawler state for recovery"""
        checkpoint = {
            'frontier_size': self.url_frontier.size(),
            'urls_crawled': self.metrics.pages_crawled,
            'timestamp': time.time(),
            'frontier_sample': self.url_frontier.get_sample(10000)
        }

        # Save to persistent storage
        self.save_to_s3('checkpoints/latest.json', checkpoint)

    def restore_from_checkpoint(self):
        """Restore crawler state after failure"""
        checkpoint = self.load_from_s3('checkpoints/latest.json')

        # Restore frontier
        for url in checkpoint['frontier_sample']:
            self.url_frontier.add_url(url)

        # Restore metrics
        self.metrics.pages_crawled = checkpoint['urls_crawled']
```

## 9. Monitoring & Observability

### Key Metrics

```python
class CrawlerMetrics:
    # Throughput
    pages_crawled_per_sec = Gauge()
    bytes_downloaded_per_sec = Gauge()

    # Latency
    fetch_latency_p50 = Histogram()
    fetch_latency_p99 = Histogram()
    dns_resolution_latency = Histogram()

    # Queue metrics
    url_frontier_size = Gauge()
    pending_urls_by_priority = Gauge(labels=['priority'])

    # Success/error rates
    successful_crawls = Counter()
    failed_crawls = Counter(labels=['error_type'])
    blocked_by_robots = Counter()

    # Resource utilization
    active_workers = Gauge()
    cpu_utilization = Gauge()
    memory_utilization = Gauge()
    disk_utilization = Gauge()

    # Domain coverage
    unique_domains_crawled = Counter()
    domains_per_hour = Gauge()

    # Content metrics
    duplicate_content_detected = Counter()
    new_urls_discovered = Counter()
```

### Alerting

```yaml
alerts:
  - name: CrawlRateDrop
    condition: pages_crawled_per_sec < 1000
    severity: warning
    description: "Crawl rate dropped below threshold"

  - name: HighErrorRate
    condition: failed_crawls / total_crawls > 0.1
    severity: critical
    description: "Error rate >10%"

  - name: FrontierDepleted
    condition: url_frontier_size < 10000
    severity: warning
    description: "URL frontier running low"

  - name: WorkerDown
    condition: active_workers < min_workers
    severity: critical
    description: "Not enough active workers"
```

## 10. Scalability

### Horizontal Scaling

```python
# Add more crawler workers
def scale_crawlers(target_throughput: int):
    """
    Scale crawler workers based on target throughput
    target_throughput: pages/second
    """
    pages_per_worker = 5  # Each worker crawls ~5 pages/sec
    required_workers = target_throughput / pages_per_worker

    current_workers = len(get_active_workers())

    if required_workers > current_workers:
        # Scale up
        new_workers = required_workers - current_workers
        for i in range(new_workers):
            start_crawler_worker()
    elif required_workers < current_workers:
        # Scale down
        workers_to_remove = current_workers - required_workers
        for i in range(workers_to_remove):
            stop_crawler_worker()
```

### Partitioning Strategies

**Domain-based Partitioning**
```python
def assign_domain_to_worker(domain: str, num_workers: int) -> int:
    """
    Assign domain to specific worker using consistent hashing
    Ensures all URLs from same domain go to same worker (politeness)
    """
    return consistent_hash(domain, num_workers)
```

### Caching Strategies

```python
class CrawlerCache:
    # DNS cache (reduce DNS queries)
    dns_cache = LRUCache(capacity=1_000_000, ttl=3600)

    # robots.txt cache
    robots_cache = LRUCache(capacity=100_000, ttl=86400)

    # PageRank cache
    pagerank_cache = LRUCache(capacity=10_000_000, ttl=604800)
```

## 11. Trade-offs

### Politeness vs Throughput
- **Polite (1 req/sec/domain)**: Respectful, but slower overall crawl
- **Aggressive (10 req/sec/domain)**: Faster, but risk of bans

### Freshness vs Coverage
- **Fresh (recrawl frequently)**: Up-to-date content, but limited coverage
- **Coverage (crawl new pages)**: More pages indexed, but stale content

### URL Normalization Strictness
- **Strict**: Fewer duplicates, but may miss content variations
- **Lenient**: More content, but higher duplicate rate

### Content Storage
- **Store raw HTML**: Enables reprocessing, but high storage cost
- **Store extracted text**: Lower storage, but can't reprocess

### Deduplication Strategy
- **Bloom filter only**: Fast, probabilistic (false positives possible)
- **Exact matching**: Accurate, but slower and more storage

## 12. Follow-up Questions

1. How would you handle JavaScript-heavy websites?
2. How would you detect and avoid crawler traps?
3. How would you implement focused crawling for specific topics?
4. How would you handle different document types (PDF, Word, etc.)?
5. How would you detect and handle cloaking (showing different content to crawlers)?
6. How would you implement incremental crawling (only crawl changed pages)?
7. How would you handle multilingual websites and character encodings?
8. How would you extract and store images efficiently?
9. How would you implement sitemap-based crawling?
10. How would you detect and respect dynamic crawl-delay directives?
11. How would you handle authentication and cookie-based sessions?
12. How would you implement a crawler for the dark web or Tor network?
13. How would you detect near-duplicate content more accurately?
14. How would you implement URL frontier prioritization based on link analysis?
15. How would you handle rate limiting from CDNs like Cloudflare?
16. How would you detect and filter low-quality or spam pages?
17. How would you implement crawl budget optimization?
18. How would you handle pagination and infinite scroll?
19. How would you crawl mobile-specific versions of websites?
20. How would you detect and handle soft-404 errors?
