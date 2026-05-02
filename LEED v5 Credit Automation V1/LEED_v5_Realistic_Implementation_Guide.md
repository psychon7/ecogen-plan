# LEED v5 AI Automation Platform - Realistic Implementation Guide

## Executive Summary: The Honest Assessment

This document provides a **realistic, executable plan** for building a LEED v5 automation platform based on **current AI capabilities** (May 2026). It includes agentic workflow patterns, HITL (Human-in-the-Loop) design, durable workflows, and a skill-based architecture.

### The Reality Check

**What AI Can Do Well (90%+ reliability):**
- Generate documents from structured templates
- Integrate with documented APIs
- Perform calculations with clear formulas
- Validate data against rules
- Route workflows based on conditions

**What AI Cannot Do Reliably:**
- Interpret complex CAD/site plans without human assistance
- Make final compliance decisions
- Handle edge cases without guidance
- Verify accuracy of external data
- Work autonomously without oversight

**The Honest Automation Potential:**
- **90%+ draft automation** only for narrow, deterministic workflows with verified data sources and final review.
- **50-85% automation** for most commercially useful LEED workflows after project teams provide source inputs.
- **Assist-only** for energy modeling, physical testing, field verification, WBLCA execution, and final compliance judgment.
- **Kimi-aligned MVP:** launch suites before broad catalog breadth: WEp2+WEc2, EAp5+EAc7, EQp1+EQp2, IPp1+IPp2, and MRc3.

---

## Part 1: AI Capability Deep Dive

### 1.1 Document Generation - HIGH Capability (95% confidence)

**What Works:**
```python
# AI excels at this:
- Template filling with structured data
- Formatting documents per specifications
- Generating narrative sections from data
- Creating tables and charts
```

**Limitations:**
- Cannot verify if data is correct
- May reference wrong regulation versions
- Needs explicit template structure
- Compliance claims need human verification

**Best Practice:**
```python
def generate_credit_document(template_path, data, validation_rules):
    """
    HITL Checkpoint 1: AI generates draft
    HITL Checkpoint 2: Human reviews compliance claims
    HITL Checkpoint 3: Human approves for submission
    """
    # AI generates from template
    draft = llm.fill_template(template_path, data)
    
    # AI validates against rules
    validation = validate_against_rules(draft, validation_rules)
    
    # Return for human review
    return {
        'draft': draft,
        'validation': validation,
        'status': 'awaiting_human_review',
        'confidence_score': calculate_confidence(data, validation)
    }
```

### 1.2 Data Extraction - MEDIUM-HIGH Capability (85% confidence)

**What Works:**
```python
# AI can extract from:
- Structured PDFs (forms, tables)
- Excel/CSV files
- Text documents with clear structure
- Simple images with text
```

**What Doesn't Work:**
```python
# AI struggles with:
- Complex CAD drawings with layers
- Site plans requiring spatial reasoning
- Handwritten notes
- Multi-page complex tables
- Documents with mixed orientations
```

**The Solution - Pre-Processing Pipeline:**
```python
def extract_data_from_document(file_path, doc_type):
    """
    Break down complex extraction into steps
    """
    if doc_type == 'site_plan':
        # Step 1: Use specialized CAD tools (AutoCAD API, not AI)
        cad_data = extract_cad_data(file_path)
        
        # Step 2: AI processes extracted structured data
        summary = llm.summarize_cad_data(cad_data)
        
        # Step 3: Human verifies critical measurements
        return {'data': cad_data, 'summary': summary, 'needs_verification': True}
    
    elif doc_type == 'energy_model':
        # Step 1: Parse structured output (CSV/XML)
        raw_data = parse_energy_model(file_path)
        
        # Step 2: AI validates completeness
        validation = llm.validate_energy_data(raw_data)
        
        return {'data': raw_data, 'validation': validation}
```

### 1.3 Image/Multimodal Analysis - MEDIUM Capability (70% confidence)

**The Hard Truth About Site Plans:**

GPT-4 Vision and similar models **cannot reliably**:
- Read precise measurements from CAD drawings
- Calculate areas from scaled drawings
- Interpret complex site features
- Understand building codes from visual context

**What They CAN Do:**
- Identify general features (building, parking, landscape)
- Read text labels on plans
- Detect anomalies (missing elements)
- Summarize what's visible

**The Proper Approach:**
```python
class SitePlanProcessor:
    """
    Hybrid approach: Tools + AI + Human
    """
    def process_site_plan(self, image_path):
        # Step 1: Use computer vision for basic extraction
        cv_results = self.computer_vision.extract(image_path)
        
        # Step 2: Use specialized tools for measurements
        if self.has_cad_file(image_path):
            measurements = self.cad_tool.extract_measurements(self.get_cad_file())
        else:
            # No CAD - flag for manual entry
            measurements = {'status': 'manual_entry_required'}
        
        # Step 3: AI generates summary from structured data
        ai_summary = llm.generate_site_summary(cv_results, measurements)
        
        # Step 4: Human verifies and corrects
        return {
            'cv_data': cv_results,
            'measurements': measurements,
            'ai_summary': ai_summary,
            'verification_required': True,
            'confidence': 'medium' if measurements else 'low'
        }
```

### 1.4 Calculation Automation - HIGH Capability (90% confidence)

**What Works:**
```python
# AI can implement:
- Formula-based calculations
- Unit conversions
- Percentage calculations
- Comparison to baselines
- Points determination
```

**Critical Requirement - Explicit Formulas:**
```python
# GOOD - Clear formula
def calculate_water_reduction(baseline, proposed):
    """
    Formula: (Baseline - Proposed) / Baseline * 100
    """
    return ((baseline - proposed) / baseline) * 100

# BAD - Asking AI to "figure it out"
def calculate_water_reduction_vague(inputs):
    """
    DON'T: Ask AI to determine the formula
    """
    return llm.calculate_reduction(inputs)  # Unreliable!
```

---

## Part 2: Skill-Based Architecture

### 2.1 Each Credit = One Skill

Following the skill.md standard, each LEED credit becomes a modular skill:

```
skills/
├── we_p2_water_min/
│   ├── SKILL.md          # Credit contract
│   ├── agent.py          # Durable workflow implementation
│   ├── calculations.py   # Baseline/design water formulas
│   ├── templates/        # Evidence pack templates
│   └── tests/            # Unit, HITL, regional fallback tests
├── we_c2_water_enhanced/
│   └── ...               # Consumes WEp2 normalized fixture data
├── ea_p5_refrigerant/
├── ea_c7_refrigerant/
├── eq_p1_construction_management/      # to create
├── eq_p2_fundamental_air_quality/      # to create
├── ip_p1_climate_resilience/           # to create
├── ip_p2_human_impact/                 # to create
├── mr_c3_low_emitting_materials/       # to create
└── assisted_catalog/                   # existing generated skill drafts
```

### 2.2 Skill Structure

Each skill has:

**SKILL.md** - The Contract:
```markdown
# Skill: WEp2 Minimum Water Efficiency

## Purpose
Calculate baseline versus design indoor water use, verify the prerequisite reduction, and produce a reviewer-ready evidence pack that can feed WEc2.

## Automation Level
- Calculation: 95% automated once fixture and occupancy data are normalized
- Document Generation: 90% automated
- Data Retrieval/Product Matching: 70-85% depending on WaterSense/ENERGY STAR coverage and fixture schedule quality
- **Overall: 85-90% draft automation with human review**

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| fixture_schedule | file/table | Upload or manual entry | Fixture type, quantity, flow/flush rate |
| occupancy_counts | object | Project team | FTE, visitors, gender ratio assumptions |
| operating_days | integer | Project team | Positive annual value |
| building_type | string | Project intake | Supported default usage pattern |

## Inputs (Optional)
| Field | Type | Default |
|-------|------|---------|
| product_cut_sheets | files | None |
| watersense_lookup | boolean | true |
| reviewer_email | string | Project LEED reviewer |

## Workflow (Durable - Resumable)
1. **validate_inputs** - Check all required data present
2. **parse_fixture_schedule** - Normalize structured upload or manual table
3. **verify_product_data** - Optional WaterSense/ENERGY STAR lookup with fallback flags
4. **calculate_baseline** - Apply versioned LEED v5 baseline rates
5. **calculate_design** - Apply proposed fixture rates and usage assumptions
6. **calculate_reduction** - Compare to prerequisite threshold
7. **generate_evidence_pack** - PDF, XLSX, source index, formula trail
8. **HITL_REVIEW** - Human confirms fixture schedule, occupancy, and results
9. **finalize_output** - Generate approved package and WEc2 handoff data

## HITL Checkpoints
| Step | Who | Action | SLA |
|------|-----|--------|-----|
| After calculation package | LEED Consultant | Verify fixture schedule, occupancy assumptions, and reduction result | 24 hours |
| If product lookup fails | Project team | Upload cut sheet or manually confirm flow/flush rate | 48 hours |

## Outputs
| Document | Format | Description |
|----------|--------|-------------|
| water_efficiency_report | PDF | Methodology, inputs, baseline/design summary, pass/fail status |
| calculation_workbook | XLSX | Transparent formulas and intermediate values |
| source_index | JSON/PDF | Uploads, API lookups, assumptions, reviewer changes |
| wec2_handoff | JSON | Normalized fixture/occupancy data for enhanced water workflow |

## API Dependencies
| API | Purpose | Regional Availability | Fallback |
|-----|---------|----------------------|----------|
| EPA WaterSense | Fixture certification support | US-centric/global product access varies | Manual cut sheet verification |
| ENERGY STAR | Appliance verification | US-centric | Manufacturer documentation |
| Project uploads | Primary fixture source | Global | Manual table entry |

## Error Handling
| Error | Action | Retry |
|-------|--------|-------|
| API timeout | Retry 3x with backoff | Auto |
| Invalid coordinates | Prompt user for correction | Manual |
| Missing material data | Flag for manual entry | Manual |
| Calculation mismatch | Alert human reviewer | Manual |

## Testing
```bash
# Run skill tests
python -m pytest skills/we_p2_water_min/tests/

# Run integration test
python skills/we_p2_water_min/agent.py --test-mode
```
```

### 2.3 Agent Implementation

```python
# skills/ip_p3_carbon_assessment/agent.py
from durable_workflows import DurableOrchestrator, step
from hitl import HITLCheckpoint
from validations import validate_inputs, validate_calculations

class CarbonAssessmentSkill:
    """
    Durable, resumable workflow for IPp3 Carbon Assessment
    """
    
    def __init__(self, project_id, inputs):
        self.project_id = project_id
        self.inputs = inputs
        self.orchestrator = DurableOrchestrator()
        self.hitl = HITLCheckpoint()
    
    @step(name="validate_inputs", retry=3)
    async def validate_inputs(self):
        """Step 1: Validate all required inputs"""
        validation = validate_inputs(self.inputs)
        if not validation.valid:
            raise ValueError(f"Invalid inputs: {validation.errors}")
        return validation
    
    @step(name="fetch_grid_factors", retry=3, timeout=30)
    async def fetch_grid_factors(self, validation):
        """Step 2: Fetch grid emission factors"""
        location = self.inputs['project_location']
        
        # Try EPA eGRID first (US)
        if is_us_location(location):
            data = await epa_egrid_api.get_factors(location)
        else:
            # Fallback to national source
            data = await national_grid_api.get_factors(location)
        
        return {'grid_factors': data}
    
    @step(name="fetch_embodied_carbon", retry=3, timeout=30)
    async def fetch_embodied_carbon(self):
        """Step 3: Fetch embodied carbon data from EC3"""
        materials = self.inputs['material_quantities']
        
        results = []
        for material in materials:
            ec3_data = await ec3_api.search_material(material['name'])
            results.append({
                'material': material,
                'gwp_per_unit': ec3_data['gwp'],
                'total_gwp': material['quantity'] * ec3_data['gwp']
            })
        
        return {'embodied_carbon': results}
    
    @step(name="calculate_operational", retry=1)
    async def calculate_operational(self, grid_factors):
        """Step 4: Calculate operational carbon"""
        energy_data = self.inputs['energy_model_output']
        
        # Python calculation (not AI)
        annual_co2 = (
            energy_data['electricity_kwh'] * grid_factors['co2_factor'] +
            energy_data['natural_gas_therms'] * 0.0053 +
            energy_data['steam_mmbtu'] * 66.3
        )
        
        twenty_five_year = annual_co2 * 25
        
        return {
            'annual_operational_co2': annual_co2,
            '25yr_operational_co2': twenty_five_year
        }
    
    @step(name="calculate_refrigerant", retry=1)
    async def calculate_refrigerant(self):
        """Step 5: Calculate refrigerant emissions"""
        if 'refrigerant_schedule' not in self.inputs:
            return {'refrigerant_co2': 0}
        
        # Python calculation
        refrigerants = self.inputs['refrigerant_schedule']
        total = sum(
            r['charge_kg'] * r['gwp'] * 0.025 * 25  # 2.5% leak rate
            for r in refrigerants
        )
        
        return {'refrigerant_co2': total}
    
    @step(name="calculate_embodied", retry=1)
    async def calculate_embodied(self, embodied_carbon):
        """Step 6: Sum embodied carbon"""
        total = sum(item['total_gwp'] for item in embodied_carbon)
        return {'embodied_co2': total}
    
    @step(name="generate_projection", retry=1)
    async def generate_projection(self, operational, refrigerant, embodied):
        """Step 7: Generate 25-year projection"""
        total = (
            operational['25yr_operational_co2'] +
            refrigerant['refrigerant_co2'] +
            embodied['embodied_co2']
        )
        
        return {
            'operational': operational['25yr_operational_co2'],
            'refrigerant': refrigerant['refrigerant_co2'],
            'embodied': embodied['embodied_co2'],
            'total_25yr_co2': total
        }
    
    @step(name="generate_report", retry=2)
    async def generate_report(self, projection):
        """Step 8: Generate report from template"""
        template = load_template('ip_p3_carbon_report.html')
        
        # Fill template with data
        report_html = template.render(
            project_id=self.project_id,
            projection=projection,
            inputs=self.inputs
        )
        
        # Convert to PDF
        pdf_path = generate_pdf(report_html)
        
        return {'report_path': pdf_path, 'projection': projection}
    
    @hitl_checkpoint(
        name="human_review",
        assignee="leed_consultant",
        sla_hours=24,
        instructions="Review carbon calculations for accuracy. Verify energy model inputs match project. Check material quantities."
    )
    async def human_review(self, report):
        """Step 9: HITL - Human reviews report"""
        # Workflow pauses here, sends notification
        review_result = await self.hitl.request_review(
            project_id=self.project_id,
            document_path=report['report_path'],
            checklist=[
                "Energy model inputs verified",
                "Material quantities accurate",
                "Grid emission factors appropriate",
                "Calculations reasonable"
            ]
        )
        
        if review_result['approved']:
            return {'status': 'approved', 'reviewer': review_result['reviewer']}
        else:
            # Return to appropriate step for corrections
            return {
                'status': 'rejected',
                'corrections_needed': review_result['comments'],
                'return_to_step': review_result['return_to_step']
            }
    
    @step(name="finalize", retry=1)
    async def finalize(self, review_result, report):
        """Step 10: Finalize output"""
        if review_result['status'] != 'approved':
            raise ValueError("Review not approved")
        
        # Generate final documents
        final_pdf = generate_final_pdf(report['report_path'])
        excel_workbook = generate_excel_workbook(report['projection'])
        
        return {
            'status': 'completed',
            'documents': {
                'pdf_report': final_pdf,
                'excel_workbook': excel_workbook
            },
            'review_record': review_result
        }
    
    async def execute(self):
        """Execute the durable workflow"""
        return await self.orchestrator.run([
            self.validate_inputs,
            self.fetch_grid_factors,
            self.fetch_embodied_carbon,
            self.calculate_operational,
            self.calculate_refrigerant,
            self.calculate_embodied,
            self.generate_projection,
            self.generate_report,
            self.human_review,
            self.finalize
        ])
```

---

## Part 3: Durable Workflows

### 3.1 Why Durable Workflows Matter

**Problem:** API calls fail, servers restart, humans take days to review.

**Solution:** Durable workflows that:
- Save state after each step
- Resume from failures
- Handle long-running processes (human review)
- Maintain audit trail

### 3.2 Implementation

```python
# durable_workflows.py
import json
import hashlib
from datetime import datetime
from typing import List, Callable, Any

class DurableOrchestrator:
    """
    Durable workflow engine for credit processing
    """
    
    def __init__(self, storage_path="/data/workflows"):
        self.storage_path = storage_path
    
    async def run(self, steps: List[Callable], workflow_id=None):
        """
        Execute steps with durability
        """
        workflow_id = workflow_id or self.generate_id()
        state = self.load_state(workflow_id)
        
        for i, step in enumerate(steps):
            # Skip completed steps
            if i < state['current_step']:
                continue
            
            try:
                # Execute step
                result = await step(**state['context'])
                
                # Save state
                state['current_step'] = i + 1
                state['context'][step.__name__] = result
                state['completed_at'] = datetime.utcnow().isoformat()
                self.save_state(workflow_id, state)
                
            except Exception as e:
                # Log failure, can resume later
                state['error'] = str(e)
                state['failed_step'] = i
                self.save_state(workflow_id, state)
                raise WorkflowPaused(f"Step {i} failed: {e}")
        
        return state['context']
    
    def load_state(self, workflow_id):
        """Load workflow state from storage"""
        try:
            with open(f"{self.storage_path}/{workflow_id}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return {'current_step': 0, 'context': {}}
    
    def save_state(self, workflow_id, state):
        """Save workflow state"""
        with open(f"{self.storage_path}/{workflow_id}.json", 'w') as f:
            json.dump(state, f)

def step(name, retry=1, timeout=None):
    """Decorator for workflow steps"""
    def decorator(func):
        func._step_name = name
        func._retry = retry
        func._timeout = timeout
        return func
    return decorator
```

---

## Part 4: HITL (Human-in-the-Loop) Design

### 4.1 HITL Checkpoints

Every skill has explicit HITL checkpoints:

```python
class HITLCheckpoint:
    """
    Human-in-the-Loop checkpoint system
    """
    
    async def request_review(self, project_id, document_path, checklist, sla_hours=24):
        """
        Pause workflow, notify human, wait for response
        """
        # Create review task
        review_task = {
            'id': generate_id(),
            'project_id': project_id,
            'document_path': document_path,
            'checklist': checklist,
            'status': 'pending',
            'created_at': datetime.utcnow(),
            'sla_hours': sla_hours
        }
        
        # Save to database
        await db.reviews.insert(review_task)
        
        # Send notification (email, Slack, in-app)
        await notifications.send(
            to=await self.get_assignee(project_id, 'leed_consultant'),
            subject=f"Review Required: {project_id}",
            body=f"Document ready for review: {document_path}",
            action_link=f"/review/{review_task['id']}"
        )
        
        # Pause workflow (will resume when human responds)
        return await self.wait_for_response(review_task['id'])
    
    async def wait_for_response(self, review_id, timeout_hours=48):
        """
        Poll for human response
        """
        start = datetime.utcnow()
        
        while (datetime.utcnow() - start).total_seconds() < timeout_hours * 3600:
            review = await db.reviews.find_one({'id': review_id})
            
            if review['status'] == 'approved':
                return {
                    'approved': True,
                    'reviewer': review['reviewer'],
                    'comments': review.get('comments', '')
                }
            elif review['status'] == 'rejected':
                return {
                    'approved': False,
                    'comments': review['comments'],
                    'return_to_step': review.get('return_to_step')
                }
            
            # Wait before polling again
            await asyncio.sleep(60)  # Check every minute
        
        # SLA breached
        await self.escalate(review_id)
        raise TimeoutError("Review SLA breached")
```

### 4.2 HITL UI Components

```typescript
// ReviewInterface.tsx
interface ReviewTask {
  id: string;
  projectId: string;
  documentPath: string;
  checklist: string[];
  status: 'pending' | 'approved' | 'rejected';
}

const ReviewInterface: React.FC<{ task: ReviewTask }> = ({ task }) => {
  const [comments, setComments] = useState('');
  const [checklistState, setChecklistState] = useState<Record<string, boolean>>({});
  
  const handleApprove = async () => {
    await api.post(`/reviews/${task.id}/approve`, {
      comments,
      checklist: checklistState
    });
  };
  
  const handleReject = async () => {
    await api.post(`/reviews/${task.id}/reject`, {
      comments,
      returnToStep: identifyStepFromComments(comments)
    });
  };
  
  return (
    <div className="review-interface">
      <DocumentViewer path={task.documentPath} />
      
      <div className="checklist">
        <h3>Review Checklist</h3>
        {task.checklist.map((item, i) => (
          <label key={i}>
            <input
              type="checkbox"
              checked={checklistState[i] || false}
              onChange={(e) => setChecklistState({...checklistState, [i]: e.target.checked})}
            />
            {item}
          </label>
        ))}
      </div>
      
      <textarea
        placeholder="Comments (required for rejection)"
        value={comments}
        onChange={(e) => setComments(e.target.value)}
      />
      
      <div className="actions">
        <button onClick={handleApprove} className="approve">
          Approve
        </button>
        <button onClick={handleReject} className="reject">
          Request Corrections
        </button>
      </div>
    </div>
  );
};
```

---

## Part 5: Reality-Based Credit Assessment

### 5.1 Kimi-Aligned Production Suites

The production MVP should be organized around credit suites rather than the older 16-credit list. Suite packaging reflects how consultants work and how data flows across credits.

| Suite | Credits | Product Posture | Why |
|-------|---------|-----------------|-----|
| Water Efficiency | WEp2 + WEc2 | First commercial wedge | Universal prerequisite, deterministic formulas, transparent point optimization |
| Refrigerant Management | EAp5 + EAc7 | Early production suite | One equipment schedule feeds both prerequisite and credit |
| Quality Plans | EQp1 + EQp2 | Early production suite with review | Repeatable plans plus ventilation/filtration calculations |
| Integrative Process Assessment | IPp1 + IPp2 | Research/narrative assistant | Public data retrieval and source-grounded assessment drafting |
| Low-Emitting Materials | MRc3 | High-value product database workflow | Large manual certification lookup burden across many products |

### 5.2 Assisted Catalog And Deferrals

The existing generated 16 skills remain useful, but they should be described as assisted workflows until their sources, tests, review checklists, and regional fallbacks are verified.

| Workflow | Treatment |
|----------|-----------|
| IPp3 Carbon Assessment | Cross-credit compilation after EAp1, EAp5, and MRp2 source data is ready |
| MRp2 Quantify Embodied Carbon | EPD parsing/matching/reporting with LCA scope and quantity review |
| MRc2 Reduce Embodied Carbon | Automate EPD/threshold documentation; WBLCA remains external expert-tool work |
| EAp2/EAc2/EAc3 | Parse completed energy model outputs; do not automate model creation/calibration |
| LTc1/LTc3/SSc3/SSc5/SSc6 | Useful workflows with regional data checks, site/GIS review, and manual fallback |
| PRc2 LEED AP | Good pipeline proof, low standalone commercial value |

### 5.3 Credits Requiring Significant Human Input

**Energy modeling credits**
- Energy models must be created and validated by qualified modelers.
- Ecogen parses outputs, checks consistency, maps points, and drafts documentation.

**WBLCA and embodied carbon reduction**
- Whole-building LCA must be performed in expert tools such as Tally or One Click LCA.
- Ecogen can import outputs, validate consistency, parse EPDs, and prepare evidence packs.

**GIS/site credits**
- GIS APIs can accelerate US projects, but local datasets and site interpretation remain human-reviewed.
- LTc1 is especially US-centric because primary sensitive-land datasets are US federal sources.

**Integrative process and human impact**
- AI can retrieve data and draft assessments.
- Consultants still own local context, priority selection, owner engagement, and final narrative approval.

### 5.4 Breaking Down Complex Problems

**Example: Site Plan Analysis**

```python
# DON'T: Ask AI to interpret site plan directly
def analyze_site_plan_wrong(image_path):
    """
    This will fail - AI cannot reliably interpret CAD
    """
    result = gpt4_vision.analyze(image_path, "Extract all site information")
    return result  # Unreliable!

# DO: Break into specialized steps
def analyze_site_plan_correct(file_path, file_type):
    """
    Hybrid approach: Tools + AI + Human
    """
    results = {}
    
    # Step 1: Extract from CAD (specialized tool, not AI)
    if file_type == 'dwg':
        cad_data = extract_with_autocad_api(file_path)
        results['building_area'] = cad_data.get('building_area')
        results['site_area'] = cad_data.get('site_area')
        results['parking_count'] = cad_data.get('parking_count')
        results['impervious_area'] = cad_data.get('impervious_area')
    
    # Step 2: Extract from PDF (OCR + structure)
    elif file_type == 'pdf':
        # Use Azure Document Intelligence, not generic AI
        ocr_result = azure_doc_intel.extract_tables(file_path)
        results['area_schedule'] = ocr_result.tables.get('area_schedule')
    
    # Step 3: AI generates summary from STRUCTURED data
    ai_summary = llm.generate_summary(
        building_area=results.get('building_area'),
        site_area=results.get('site_area'),
        parking_count=results.get('parking_count')
    )
    results['ai_summary'] = ai_summary
    
    # Step 4: Flag missing data for human entry
    missing = [k for k, v in results.items() if v is None]
    if missing:
        results['needs_manual_entry'] = True
        results['missing_fields'] = missing
        
        # Create form for human to fill
        results['manual_entry_form'] = generate_form(missing)
    
    return results
```

---

## Part 6: Realistic Delivery Plan

### 6.1 Fourteen-Day Demo

The 14-day path is a demo/proof, not a production MVP. It should prove intake, workflow state, document generation, HITL, and manual export.

Recommended demo scope:

- PRc2 to validate the simplest end-to-end pipeline.
- WEp2 to validate the first commercial wedge.
- EAp5/EAc7 to prove shared-input reuse.
- One assisted workflow such as MRp2 or IPp3 to prove expert review and source confidence handling.

Do not include direct Arc submission, broad regional claims, or autonomous energy modeling in this demo.

### 6.2 Production MVP Suites

| Phase | Focus | Exit Criteria |
|-------|-------|---------------|
| Phase 1 | WEp2/WEc2, EAp5/EAc7, EQp1 first pass | Shared parser/runtime, calculation tests, evidence pack format, HITL dashboard |
| Phase 2 | EQp2, IPp1/IPp2, MRc3 | ASHRAE table handling, public-data research agents, product database lookup and exception review |
| Phase 3 | Cross-suite integration and beta hardening | Confidence tiers, regional source routers, source health dashboard, customer pilots |

### 6.3 Parallel Development Tracks

**Track 1: Frontend**
- Project setup with regional availability.
- Suite workflows and manual fallback forms.
- HITL review dashboard and evidence preview.

**Track 2: Backend + APIs**
- FastAPI endpoints, workflow state, source metadata, cache/rate limit/fallback.
- Evidence pack manifest and audit ledger.

**Track 3: Skill Runtime**
- Durable workflow execution.
- HITL pause/resume and rejection loops.
- Artifact generation and tests.

**Track 4: Credit Suites**
- Water, refrigerant, EQ, IP, and MRc3 implementations.
- Assisted catalog normalization only after source and test verification.

---

## Part 7: Success Metrics (Realistic)

### Technical Metrics
- **Document generation accuracy:** 95% (template filling)
- **Calculation accuracy:** 99% (with unit tests)
- **API uptime:** 99.5%
- **Workflow completion rate:** 90% (10% need human intervention)

### Business Metrics
- **Water Efficiency time savings:** 60-80% of documentation effort after source data is available
- **Production suite coverage:** five Kimi-aligned suites before broad catalog expansion
- **Assisted catalog:** existing generated skill drafts exposed only with review, regional gating, and source caveats
- **Reviewer confidence:** fewer missing evidence items and clearer audit trails

---

## Conclusion: The Executable Plan

**What We're Building:**
A platform that prepares source-grounded, calculation-backed, review-ready LEED v5 evidence packs, with clear HITL checkpoints before submission.

**What We're NOT Building:**
A fully autonomous system that replaces LEED consultants. AI assists, humans decide.

**The Honest Value Proposition:**
- Save consultants **60-70%** of documentation time
- Reduce errors through automated calculations
- Ensure consistency across projects
- Enable consultants to handle **2-3x more projects**

**Investment Required:**
- 14-day demo budget is separate from production MVP funding
- Production suite MVP requires a multi-phase build with engineering plus LEED review support
- **$10K/month** ongoing (API costs, infrastructure)

**Realistic Timeline:**
- **Demo proof:** 14 days
- **Production suite MVP:** multi-month phased delivery
- **Assisted catalog expansion:** after source verification, test fixtures, and regional fallback checks

---

## Appendix: Skill Templates

### SKILL.md Template

```markdown
# Skill: [Credit Code] - [Credit Name]

## Metadata
- **Automation Level:** [X%]
- **Complexity:** [Low/Medium/High]
- **Primary Data Source:** [API/Manual/Calculation]
- **HITL Required:** [Yes/No]

## Inputs
| Field | Type | Required | Source | Validation |
|-------|------|----------|--------|------------|
| | | | | |

## Workflow Steps
1. [Step name] - [Description]
2. ...

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| | | | |

## API Dependencies
| API | Purpose | Fallback |
|-----|---------|----------|
| | | |

## Error Handling
| Error | Action | Human Notification |
|-------|--------|-------------------|
| | | |

## Testing
```bash
# Unit tests
pytest skills/[code]/tests/

# Integration test
python skills/[code]/agent.py --test --project-id=test123
```

## Example Usage
```python
from skills.[code] import [SkillName]

skill = [SkillName](project_id="123", inputs={...})
result = await skill.execute()
```
```
