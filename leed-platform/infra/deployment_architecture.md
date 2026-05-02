# Deployment Architecture

## Overview

Production-ready deployment using Docker containers on a cloud provider (AWS/GCP/Azure).

This deployment uses FastAPI for the public API, LangGraph for durable credit workflows, sandboxed skill containers for parsing/calculation/document generation, PostgreSQL for project state and checkpoints, Redis/RabbitMQ for queues and cache, object storage for evidence packages, and Vault for secrets. Celery workers may remain for background jobs such as document rendering and audit export assembly, but credit workflow state is owned by LangGraph checkpoints.

V1 boundary: the platform generates downloadable LEED submission packages after HITL approval. Direct USGBC Arc submission is disabled by default and controlled by `ENABLE_USGBC_INTEGRATION=false`.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CDN (CloudFront/CloudFlare)                     │
│                         Static Assets + API Caching                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Load Balancer                                   │
│                         (Application Load Balancer)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│   Frontend (Nginx)  │ │   Backend API       │ │   Backend API       │
│   (React Static)    │ │   (FastAPI)         │ │   (FastAPI)         │
│                     │ │   Instance 1        │ │   Instance 2        │
│  /usr/share/nginx   │ │                     │ │                     │
│  /html              │ │  - REST API         │ │  - REST API         │
│                     │ │  - WebSocket        │ │  - WebSocket        │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
          │                       │                           │
          │                       └───────────┬───────────────┘
          │                                   │
          │                       ┌───────────┴───────────┐
          │                       │                       │
          │                       ▼                       ▼
          │           ┌─────────────────────┐ ┌─────────────────────┐
          │           │   Agent Workers     │ │   Agent Workers     │
          │           │   (Celery)          │ │   (Celery)          │
          │           │                     │ │                     │
          │           │  - Credit agents    │ │  - Credit agents    │
          │           │  - API calls        │ │  - API calls        │
          │           │  - Document gen     │ │  - Document gen     │
          │           └─────────────────────┘ └─────────────────────┘
          │                       │
          │                       ▼
          │           ┌─────────────────────┐
          │           │   Message Queue     │
          │           │   (RabbitMQ)        │
          │           └─────────────────────┘
          │
          └───────────────────┬───────────────────┐
                              │                   │
                              ▼                   ▼
                  ┌─────────────────────┐ ┌─────────────────────┐
                  │   PostgreSQL        │ │   Redis             │
                  │   (Primary)         │ │   (Cache + Sessions)│
                  │                     │ │                     │
                  │  - Users            │ │  - Sessions         │
                  │  - Projects         │ │  - Cache            │
                  │  - Credits          │ │  - Rate limiting    │
                  │  - Workflows        │ │                     │
                  └─────────────────────┘ └─────────────────────┘
                              │
                              ▼
                  ┌─────────────────────┐
                  │   Object Storage    │
                  │   (S3 / GCS)        │
                  │                     │
                  │  - Documents        │
                  │  - Uploads          │
                  │  - Templates        │
                  └─────────────────────┘
```

## Container Structure

### Frontend Container
```dockerfile
# Dockerfile.frontend
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### Backend Container
```dockerfile
# Dockerfile.backend
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Worker Container
```dockerfile
# Dockerfile.worker
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
```

### LangGraph Workflow Container
```dockerfile
# Dockerfile.langgraph
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8123
CMD ["python", "-m", "langgraph_api.server", "--host", "0.0.0.0", "--port", "8123"]
```

### Skill Sandbox Container
```dockerfile
# Dockerfile.skill-sandbox
FROM python:3.12-slim
WORKDIR /sandbox
RUN useradd -m sandbox
USER sandbox
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "sandbox_runner"]
```

Skill sandboxes run with read-only root filesystems, CPU/memory limits, no host filesystem mounts except scoped project working directories, and network egress restricted to allowlisted APIs.

## Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/leed
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
    depends_on:
      - db
      - redis
      - rabbitmq

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.worker
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/leed
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
    depends_on:
      - db
      - redis
      - rabbitmq

  langgraph:
    build:
      context: ./backend
      dockerfile: Dockerfile.langgraph
    ports:
      - "8123:8123"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/leed
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
      - LANGGRAPH_CHECKPOINT_TABLE=langgraph_checkpoints
    depends_on:
      - db
      - redis
      - rabbitmq

  sandbox:
    build:
      context: ./backend
      dockerfile: Dockerfile.skill-sandbox
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    environment:
      - SANDBOX_OUTPUT_DIR=/mnt/user-data/outputs

  db:
    image: postgis/postgis:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=leed
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-alpine
    ports:
      - "5672:5672"
      - "15672:15672"

volumes:
  postgres_data:
```

## Kubernetes (Production)

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leed-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: leed-backend
  template:
    metadata:
      labels:
        app: leed-backend
    spec:
      containers:
      - name: backend
        image: leedai/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-credentials
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: leed-backend
spec:
  selector:
    app: leed-backend
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

## Environment Variables

### Required
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379

# Message Queue
RABBITMQ_URL=amqp://user:pass@host:5672

# Durable workflows
LANGGRAPH_URL=http://langgraph:8123
LANGGRAPH_CHECKPOINT_TABLE=langgraph_checkpoints
WORKFLOW_RETENTION_YEARS=7

# Object Storage
S3_BUCKET=leedai-documents
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx

# Auth
JWT_SECRET=xxx
JWT_ALGORITHM=HS256

# Secrets
VAULT_ADDR=https://vault.internal
VAULT_ROLE=leed-platform

# External APIs
OPENAI_API_KEY=xxx
EPA_EGRID_API_KEY=xxx
EC3_API_KEY=xxx
```

### Optional
```bash
# Monitoring
SENTRY_DSN=xxx
DATADOG_API_KEY=xxx

# Feature Flags
ENABLE_BETA_CREDITS=false
ENABLE_USGBC_INTEGRATION=false
ENABLE_DIRECT_ARC_SUBMISSION=false
ENABLE_REGIONAL_MANUAL_OVERRIDE=true
```

## Scaling Strategy

### Horizontal Scaling

| Service | Min | Max | Metric |
|---------|-----|-----|--------|
| Frontend | 2 | 10 | CPU > 70% |
| Backend API | 3 | 20 | CPU > 70%, Latency > 500ms |
| LangGraph workflow | 2 | 12 | Workflow queue depth, checkpoint latency |
| Workers | 5 | 50 | Queue depth > 100 |
| Skill sandboxes | 0 | 100 | Active skill executions |

### Database Scaling

**Read Replicas:**
- 2 read replicas for API queries
- 1 read replica for analytics

**Connection Pooling:**
- PgBouncer for connection pooling
- Max connections: 100 per instance

### Caching Strategy

| Data | TTL | Strategy |
|------|-----|----------|
| User sessions | 24h | Redis |
| API responses | API-specific | Redis with source snapshot persisted to PostgreSQL/S3 |
| Credit definitions | 1h | In-memory |
| Static assets | 1y | CDN |
| Documents | 1h | CDN signed URLs |
| Source snapshots | 7y | PostgreSQL metadata + S3 payload |

## Monitoring & Observability

### Health Checks

```python
# /health endpoint
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "rabbitmq": await check_rabbitmq(),
        "langgraph": await check_langgraph(),
        "vault": await check_vault(),
    }
    
    all_healthy = all(checks.values())
    status = 200 if all_healthy else 503
    
    return JSONResponse(
        content={"status": "healthy" if all_healthy else "unhealthy", "checks": checks},
        status_code=status
    )
```

### Metrics

| Metric | Type | Alert Threshold |
|--------|------|-----------------|
| API latency | Histogram | p95 > 500ms |
| Error rate | Counter | > 1% |
| Queue depth | Gauge | > 1000 |
| Worker utilization | Gauge | > 80% |
| Database connections | Gauge | > 80% |
| LangGraph checkpoint latency | Histogram | p95 > 500ms |
| Skill failure rate | Counter | > 5% for 10 min |
| HITL SLA breach rate | Gauge | > 10% |
| API circuit open count | Gauge | > 0 critical APIs |
| Low-confidence output rate | Gauge | > 20% per skill |

### Logging

```python
# Structured logging
logger.info("Credit automation started", extra={
    "credit_code": "IPp3",
    "project_id": "proj-123",
    "user_id": "user-456",
    "workflow_id": "wf-789"
})
```

## Backup Strategy

### Database
- **Frequency:** Daily at 2 AM UTC, with point-in-time recovery where supported
- **Operational backup retention:** 30 days
- **Audit metadata retention:** 7 years for workflow checkpoints, source snapshots, calculation records, and HITL records
- **Storage:** S3 Glacier
- **Encryption:** AES-256

### Documents
- **Storage:** S3 with versioning
- **Lifecycle:** Move audit packages and generated evidence documents to Glacier after 90 days
- **Retention:** 7 years unless a customer contract requires longer retention
- **Cross-region:** Replicate to secondary region

## Disaster Recovery

### RPO (Recovery Point Objective)
- Database: 24 hours (daily backups)
- Documents: Real-time (S3 versioning)

### RTO (Recovery Time Objective)
- Database: 2 hours (restore from backup)
- Full system: 4 hours (redeploy to new region)

### Failover
- Multi-AZ deployment
- Automatic failover for database
- Manual failover for region (runbook)

## Cost Estimates

### Monthly (Production)

| Service | Instance | Cost |
|---------|----------|------|
| Frontend (2x) | t3.medium | $60 |
| Backend (3x) | t3.large | $180 |
| Workers (5x) | t3.medium | $150 |
| PostgreSQL | db.t3.large | $200 |
| Redis | cache.t3.micro | $15 |
| RabbitMQ | t3.micro | $30 |
| S3 Storage | 100GB | $5 |
| CDN | 1TB transfer | $50 |
| **Total** | | **~$690/month** |

---

*Version: 1.0*
*Last Updated: 2026-03-21*
