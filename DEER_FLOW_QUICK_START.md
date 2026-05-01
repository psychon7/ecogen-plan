# Deer-Flow Quick Start for LEED Platform

## 5-Minute Setup

```bash
# 1. Clone Deer-Flow
git clone https://github.com/bytedance/deer-flow.git leed-platform
cd leed-platform

# 2. Run setup wizard
make setup
# Follow prompts:
# - Choose LLM provider (OpenAI recommended)
# - Enter API keys
# - Skip web search for now
# - Choose sandbox mode (Docker recommended)

# 3. Verify setup
make doctor

# 4. Start services
make docker-start

# 5. Access UI
open http://localhost:2026
```

## Create First LEED Skill (PRc2 - LEED AP)

```bash
# Create skill directory
mkdir -p skills/leed/pr-c2-leed-ap

# Create SKILL.md
cat > skills/leed/pr-c2-leed-ap/SKILL.md << 'EOF'
---
name: pr-c2-leed-ap
version: 1.0.0
author: LEED Platform Team
description: Verify LEED AP credentials for project team
---

## Inputs
```json
{
  "team_members": [
    {"name": "John Doe", "leed_ap_number": "12345"}
  ],
  "project_rating_system": "BD+C"
}
```

## Workflow
1. Validate team_members array
2. For each member, query GBCI Credential Directory
3. Verify credential status is active
4. Check specialty matches project type
5. Generate verification report

## Tools
- web_search (for GBCI API)
- file_write (for report generation)

## Output
```json
{
  "verification_results": [
    {
      "name": "John Doe",
      "credential": "LEED AP BD+C",
      "status": "active",
      "expires": "2025-12-31",
      "specialty_match": true
    }
  ],
  "all_verified": true
}
```
EOF
```

## Test the Skill

```bash
# Via web UI
curl -X POST http://localhost:2026/api/threads \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "pr-c2-leed-ap",
    "inputs": {
      "team_members": [{"name": "Test", "leed_ap_number": "12345"}],
      "project_rating_system": "BD+C"
    }
  }'
```

## Add API Integration

```python
# backend/deerflow/tools/leed/gbci_api.py

from deerflow.tools.base import BaseTool
import requests

class GBCIVerificationTool(BaseTool):
    name = "gbci_verify"
    description = "Verify LEED AP credential with GBCI"
    
    async def run(self, leed_ap_number: str) -> dict:
        url = f"https://www.usgbc.org/api/credentials/{leed_ap_number}"
        response = requests.get(url)
        return response.json()
```

## Enable Slack HITL

```yaml
# config.yaml
channels:
  slack:
    enabled: true
    bot_token: "xoxb-your-bot-token"
    app_token: "xapp-your-app-token"
```

```bash
# Set environment variables
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."

# Restart
make docker-start
```

## Project Structure

```
leed-platform/
├── backend/
│   └── deerflow/
│       └── tools/
│           └── leed/           # LEED-specific tools
│               ├── gbci_api.py
│               ├── epa_egrid.py
│               ├── ec3_database.py
│               └── ...
├── skills/
│   └── leed/                   # LEED credit skills
│       ├── ip-p3-carbon/
│       ├── ea-p1-op-carbon/
│       ├── we-p2-water-min/
│       └── ... (16 skills)
├── frontend/                   # Deer-Flow UI (extend)
└── docker/                     # Deployment configs
```

## Development Workflow

```bash
# 1. Start in dev mode
make dev

# 2. Edit skill
vim skills/leed/ip-p3-carbon/SKILL.md

# 3. Test skill
# Via web UI at http://localhost:2026

# 4. Check logs
docker logs deerflow-backend

# 5. Iterate
# Edit → Test → Repeat
```

## Deploy to Production

```bash
# Build production images
make up

# Or deploy to cloud
# (See Deer-Flow docs for Kubernetes deployment)
```

## Common Commands

```bash
# Start services
make docker-start

# Stop services
make docker-stop

# View logs
docker logs deerflow-backend -f

# Check health
make doctor

# Reset everything
make clean && make docker-start
```

## Next Steps

1. ✅ Setup Deer-Flow (5 min)
2. ✅ Create first skill (10 min)
3. ⏳ Create remaining 15 skills (1 week)
4. ⏳ Add API integrations (3 days)
5. ⏳ Build HITL dashboard (2 days)
6. ⏳ Deploy to production (1 day)

**Total: 2-3 weeks to MVP**
