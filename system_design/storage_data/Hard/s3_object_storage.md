# Design S3-like Object Storage (Distributed Object Storage)

**Difficulty:** Hard

## 1. Problem Statement

Design a highly scalable, durable, and available object storage system like Amazon S3 that can store and retrieve any amount of data from anywhere on the web. The system should provide simple APIs for storing and retrieving objects (files), support massive scale (trillions of objects), ensure 99.999999999% (11 nines) durability, and provide cost-effective storage tiers.

**Key Challenges:**
- Exabyte-scale storage
- 11 nines durability (no data loss)
- High availability (99.99%)
- Strong consistency for metadata
- Eventual consistency for replication
- Cost optimization (hot vs. cold storage)

## 2. Requirements

### Functional Requirements
1. **Object Operations**:
   - PUT: Upload objects (up to 5 TB)
   - GET: Retrieve objects
   - DELETE: Remove objects
   - LIST: List objects in bucket
   - HEAD: Get object metadata
2. **Bucket Management**: Create, delete, configure buckets
3. **Versioning**: Keep multiple versions of same object
4. **Access Control**: IAM policies, ACLs, bucket policies
5. **Multipart Upload**: Split large objects into parts
6. **Object Metadata**: Custom key-value metadata
7. **Storage Classes**:
   - Standard (hot storage)
   - Infrequent Access (warm)
   - Glacier (cold/archive)

### Non-Functional Requirements
1. **Durability**: 99.999999999% (11 nines) - lose 1 object per 10 million per 10,000 years
2. **Availability**: 99.99% (Standard), 99.9% (IA)
3. **Scalability**:
   - Trillions of objects
   - Millions of requests per second
   - Exabytes of data
4. **Performance**:
   - PUT/GET latency: 100-200ms (p99)
   - Throughput: Unlimited (per-bucket)
5. **Consistency**:
   - Strong read-after-write for new objects
   - Eventual consistency for overwrites/deletes (S3 legacy)
   - Strong consistency (S3 Strong Consistency update)
6. **Cost Efficiency**: Optimize storage costs per GB

### Out of Scope
- Content delivery (use CDN separately)
- Compute on data (S3 Select)
- Complex querying (Athena)
- File system interface (EFS)

## 3. Storage Estimation

### Assumptions
- **Total Objects**: 100 trillion objects
- **Average Object Size**: 100 KB
- **Growth Rate**: 50% per year
- **Request Rate**: 50 million requests/second (peak)
- **Read:Write Ratio**: 80:20

### Calculations

**Total Storage:**
```
100 trillion objects × 100 KB = 10,000 trillion KB = 10 Exabytes (EB)
With replication (3x): 30 EB
With erasure coding (1.5x): 15 EB
```

**Annual Growth:**
```
10 EB × 50% = 5 EB/year
Over 5 years: 10 + 5 + 2.5 + 1.25 + 0.625 = ~19.4 EB
```

**Metadata Storage:**
```
Per object metadata: 1 KB (key, size, timestamps, checksum, ACL)
100 trillion × 1 KB = 100 TB metadata
```

**Request Load:**
```
Peak: 50M requests/sec
- GET: 40M/sec (80%)
- PUT: 10M/sec (20%)
- DELETE/LIST: Negligible

Daily requests: 50M × 86,400 = 4.32 trillion requests/day
```

**Bandwidth:**
```
GET: 40M requests/sec × 100 KB = 4,000,000 MB/sec = 4 TB/sec = 32 Tbps
PUT: 10M requests/sec × 100 KB = 1,000,000 MB/sec = 1 TB/sec = 8 Tbps
Total: 40 Tbps peak
```

**Storage Nodes:**
```
Assuming 100 TB per storage node:
10 EB / 100 TB = 100,000 storage nodes
With erasure coding: 150,000 nodes (accounting for parity)
```

## 4. High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ AWS SDK  │  │  REST    │  │ S3 CLI   │             │
│  │          │  │  API     │  │          │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└──────────────────────────────────────────────────────────┘
                        │
                        │ HTTPS
                        ▼
            ┌────────────────────────┐
            │   Load Balancer        │
            │  (Global Anycast DNS)  │
            └──────────┬─────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   API        │ │   API        │ │   API        │
│  Server 1    │ │  Server 2    │ │  Server N    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐         ┌─────────────────────┐
│  Metadata       │         │  Placement Service  │
│  Service        │         │  (Shard mapping)    │
│  (Raft/Paxos)   │         └─────────┬───────────┘
└────────┬────────┘                   │
         │                             │
         ▼                             ▼
┌─────────────────────────────────────────────────┐
│         Metadata Storage Cluster                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Shard 1 │  │  Shard 2 │  │  Shard N │     │
│  │ (Raft)   │  │ (Raft)   │  │ (Raft)   │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
         │
         │
         ▼
┌──────────────────────────────────────────────────┐
│          Storage Node Cluster                    │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Zone A  │  │  Zone B  │  │  Zone C  │      │
│  │┌────────┐│  │┌────────┐│  │┌────────┐│      │
│  ││Storage ││  ││Storage ││  ││Storage ││      │
│  ││Node 1-N││  ││Node 1-N││  ││Node 1-N││      │
│  │└────────┘│  │└────────┘│  │└────────┘│      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                  │
│  Each node: 100 TB storage, 10 Gbps network     │
└──────────────────────────────────────────────────┘
```

### Key Components

1. **API Servers**: Handle HTTP requests, authentication, authorization
2. **Metadata Service**: Manages object metadata, bucket info
3. **Placement Service**: Maps objects to storage nodes
4. **Metadata Storage**: Distributed database (sharded, replicated)
5. **Storage Nodes**: Physical storage (HDDs/SSDs)
6. **Replication Manager**: Ensures data durability
7. **Background Jobs**:
   - Garbage collection
   - Integrity checking
   - Tiering (move cold data to glacier)

## 5. API Design

### Object Operations

#### PUT Object
```http
PUT /bucket-name/object-key HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...
Content-Length: 1048576
Content-Type: application/octet-stream
x-amz-storage-class: STANDARD
x-amz-server-side-encryption: AES256
x-amz-meta-custom-key: custom-value

[Binary object data]

Response (200 OK):
{
  "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
  "VersionId": "version_abc123",
  "ServerSideEncryption": "AES256"
}
```

#### GET Object
```http
GET /bucket-name/object-key HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...
Range: bytes=0-1023 (optional, for partial reads)

Response (200 OK):
Content-Length: 1048576
Content-Type: application/octet-stream
ETag: "d41d8cd98f00b204e9800998ecf8427e"
Last-Modified: Tue, 12 Nov 2025 12:00:00 GMT
x-amz-version-id: version_abc123
x-amz-storage-class: STANDARD

[Binary object data]
```

#### DELETE Object
```http
DELETE /bucket-name/object-key?versionId=version_abc123 HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...

Response (204 No Content):
x-amz-delete-marker: true
x-amz-version-id: delete_marker_xyz
```

#### HEAD Object (Get Metadata)
```http
HEAD /bucket-name/object-key HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...

Response (200 OK):
Content-Length: 1048576
Content-Type: application/octet-stream
ETag: "d41d8cd98f00b204e9800998ecf8427e"
Last-Modified: Tue, 12 Nov 2025 12:00:00 GMT
x-amz-version-id: version_abc123
x-amz-storage-class: STANDARD
x-amz-meta-custom-key: custom-value
```

#### LIST Objects
```http
GET /bucket-name?prefix=photos/2025/&max-keys=1000&delimiter=/ HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...

Response (200 OK):
{
  "Name": "bucket-name",
  "Prefix": "photos/2025/",
  "Delimiter": "/",
  "MaxKeys": 1000,
  "IsTruncated": true,
  "NextContinuationToken": "token_xyz",
  "Contents": [
    {
      "Key": "photos/2025/image1.jpg",
      "Size": 524288,
      "ETag": "\"abc123\"",
      "LastModified": "2025-11-12T12:00:00Z",
      "StorageClass": "STANDARD"
    }
  ],
  "CommonPrefixes": [
    {"Prefix": "photos/2025/january/"},
    {"Prefix": "photos/2025/february/"}
  ]
}
```

### Multipart Upload

#### Initiate Multipart Upload
```http
POST /bucket-name/large-file.zip?uploads HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...
Content-Type: application/zip

Response (200 OK):
{
  "Bucket": "bucket-name",
  "Key": "large-file.zip",
  "UploadId": "upload_abc123xyz"
}
```

#### Upload Part
```http
PUT /bucket-name/large-file.zip?partNumber=1&uploadId=upload_abc123xyz HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...
Content-Length: 10485760

[Binary part data - 10 MB]

Response (200 OK):
{
  "ETag": "\"part1_etag\""
}
```

#### Complete Multipart Upload
```http
POST /bucket-name/large-file.zip?uploadId=upload_abc123xyz HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...
Content-Type: application/xml

<CompleteMultipartUpload>
  <Part>
    <PartNumber>1</PartNumber>
    <ETag>"part1_etag"</ETag>
  </Part>
  <Part>
    <PartNumber>2</PartNumber>
    <ETag>"part2_etag"</ETag>
  </Part>
</CompleteMultipartUpload>

Response (200 OK):
{
  "Location": "https://s3.amazonaws.com/bucket-name/large-file.zip",
  "Bucket": "bucket-name",
  "Key": "large-file.zip",
  "ETag": "\"combined_etag\""
}
```

### Bucket Operations

#### Create Bucket
```http
PUT /new-bucket HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 ...
Content-Type: application/xml

<CreateBucketConfiguration>
  <LocationConstraint>us-west-2</LocationConstraint>
</CreateBucketConfiguration>

Response (200 OK):
{
  "Location": "/new-bucket"
}
```

## 6. Storage Strategy

### Data Placement

**Consistent Hashing for Shard Selection:**

```python
class ConsistentHashing:
    def __init__(self, num_virtual_nodes=150):
        self.ring = {}
        self.sorted_keys = []
        self.num_virtual_nodes = num_virtual_nodes

    def add_node(self, node):
        # Add virtual nodes for better distribution
        for i in range(self.num_virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self.hash(virtual_key)
            self.ring[hash_value] = node
        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key):
        # Find node responsible for this key
        hash_value = self.hash(key)

        # Binary search for next node on ring
        idx = bisect.bisect_right(self.sorted_keys, hash_value)
        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]

    def hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

**Object Storage Path:**
```
Object Key: bucket-name/photos/2025/image.jpg
↓
Hash: MD5(bucket-name + "/" + key) = abc123def456...
↓
Consistent Hash → Shard ID: 42
↓
Shard 42 → Storage Nodes: [node_100, node_205, node_387]
↓
Physical Path: /mnt/disk1/shard42/abc/123/def/abc123def456.dat
```

### Durability via Replication

**Replication Strategy:**

1. **Synchronous Replication** (Strong Durability):
   - Write to 3 different zones simultaneously
   - Acknowledge to client only after 3 writes succeed
   - If 1 zone fails, retry to another zone

2. **Asynchronous Replication** (Optional):
   - Write to 3 zones in primary region
   - Async replicate to secondary region (cross-region replication)

**Implementation:**
```python
class ReplicationManager:
    def write_object(self, object_key, data):
        # 1. Calculate placement
        shard_id = self.placement_service.get_shard(object_key)

        # 2. Get replica nodes (3 in different zones)
        replica_nodes = self.get_replica_nodes(shard_id, count=3)

        # 3. Write to all replicas (synchronous)
        write_futures = []
        for node in replica_nodes:
            future = self.async_write_to_node(node, object_key, data)
            write_futures.append(future)

        # 4. Wait for all writes to succeed
        results = await asyncio.gather(*write_futures)

        # 5. If any write failed, retry
        failed_writes = [r for r in results if not r.success]
        if failed_writes:
            # Retry with different nodes
            backup_nodes = self.get_backup_nodes(shard_id, count=len(failed_writes))
            for node in backup_nodes:
                await self.async_write_to_node(node, object_key, data)

        # 6. Update metadata
        metadata = {
            'object_key': object_key,
            'size': len(data),
            'replicas': [n.id for n in replica_nodes],
            'timestamp': now(),
            'checksum': md5(data)
        }
        self.metadata_service.store(metadata)

        return metadata
```

### Durability via Erasure Coding

**Why Erasure Coding?**
- Replication (3x) → 200% storage overhead
- Erasure Coding (12+4) → 33% overhead
- 11 nines durability maintained

**Reed-Solomon Erasure Coding:**
```
Original data: 12 data blocks
Generate: 4 parity blocks
Total: 16 blocks

Can lose any 4 blocks and still recover data
Storage efficiency: 12 / 16 = 75% (vs. 33% for 3x replication)
```

**Implementation:**
```python
class ErasureCoding:
    def __init__(self, data_blocks=12, parity_blocks=4):
        self.data_blocks = data_blocks
        self.parity_blocks = parity_blocks
        self.total_blocks = data_blocks + parity_blocks

    def encode(self, data):
        # Split data into 12 equal-sized chunks
        block_size = len(data) // self.data_blocks
        data_chunks = [
            data[i * block_size:(i + 1) * block_size]
            for i in range(self.data_blocks)
        ]

        # Generate 4 parity chunks using Reed-Solomon
        encoder = ReedSolomonEncoder(self.data_blocks, self.parity_blocks)
        parity_chunks = encoder.encode(data_chunks)

        # Return 16 total chunks
        return data_chunks + parity_chunks

    def decode(self, available_chunks):
        # Need at least 12 out of 16 chunks to reconstruct
        if len(available_chunks) < self.data_blocks:
            raise Exception("Insufficient chunks for recovery")

        decoder = ReedSolomonDecoder(self.data_blocks, self.parity_blocks)
        reconstructed_data = decoder.decode(available_chunks)

        return reconstructed_data

    def store_with_ec(self, object_key, data):
        # 1. Encode data into 16 chunks
        chunks = self.encode(data)

        # 2. Store each chunk on different node
        nodes = self.select_nodes(count=16, ensure_diversity=True)

        for i, (chunk, node) in enumerate(zip(chunks, nodes)):
            chunk_key = f"{object_key}.chunk.{i}"
            node.write(chunk_key, chunk)

        # 3. Store metadata
        metadata = {
            'object_key': object_key,
            'encoding': 'reed-solomon-12-4',
            'chunks': [
                {'chunk_id': i, 'node_id': node.id}
                for i, node in enumerate(nodes)
            ]
        }
        self.metadata_service.store(metadata)
```

### Storage Tiers

**1. Standard (Hot Storage):**
```
Storage: SSD + HDD
Access latency: 10-50ms
Cost: $0.023/GB/month
Use case: Frequently accessed data
```

**2. Infrequent Access (IA - Warm Storage):**
```
Storage: HDD
Access latency: 50-100ms
Cost: $0.0125/GB/month + retrieval fee
Use case: Accessed < 1 time/month
```

**3. Glacier (Cold Storage / Archive):**
```
Storage: Tape / Cold HDD
Access latency: Minutes to hours
Cost: $0.004/GB/month + retrieval fee
Use case: Long-term archival, compliance
```

**Tiering Policy:**
```python
class StorageTieringService:
    def analyze_access_patterns(self, object_key):
        # Get access history for last 90 days
        access_log = self.get_access_log(object_key, days=90)

        # Calculate access frequency
        access_count = len(access_log)
        last_access = max(access_log, key=lambda x: x.timestamp)

        # Tiering rules
        if access_count == 0 and last_access > 365 days ago:
            return 'GLACIER'  # Not accessed in 1 year
        elif access_count < 10 and last_access > 30 days ago:
            return 'INFREQUENT_ACCESS'  # Rarely accessed
        else:
            return 'STANDARD'  # Frequently accessed

    def migrate_object(self, object_key, target_tier):
        # 1. Read object from current tier
        object_data = self.read_object(object_key)

        # 2. Write to target tier
        if target_tier == 'GLACIER':
            self.write_to_glacier(object_key, object_data)
        elif target_tier == 'INFREQUENT_ACCESS':
            self.write_to_ia(object_key, object_data)

        # 3. Update metadata
        self.metadata_service.update(object_key, {
            'storage_class': target_tier,
            'migrated_at': now()
        })

        # 4. Delete from old tier
        self.delete_from_old_tier(object_key)
```

## 7. Metadata Management

### Metadata Schema

**Bucket Metadata:**
```json
{
  "bucket_name": "my-bucket",
  "region": "us-west-2",
  "created_at": "2025-01-01T00:00:00Z",
  "owner": "account_123",
  "versioning": "Enabled",
  "encryption": {
    "type": "SSE-S3",
    "algorithm": "AES256"
  },
  "lifecycle_rules": [
    {
      "id": "rule1",
      "prefix": "logs/",
      "transitions": [
        {"days": 30, "storage_class": "INFREQUENT_ACCESS"},
        {"days": 365, "storage_class": "GLACIER"}
      ],
      "expiration": {"days": 730}
    }
  ],
  "access_policy": {...},
  "cors_policy": {...}
}
```

**Object Metadata:**
```json
{
  "object_key": "photos/2025/image.jpg",
  "bucket": "my-bucket",
  "version_id": "version_abc123",
  "size": 1048576,
  "content_type": "image/jpeg",
  "etag": "d41d8cd98f00b204e9800998ecf8427e",
  "created_at": "2025-11-12T12:00:00Z",
  "modified_at": "2025-11-12T12:00:00Z",
  "storage_class": "STANDARD",
  "encryption": {
    "type": "SSE-S3",
    "algorithm": "AES256",
    "key_id": "key_xyz"
  },
  "replicas": [
    {"node_id": "node_100", "zone": "us-west-2a", "checksum": "abc123"},
    {"node_id": "node_205", "zone": "us-west-2b", "checksum": "abc123"},
    {"node_id": "node_387", "zone": "us-west-2c", "checksum": "abc123"}
  ],
  "custom_metadata": {
    "x-amz-meta-user-id": "user_456",
    "x-amz-meta-project": "website"
  },
  "access_control": {
    "owner": "account_123",
    "grants": [...]
  }
}
```

### Metadata Storage Architecture

**Distributed Metadata Database:**

```
Sharding by bucket+key hash:
- Shard 0: hash(bucket+key) % 1000 == 0
- Shard 1: hash(bucket+key) % 1000 == 1
- ...
- Shard 999: hash(bucket+key) % 1000 == 999

Each shard:
- Raft consensus group (3-5 nodes)
- One leader (handles writes)
- Multiple followers (handle reads)
```

**Raft Consensus for Strong Consistency:**
```python
class MetadataRaftGroup:
    def __init__(self, shard_id, nodes):
        self.shard_id = shard_id
        self.nodes = nodes
        self.leader = None
        self.log = []

    def write_metadata(self, object_key, metadata):
        # 1. Client sends write to leader
        if not self.is_leader():
            return self.forward_to_leader(object_key, metadata)

        # 2. Leader appends to local log
        log_entry = {
            'term': self.current_term,
            'index': len(self.log),
            'command': 'PUT',
            'key': object_key,
            'value': metadata
        }
        self.log.append(log_entry)

        # 3. Leader replicates to followers
        replicated_count = 1  # Leader counts as 1
        for follower in self.followers:
            if follower.append_entry(log_entry):
                replicated_count += 1

        # 4. Wait for majority (quorum)
        if replicated_count >= (len(self.nodes) + 1) // 2:
            # Commit entry
            self.commit_index = log_entry['index']
            self.apply_to_state_machine(log_entry)
            return {'success': True}
        else:
            # Failed to reach quorum
            return {'success': False, 'error': 'Replication failed'}

    def read_metadata(self, object_key):
        # Read from local state machine (eventually consistent read)
        # OR read from leader (strongly consistent read)
        return self.state_machine.get(object_key)
```

## 8. Consistency Model

### S3 Strong Consistency (2020 Update)

**Read-After-Write Consistency:**
- PUT new object → Immediately visible in GET/LIST
- PUT overwrite → Immediately reflects new data
- DELETE → Immediately removes object

**Implementation:**
```python
class StrongConsistencyService:
    def put_object(self, bucket, key, data):
        # 1. Generate version ID
        version_id = generate_uuid()

        # 2. Write to metadata service (Raft consensus)
        metadata = {
            'bucket': bucket,
            'key': key,
            'version_id': version_id,
            'size': len(data),
            'timestamp': now(),
            'storage_nodes': []
        }

        # Wait for metadata write to be committed (quorum)
        self.metadata_service.write_sync(f"{bucket}/{key}", metadata)

        # 3. Write data to storage nodes (replicas)
        nodes = self.placement_service.get_nodes(f"{bucket}/{key}")
        for node in nodes:
            node.write(version_id, data)
            metadata['storage_nodes'].append(node.id)

        # 4. Update metadata with storage locations
        self.metadata_service.update_sync(f"{bucket}/{key}", metadata)

        return version_id

    def get_object(self, bucket, key):
        # 1. Read from metadata service (strongly consistent)
        metadata = self.metadata_service.read_from_leader(f"{bucket}/{key}")

        if not metadata:
            raise ObjectNotFound()

        # 2. Read from any replica
        for node_id in metadata['storage_nodes']:
            try:
                data = self.storage_node(node_id).read(metadata['version_id'])
                return data
            except NodeUnavailable:
                continue  # Try next replica

        raise AllReplicasUnavailable()
```

## 9. Scalability & Performance

### Horizontal Scaling

**API Servers:**
```
Stateless design:
- Auto-scale based on request rate
- Target: 5,000 requests/sec per server
- 50M requests/sec → 10,000 API servers
```

**Metadata Shards:**
```
Sharding strategy:
- 1,000 shards initially
- Each shard: 5-node Raft group
- Total: 5,000 metadata nodes

Shard split when:
- > 10 TB metadata per shard
- > 100 billion objects per shard
```

**Storage Nodes:**
```
Add nodes as needed:
- New node joins cluster
- Consistent hashing automatically rebalances
- Background data migration

Example:
- Current: 100,000 nodes
- Add: 10,000 nodes
- Rebalance: ~9% of data migrates
```

### Performance Optimizations

**1. Read Optimization:**
```python
# Read from nearest replica
def get_object_optimized(self, bucket, key):
    metadata = self.metadata_service.read_from_cache(f"{bucket}/{key}")

    if not metadata:
        metadata = self.metadata_service.read_from_leader(f"{bucket}/{key}")
        self.metadata_service.cache(f"{bucket}/{key}", metadata, ttl=60)

    # Select nearest storage node
    user_location = self.get_user_location()
    nearest_node = self.select_nearest_node(
        metadata['storage_nodes'],
        user_location
    )

    data = nearest_node.read(metadata['version_id'])
    return data
```

**2. Write Optimization:**
```python
# Parallel writes to replicas
async def put_object_parallel(self, bucket, key, data):
    nodes = self.placement_service.get_nodes(f"{bucket}/{key}")

    # Write to all nodes in parallel
    write_tasks = [
        node.async_write(key, data)
        for node in nodes
    ]

    results = await asyncio.gather(*write_tasks)

    # Check if majority succeeded
    success_count = sum(1 for r in results if r.success)
    if success_count >= 2:  # Quorum for 3 replicas
        return {'success': True}
    else:
        return {'success': False}
```

**3. Caching:**
```
L1: API server memory cache
- Hot object metadata: 1 min TTL
- Bucket policies: 5 min TTL

L2: Distributed cache (Redis)
- Frequently accessed metadata: 10 min TTL
- LIST results: 1 min TTL

L3: CDN (for public objects)
- Cached at edge: 24 hours
```

**4. Multipart Upload Optimization:**
```python
def multipart_upload(self, bucket, key, parts):
    # Parts uploaded in parallel by client
    # Each part: 5 MB - 5 GB

    # 1. Client initiates
    upload_id = self.initiate_multipart_upload(bucket, key)

    # 2. Client uploads parts in parallel (up to 10,000 parts)
    # Each part stored independently

    # 3. Complete: Assemble parts
    def complete_multipart(upload_id, part_etags):
        # Verify all parts exist
        parts = self.list_parts(upload_id)

        # Create manifest (pointer to parts)
        manifest = {
            'bucket': bucket,
            'key': key,
            'parts': [
                {'part_number': i, 'etag': etag, 'size': size}
                for i, etag, size in part_etags
            ],
            'total_size': sum(p['size'] for p in part_etags)
        }

        # Store manifest as object metadata
        # Actual data remains as separate part objects
        self.metadata_service.write(f"{bucket}/{key}", manifest)

        return manifest
```

## 10. Advanced Features

### Versioning

**Enable Versioning:**
```python
def enable_versioning(self, bucket):
    self.metadata_service.update_bucket(bucket, {'versioning': 'Enabled'})

def put_object_with_versioning(self, bucket, key, data):
    # Check if versioning enabled
    bucket_metadata = self.metadata_service.get_bucket(bucket)

    if bucket_metadata['versioning'] == 'Enabled':
        # Generate new version ID
        version_id = generate_uuid()
    else:
        # Use null version
        version_id = 'null'

    # Store with version ID
    self.write_object(bucket, key, version_id, data)

    # Update latest version pointer
    self.metadata_service.update(f"{bucket}/{key}", {
        'latest_version': version_id
    })

    return version_id

def list_object_versions(self, bucket, key):
    # Query all versions from metadata
    versions = self.metadata_service.query_versions(f"{bucket}/{key}")
    return sorted(versions, key=lambda v: v['timestamp'], reverse=True)
```

### Cross-Region Replication

**Async Replication:**
```python
class CrossRegionReplication:
    def replicate_object(self, source_bucket, source_key, target_region):
        # 1. Read object from source
        obj = self.s3_client.get_object(source_bucket, source_key)

        # 2. Write to target region
        target_bucket = f"{source_bucket}-{target_region}"
        self.s3_client_target.put_object(
            target_bucket,
            source_key,
            obj['Body']
        )

        # 3. Log replication
        self.log_replication(source_bucket, source_key, target_region)

    def setup_replication_rule(self, source_bucket, target_bucket, target_region):
        rule = {
            'id': 'replicate-to-eu',
            'status': 'Enabled',
            'priority': 1,
            'filter': {'prefix': ''},  # Replicate all objects
            'destination': {
                'bucket': target_bucket,
                'region': target_region,
                'storage_class': 'STANDARD'
            }
        }

        # Store in bucket metadata
        self.metadata_service.add_replication_rule(source_bucket, rule)

        # Background job picks up changes and replicates
        self.replication_worker.subscribe(source_bucket)
```

### Lifecycle Management

**Automatic Tiering and Expiration:**
```python
class LifecycleManager:
    def apply_lifecycle_rules(self, bucket):
        rules = self.metadata_service.get_lifecycle_rules(bucket)

        for rule in rules:
            objects = self.list_objects(bucket, prefix=rule['prefix'])

            for obj in objects:
                age_days = (now() - obj['last_modified']).days

                # Transition to IA after 30 days
                if age_days >= 30 and obj['storage_class'] == 'STANDARD':
                    self.transition_object(obj, 'INFREQUENT_ACCESS')

                # Transition to Glacier after 365 days
                elif age_days >= 365 and obj['storage_class'] == 'INFREQUENT_ACCESS':
                    self.transition_object(obj, 'GLACIER')

                # Expire (delete) after 730 days
                elif age_days >= 730:
                    self.delete_object(obj)
```

### Server-Side Encryption

**SSE-S3 (S3-managed keys):**
```python
def put_object_encrypted(self, bucket, key, data):
    # 1. Generate data encryption key (DEK)
    dek = generate_random_key(256)  # AES-256

    # 2. Encrypt data with DEK
    encrypted_data = aes_encrypt(data, dek)

    # 3. Encrypt DEK with master key
    master_key = self.get_master_key()
    encrypted_dek = rsa_encrypt(dek, master_key)

    # 4. Store encrypted data
    self.write_to_storage(bucket, key, encrypted_data)

    # 5. Store encrypted DEK in metadata
    self.metadata_service.write(f"{bucket}/{key}", {
        'encryption': 'SSE-S3',
        'encrypted_dek': encrypted_dek
    })

def get_object_encrypted(self, bucket, key):
    # 1. Get encrypted DEK from metadata
    metadata = self.metadata_service.read(f"{bucket}/{key}")
    encrypted_dek = metadata['encrypted_dek']

    # 2. Decrypt DEK with master key
    master_key = self.get_master_key()
    dek = rsa_decrypt(encrypted_dek, master_key)

    # 3. Read encrypted data
    encrypted_data = self.read_from_storage(bucket, key)

    # 4. Decrypt data with DEK
    data = aes_decrypt(encrypted_data, dek)

    return data
```

## 11. Trade-offs

### Replication vs. Erasure Coding

**Replication (3x):**
- ✅ Simple implementation
- ✅ Fast reads (any replica)
- ✅ Fast writes (parallel)
- ❌ High storage cost (3x)

**Erasure Coding (12+4):**
- ✅ Lower storage cost (1.33x)
- ✅ Same durability
- ❌ Slower reads (must fetch 12+ blocks)
- ❌ Slower writes (must compute parity)

**Decision:** Replication for hot data, erasure coding for cold data

### Strong vs. Eventual Consistency

**Strong Consistency:**
- ✅ No stale reads
- ✅ Simpler application logic
- ❌ Higher latency (wait for quorum)
- ❌ Lower availability during partitions

**Eventual Consistency:**
- ✅ Lower latency
- ✅ Higher availability
- ❌ Stale reads possible
- ❌ Complex conflict resolution

**Decision:** Strong consistency (S3's 2020 update)

### SSD vs. HDD

**SSD:**
- ✅ Low latency (< 10ms)
- ✅ High IOPS
- ❌ Expensive (10x HDD)

**HDD:**
- ✅ Cost-effective
- ✅ High capacity
- ❌ Slower (50-100ms latency)

**Decision:** SSD for metadata, HDD for object data (Standard tier)

## 12. Follow-up Questions

1. **How do you handle concurrent writes to the same object?**
   - Last-write-wins based on timestamp
   - Version IDs ensure no data loss
   - Both versions accessible via version IDs

2. **How would you implement object locking (WORM - Write Once Read Many)?**
   - Add `lock_until` timestamp to metadata
   - Reject DELETE/overwrite until timestamp expires
   - Use for compliance (SEC, FINRA)

3. **How do you detect and repair corrupt data?**
   - Background scrubber checks checksums
   - Compare checksums across replicas
   - If mismatch, use majority voting
   - Re-replicate corrupted block

4. **How would you implement presigned URLs?**
   - Generate temporary URL with HMAC signature
   - Include expiration timestamp
   - API server validates signature and expiry
   - No authentication required if signature valid

5. **How do you handle hot partitions (celebrity problem)?**
   - Detect hot keys via metrics
   - Add more replicas for hot objects
   - Use CDN in front of S3
   - Rate limit per-object requests

6. **How would you implement S3 Select (query data without downloading)?**
   - Store data in columnar format (Parquet)
   - Push down filtering to storage nodes
   - Return only matching rows
   - Reduce data transfer

7. **How do you handle network partitions?**
   - Continue accepting writes (AP in CAP)
   - Use version vectors for conflict detection
   - Reconcile after partition heals
   - Or: Refuse writes (CP in CAP) - metadata service approach

8. **How would you implement access logs?**
   - Async log writes to separate bucket
   - Don't block object operations
   - Aggregate logs periodically
   - Store in compressed format

9. **How do you optimize costs?**
   - Intelligent tiering (auto-move to IA/Glacier)
   - Compression for text/JSON
   - Lifecycle policies (auto-delete old data)
   - Reserved capacity pricing

10. **How would you implement bucket notifications (events)?**
    - Publish events to message queue (Kafka/SQS)
    - Event types: ObjectCreated, ObjectRemoved
    - Consumers: Lambda functions, webhooks
    - At-least-once delivery guarantee

## Complexity Analysis

- **Time Complexity:**
  - PUT: O(1) for metadata, O(n) for data where n = object size
  - GET: O(1) metadata lookup, O(n) data transfer
  - LIST: O(k) where k = number of objects to list
  - DELETE: O(1)

- **Space Complexity:**
  - Total: O(n) where n = total data stored
  - With replication: O(3n)
  - With erasure coding: O(1.33n)
  - Metadata: O(m) where m = number of objects

## References

- [Amazon S3 Architecture](https://www.allthingsdistributed.com/2023/07/building-and-operating-a-pretty-big-storage-system.html)
- [Dynamo Paper (Amazon)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Raft Consensus Algorithm](https://raft.github.io/)
- [Reed-Solomon Erasure Coding](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction)
- [Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing)
- [S3 Strong Consistency](https://aws.amazon.com/blogs/aws/amazon-s3-update-strong-read-after-write-consistency/)
