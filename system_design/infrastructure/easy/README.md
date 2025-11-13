# Infrastructure - Easy Level

## Overview
This directory contains foundational infrastructure system design problems suitable for beginners. These problems introduce core concepts of building internet-scale systems with manageable scope and complexity.

## Problems

### 1. Web Crawler Basics
**File**: `web_crawler_basics.md`

**Description**: Design a basic web crawler that systematically browses the web and downloads pages. This problem introduces fundamental concepts like URL frontier management, deduplication, politeness policies, and content extraction.

**Key Concepts**:
- Breadth-First Search (BFS) traversal
- URL normalization and deduplication
- Rate limiting and politeness
- HTML parsing and link extraction
- Basic error handling

**Why Start Here**:
- Introduces graph traversal in web context
- Simple state management with queues and sets
- Foundation for understanding distributed crawling systems
- Practical application of data structures (queue, set, hash table)

**Related Problems**:
- Medium: Design Web Crawler (large-scale, distributed version)
- Core Components: Load Balancer (traffic distribution)
- Storage & Data: Content Delivery Network (content distribution)

## Learning Path

### Prerequisites
- Basic data structures (Queue, Set, Hash Table)
- HTTP fundamentals
- Graph traversal algorithms (BFS/DFS)
- Basic Python/Java programming

### Skills Developed
1. **System Design Fundamentals**
   - Breaking down problems into components
   - Identifying functional vs non-functional requirements
   - Making design trade-offs

2. **Data Structure Application**
   - Using queues for BFS traversal
   - Hash sets for deduplication
   - Hash maps for tracking state

3. **Network Programming**
   - HTTP request/response handling
   - Timeout and retry strategies
   - Understanding politeness and rate limiting

4. **Error Handling**
   - Graceful degradation
   - Retry mechanisms
   - State persistence for recovery

### Next Steps
After mastering easy-level problems, progress to:
- **Medium Level**: Distributed message queues, large-scale web crawlers, metrics monitoring
- **Hard Level**: Distributed caching, job scheduling, service mesh

## Interview Tips

### Common Questions
1. **Deduplication**: "How do you prevent visiting the same URL multiple times?"
   - Answer: Use hash set for O(1) lookup, normalize URLs first

2. **Politeness**: "How do you avoid overloading target servers?"
   - Answer: Rate limiting (delay between requests), respect robots.txt

3. **Traversal Strategy**: "Why use BFS instead of DFS?"
   - Answer: BFS discovers important pages faster, avoids deep crawl traps

4. **Error Handling**: "What if a page fails to download?"
   - Answer: Skip and continue, implement retry with exponential backoff

### Discussion Points
- Trade-offs between speed and politeness
- File storage vs database for content
- Single-threaded vs multi-threaded crawling
- Memory efficiency at different scales

## Practice Approach

### Step 1: Understand Requirements
- Read problem statement carefully
- Clarify functional vs non-functional requirements
- Ask about scale and constraints

### Step 2: High-Level Design
- Draw component diagram
- Identify main data flows
- List key components and their responsibilities

### Step 3: Deep Dive
- Design each component's interface
- Choose appropriate data structures
- Consider error cases

### Step 4: Consider Trade-offs
- Discuss alternatives
- Explain why you chose specific approaches
- Talk about scalability limitations

### Step 5: Wrap Up
- Discuss monitoring and operations
- Talk about testing strategy
- Mention future improvements

## Additional Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "System Design Interview" by Alex Xu
- "Web Scraping with Python" by Ryan Mitchell

### Online Resources
- How Google Search Works (Google documentation)
- robots.txt specification (RFC)
- HTTP/1.1 specification (RFC 2616)

### Related Technologies
- **Libraries**: BeautifulSoup (parsing), Scrapy (framework), requests (HTTP)
- **Protocols**: HTTP, robots.txt, sitemap.xml
- **Patterns**: Producer-Consumer, BFS traversal

## Common Mistakes to Avoid

1. **Not normalizing URLs**: Leads to duplicate crawling
2. **Ignoring rate limiting**: May get IP banned
3. **Poor error handling**: Crawler crashes on first error
4. **Not tracking depth**: May crawl indefinitely
5. **Memory leaks**: Not clearing processed URLs from frontier
6. **No politeness**: Being a bad internet citizen

## Success Criteria

You've mastered this level when you can:
- Explain the complete crawling flow from seed URLs to storage
- Design appropriate data structures for each component
- Implement basic politeness and rate limiting
- Handle common error scenarios gracefully
- Discuss trade-offs between different design choices
- Estimate capacity and storage requirements
- Explain how to scale from basic to medium complexity

## Time Estimates

- **Reading & Understanding**: 30-45 minutes
- **Initial Design**: 30-45 minutes
- **Implementation (optional)**: 3-4 hours
- **Interview Discussion**: 20-30 minutes

Start with understanding the problem thoroughly before diving into code. Focus on design decisions and trade-offs during interviews.
