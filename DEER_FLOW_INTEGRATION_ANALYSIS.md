# Deer-Flow Integration Analysis for LEED v5 Automation Platform

## Executive Summary

**Deer-Flow** is ByteDance's open-source "SuperAgent Harness" (60.2k stars) that provides exactly the infrastructure we need for building the LEED v5 automation platform. It offers:

- **Skill-based architecture** - Each credit can be a skill
- **Sub-agent orchestration** - Parallel processing of credit tasks
- **Durable workflows** - State persistence for long-running tasks
- **Sandbox execution** - Isolated environments for calculations
- **Memory system** - Persistent knowledge across sessions
- **HITL support** - Human-in-the-loop via messaging channels

**Verdict:** Deer-Flow provides 70-80% of the infrastructure we need. We can build the LEED-specific layer on top.

---

## What Deer-Flow Provides

### 1. Skill System (Perfect for LEED Credits)

Deer-Flow's skill system is exactly what we designed:

```
/mnt/skills/public/
├── research/SKILL.md
├── report-generation/SKILL.md
├── slide-creation/SKILL.md
└── web-page/SKILL.md

# Our LEED skills would be:
/mnt/skills/leed/
├── ip-p3-carbon/SKILL.md
├── ea-p1-op-carbon/SKILL.md
├── we-p2-water-min/SKILL.md
└── ... (16 skills)
```

**Skill Structure in Deer-Flow:**
```markdown
# SKILL.md format (Deer-Flow compatible)
---
name: ip-p3-carbon-assessment
version: 1.0.0
author: LEED Platform Team
description: Calculate 25-year carbon projection
---

## Workflow
1. Validate inputs
2. Fetch grid emission factors from EPA eGRID
3. Fetch embodied carbon from EC3
4. Calculate operational carbon
5. Calculate refrigerant emissions
6. Generate projection report
7. [HITL] Review by LEED consultant
8. Finalize output

## Tools Required
- web_search (for data lookup)
- file_read (for energy model parsing)
- file_write (for report generation)
- bash (for calculations)

## Sub-Agents
- carbon_calculator: Performs calculations
- report_generator: Creates PDF/Excel outputs
```

### 2. Sub-Agent Orchestration

Deer-Flow can spawn sub-agents for parallel processing:

```python
# Lead agent spawns sub-agents for each credit
sub_agents = [
    {"name": "ip-p3-agent", "skill": "ip-p3-carbon"},
    {"name": "we-p2-agent", "skill": "we-p2-water"},
    {"name": "ea-p5-agent", "skill": "ea-p5-refrigerant"},
    # ... all 16 credits
]

# Run in parallel
results = await lead_agent.spawn_parallel(sub_agents, inputs)
```

### 3. Durable Workflows (Built-in)

Deer-Flow uses LangGraph for durable workflows:

```python
from langgraph.graph import StateGraph

# Workflow survives restarts, API failures, human delays
workflow = StateGraph(LEEDState)

# Each node is checkpointed automatically
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_data", fetch_api_data)
workflow.add_node("calculate", perform_calculations)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate", generate_documents)

# Conditional edges based on HITL response
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_result"]["action"],
    {
        "approve": "generate",
        "reject": "validate",
        "request_changes": "calculate"
    }
)
```

### 4. Sandbox Execution

Deer-Flow provides isolated execution environments:

```yaml
# config.yaml
sandbox:
  use: deerflow.community.aio_sandbox:AioSandboxProvider
  provisioner_url: http://localhost:8080
  
  # Each credit calculation runs in isolated container
  # Files are persisted across steps
  # Bash execution is sandboxed
```

**For LEED Platform:**
- Each credit calculation runs in isolated sandbox
- Energy model parsing doesn't affect other credits
- Document generation has clean environment
- Files persisted at `/mnt/user-data/outputs/`

### 5. Memory System

Deer-Flow's memory system can store:

```python
# Project-specific memory
memory.save(
    thread_id="project-123",
    facts=[
        "Building type: Office",
        "Location: New York, NY",
        "Target certification: Gold",
        "Energy modeler: John Doe",
        "Preferred units: Imperial"
    ]
)

# Retrieved in future sessions
context = memory.load(thread_id="project-123")
# Returns all project context
```

### 6. HITL via Messaging Channels

Deer-Flow supports multiple channels for human interaction:

```yaml
# config.yaml
channels:
  slack:
    enabled: true
    bot_token: $SLACK_BOT_TOKEN
    app_token: $SLACK_APP_TOKEN
    
  telegram:
    enabled: true
    bot_token: $TELEGRAM_BOT_TOKEN
```

**For LEED Platform:**
- LEED consultant gets Slack notification when review needed
- Clicks approve/reject with comments
- Workflow automatically resumes
- All interactions logged

---

## What We Need to Build on Top

### 1. LEED-Specific Skills (16 Skills)

Convert our SKILL.md files to Deer-Flow format:

```markdown
# /mnt/skills/leed/ip-p3-carbon/SKILL.md
---
name: ip-p3-carbon-assessment
version: 1.0.0
author: LEED Platform Team
description: |
  Calculate 25-year carbon projection including operational,
  refrigerant, and embodied carbon sources.
---

## Inputs
```json
{
  "project_location": {"lat": 40.7128, "lon": -74.0060},
  "energy_model_output": {"electricity_kwh": 500000, ...},
  "material_quantities": [{"name": "Concrete", "quantity": 1000, "unit": "m3"}],
  "service_life": 25
}
```

## Workflow
1. [AGENT] Validate inputs using validation schema
2. [TOOL:web_search] Fetch grid emission factors from EPA eGRID
3. [TOOL:web_search] Fetch embodied carbon from EC3 Database
4. [AGENT:carbon_calculator] Calculate operational carbon
5. [AGENT:carbon_calculator] Calculate refrigerant emissions
6. [AGENT:carbon_calculator] Calculate embodied carbon
7. [AGENT:report_generator] Generate 25-year projection
8. [HITL] Send to LEED consultant for review
9. [AGENT:report_generator] Finalize PDF/Excel outputs

## HITL Configuration
```yaml
hitl_points:
  - step: 8
    assignee_role: leed_consultant
    sla_hours: 24
    notification_channels: [slack, email]
    checklist:
      - Energy model inputs verified
      - Material quantities accurate
      - Grid factors appropriate
```

## Output
```json
{
  "documents": {
    "pdf_report": "/outputs/carbon_projection.pdf",
    "excel_workbook": "/outputs/carbon_calculations.xlsx"
  },
  "calculations": {
    "operational_co2": 1250000,
    "refrigerant_co2": 50000,
    "embodied_co2": 800000,
    "total_25yr_co2": 2100000
  }
}
```
```

### 2. API Integration Layer

Deer-Flow has web search/fetch tools. We need to add LEED-specific API tools:

```python
# /backend/deerflow/tools/leed_apis.py

from deerflow.tools.base import BaseTool

class EPAeGRIDTool(BaseTool):
    """Fetch grid emission factors from EPA eGRID"""
    name = "epa_egrid"
    description = "Get CO2 emission factors by US grid region"
    
    async def run(self, region: str) -> dict:
        # Call EPA eGRID API
        return {"co2_factor": 0.0005, "source": "EPA eGRID 2023"}

class EC3DatabaseTool(BaseTool):
    """Query Building Transparency EC3 Database"""
    name = "ec3_database"
    description = "Get embodied carbon data for construction materials"
    
    async def run(self, material_name: str) -> dict:
        # Call EC3 API
        return {"gwp_per_kg": 0.25, "category": "Concrete"}

class USGBCArcTool(BaseTool):
    """Submit documents to USGBC Arc platform"""
    name = "usgbc_arc"
    description = "Submit credit documentation to LEED Online"
    
    async def run(self, project_id: str, credit_code: str, documents: list) -> dict:
        # Call USGBC Arc API
        return {"submission_id": "SUB-12345", "status": "submitted"}
```

### 3. Document Templates

Deer-Flow's report generation skill can be customized:

```python
# /mnt/skills/leed/templates/ip-p3-carbon-report.html

<!DOCTYPE html>
<html>
<head>
    <title>Carbon Assessment - {{ project_id }}</title>
    <style>
        /* LEED-compliant styling */
    </style>
</head>
<body>
    <h1>25-Year Carbon Projection</h1>
    
    <h2>Executive Summary</h2>
    <p>Total 25-year CO2e: {{ total_25yr_co2 | number_format }} kg</p>
    
    <h2>Emission Sources</h2>
    <table>
        <tr>
            <td>Operational Carbon</td>
            <td>{{ operational_co2 | number_format }} kg</td>
            <td>{{ (operational_co2 / total_25yr_co2 * 100) | round(1) }}%</td>
        </tr>
        <tr>
            <td>Refrigerant Emissions</td>
            <td>{{ refrigerant_co2 | number_format }} kg</td>
            <td>{{ (refrigerant_co2 / total_25yr_co2 * 100) | round(1) }}%</td>
        </tr>
        <tr>
            <td>Embodied Carbon</td>
            <td>{{ embodied_co2 | number_format }} kg</td>
            <td>{{ (embodied_co2 / total_25yr_co2 * 100) | round(1) }}%</td>
        </tr>
    </table>
    
    <h2>Top 3 Carbon Hotspots</h2>
    {% for hotspot in top_3_hotspots %}
    <p>{{ loop.index }}. {{ hotspot.material }}: {{ hotspot.co2 | number_format }} kg</p>
    {% endfor %}
    
    <h2>Decarbonization Pathway</h2>
    <!-- AI-generated recommendations -->
    {{ decarbonization_recommendations | markdown }}
</body>
</html>
```

### 4. Regional Data Availability Filter

Add middleware to filter skills by region:

```python
# /backend/deerflow/middleware/regional_filter.py

class RegionalSkillFilter:
    """Filter skills based on regional data availability"""
    
    def __init__(self, project_location):
        self.region = self.detect_region(project_location)
    
    def filter_available_skills(self, skills: list) -> list:
        """Return only skills available for this region"""
        available = []
        for skill in skills:
            if self.is_skill_available(skill):
                available.append(skill)
            else:
                available.append({
                    **skill,
                    "disabled": True,
                    "reason": f"Data not available in {self.region}"
                })
        return available
    
    def is_skill_available(self, skill) -> bool:
        """Check if skill's required APIs are available in region"""
        required_apis = skill.metadata.get("required_apis", [])
        for api in required_apis:
            if not api.available_in(self.region):
                return False
        return True
```

### 5. HITL Dashboard

Build a web UI for HITL reviews (Deer-Flow provides messaging channels):

```typescript
// /frontend/src/components/HITLReview.tsx

interface HITLTask {
  id: string;
  project_id: string;
  skill_name: string;
  document_url: string;
  checklist: string[];
  sla_expires: Date;
}

const HITLReview: React.FC<{ task: HITLTask }> = ({ task }) => {
  const [checklist, setChecklist] = useState<Record<string, boolean>>({});
  const [comments, setComments] = useState("");
  
  const handleApprove = async () => {
    await api.post(`/hitl/${task.id}/approve`, {
      checklist,
      comments
    });
    // Workflow automatically resumes
  };
  
  const handleReject = async () => {
    await api.post(`/hitl/${task.id}/reject`, {
      comments,
      returnToStep: identifyStepFromComments(comments)
    });
  };
  
  return (
    <div className="hitl-review">
      <DocumentViewer url={task.document_url} />
      
      <Checklist
        items={task.checklist}
        onChange={setChecklist}
      />
      
      <textarea
        placeholder="Comments..."
        value={comments}
        onChange={(e) => setComments(e.target.value)}
      />
      
      <div className="actions">
        <button onClick={handleApprove}>Approve</button>
        <button onClick={handleReject}>Request Changes</button>
      </div>
      
      <SLACountdown expires={task.sla_expires} />
    </div>
  );
};
```

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LEED v5 Automation Platform                  │
│                     (Built on Deer-Flow)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Frontend   │  │   Gateway    │  │  LangGraph   │          │
│  │   (React)    │◄─┤    API       │◄─┤   Server     │          │
│  │              │  │              │  │              │          │
│  │ - Credit     │  │ - Auth       │  │ - Workflow   │          │
│  │   selection  │  │ - Routing    │  │   engine     │          │
│  │ - HITL UI    │  │ - HITL       │  │ - State      │          │
│  │ - Dashboard  │  │   webhooks   │  │   management │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                 │                   │
│         └─────────────────┴─────────────────┘                   │
│                           │                                      │
│                    ┌──────┴──────┐                              │
│                    │   Sandbox   │                              │
│                    │  (Docker)   │                              │
│                    │             │                              │
│                    │ /mnt/skills │                              │
│                    │ /mnt/user-data│                            │
│                    └──────┬──────┘                              │
│                           │                                      │
│  ┌────────────────────────┼────────────────────────┐            │
│  │                   SKILLS                        │            │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │            │
│  │  │ IP-p3   │ │ WE-p2   │ │ EA-c3   │ ...      │            │
│  │  │ Carbon  │ │ Water   │ │ Energy  │          │            │
│  │  └─────────┘ └─────────┘ └─────────┘          │            │
│  └────────────────────────────────────────────────┘            │
│                                                                  │
│  ┌────────────────────────────────────────────────┐            │
│  │              EXTERNAL APIs                      │            │
│  │  EPA eGRID │ EC3 │ USGBC Arc │ NOAA │ ...      │            │
│  └────────────────────────────────────────────────┘            │
│                                                                  │
│  ┌────────────────────────────────────────────────┐            │
│  │              HITL CHANNELS                      │            │
│  │  Slack │ Email │ Web UI │ Telegram             │            │
│  └────────────────────────────────────────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan Using Deer-Flow

### Phase 1: Setup Deer-Flow (Day 1-2)

```bash
# Clone Deer-Flow
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow

# Run setup wizard
make setup
# Configure: OpenAI API, optional web search

# Configure for LEED platform
cat > config.yaml << EOF
models:
  - name: gpt-4o
    display_name: GPT-4o
    use: langchain_openai:ChatOpenAI
    model: gpt-4o
    api_key: $OPENAI_API_KEY

sandbox:
  use: deerflow.community.aio_sandbox:AioSandboxProvider
  provisioner_url: http://localhost:8080

channels:
  slack:
    enabled: true
    bot_token: $SLACK_BOT_TOKEN
    app_token: $SLACK_APP_TOKEN
EOF

# Start services
make docker-start
```

### Phase 2: Create LEED Skills (Day 3-10)

```bash
# Create skill directory structure
mkdir -p skills/leed/{ip-p3,ea-p1,we-p2,ea-p2,ea-p5,mr-p2,ea-c3,we-c2,mr-c2,lt-c3,ss-c3,ea-c7,ss-c5,ss-c6,pr-c2,lt-c1}

# For each skill, create SKILL.md
# (Use our existing SKILL.md files, convert to Deer-Flow format)
```

### Phase 3: Build API Integration Layer (Day 8-12)

```python
# Create LEED-specific tools
# /backend/deerflow/tools/leed/

# - epa_egrid.py
# - ec3_database.py
# - usgbc_arc.py
# - noaa_climate.py
# - ... (36 API integrations)
```

### Phase 4: Build HITL Dashboard (Day 11-14)

```typescript
// Extend Deer-Flow frontend with LEED-specific components

// - Credit selection wizard
// - Regional availability filter
// - HITL review interface
// - Project dashboard
// - USGBC submission portal
```

---

## Benefits of Using Deer-Flow

| Feature | Build from Scratch | Use Deer-Flow | Time Saved |
|---------|-------------------|---------------|------------|
| Skill system | 2 weeks | ✅ Included | 2 weeks |
| Durable workflows | 2 weeks | ✅ LangGraph | 2 weeks |
| Sandbox execution | 1 week | ✅ Docker | 1 week |
| Memory system | 1 week | ✅ Built-in | 1 week |
| HITL channels | 1 week | ✅ Slack/Telegram | 1 week |
| Sub-agent orchestration | 2 weeks | ✅ Built-in | 2 weeks |
| Web UI | 2 weeks | ✅ Included | 2 weeks |
| API gateway | 1 week | ✅ Included | 1 week |
| **Total** | **12 weeks** | **2 weeks** | **10 weeks** |

**Net result:** We can build the LEED platform in **2-3 weeks** instead of **3-4 months**.

---

## Customization Required

### 1. LEED-Specific Skills (16 skills)
- Convert our SKILL.md files to Deer-Flow format
- ~1 week with 2 developers

### 2. API Integration Layer (36 APIs)
- Create tools for EPA eGRID, EC3, USGBC Arc, etc.
- ~3 days with 1 developer

### 3. Document Templates
- Create Jinja2 templates for each credit
- ~2 days with 1 developer

### 4. Regional Filtering
- Add middleware to filter by region
- ~1 day

### 5. HITL Dashboard Enhancements
- Add LEED-specific review checklists
- ~2 days

**Total customization: ~2 weeks**

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Deer-Flow too complex | Start with basic skills, add complexity gradually |
| LangGraph learning curve | Deer-Flow abstracts most of it |
| Customization limitations | Deer-Flow is extensible, can fork if needed |
| Community support | 60.2k stars, active development |

---

## Recommendation

**Use Deer-Flow as the foundation.** It provides:

1. ✅ Skill-based architecture (matches our design)
2. ✅ Durable workflows (LangGraph)
3. ✅ Sandbox execution (Docker)
4. ✅ Memory system
5. ✅ HITL channels (Slack, Telegram)
6. ✅ Sub-agent orchestration
7. ✅ Web UI
8. ✅ API gateway

**We build on top:**
1. LEED-specific skills (16 credits)
2. API integration layer (36 APIs)
3. Document templates
4. Regional filtering
5. HITL dashboard enhancements

**Timeline:**
- **MVP with 8 credits:** 2 weeks
- **All 16 credits:** 3 weeks
- **Production ready:** 4 weeks

**vs. building from scratch:**
- **MVP:** 8 weeks
- **All 16 credits:** 12 weeks
- **Production ready:** 16 weeks

**Time saved: 12 weeks (75% reduction)**

---

## Next Steps

1. **Clone Deer-Flow** and run locally
2. **Create first LEED skill** (PRc2 - LEED AP, simplest)
3. **Test end-to-end** workflow
4. **Validate HITL** via Slack
5. **Build remaining 15 skills** in parallel
6. **Deploy to production**

---

## Resources

- **Deer-Flow GitHub:** https://github.com/bytedance/deer-flow
- **Official Website:** https://deerflow.tech
- **Documentation:** https://github.com/bytedance/deer-flow/tree/main/docs
- **Skills Directory:** https://github.com/bytedance/deer-flow/tree/main/skills/public

---

*Analysis Date: March 21, 2026*
*Deer-Flow Version: 2.0*
