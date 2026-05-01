# Agent Architecture

## Overview

The LEED AI Platform uses a multi-agent system built on Deer-Flow for orchestrating credit automation workflows.

## Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                      LEAD AGENT                                  │
│              (Orchestrates project-level tasks)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  CREDIT AGENT 1 │ │  CREDIT AGENT 2 │ │  CREDIT AGENT N │
│   (IPp3 Carbon) │ │   (WEp2 Water)  │ │    (etc.)       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                     SUB-AGENTS                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Data     │ │ Calc     │ │ Report   │ │ Review   │       │
│  │ Extractor│ │ Engine   │ │ Generator│ │ Checker  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Agent Types

### 1. Lead Agent

**Purpose:** Project-level orchestration and coordination.

**Responsibilities:**
- Initialize credit agents in parallel
- Aggregate results
- Handle project-level decisions
- Manage user communication

**Tools:**
- `spawn_credit_agent` - Start a credit-specific agent
- `aggregate_results` - Combine multiple credit results
- `notify_user` - Send notifications

### 2. Credit Agents (16 total)

One agent per LEED credit. Each implements the complete workflow for that credit.

**Structure:**
```python
class CreditAgent:
    """Base class for all credit agents"""
    
    credit_code: str
    credit_name: str
    automation_level: int
    
    async def execute(self, inputs: dict) -> dict:
        """Execute the complete credit workflow"""
        pass
    
    async def validate_inputs(self, inputs: dict) -> ValidationResult:
        """Validate required inputs"""
        pass
    
    async def fetch_data(self, inputs: dict) -> dict:
        """Fetch data from external APIs"""
        pass
    
    async def calculate(self, data: dict) -> dict:
        """Perform calculations"""
        pass
    
    async def generate_documents(self, results: dict) -> dict:
        """Generate PDF/Excel documents"""
        pass
```

### 3. Sub-Agents

Specialized agents for specific tasks.

#### Data Extractor Agent
**Purpose:** Parse uploaded files and extract structured data.

**Tools:**
- `parse_energy_model` - Extract from EnergyPlus, IES, Trace
- `parse_excel` - Read Excel tables
- `parse_pdf` - Extract text and tables from PDFs
- `parse_cad` - Interface with AutoCAD API

#### Calculation Engine Agent
**Purpose:** Perform mathematical calculations.

**Tools:**
- `calculate_carbon` - Carbon emission formulas
- `calculate_water` - Water efficiency formulas
- `calculate_energy` - Energy performance formulas
- `unit_convert` - Convert between units

#### Report Generator Agent
**Purpose:** Generate documents from templates.

**Tools:**
- `render_template` - Fill Jinja2 templates
- `generate_pdf` - Convert HTML to PDF
- `generate_excel` - Create Excel workbooks
- `generate_charts` - Create data visualizations

#### Review Checker Agent
**Purpose:** Validate outputs before HITL.

**Tools:**
- `check_completeness` - Verify all required sections
- `check_calculations` - Validate math
- `check_formatting` - Ensure USGBC compliance

## Workflow Orchestration

### Durable Workflow Pattern

```python
from deerflow import Agent, step, hitl_checkpoint

class IPp3CarbonAgent(Agent):
    """Carbon Assessment credit agent"""
    
    credit_code = "IPp3"
    credit_name = "Carbon Assessment"
    
    @step(name="validate", retry=1)
    async def validate_inputs(self, context):
        """Step 1: Validate all required inputs"""
        validation = self.validate_schema(context.inputs)
        if not validation.valid:
            raise ValueError(f"Invalid inputs: {validation.errors}")
        return validation
    
    @step(name="fetch_grid", retry=3, timeout=30)
    async def fetch_grid_factors(self, context):
        """Step 2: Fetch grid emission factors"""
        location = context.inputs['project_location']
        
        if is_us_location(location):
            data = await self.tools.epa_egrid.get_factors(location)
        else:
            data = await self.tools.national_grid.get_factors(location)
        
        return {'grid_factors': data}
    
    @step(name="fetch_ec3", retry=3, timeout=60)
    async def fetch_embodied_carbon(self, context):
        """Step 3: Fetch embodied carbon from EC3"""
        materials = context.inputs['material_quantities']
        
        results = []
        for material in materials:
            ec3_data = await self.tools.ec3_database.search(material['name'])
            results.append({
                'material': material,
                'gwp_per_unit': ec3_data['gwp'],
                'total_gwp': material['quantity'] * ec3_data['gwp']
            })
        
        return {'embodied_carbon': results}
    
    @step(name="calculate_operational", retry=1)
    async def calculate_operational(self, context):
        """Step 4: Calculate operational carbon"""
        energy = context.inputs['energy_model_output']
        grid = context.step_results['fetch_grid']['grid_factors']
        
        annual_co2 = (
            energy['electricity_kwh'] * grid['co2_factor'] +
            energy['natural_gas_therms'] * 0.0053 +
            energy['steam_mmbtu'] * 66.3
        )
        
        return {
            'annual_operational_co2': annual_co2,
            '25yr_operational_co2': annual_co2 * 25
        }
    
    @step(name="calculate_embodied", retry=1)
    async def calculate_embodied(self, context):
        """Step 5: Calculate embodied carbon"""
        materials = context.step_results['fetch_ec3']['embodied_carbon']
        
        total = sum(item['total_gwp'] for item in materials)
        top_3 = sorted(materials, key=lambda x: x['total_gwp'], reverse=True)[:3]
        
        return {
            'embodied_co2': total,
            'top_3_hotspots': top_3
        }
    
    @step(name="generate_projection", retry=1)
    async def generate_projection(self, context):
        """Step 6: Generate 25-year projection"""
        operational = context.step_results['calculate_operational']
        embodied = context.step_results['calculate_embodied']
        
        total = (
            operational['25yr_operational_co2'] +
            embodied['embodied_co2']
        )
        
        return {
            'operational': operational['25yr_operational_co2'],
            'embodied': embodied['embodied_co2'],
            'total_25yr_co2': total
        }
    
    @step(name="generate_report", retry=2)
    async def generate_report(self, context):
        """Step 7: Generate documents"""
        projection = context.step_results['generate_projection']
        
        # Generate PDF report
        pdf = await self.tools.report_generator.render_pdf(
            template='ip-p3-carbon-report.html',
            data=projection
        )
        
        # Generate Excel workbook
        excel = await self.tools.report_generator.render_excel(
            template='ip-p3-carbon-workbook.xlsx',
            data=projection
        )
        
        return {
            'pdf_url': pdf.url,
            'excel_url': excel.url,
            'projection': projection
        }
    
    @hitl_checkpoint(
        name="human_review",
        assignee_role="leed_consultant",
        sla_hours=24,
        instructions="""
        Review the carbon assessment report and verify:
        1. Energy model inputs match project
        2. Material quantities are accurate
        3. Grid emission factors are appropriate
        4. Calculations are reasonable
        5. Top 3 hotspots are correctly identified
        """
    )
    async def human_review(self, context):
        """Step 8: Human review checkpoint"""
        report = context.step_results['generate_report']
        
        # Create HITL task
        task = await self.hitl.create_task(
            document_url=report['pdf_url'],
            checklist=[
                "Energy model inputs verified",
                "Material quantities accurate",
                "Grid factors appropriate",
                "Calculations reasonable",
                "Hotspots identified correctly"
            ]
        )
        
        # Workflow pauses here, resumes when human responds
        result = await self.hitl.wait_for_response(task.id)
        
        if result['action'] == 'approve':
            return {'status': 'approved', 'reviewer': result['reviewer']}
        else:
            return {
                'status': 'rejected',
                'comments': result['comments'],
                'return_to_step': result['return_to_step']
            }
    
    @step(name="finalize", retry=1)
    async def finalize(self, context):
        """Step 9: Finalize output"""
        review = context.step_results['human_review']
        report = context.step_results['generate_report']
        
        if review['status'] != 'approved':
            raise ValueError("Review not approved")
        
        # Generate final USGBC submission form
        usgbc_form = await self.tools.report_generator.render_pdf(
            template='ip-p3-usgbc-form.html',
            data=report['projection']
        )
        
        return {
            'status': 'completed',
            'documents': {
                'pdf_report': report['pdf_url'],
                'excel_workbook': report['excel_url'],
                'usgbc_form': usgbc_form.url
            },
            'calculations': report['projection'],
            'review_record': review
        }
```

## Tool Registry

### External API Tools

```python
# agents/tools/external_apis.py

class EPAeGRIDTool(Tool):
    """Fetch grid emission factors from EPA eGRID"""
    name = "epa_egrid"
    
    async def run(self, location: dict) -> dict:
        """Get CO2 emission factors by region"""
        response = await self.http.get(
            "https://www.epa.gov/egrid/api/factors",
            params={"lat": location["lat"], "lng": location["lng"]}
        )
        return response.json()

class EC3DatabaseTool(Tool):
    """Query Building Transparency EC3 Database"""
    name = "ec3_database"
    
    async def search(self, material_name: str) -> dict:
        """Search for material GWP data"""
        response = await self.http.get(
            "https://buildingtransparency.org/api/v2/materials",
            params={"query": material_name}
        )
        return response.json()

class USGBCArcTool(Tool):
    """Submit documents to USGBC Arc platform"""
    name = "usgbc_arc"
    
    async def submit(self, project_id: str, credit_code: str, documents: list) -> dict:
        """Submit credit documentation"""
        response = await self.http.post(
            f"https://www.usgbc.org/arc/api/projects/{project_id}/credits/{credit_code}/submit",
            json={"documents": documents}
        )
        return response.json()
```

### Document Generation Tools

```python
# agents/tools/document_generation.py

class ReportGeneratorTool(Tool):
    """Generate PDF and Excel documents"""
    name = "report_generator"
    
    async def render_pdf(self, template: str, data: dict) -> Document:
        """Render HTML template to PDF"""
        # Load template
        template_content = await self.load_template(template)
        
        # Render with Jinja2
        html = self.jinja2.render(template_content, data)
        
        # Convert to PDF
        pdf = await self.pdf_engine.render(html)
        
        # Upload to storage
        url = await self.storage.upload(pdf, f"reports/{uuid()}.pdf")
        
        return Document(url=url, format="pdf")
    
    async def render_excel(self, template: str, data: dict) -> Document:
        """Render Excel workbook from template"""
        # Load template
        workbook = await self.load_excel_template(template)
        
        # Fill data
        for sheet_name, sheet_data in data.items():
            workbook[sheet_name].fill(sheet_data)
        
        # Save and upload
        url = await self.storage.upload(workbook, f"workbooks/{uuid()}.xlsx")
        
        return Document(url=url, format="excel")
```

### Data Extraction Tools

```python
# agents/tools/data_extraction.py

class EnergyModelParserTool(Tool):
    """Parse energy model outputs"""
    name = "energy_model_parser"
    
    async def parse(self, file_path: str, format: str) -> dict:
        """Parse energy model based on format"""
        parsers = {
            "energyplus": self._parse_energyplus,
            "ies": self._parse_ies,
            "trace": self._parse_trace,
            "equest": self._parse_equest
        }
        
        parser = parsers.get(format)
        if not parser:
            raise ValueError(f"Unsupported format: {format}")
        
        return await parser(file_path)
    
    async def _parse_energyplus(self, file_path: str) -> dict:
        """Parse EnergyPlus HTML output"""
        html = await self.files.read(file_path)
        tables = self.html_parser.extract_tables(html)
        
        return {
            "electricity_kwh": self._extract_value(tables, "Electricity", "Total"),
            "natural_gas_therms": self._extract_value(tables, "Natural Gas", "Total"),
            "steam_mmbtu": self._extract_value(tables, "Steam", "Total")
        }
```

## Memory System

### Project Memory

```python
# agents/memory/project_memory.py

class ProjectMemory:
    """Persistent memory for project context"""
    
    async def save(self, project_id: str, facts: list):
        """Save project facts to memory"""
        await self.db.execute("""
            INSERT INTO project_memories (project_id, facts)
            VALUES ($1, $2)
            ON CONFLICT (project_id) DO UPDATE
            SET facts = $2, updated_at = NOW()
        """, project_id, json.dumps(facts))
    
    async def load(self, project_id: str) -> list:
        """Load project facts from memory"""
        result = await self.db.fetchrow("""
            SELECT facts FROM project_memories
            WHERE project_id = $1
        """, project_id)
        
        return json.loads(result["facts"]) if result else []
    
    async def add_fact(self, project_id: str, fact: str):
        """Add a single fact to project memory"""
        facts = await self.load(project_id)
        facts.append(fact)
        await self.save(project_id, facts)
```

### Usage in Agents

```python
@step(name="initialize")
async def initialize(self, context):
    """Load project memory at start"""
    project_id = context.inputs['project_id']
    
    # Load existing facts
    facts = await self.memory.load(project_id)
    
    # Add to context for all subsequent steps
    context.project_facts = facts
    
    return {'initialized': True}
```

## Error Handling

### Retry Strategy

```python
@step(name="fetch_data", retry=3, timeout=30)
async def fetch_data(self, context):
    """Step with retry logic"""
    try:
        return await self.tools.api.call()
    except APITimeout:
        # Will retry automatically
        raise
    except APIError as e:
        # Log and raise
        self.logger.error(f"API error: {e}")
        raise
```

### Fallback Strategy

```python
@step(name="fetch_grid", retry=3)
async def fetch_grid_factors(self, context):
    """Step with fallback"""
    location = context.inputs['project_location']
    
    try:
        # Try primary API
        data = await self.tools.epa_egrid.get_factors(location)
        return {'grid_factors': data, 'source': 'EPA eGRID'}
    except APIError:
        # Fallback to national source
        data = await self.tools.national_grid.get_factors(location)
        return {'grid_factors': data, 'source': 'National Grid'}
```

## Monitoring & Observability

### Agent Metrics

```python
# Track agent performance
agent_metrics = {
    "credit_code": "IPp3",
    "workflow_id": "wf-123",
    "steps_completed": 7,
    "steps_total": 9,
    "api_calls": 12,
    "api_errors": 0,
    "duration_seconds": 45.2,
    "hitl_wait_seconds": 3600
}
```

### Logging

```python
# Structured logging for each step
logger.info("Step completed", extra={
    "workflow_id": context.workflow_id,
    "step_name": "fetch_grid",
    "duration_ms": 1250,
    "api_calls": 1,
    "success": True
})
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
