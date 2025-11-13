# Design File Upload Service

**Difficulty:** Easy

## 1. Problem Statement

Design a basic file upload and download service that allows users to upload files to the cloud, store them securely, and download them on demand. The service should handle multiple file types, provide basic metadata tracking, and ensure reliable storage.

**Example Use Cases:**
- Users uploading profile pictures
- Document sharing in small teams
- Basic file backup service
- Form attachments in web applications

## 2. Requirements

### Functional Requirements
1. **Upload Files**: Users can upload files (images, documents, videos)
2. **Download Files**: Users can retrieve uploaded files
3. **Delete Files**: Users can remove their files
4. **List Files**: Users can view their uploaded files
5. **File Metadata**: Track file name, size, upload time, type
6. **File Size Limit**: Support files up to 100 MB per upload

### Non-Functional Requirements
1. **Availability**: 99.9% uptime
2. **Durability**: Files should not be lost (99.99% durability)
3. **Scalability**: Support 10,000 active users initially
4. **Performance**: Upload/download within 5 seconds for 10MB files
5. **Security**: Secure file storage and access control

### Out of Scope
- File versioning
- Real-time collaboration
- Advanced sharing and permissions
- File synchronization across devices

## 3. Storage Estimation

### Assumptions
- **Total Users**: 10,000 active users
- **Average Files per User**: 20 files
- **Average File Size**: 5 MB
- **Upload Frequency**: Each user uploads 2 files per week
- **Retention**: Files stored for 1 year minimum

### Calculations

**Total Files:**
```
10,000 users × 20 files = 200,000 files
```

**Total Storage:**
```
200,000 files × 5 MB = 1,000,000 MB = 1 TB (approx)
With replication (3x): 3 TB
```

**Daily Upload Volume:**
```
10,000 users × 2 files/week ÷ 7 days = ~2,857 files/day
2,857 files × 5 MB = 14,285 MB = ~14 GB/day
```

**Bandwidth Estimation:**
```
Upload bandwidth: 14 GB/day ÷ 86,400 sec = ~162 KB/s average
Download (assume 2x upload): 324 KB/s average
Peak traffic (10x average): 1.6 MB/s upload, 3.2 MB/s download
```

**Metadata Storage:**
```
Per file metadata: ~500 bytes (ID, name, size, type, timestamps, user_id)
Total metadata: 200,000 × 500 bytes = 100 MB
```

## 4. High-Level Architecture

```
┌─────────────┐
│   Client    │
│ (Web/Mobile)│
└──────┬──────┘
       │
       │ HTTPS
       ▼
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│   API Servers        │
│  (Upload/Download)   │
└────────┬─────────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌─────────┐  ┌──────────────┐
│Metadata │  │ Blob Storage │
│Database │  │   (S3/GCS)   │
│(MySQL)  │  └──────────────┘
└─────────┘
```

### Components

1. **Client**: Web/mobile application for file upload/download
2. **Load Balancer**: Distributes traffic across API servers
3. **API Servers**: Handle upload/download requests and business logic
4. **Metadata Database**: Stores file metadata (MySQL/PostgreSQL)
5. **Blob Storage**: Object storage for actual files (AWS S3, Google Cloud Storage)

## 5. API Design

### Upload File
```http
POST /api/v1/files/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}

Request Body:
- file: binary data
- metadata: {
    "filename": "document.pdf",
    "description": "Optional description"
  }

Response (201 Created):
{
  "file_id": "abc123xyz",
  "filename": "document.pdf",
  "size": 5242880,
  "upload_time": "2025-11-12T10:30:00Z",
  "file_type": "application/pdf",
  "download_url": "https://api.example.com/api/v1/files/abc123xyz"
}
```

### Download File
```http
GET /api/v1/files/{file_id}
Authorization: Bearer {token}

Response (200 OK):
- Binary file data
- Headers:
  Content-Type: application/pdf
  Content-Disposition: attachment; filename="document.pdf"
  Content-Length: 5242880
```

### List Files
```http
GET /api/v1/files?page=1&limit=20
Authorization: Bearer {token}

Response (200 OK):
{
  "files": [
    {
      "file_id": "abc123xyz",
      "filename": "document.pdf",
      "size": 5242880,
      "upload_time": "2025-11-12T10:30:00Z",
      "file_type": "application/pdf"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 20
}
```

### Delete File
```http
DELETE /api/v1/files/{file_id}
Authorization: Bearer {token}

Response (204 No Content)
```

### Get File Metadata
```http
GET /api/v1/files/{file_id}/metadata
Authorization: Bearer {token}

Response (200 OK):
{
  "file_id": "abc123xyz",
  "filename": "document.pdf",
  "size": 5242880,
  "upload_time": "2025-11-12T10:30:00Z",
  "file_type": "application/pdf",
  "checksum": "a1b2c3d4e5f6...",
  "user_id": "user789"
}
```

## 6. Storage Strategy

### Blob Storage (Object Storage)

**Storage Choice:** AWS S3 / Google Cloud Storage / Azure Blob Storage

**Advantages:**
- High durability (99.999999999%)
- Automatic scaling
- Cost-effective for large volumes
- Built-in redundancy
- Easy integration

**File Organization:**
```
bucket-name/
├── users/
│   ├── user_123/
│   │   ├── abc123xyz.pdf
│   │   ├── def456uvw.jpg
│   │   └── ...
│   └── user_456/
│       └── ...
```

**File Naming Strategy:**
- Generate unique file ID (UUID)
- Store original filename in metadata database
- Use file_id as object key to prevent collisions
- Include user_id in path for organization

### Metadata Storage

**Database:** PostgreSQL / MySQL

**Schema:**
```sql
CREATE TABLE files (
    file_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    status ENUM('active', 'deleted') DEFAULT 'active',

    INDEX idx_user_id (user_id),
    INDEX idx_upload_time (upload_time),
    INDEX idx_status (status)
);

CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    storage_used BIGINT DEFAULT 0,
    storage_limit BIGINT DEFAULT 1073741824, -- 1 GB default
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Data Durability & Redundancy

1. **Object Storage Redundancy**: S3 automatically replicates across multiple availability zones
2. **Metadata Database**: Master-slave replication with automatic failover
3. **Backups**: Daily automated backups with 30-day retention
4. **Checksums**: MD5/SHA-256 for integrity verification

## 7. Upload/Download Flow

### Upload Flow

```
1. Client Request
   ├─→ Client initiates upload with file
   └─→ Request hits Load Balancer

2. API Server Processing
   ├─→ Validate file size, type, user quota
   ├─→ Generate unique file_id (UUID)
   ├─→ Calculate checksum (MD5)
   └─→ Check user storage limit

3. Storage
   ├─→ Upload file to blob storage (S3)
   │   └─→ Path: users/{user_id}/{file_id}.ext
   └─→ Store metadata in database
       └─→ file_id, filename, size, type, path, checksum

4. Response
   └─→ Return file_id and download URL to client
```

### Download Flow

```
1. Client Request
   ├─→ Client requests file by file_id
   └─→ Request hits Load Balancer

2. API Server Processing
   ├─→ Validate user authorization
   ├─→ Fetch metadata from database
   └─→ Verify file ownership

3. File Retrieval
   ├─→ Generate signed URL from blob storage
   │   OR
   └─→ Stream file directly through API server

4. Response
   └─→ Return file with appropriate headers
```

### Optimization: Presigned URLs

For better performance, use presigned URLs:

```python
# Instead of streaming through API server
# Generate temporary signed URL (valid for 5 minutes)
signed_url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'bucket-name', 'Key': file_path},
    ExpiresIn=300
)
# Return signed URL to client
# Client downloads directly from S3
```

## 8. Security Considerations

### Authentication & Authorization
- **JWT Tokens**: For API authentication
- **User Ownership**: Verify user owns file before download/delete
- **HTTPS**: All communication encrypted

### File Security
- **Private Buckets**: No public access to S3 bucket
- **Signed URLs**: Temporary access URLs with expiration
- **Virus Scanning**: Optional integration with antivirus (ClamAV)
- **Content Type Validation**: Verify file type matches content

### Storage Security
- **Encryption at Rest**: S3 server-side encryption (SSE-S3)
- **Encryption in Transit**: TLS 1.2+
- **Access Control**: IAM roles with least privilege

## 9. Scalability

### Horizontal Scaling
- **API Servers**: Add more instances behind load balancer
- **Database**: Read replicas for query distribution
- **Object Storage**: Automatically scales

### Performance Optimization
- **Chunked Upload**: For large files, upload in chunks
- **Multipart Upload**: S3 multipart upload API for files > 5MB
- **Connection Pooling**: Reuse database connections
- **Caching**: Redis cache for frequently accessed metadata

### Monitoring
- **Metrics**: Upload/download latency, error rates, storage usage
- **Alerts**: Disk space, API errors, slow queries
- **Logging**: Centralized logging (ELK stack)

## 10. Trade-offs

### Direct Upload vs. Server Upload

**Through Server:**
- ✅ Better control and validation
- ✅ Easy to implement virus scanning
- ❌ Server bandwidth bottleneck
- ❌ Higher latency

**Direct to S3 (Presigned POST):**
- ✅ Faster uploads
- ✅ No server bandwidth usage
- ❌ Limited validation before upload
- ❌ More complex implementation

**Decision:** For simplicity, start with server upload. Migrate to presigned URLs as traffic grows.

### File Storage: Database vs. Blob Storage

**Database (BLOB column):**
- ✅ Simpler architecture
- ✅ ACID transactions
- ❌ Expensive at scale
- ❌ Limited size (1-16 MB typical)
- ❌ Database bloat

**Blob Storage (S3):**
- ✅ Cost-effective
- ✅ Unlimited scalability
- ✅ Built-in CDN integration
- ❌ Eventual consistency (older S3 regions)
- ❌ Additional service dependency

**Decision:** Use blob storage for files, database for metadata.

## 11. Advanced Features (Future)

### File Deduplication
- Calculate hash (SHA-256) before upload
- Check if file already exists
- Store reference instead of duplicate
- Save storage costs

### Thumbnail Generation
- For images, generate thumbnails asynchronously
- Store multiple sizes (small, medium, large)
- Improve UI performance

### Resumable Uploads
- Support upload resumption for large files
- Track uploaded chunks
- Client can retry failed chunks

## 12. Follow-up Questions

1. **How would you handle file uploads larger than 100 MB?**
   - Implement chunked/multipart upload
   - Upload file in 5 MB chunks
   - Assemble chunks on server or use S3 multipart API
   - Add progress tracking

2. **How would you implement file sharing with other users?**
   - Add `file_permissions` table with columns: file_id, user_id, permission_type (read/write)
   - Add `shared_links` table for public sharing with expiration
   - Modify authorization logic to check permissions

3. **What happens if upload fails midway?**
   - Implement retry logic with exponential backoff
   - For chunked uploads, track uploaded chunks
   - Clean up orphaned files periodically (uploaded to S3 but no metadata)
   - Return error to client with retry instructions

4. **How would you prevent duplicate file uploads?**
   - Calculate file hash (SHA-256) on client side
   - Check if hash exists in database
   - If exists, create metadata entry pointing to existing file
   - Reference counting for deletion

5. **How do you handle virus-infected files?**
   - Integrate virus scanning (ClamAV) after upload
   - Scan asynchronously in background
   - Mark file status as "scanning", "clean", or "infected"
   - Quarantine infected files, notify user

6. **How would you optimize for frequent downloads of the same file?**
   - Add CloudFront/CDN in front of S3
   - Cache frequently accessed files at edge locations
   - Reduce latency for global users
   - Add cache headers to responses

7. **How would you implement storage quotas per user?**
   - Track `storage_used` in users table
   - Check before upload: `storage_used + file_size <= storage_limit`
   - Update `storage_used` after successful upload
   - Use database transaction to ensure consistency

8. **What metrics would you track?**
   - Upload success/failure rate
   - Average upload/download time
   - Storage usage per user
   - Top file types
   - API response times (p50, p95, p99)
   - Error rates by endpoint

9. **How would you handle file deletion?**
   - Soft delete: Mark status as "deleted", keep file for 30 days
   - Background job: Permanently delete after retention period
   - Update user's `storage_used` immediately
   - Allows recovery from accidental deletion

10. **How would you scale the database?**
    - Vertical scaling: Increase DB instance size
    - Read replicas: Route read queries to replicas
    - Sharding: Partition by user_id for horizontal scaling
    - Caching: Redis for hot metadata queries

## Complexity Analysis

- **Time Complexity:**
  - Upload: O(n) where n = file size
  - Download: O(n) where n = file size
  - List files: O(m) where m = number of files to list
  - Delete: O(1) metadata update

- **Space Complexity:**
  - O(f) where f = total number of files stored
  - Metadata: O(f × metadata_size)
  - Actual files: O(Σ file_sizes)

## References & Further Reading

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Multipart Upload Overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
- [Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)
- [File Upload Best Practices](https://web.dev/file-upload-best-practices/)
