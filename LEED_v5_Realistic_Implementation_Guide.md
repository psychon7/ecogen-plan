# LEED v5 AI Automation Platform - Realistic Implementation Guide

## Executive Summary: The Honest Assessment

This document provides a **realistic, executable plan** for building a LEED v5 automation platform based on **current AI capabilities** (March 2026). It includes agentic workflow patterns, HITL (Human-in-the-Loop) design, durable workflows, and a skill-based architecture.

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
- **70% automation** for straightforward credits (calculations, API data)
- **50% automation** for complex credits (requires human review)
- **30% automation** for credits requiring site-specific interpretation

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
├── ip_p3_carbon_assessment/
│   ├── SKILL.md          # Instructions, inputs, outputs
│   ├── agent.py          # Credit-specific agent
│   ├── templates/        # Document templates
│   ├── validations.py    # Validation rules
│   └── tests/            # Unit tests
├── ea_p1_operational_carbon/
│   ├── SKILL.md
│   ├── agent.py
│   └── ...
└── ... (16 skills total)
```

### 2.2 Skill Structure

Each skill has:

**SKILL.md** - The Contract:
```markdown
# Skill: IPp3 Carbon Assessment

## Purpose
Calculate 25-year carbon projection from operational, refrigerant, and embodied sources.

## Automation Level
- Calculation: 95% automated
- Document Generation: 90% automated
- Data Retrieval: 85% automated
- **Overall: 90% (requires human review)**

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| project_location | coordinates | User input | Valid lat/lon |
| energy_model_output | file | Upload | Valid format |
| material_quantities | JSON | Upload or manual | Required fields |
| service_life | integer | User input | 25-100 years |

## Inputs (Optional)
| Field | Type | Default |
|-------|------|---------|
| grid_region | string | Auto-detect from location |
| refrigerant_schedule | file | None |

## Workflow (Durable - Resumable)
1. **validate_inputs** - Check all required data present
2. **fetch_grid_emission_factors** - API call to EPA eGRID (US) or national source
3. **fetch_embodied_carbon_data** - API call to EC3 Database
4. **calculate_operational_carbon** - Python calculation
5. **calculate_refrigerant_emissions** - Python calculation
6. **calculate_embodied_carbon** - Python calculation
7. **generate_projection** - Sum all sources for 25-year projection
8. **generate_report** - Fill template with calculated data
9. **HITL_REVIEW** - Human reviews and approves
10. **finalize_output** - Generate final PDF/Excel

## HITL Checkpoints
| Step | Who | Action | SLA |
|------|-----|--------|-----|
| After report generation | LEED Consultant | Review calculations and approve | 24 hours |
| If API data missing | Data Steward | Provide manual data entry | 48 hours |
| Final submission | Project Manager | Approve for USGBC submission | 24 hours |

## Outputs
| Document | Format | Description |
|----------|--------|-------------|
| carbon_projection_report | PDF | 25-year projection with charts |
| calculation_workbook | Excel | Detailed calculations |
| usgbc_submission_form | PDF | Pre-filled USGBC form |

## API Dependencies
| API | Purpose | Regional Availability | Fallback |
|-----|---------|----------------------|----------|
| EPA eGRID | Grid emission factors | US only | Use national grid data |
| EC3 Database | Embodied carbon | Global | Manual EPD entry |
| NREL Cambium | Future grid scenarios | US only | Skip future projections |

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
python -m pytest skills/ip_p3_carbon_assessment/tests/

# Run integration test
python skills/ip_p3_carbon_assessment/agent.py --test-mode
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

### 5.1 Honest Automation Levels

| Credit | Claimed | **Realistic** | Why |
|--------|---------|---------------|-----|
| IPp3 Carbon Assessment | 92.5% | **85%** | EC3 API reliable, but material matching needs human |
| EAp1 Op Carbon | 89.4% | **80%** | Grid data varies by country, future projections US-only |
| WEp2 Water Efficiency | 89.3% | **90%** | Calculations straightforward, fixture data available |
| EAp2 Energy Code | 85.7% | **75%** | Energy model interpretation needs expertise |
| EAp5 Refrigerant | 85.2% | **90%** | Database lookup, clear compliance rules |
| MRp2 Embodied Carbon | 87.0% | **85%** | EC3 reliable, but quantity verification needed |
| EAc3 Energy Efficiency | 87.7% | **70%** | Energy modeling is complex, requires expert review |
| WEc2 Water Efficiency | 87.5% | **85%** | Calculations clear, alternative water sources vary |
| MRc2 Reduce Embodied | 88.4% | **80%** | WBLCA comparison needs expert judgment |
| LTc3 Location | 88.0% | **75%** | Walk Score limited to certain countries |
| SSc3 Rainwater | 88.0% | **80%** | Rainfall data varies by country |
| EAc7 Refrigerant | 89.3% | **90%** | Clear calculations, good databases |
| SSc5 Heat Island | 85.3% | **85%** | SRI calculations straightforward |
| SSc6 Light Pollution | 90.6% | **95%** | BUG ratings are standardized |
| PRc2 LEED AP | 90.1% | **95%** | Simple API verification |
| LTc1 Land Protection | 87.6% | **60%** | **GIS data very limited outside US** |

**Average Realistic Automation: 82%** (not 88%)

### 5.2 Credits Requiring Significant Human Input

**LTc1 - Sensitive Land Protection (60% realistic)**
- FEMA flood maps: US only
- Wetlands data: US only
- Protected species: US only
- **Outside US: Requires manual GIS analysis**

**EAc3 - Enhanced Energy Efficiency (70% realistic)**
- Energy modeling is expert work
- Baseline modeling requires judgment
- Optimization recommendations need expertise
- **AI assists, but cannot replace energy modeler**

**MRc2 - Reduce Embodied Carbon (80% realistic)**
- WBLCA requires expert judgment
- Baseline selection is project-specific
- Material substitution recommendations need expertise
- **AI calculates, but expert interprets**

### 5.3 Breaking Down Complex Problems

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

## Part 6: Realistic 14-Day Implementation Plan

### Week 1: Foundation + Simple Credits

**Day 1-2: Setup**
- Initialize project (React + FastAPI + PostgreSQL)
- Set up durable workflow engine
- Create HITL notification system
- Deploy to staging

**Day 3-4: Build 3 Simple Skills**
- PRc2 (LEED AP) - 95% automated, API verification
- SSc6 (Light Pollution) - 95% automated, BUG rating lookup
- EAp5 (Refrigerant) - 90% automated, database lookup

**Day 5-7: Build 3 More Skills**
- WEp2 (Water Efficiency) - 90% automated, calculations
- SSc5 (Heat Island) - 85% automated, SRI calculations
- EAc7 (Refrigerant) - 90% automated, GWP calculations

### Week 2: Complex Credits + Integration

**Day 8-10: Medium Complexity**
- IPp3 (Carbon Assessment) - 85% automated
- WEc2 (Water Efficiency) - 85% automated
- MRp2 (Embodied Carbon) - 85% automated

**Day 11-12: High Complexity (with HITL)**
- EAc3 (Energy Efficiency) - 70% automated, requires energy modeler review
- MRc2 (Reduce Embodied) - 80% automated, requires WBLCA expert
- LTc3 (Location) - 75% automated, limited by Walk Score regions

**Day 13-14: Integration & Polish**
- USGBC Arc integration
- Regional filtering UI
- Admin dashboard
- Documentation
- Deploy to production

### Parallel Development Tracks

**Track 1: Frontend (1 developer)**
- Credit selection with regional filtering
- Document upload interfaces
- Review dashboard for HITL

**Track 2: Backend + APIs (1 developer)**
- FastAPI endpoints
- Database models
- API integrations (36 services)

**Track 3: Credit Agents (2 developers)**
- 8 skills each
- Durable workflows
- HITL integration

---

## Part 7: Success Metrics (Realistic)

### Technical Metrics
- **Document generation accuracy:** 95% (template filling)
- **Calculation accuracy:** 99% (with unit tests)
- **API uptime:** 99.5%
- **Workflow completion rate:** 90% (10% need human intervention)

### Business Metrics
- **Time savings:** 60-70% (not 80%)
- **Credits automated:** 12 of 16 (75%) fully automated
- **Credits with HITL:** 4 of 16 (25%) require human review
- **Projects per month:** 50 (with 5 consultants reviewing)

---

## Conclusion: The Executable Plan

**What We're Building:**
A platform that automates **70-85%** of LEED documentation, with clear HITL checkpoints for the remaining 15-30%.

**What We're NOT Building:**
A fully autonomous system that replaces LEED consultants. AI assists, humans decide.

**The Honest Value Proposition:**
- Save consultants **60-70%** of documentation time
- Reduce errors through automated calculations
- Ensure consistency across projects
- Enable consultants to handle **2-3x more projects**

**Investment Required:**
- **$150K-200K** (not $225-300K) - 14 days with 4 developers
- **$10K/month** ongoing (API costs, infrastructure)

**Realistic Timeline:**
- **MVP with 12 credits:** 14 days
- **All 16 credits polished:** 30 days
- **Production ready:** 45 days

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
