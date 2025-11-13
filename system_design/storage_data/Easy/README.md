# Easy Level - Storage & Data System Design

This folder contains system design problems focused on basic storage and data management concepts. These problems are suitable for beginners learning system design fundamentals.

## Problems

### 1. File Upload Service
**File:** `file_upload_service.md`

Design a basic file upload and download service that allows users to store files in the cloud.

**Key Concepts:**
- Basic file operations (upload, download, delete)
- Blob storage (S3/GCS)
- Metadata management
- Simple API design
- Storage estimation
- Durability and replication

**Learning Outcomes:**
- Understanding cloud storage basics
- API design for file operations
- Storage vs. metadata separation
- Basic security considerations
- Scalability fundamentals

## How to Use These Problems

1. **Read the Problem Statement**: Understand requirements and constraints
2. **Estimate Scale**: Calculate storage, bandwidth, and QPS requirements
3. **Design Architecture**: Draw high-level and detailed component diagrams
4. **Design APIs**: Define clear RESTful or RPC interfaces
5. **Consider Trade-offs**: Evaluate different approaches
6. **Answer Follow-ups**: Practice responding to interviewer questions

## Key Patterns at This Level

- **Storage Abstraction**: Using cloud blob storage (S3/GCS) vs. local file systems
- **Metadata Management**: Separating file content from metadata
- **Basic Durability**: Understanding replication for data protection
- **Simple Authentication**: Token-based auth, basic access control
- **Direct Upload vs. Server Upload**: When to stream through server vs. direct-to-storage

## Prerequisites

Before attempting these problems, you should understand:
- Basic HTTP/REST concepts
- Database fundamentals (SQL)
- Cloud storage basics (S3 buckets, blob storage)
- Basic networking (HTTP, HTTPS)

## Next Steps

Once comfortable with Easy problems, move to Medium level which covers:
- Distributed file synchronization (Dropbox)
- Advanced permissions and sharing (Google Drive)
- Video streaming platforms (YouTube, Netflix)
- Audio streaming with recommendations (Spotify)

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [REST API Design Best Practices](https://restfulapi.net/)
- [Cloud Storage Concepts](https://cloud.google.com/storage/docs/key-terms)
