# Distributed Job Scheduler

## 1. Problem Statement

Design a distributed task scheduler similar to Kubernetes CronJobs, Apache Airflow, or Temporal that can schedule, execute, and monitor millions of jobs across thousands of worker nodes. The system should support cron-style scheduling, dependency management, retry logic, resource allocation, and provide strong consistency guarantees for job execution.

## 2. Requirements

### Functional Requirements
- **Job scheduling**: Support cron expressions and one-time jobs
- **Job dependencies**: Jobs can depend on other jobs (DAG execution)
- **Distributed execution**: Execute jobs across multiple worker nodes
- **Resource management**: Allocate jobs based on CPU/memory requirements
- **Retry logic**: Automatic retries with exponential backoff
- **Job prioritization**: High-priority jobs execute first
- **Execution history**: Track all job executions and outcomes
- **Job cancellation**: Cancel running or scheduled jobs
- **Workflow orchestration**: Complex multi-step workflows
- **At-most-once execution**: Guarantee job runs at most once per trigger

### Non-Functional Requirements
- **Scale**: Schedule 1 million jobs/day across 10,000 worker nodes
- **Latency**: Job starts within 10 seconds of scheduled time
- **Throughput**: Handle 1,000 job submissions/second
- **Availability**: 99.99% uptime for scheduler
- **Consistency**: Strong consistency for job state
- **Fault tolerance**: Survive coordinator and worker failures
- **Fair scheduling**: Prevent resource starvation

### Out of Scope
- Job code deployment and versioning
- Log aggregation from jobs
- Complex machine learning workflow features
- Real-time streaming jobs

## 3. Capacity Estimation

### Scale Assumptions
- Total jobs scheduled: 1 million/day
- Average job duration: 5 minutes
- Worker nodes: 10,000
- Jobs per second (peak): 1,000
- Average job payload: 10 KB
- Job history retention: 90 days
- Active (scheduled) jobs: 100,000

### Storage Estimation
```
Job metadata:
- 1M jobs/day × 10 KB = 10 GB/day
- 90-day retention = 900 GB
- Job execution logs (10 KB per execution): 900 GB
Total job storage = 1.8 TB

Worker state:
- 10K workers × 1 KB = 10 MB

Active job queue:
- 100K jobs × 10 KB = 1 GB

Total storage: ~2 TB with overhead
```

### Memory Estimation
```
Scheduler state:
- Active jobs in memory: 100K × 1 KB = 100 MB
- Pending queue: 50K × 1 KB = 50 MB
- Worker registry: 10K × 1 KB = 10 MB

Per scheduler node: ~200 MB
Scheduler nodes (HA): 3 nodes
Total memory: ~600 MB

Worker memory:
- Per worker: 16 GB (for job execution)
- Total: 10K × 16 GB = 160 TB
```

### Compute Estimation
```
Concurrent jobs:
- Average job duration: 5 minutes
- Jobs/day: 1M
- Concurrent jobs = 1M × (5/1440) = 3,472 jobs

Worker capacity:
- Jobs per worker: 1 (for isolation)
- Required workers: 3,500
- Provisioned workers: 10,000 (3x capacity)

CPU per worker: 4 cores
Total CPU: 40,000 cores
```

## 4. High-Level Design

```
┌─────────────────────────────────────────────────┐
│               Job Submission                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   API    │  │  Cron    │  │ Workflow │    │
│  │  Client  │  │  Config  │  │  Engine  │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼───────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │      API Gateway            │
        │  - Authentication           │
        │  - Validation               │
        │  - Rate limiting            │
        └─────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────────────────┐
        │   Scheduler Cluster         │
        │   (Leader + Followers)      │
        │                             │
        │  ┌─────────────────────┐   │
        │  │  Leader Scheduler   │   │ ← Leader Election
        │  │  - Job scheduling   │   │   (via ZooKeeper/etcd)
        │  │  - Worker assignment│   │
        │  │  - State management │   │
        │  └──────────┬──────────┘   │
        │             │               │
        │  ┌──────────┴──────────┐   │
        │  │  Follower Schedulers│   │ (Standby)
        │  └─────────────────────┘   │
        └──────────┬──────────────────┘
                   │
                   │ Distribute jobs
                   ▼
        ┌──────────────────────────────┐
        │     Job Queue (Kafka)        │
        │  Topics by priority:         │
        │  - high_priority_jobs        │
        │  - normal_priority_jobs      │
        │  - low_priority_jobs         │
        └──────┬───────────────────────┘
               │
               │ Pull jobs
               ▼
        ┌──────────────────────────────────────┐
        │          Worker Pool                  │
        │  ┌────────┐  ┌────────┐  ┌────────┐ │
        │  │Worker 1│  │Worker 2│  │Worker N│ │
        │  │ - Poll │  │ - Poll │  │ - Poll │ │
        │  │ - Exec │  │ - Exec │  │ - Exec │ │
        │  │ - Heartbeat│ - Heartbeat│ - HB │ │
        │  └───┬────┘  └───┬────┘  └───┬────┘ │
        └──────┼───────────┼───────────┼──────┘
               │           │           │
               └───────────┴───────────┘
                          │
                          ▼ Report status
        ┌──────────────────────────────────────┐
        │       State Store (DB)               │
        │  - Job definitions                   │
        │  - Job executions                    │
        │  - Worker registry                   │
        │  - Dependency DAG                    │
        └──────────────────────────────────────┘

Supporting Services:
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ Coordination│  │ Monitoring  │  │ Time Service │
│ (ZooKeeper) │  │ & Alerting  │  │ (NTP)        │
└─────────────┘  └─────────────┘  └──────────────┘
```

### Core Components
1. **Scheduler**: Orchestrates job execution
2. **Job Queue**: Buffers jobs for workers
3. **Worker Pool**: Executes jobs
4. **State Store**: Persistent job and execution state
5. **Coordinator**: Leader election and consensus
6. **Time Service**: Synchronized time for scheduling
7. **Dependency Manager**: Handles job dependencies

## 5. API Design

### Job Management API

```python
class JobSchedulerAPI:
    def create_job(self, job: JobDefinition) -> JobID:
        """
        Create a new job
        JobDefinition: {
            name: str,
            schedule: str,  # Cron expression or "once"
            command: str,
            arguments: List[str],
            environment: Dict[str, str],
            resources: ResourceRequirements,
            retry_policy: RetryPolicy,
            timeout: int,  # seconds
            dependencies: List[JobID],
            priority: int,  # 0-10
            metadata: Dict[str, str]
        }
        Returns: job_id
        """
        pass

    def update_job(self, job_id: JobID, updates: JobDefinition) -> bool:
        """Update job definition"""
        pass

    def delete_job(self, job_id: JobID) -> bool:
        """Delete job (stops future executions)"""
        pass

    def trigger_job(self, job_id: JobID) -> ExecutionID:
        """Manually trigger job execution"""
        pass

    def cancel_execution(self, execution_id: ExecutionID) -> bool:
        """Cancel running execution"""
        pass

    def get_job_status(self, job_id: JobID) -> JobStatus:
        """
        Get job status
        Returns: next_run_time, last_run_time, last_status
        """
        pass

    def list_executions(self, job_id: JobID, limit: int) -> List[Execution]:
        """Get execution history for job"""
        pass

    def get_execution_logs(self, execution_id: ExecutionID) -> str:
        """Get logs from job execution"""
        pass
```

### Worker API

```python
class WorkerAPI:
    def register_worker(self, worker: WorkerInfo) -> WorkerID:
        """
        Register worker with scheduler
        WorkerInfo: {
            hostname: str,
            ip_address: str,
            resources: ResourceCapacity,
            labels: Dict[str, str]
        }
        """
        pass

    def heartbeat(self, worker_id: WorkerID, status: WorkerStatus):
        """Send heartbeat to scheduler"""
        pass

    def poll_job(self, worker_id: WorkerID) -> Optional[Job]:
        """Poll for next job to execute"""
        pass

    def report_execution_result(self, execution_id: ExecutionID, result: ExecutionResult):
        """
        Report job execution outcome
        ExecutionResult: {
            status: str,  # success, failed, timeout
            exit_code: int,
            stdout: str,
            stderr: str,
            duration: int
        }
        """
        pass
```

## 6. Component Design

### Scheduler Core

**Job Scheduling Algorithm**

```python
class Scheduler:
    """Main scheduler component"""

    def __init__(self):
        self.job_store = JobStore()
        self.execution_store = ExecutionStore()
        self.worker_registry = WorkerRegistry()
        self.job_queue = JobQueue()
        self.dependency_manager = DependencyManager()
        self.time_wheel = TimeWheel()  # Efficient timer implementation
        self.is_leader = False

    async def run(self):
        """Main scheduler loop"""
        await self.ensure_leader()

        if not self.is_leader:
            # Follower mode: standby
            await self.follower_mode()
            return

        # Leader mode: active scheduling
        asyncio.create_task(self.schedule_loop())
        asyncio.create_task(self.monitor_workers())
        asyncio.create_task(self.process_completions())

    async def schedule_loop(self):
        """Continuously schedule jobs"""
        while True:
            current_time = self.get_current_time()

            # Get jobs due for execution
            due_jobs = self.time_wheel.get_due_jobs(current_time)

            for job in due_jobs:
                await self.schedule_job(job)

            await asyncio.sleep(1)  # Check every second

    async def schedule_job(self, job: Job):
        """Schedule single job for execution"""
        # 1. Check dependencies
        if job.dependencies:
            deps_satisfied = await self.dependency_manager.check_dependencies(job)
            if not deps_satisfied:
                # Reschedule for later
                self.time_wheel.schedule(job, delay=60)
                return

        # 2. Find suitable worker
        worker = await self.find_worker(job.resources)
        if not worker:
            # No available worker, requeue
            self.job_queue.enqueue(job, priority=job.priority)
            return

        # 3. Create execution record
        execution = Execution(
            job_id=job.id,
            scheduled_time=job.next_run_time,
            status='scheduled',
            worker_id=worker.id
        )
        await self.execution_store.save(execution)

        # 4. Assign to worker
        await self.assign_job_to_worker(job, worker, execution.id)

        # 5. Schedule next run (for recurring jobs)
        if job.schedule != 'once':
            next_run_time = self.calculate_next_run(job.schedule)
            job.next_run_time = next_run_time
            self.time_wheel.schedule(job, next_run_time)

    async def find_worker(self, required_resources: ResourceRequirements) -> Optional[Worker]:
        """
        Find worker with sufficient resources
        Implements bin-packing with best-fit strategy
        """
        available_workers = self.worker_registry.get_available_workers()

        # Filter workers with sufficient resources
        suitable_workers = [
            w for w in available_workers
            if self.has_sufficient_resources(w, required_resources)
        ]

        if not suitable_workers:
            return None

        # Sort by resource utilization (prefer least loaded)
        suitable_workers.sort(key=lambda w: w.utilization)

        return suitable_workers[0]

    def has_sufficient_resources(self, worker: Worker, required: ResourceRequirements) -> bool:
        """Check if worker has sufficient resources"""
        return (
            worker.available_cpu >= required.cpu and
            worker.available_memory >= required.memory and
            worker.available_disk >= required.disk
        )

    def calculate_next_run(self, cron_expression: str) -> int:
        """
        Calculate next run time from cron expression
        Format: "minute hour day month weekday"
        Example: "0 2 * * *" = 2 AM daily
        """
        cron = croniter(cron_expression, datetime.now())
        next_run = cron.get_next(datetime)
        return int(next_run.timestamp())
```

### Time Wheel Implementation

**Hierarchical Time Wheel for Efficient Scheduling**

```python
class TimeWheel:
    """
    Hierarchical time wheel for efficient timer management
    Inspired by Kafka's purgatory and Linux timer wheel

    Structure:
    - Wheel 0: 1-second slots (0-59 seconds)
    - Wheel 1: 1-minute slots (0-59 minutes)
    - Wheel 2: 1-hour slots (0-23 hours)
    - Wheel 3: 1-day slots (0-30 days)
    """

    def __init__(self):
        self.wheels = [
            TimerWheel(tick_ms=1000, wheel_size=60),    # Seconds
            TimerWheel(tick_ms=60000, wheel_size=60),   # Minutes
            TimerWheel(tick_ms=3600000, wheel_size=24), # Hours
            TimerWheel(tick_ms=86400000, wheel_size=30) # Days
        ]
        self.current_time = 0

    def schedule(self, job: Job, target_time: int):
        """Schedule job for target time"""
        delay_ms = (target_time - self.current_time) * 1000

        # Find appropriate wheel
        for i, wheel in enumerate(self.wheels):
            if delay_ms < wheel.interval:
                wheel.add(job, delay_ms)
                return

        # If beyond all wheels, schedule in last wheel
        self.wheels[-1].add(job, delay_ms)

    def advance_time(self, current_time: int):
        """Advance time and cascade overflows"""
        self.current_time = current_time

        # Advance each wheel
        for i, wheel in enumerate(self.wheels):
            overflow_jobs = wheel.tick()

            # Cascade overflow to lower wheel
            if overflow_jobs and i > 0:
                for job in overflow_jobs:
                    self.wheels[i-1].add(job, 0)

    def get_due_jobs(self, current_time: int) -> List[Job]:
        """Get all jobs due at current time"""
        self.advance_time(current_time)
        return self.wheels[0].get_expired()

class TimerWheel:
    """Single wheel in hierarchical time wheel"""

    def __init__(self, tick_ms: int, wheel_size: int):
        self.tick_ms = tick_ms
        self.wheel_size = wheel_size
        self.buckets = [[] for _ in range(wheel_size)]
        self.current_bucket = 0
        self.interval = tick_ms * wheel_size

    def add(self, job: Job, delay_ms: int):
        """Add job to wheel"""
        ticks = delay_ms // self.tick_ms
        bucket_index = (self.current_bucket + ticks) % self.wheel_size
        self.buckets[bucket_index].append(job)

    def tick(self) -> List[Job]:
        """Advance wheel by one tick"""
        overflow = []

        if self.current_bucket == self.wheel_size - 1:
            # End of wheel, return all jobs in last bucket for cascading
            overflow = self.buckets[self.current_bucket]
            self.buckets[self.current_bucket] = []

        self.current_bucket = (self.current_bucket + 1) % self.wheel_size
        return overflow

    def get_expired(self) -> List[Job]:
        """Get jobs in current bucket"""
        jobs = self.buckets[self.current_bucket]
        self.buckets[self.current_bucket] = []
        return jobs
```

**Time Complexity**: O(1) for insert, O(1) amortized for tick
**Space Complexity**: O(n) where n is number of scheduled jobs

### Dependency Manager

**DAG-based Dependency Resolution**

```python
class DependencyManager:
    """Manage job dependencies as DAG"""

    def __init__(self):
        self.dag = {}  # job_id -> set of dependency job_ids
        self.execution_store = ExecutionStore()

    def add_dependency(self, job_id: str, depends_on: str):
        """Add dependency relationship"""
        if job_id not in self.dag:
            self.dag[job_id] = set()
        self.dag[job_id].add(depends_on)

        # Detect cycles
        if self.has_cycle(job_id):
            raise ValueError("Cyclic dependency detected")

    def has_cycle(self, start_job: str) -> bool:
        """Detect cycles using DFS"""
        visited = set()
        rec_stack = set()

        def dfs(job_id: str) -> bool:
            visited.add(job_id)
            rec_stack.add(job_id)

            for dep in self.dag.get(job_id, []):
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    return True

            rec_stack.remove(job_id)
            return False

        return dfs(start_job)

    async def check_dependencies(self, job: Job) -> bool:
        """Check if all dependencies are satisfied"""
        if not job.dependencies:
            return True

        for dep_job_id in job.dependencies:
            # Get latest execution of dependency
            last_execution = await self.execution_store.get_latest_execution(dep_job_id)

            # Check if dependency completed successfully
            if not last_execution or last_execution.status != 'success':
                return False

            # Check if dependency completed recently
            if job.dependency_timeout:
                elapsed = time.time() - last_execution.completed_at
                if elapsed > job.dependency_timeout:
                    return False

        return True

    def get_execution_order(self, job_ids: List[str]) -> List[str]:
        """
        Get topological sort of jobs for execution
        Returns jobs in dependency order
        """
        in_degree = {}
        adj_list = defaultdict(list)

        # Build graph
        for job_id in job_ids:
            in_degree[job_id] = 0

        for job_id in job_ids:
            for dep in self.dag.get(job_id, []):
                if dep in job_ids:
                    adj_list[dep].append(job_id)
                    in_degree[job_id] += 1

        # Kahn's algorithm for topological sort
        queue = deque([job_id for job_id in job_ids if in_degree[job_id] == 0])
        result = []

        while queue:
            job_id = queue.popleft()
            result.append(job_id)

            for neighbor in adj_list[job_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result
```

### Worker Management

**Worker Registration and Health Monitoring**

```python
class WorkerRegistry:
    """Track available workers and their state"""

    def __init__(self):
        self.workers = {}  # worker_id -> Worker
        self.heartbeat_timeout = 30  # seconds
        self.lock = asyncio.Lock()

    async def register_worker(self, worker_info: WorkerInfo) -> str:
        """Register new worker"""
        worker_id = self.generate_worker_id()

        worker = Worker(
            id=worker_id,
            hostname=worker_info.hostname,
            ip_address=worker_info.ip_address,
            resources=worker_info.resources,
            labels=worker_info.labels,
            status='idle',
            last_heartbeat=time.time(),
            current_job=None
        )

        async with self.lock:
            self.workers[worker_id] = worker

        return worker_id

    async def update_heartbeat(self, worker_id: str, status: WorkerStatus):
        """Update worker heartbeat"""
        async with self.lock:
            if worker_id in self.workers:
                worker = self.workers[worker_id]
                worker.last_heartbeat = time.time()
                worker.status = status.state
                worker.available_cpu = status.available_cpu
                worker.available_memory = status.available_memory

    async def get_available_workers(self) -> List[Worker]:
        """Get workers available for new jobs"""
        current_time = time.time()
        available = []

        async with self.lock:
            for worker in self.workers.values():
                # Check heartbeat
                if current_time - worker.last_heartbeat > self.heartbeat_timeout:
                    worker.status = 'dead'
                    continue

                if worker.status == 'idle':
                    available.append(worker)

        return available

    async def mark_worker_busy(self, worker_id: str, job_id: str):
        """Mark worker as busy with job"""
        async with self.lock:
            if worker_id in self.workers:
                self.workers[worker_id].status = 'busy'
                self.workers[worker_id].current_job = job_id

    async def mark_worker_idle(self, worker_id: str):
        """Mark worker as idle"""
        async with self.lock:
            if worker_id in self.workers:
                self.workers[worker_id].status = 'idle'
                self.workers[worker_id].current_job = None

    async def remove_dead_workers(self):
        """Remove workers that haven't sent heartbeat"""
        current_time = time.time()

        async with self.lock:
            dead_workers = [
                worker_id
                for worker_id, worker in self.workers.items()
                if current_time - worker.last_heartbeat > self.heartbeat_timeout * 2
            ]

            for worker_id in dead_workers:
                # Reassign jobs from dead worker
                worker = self.workers[worker_id]
                if worker.current_job:
                    await self.reschedule_job(worker.current_job)

                del self.workers[worker_id]
```

### Job Execution (Worker)

**Job Execution with Retry and Timeout**

```python
class Worker:
    """Worker that executes jobs"""

    def __init__(self, worker_id: str, scheduler_url: str):
        self.worker_id = worker_id
        self.scheduler_url = scheduler_url
        self.current_execution = None
        self.is_running = True

    async def run(self):
        """Main worker loop"""
        while self.is_running:
            try:
                # Send heartbeat
                await self.send_heartbeat()

                # Poll for job
                job = await self.poll_job()

                if job:
                    await self.execute_job(job)
                else:
                    await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(10)

    async def execute_job(self, job: Job):
        """Execute single job"""
        execution_id = job.execution_id
        self.current_execution = execution_id

        # Create isolated execution environment
        try:
            # Start execution
            await self.report_status(execution_id, 'running')

            # Execute with timeout
            result = await asyncio.wait_for(
                self.run_job_command(job),
                timeout=job.timeout
            )

            # Report success
            await self.report_result(execution_id, result)

        except asyncio.TimeoutError:
            # Job timeout
            await self.report_status(execution_id, 'timeout')
            await self.cleanup(job)

        except Exception as e:
            # Job failed
            logger.error(f"Job execution failed: {e}")
            await self.report_status(execution_id, 'failed', error=str(e))

        finally:
            self.current_execution = None

    async def run_job_command(self, job: Job) -> ExecutionResult:
        """Run job command in subprocess"""
        # Build command
        cmd = [job.command] + job.arguments

        # Set environment variables
        env = os.environ.copy()
        env.update(job.environment)

        # Execute subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        # Wait for completion
        stdout, stderr = await process.communicate()

        return ExecutionResult(
            exit_code=process.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
            status='success' if process.returncode == 0 else 'failed'
        )

    async def send_heartbeat(self):
        """Send heartbeat to scheduler"""
        status = WorkerStatus(
            worker_id=self.worker_id,
            state='busy' if self.current_execution else 'idle',
            available_cpu=self.get_available_cpu(),
            available_memory=self.get_available_memory(),
            current_job=self.current_execution
        )

        await self.api_client.heartbeat(self.worker_id, status)

    async def poll_job(self) -> Optional[Job]:
        """Poll scheduler for next job"""
        return await self.api_client.poll_job(self.worker_id)
```

### Retry Logic

**Exponential Backoff with Jitter**

```python
class RetryManager:
    """Manage job retries"""

    def __init__(self):
        self.max_retries = 3
        self.base_delay = 60  # seconds
        self.max_delay = 3600  # 1 hour

    async def handle_failed_execution(self, execution: Execution):
        """Handle failed job execution"""
        job = await self.job_store.get_job(execution.job_id)

        # Check retry policy
        if not job.retry_policy or not job.retry_policy.enabled:
            # No retries, mark as failed
            return

        # Check retry count
        if execution.retry_count >= job.retry_policy.max_retries:
            # Max retries exceeded
            await self.notify_failure(job, execution)
            return

        # Calculate backoff delay
        delay = self.calculate_backoff(
            execution.retry_count,
            job.retry_policy
        )

        # Schedule retry
        retry_time = time.time() + delay
        job.next_run_time = retry_time
        execution.retry_count += 1

        await self.scheduler.time_wheel.schedule(job, retry_time)

    def calculate_backoff(self, retry_count: int, policy: RetryPolicy) -> int:
        """
        Calculate exponential backoff with jitter
        delay = min(base * (2 ^ retry_count), max_delay) + random_jitter
        """
        exponential_delay = policy.base_delay * (2 ** retry_count)
        capped_delay = min(exponential_delay, policy.max_delay)

        # Add jitter (±25%)
        jitter_range = capped_delay * 0.25
        jitter = random.uniform(-jitter_range, jitter_range)

        return int(capped_delay + jitter)
```

## 7. Data Structures & Storage

### Database Schema

```sql
-- Job definitions
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    schedule VARCHAR(100),  -- Cron expression
    command TEXT NOT NULL,
    arguments JSONB,
    environment JSONB,
    resources JSONB,  -- CPU, memory, disk
    retry_policy JSONB,
    timeout INTEGER,
    dependencies JSONB,  -- Array of job IDs
    priority INTEGER DEFAULT 5,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    next_run_time TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_jobs_next_run ON jobs(next_run_time) WHERE enabled = TRUE;
CREATE INDEX idx_jobs_schedule ON jobs(schedule);

-- Job executions
CREATE TABLE executions (
    id UUID PRIMARY KEY,
    job_id UUID REFERENCES jobs(id),
    worker_id VARCHAR(100),
    scheduled_time TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(50),  -- scheduled, running, success, failed, timeout, cancelled
    exit_code INTEGER,
    stdout TEXT,
    stderr TEXT,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    duration INTEGER,  -- seconds
    metadata JSONB
);

CREATE INDEX idx_executions_job ON executions(job_id, started_at DESC);
CREATE INDEX idx_executions_status ON executions(status, scheduled_time);
CREATE INDEX idx_executions_worker ON executions(worker_id);

-- Workers
CREATE TABLE workers (
    id VARCHAR(100) PRIMARY KEY,
    hostname VARCHAR(255),
    ip_address VARCHAR(50),
    resources JSONB,  -- CPU, memory capacity
    labels JSONB,
    status VARCHAR(50),  -- idle, busy, dead
    last_heartbeat TIMESTAMP,
    current_job UUID,
    registered_at TIMESTAMP
);

CREATE INDEX idx_workers_status ON workers(status, last_heartbeat);

-- Job dependencies (for efficient queries)
CREATE TABLE job_dependencies (
    job_id UUID REFERENCES jobs(id),
    depends_on_job_id UUID REFERENCES jobs(id),
    PRIMARY KEY (job_id, depends_on_job_id)
);

CREATE INDEX idx_dependencies_job ON job_dependencies(job_id);
```

## 8. Fault Tolerance & High Availability

### Leader Election

```python
# Using ZooKeeper for leader election
class LeaderElection:
    def __init__(self, zk_hosts: str, scheduler_id: str):
        self.zk = KazooClient(hosts=zk_hosts)
        self.scheduler_id = scheduler_id
        self.election_path = "/scheduler/leader"
        self.is_leader = False

    async def participate_in_election(self):
        """Participate in leader election"""
        await self.zk.start()

        # Create ephemeral sequential node
        election_node = await self.zk.create(
            f"{self.election_path}/candidate_",
            value=self.scheduler_id.encode(),
            ephemeral=True,
            sequence=True
        )

        # Watch for leader changes
        await self.watch_leader()

    async def watch_leader(self):
        """Watch for leader changes"""
        while True:
            # Get all candidates
            candidates = await self.zk.get_children(self.election_path)
            candidates.sort()

            # Check if this node is leader
            if candidates[0] == os.path.basename(self.election_node):
                # This is the leader
                if not self.is_leader:
                    await self.become_leader()
            else:
                # Watch previous candidate
                prev_candidate = candidates[candidates.index(os.path.basename(self.election_node)) - 1]
                await self.zk.exists(
                    f"{self.election_path}/{prev_candidate}",
                    watch=self.watch_leader
                )

                if self.is_leader:
                    await self.step_down()

    async def become_leader(self):
        """Transition to leader"""
        self.is_leader = True
        logger.info("Became leader")
        # Start scheduler responsibilities
        await self.scheduler.start_scheduling()

    async def step_down(self):
        """Step down from leader"""
        self.is_leader = False
        logger.info("Stepped down from leader")
        # Stop scheduler responsibilities
        await self.scheduler.stop_scheduling()
```

### Job Recovery

```python
async def recover_from_failure():
    """Recover jobs after scheduler restart"""
    # 1. Find executions that were running when scheduler crashed
    stuck_executions = await db.query(
        "SELECT * FROM executions WHERE status = 'running' OR status = 'scheduled'"
    )

    for execution in stuck_executions:
        # Check if worker is still alive
        worker = await worker_registry.get_worker(execution.worker_id)

        if not worker or worker.status == 'dead':
            # Worker is dead, reschedule job
            await reschedule_job(execution.job_id)
        else:
            # Worker alive, check if job is actually running
            is_running = await worker.check_job_status(execution.id)
            if not is_running:
                # Job not running, reschedule
                await reschedule_job(execution.job_id)
```

## 9. Monitoring & Observability

### Metrics

```python
# Job metrics
jobs_scheduled_total = Counter('jobs_scheduled_total')
jobs_completed_total = Counter('jobs_completed_total', labels=['status'])
job_duration_seconds = Histogram('job_duration_seconds')
job_queue_size = Gauge('job_queue_size', labels=['priority'])

# Scheduler metrics
scheduler_is_leader = Gauge('scheduler_is_leader')
active_workers = Gauge('active_workers')
scheduling_latency = Histogram('scheduling_latency_seconds')

# Worker metrics
worker_utilization = Gauge('worker_utilization')
job_execution_errors = Counter('job_execution_errors', labels=['error_type'])
```

## 10. Scalability

### Horizontal Scaling

- Add more workers for execution capacity
- Use partitioned job queue (Kafka) for higher throughput
- Shard job storage by job ID
- Use read replicas for query load

### Optimization

- Cache frequently accessed jobs in memory
- Use bloom filters for fast dependency checks
- Batch database operations
- Implement job coalescing for high-frequency jobs

## 11. Trade-offs

### At-most-once vs At-least-once
- **At-most-once**: Simpler, but jobs might not run
- **At-least-once**: More reliable, but need idempotency

### Centralized vs Decentralized
- **Centralized scheduler**: Simpler, potential bottleneck
- **Decentralized**: More complex, better scalability

### Strong vs Eventual Consistency
- **Strong**: Correct state, higher latency
- **Eventual**: Lower latency, temporary inconsistencies

## 12. Follow-up Questions

1. How would you implement exactly-once execution semantics?
2. How would you handle jobs that need GPU resources?
3. How would you implement job priorities with preemption?
4. How would you handle timezone-aware scheduling?
5. How would you implement workflow orchestration (branching, loops)?
6. How would you handle secrets and credentials securely?
7. How would you implement cost optimization for cloud execution?
8. How would you handle long-running jobs (days/weeks)?
9. How would you implement fair scheduling across tenants?
10. How would you handle job output artifacts?
