# Design Yelp (Full-Featured Business Discovery Platform)

## 1. Problem Overview

Design a comprehensive business discovery platform like Yelp that allows users to search for businesses, read/write reviews, upload photos, make reservations, and interact with the community. The system must handle millions of businesses, reviews, and searches while providing fast, relevant results.

**Key Challenges**:
- Advanced search with multiple filters (category, price, rating, distance, hours)
- Review and rating system with fraud detection
- Photo storage and serving at scale
- Full-text search across reviews and business info
- Personalized recommendations
- Real-time availability and reservations

## 2. Requirements

### Functional Requirements
- **Business Search**: Search by location, category, name, filters
- **Business Pages**: Display info, photos, reviews, hours, menu
- **Reviews**: Write, edit, delete reviews with ratings (1-5 stars)
- **Photos**: Upload and view business photos
- **Check-ins**: Users can check in at businesses
- **Collections**: Save businesses to lists
- **Reservations**: Book tables at restaurants (integration)
- **User Profiles**: Profile, review history, followers
- **Social Features**: Follow users, like reviews, comment

### Non-Functional Requirements
- **Availability**: 99.9% uptime
- **Latency**: < 500ms for search, < 100ms for reads
- **Scalability**: 200M users, 100M businesses, 500M reviews
- **Consistency**: Eventually consistent for reviews/ratings
- **Search Quality**: Relevant results with ranking
- **Storage**: Unlimited photos and reviews

### Out of Scope
- Yelp for Business (business owner tools)
- Advertising platform
- Delivery integration
- Events and offers

## 3. Scale Estimation

### Data Estimates
- **Businesses**: 100 million
- **Users**: 200 million
- **Reviews**: 500 million
- **Photos**: 2 billion
- **Daily searches**: 50 million
- **Daily reviews**: 500K
- **Daily photos**: 2 million

### Storage Estimates
- **Business data**: 100M × 2 KB = 200 GB
- **Reviews**: 500M × 500 bytes = 250 GB
- **Photos**: 2B × 500 KB (avg) = 1 PB
- **Total**: ~1 PB

### Traffic Estimates
- **Search QPS**: 50M / 86400 ≈ 580 QPS (avg), 1740 peak
- **Read QPS**: 2000 QPS (business pages, reviews)
- **Write QPS**: 50 QPS (reviews, photos)

## 4. High-Level Design

```
Client → CDN → Load Balancer → API Gateway
                                     │
    ┌────────────────────────────────┼─────────────────────┐
    │                                │                     │
    ▼                                ▼                     ▼
┌─────────┐                    ┌──────────┐         ┌──────────┐
│ Search  │                    │ Business │         │  Review  │
│ Service │                    │ Service  │         │ Service  │
│(Elastic)│                    └────┬─────┘         └─────┬────┘
└────┬────┘                         │                     │
     │                               │                     │
     └───────────────────────────────┴─────────────────────┘
                                     │
                ┌────────────────────┼──────────────────┐
                ▼                    ▼                  ▼
         ┌───────────┐        ┌───────────┐     ┌──────────┐
         │PostgreSQL │        │   Redis   │     │    S3    │
         │(Metadata) │        │  (Cache)  │     │ (Photos) │
         └───────────┘        └───────────┘     └──────────┘
```

## 5. Core Components

### Search Service
- **Elasticsearch** for full-text search
- **Filters**: Category, location, price, rating, hours
- **Ranking**: Distance, rating, popularity, reviews
- **Autocomplete**: Suggest as you type
- **Spell correction**: Handle typos

### Business Service
- **CRUD operations** for businesses
- **Geospatial queries** for nearby search
- **Aggregations**: Calculate average rating, review count
- **Hours and availability**
- **Photos and menu**

### Review Service
- **Create/update/delete** reviews
- **Rating calculations**: Weighted average
- **Fraud detection**: Spam, fake reviews
- **Moderation**: Inappropriate content
- **Voting**: Useful, funny, cool

### Photo Service
- **Upload to S3**
- **Image processing**: Resize, compress, thumbnails
- **CDN delivery**
- **EXIF data extraction**

### Recommendation Service
- **Personalized suggestions** based on history
- **Collaborative filtering**
- **Content-based filtering**
- **Trending businesses**

## 6. Data Models

### Business Table
```sql
CREATE TABLE businesses (
    business_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    categories TEXT[], -- ['restaurant', 'italian']
    price_range INT, -- 1-4 ($-$$$$)
    rating DECIMAL(2, 1), -- 1.0-5.0
    review_count INT DEFAULT 0,
    photo_count INT DEFAULT 0,
    hours JSONB, -- Business hours
    attributes JSONB, -- Parking, WiFi, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_location ON businesses USING GIST(location);
CREATE INDEX idx_categories ON businesses USING GIN(categories);
CREATE INDEX idx_city ON businesses(city, rating DESC);
```

### Review Table
```sql
CREATE TABLE reviews (
    review_id VARCHAR(64) PRIMARY KEY,
    business_id VARCHAR(64) REFERENCES businesses(business_id),
    user_id VARCHAR(64) REFERENCES users(user_id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    text TEXT,
    useful_count INT DEFAULT 0,
    funny_count INT DEFAULT 0,
    cool_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_business_reviews ON reviews(business_id, created_at DESC);
CREATE INDEX idx_user_reviews ON reviews(user_id, created_at DESC);
```

### Photo Table
```sql
CREATE TABLE photos (
    photo_id VARCHAR(64) PRIMARY KEY,
    business_id VARCHAR(64) REFERENCES businesses(business_id),
    user_id VARCHAR(64) REFERENCES users(user_id),
    s3_url TEXT NOT NULL,
    thumbnail_url TEXT,
    caption TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 7. Search Implementation

### Elasticsearch Index
```json
{
  "mappings": {
    "properties": {
      "business_id": {"type": "keyword"},
      "name": {
        "type": "text",
        "fields": {"keyword": {"type": "keyword"}}
      },
      "location": {"type": "geo_point"},
      "categories": {"type": "keyword"},
      "rating": {"type": "float"},
      "review_count": {"type": "integer"},
      "price_range": {"type": "integer"},
      "city": {"type": "keyword"},
      "hours": {"type": "object"},
      "review_text": {"type": "text"}
    }
  }
}
```

### Search Query
```python
def search_businesses(query, location, filters):
    must_clauses = []

    # Text search on name and categories
    if query:
        must_clauses.append({
            "multi_match": {
                "query": query,
                "fields": ["name^3", "categories^2", "review_text"],
                "type": "best_fields"
            }
        })

    # Geo distance filter
    if location:
        must_clauses.append({
            "geo_distance": {
                "distance": filters.get("radius", "10km"),
                "location": {
                    "lat": location["latitude"],
                    "lon": location["longitude"]
                }
            }
        })

    # Category filter
    if filters.get("category"):
        must_clauses.append({
            "term": {"categories": filters["category"]}
        })

    # Rating filter
    if filters.get("min_rating"):
        must_clauses.append({
            "range": {"rating": {"gte": filters["min_rating"]}}
        })

    # Price filter
    if filters.get("price"):
        must_clauses.append({
            "terms": {"price_range": filters["price"]}
        })

    # Build query
    body = {
        "query": {"bool": {"must": must_clauses}},
        "sort": [
            {"_geo_distance": {
                "location": location,
                "order": "asc",
                "unit": "km"
            }},
            {"rating": {"order": "desc"}},
            {"review_count": {"order": "desc"}}
        ],
        "size": 20
    }

    return es.search(index="businesses", body=body)
```

## 8. Rating System

### Weighted Rating Calculation
```python
def calculate_weighted_rating(reviews):
    # Bayesian average to handle few reviews
    global_avg_rating = 3.5  # Platform average
    min_reviews = 10  # Minimum reviews for confidence

    total_reviews = len(reviews)
    sum_ratings = sum(r.rating for r in reviews)

    weighted_rating = (
        (min_reviews * global_avg_rating + sum_ratings) /
        (min_reviews + total_reviews)
    )

    return round(weighted_rating, 1)

def update_business_rating(business_id, new_review):
    # Get current stats
    business = get_business(business_id)

    # Incremental update
    new_review_count = business.review_count + 1
    new_rating_sum = (business.rating * business.review_count) + new_review.rating
    new_avg = new_rating_sum / new_review_count

    # Update database
    db.execute("""
        UPDATE businesses
        SET rating = %s,
            review_count = review_count + 1
        WHERE business_id = %s
    """, (round(new_avg, 1), business_id))
```

## 9. Geospatial Indexing

Uses same concepts as simple Yelp but with additional features:
- **Multiple location searches**: "Restaurants near me and near work"
- **Polygon search**: "Businesses in this neighborhood"
- **Route-based search**: "Restaurants along my commute"

## 10. Scalability & Performance

### Caching Strategy
- **Business pages**: 1 hour TTL
- **Search results**: 5 minutes TTL (location-rounded)
- **Photos**: CDN with 1 year TTL
- **Aggregations**: Pre-compute popular stats

### Database Optimization
- **Read replicas**: Route reads to replicas
- **Partitioning**: Partition reviews by business_id
- **Archiving**: Move old reviews to cold storage
- **Denormalization**: Store rating/count on business

### Search Optimization
- **Index sharding**: Shard by geography
- **Query caching**: Cache popular queries
- **Autocomplete**: Separate index for suggestions
- **Async indexing**: Update search index asynchronously

## 11. Trade-offs

### Elasticsearch vs PostgreSQL Full-text
**Chosen: Elasticsearch**
- Pros: Better relevance, faceted search, scalable
- Cons: Additional infrastructure, eventual consistency
- Alternative: PostgreSQL (simpler, consistent, limited features)

### Rating Update Strategy
**Chosen: Incremental update**
- Pros: Fast, no need to recompute all
- Cons: Potential precision loss over time
- Alternative: Recalculate from all reviews (accurate, slow)

### Photo Storage
**Chosen: S3 + CDN**
- Pros: Scalable, durable, fast delivery
- Cons: Cost, latency for new uploads
- Alternative: Self-hosted storage (more control, harder to scale)

## 12. Follow-up Questions

1. **How would you implement personalized search?**
   - User history and preferences
   - Collaborative filtering
   - Boost businesses similar to favorites
   - A/B test ranking algorithms

2. **How would you detect fake reviews?**
   - ML-based spam detection
   - User behavior analysis
   - Review velocity monitoring
   - Social graph analysis

3. **How would you handle review moderation at scale?**
   - Automated content filtering
   - User reporting
   - Manual review queue
   - ML classification

4. **How would you implement "Search by Photo"?**
   - Image recognition ML model
   - Extract features from photos
   - Index visual features
   - Similarity search

5. **How would you scale to 10B reviews?**
   - Database sharding by business
   - Cassandra for reviews
   - Archive old reviews
   - Separate analytics pipeline
