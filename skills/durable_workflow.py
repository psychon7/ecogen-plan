"""
Durable Workflow Engine for LEED Credit Automation

Provides resumable, fault-tolerant workflows that can survive:
- API failures (with retry)
- Server restarts
- Long-running human reviews
- Network interruptions
"""

import json
import asyncio
import hashlib
from datetime import datetime, timedelta
from typing import List, Callable, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"  # Waiting for human review
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowState:
    """Serializable workflow state"""
    workflow_id: str
    project_id: str
    skill_name: str
    current_step: int
    total_steps: int
    status: WorkflowStatus
    context: Dict[str, Any]
    step_results: Dict[str, Any]
    created_at: str
    updated_at: str
    error: Optional[str] = None
    failed_step: Optional[int] = None
    hitl_task_id: Optional[str] = None


class DurableOrchestrator:
    """
    Durable workflow engine with state persistence
    """
    
    def __init__(self, storage_path: str = "/data/workflows"):
        self.storage_path = storage_path
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory exists"""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _state_path(self, workflow_id: str) -> str:
        """Get path to workflow state file"""
        return f"{self.storage_path}/{workflow_id}.json"
    
    def load_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Load workflow state from storage"""
        try:
            with open(self._state_path(workflow_id), 'r') as f:
                data = json.load(f)
                return WorkflowState(**data)
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error loading state for {workflow_id}: {e}")
            return None
    
    def save_state(self, state: WorkflowState):
        """Save workflow state to storage"""
        state.updated_at = datetime.utcnow().isoformat()
        with open(self._state_path(state.workflow_id), 'w') as f:
            json.dump(asdict(state), f, indent=2, default=str)
    
    def create_workflow(self, project_id: str, skill_name: str, 
                       total_steps: int, context: Dict[str, Any]) -> WorkflowState:
        """Create a new workflow"""
        workflow_id = self._generate_id(project_id, skill_name)
        
        state = WorkflowState(
            workflow_id=workflow_id,
            project_id=project_id,
            skill_name=skill_name,
            current_step=0,
            total_steps=total_steps,
            status=WorkflowStatus.PENDING,
            context=context,
            step_results={},
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        self.save_state(state)
        logger.info(f"Created workflow {workflow_id} for {skill_name}")
        
        return state
    
    async def run(self, workflow_id: str, steps: List[Callable]) -> Dict[str, Any]:
        """
        Execute workflow steps with durability
        
        Resumes from last completed step if workflow was interrupted
        """
        state = self.load_state(workflow_id)
        if not state:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        state.status = WorkflowStatus.RUNNING
        self.save_state(state)
        
        try:
            for i, step in enumerate(steps):
                # Skip completed steps
                if i < state.current_step:
                    logger.info(f"Skipping completed step {i}: {step.__name__}")
                    continue
                
                logger.info(f"Executing step {i}/{len(steps)}: {step.__name__}")
                
                try:
                    # Execute step with retry logic
                    result = await self._execute_step_with_retry(step, state)
                    
                    # Update state
                    state.current_step = i + 1
                    state.step_results[step.__name__] = result
                    self.save_state(state)
                    
                    logger.info(f"Step {i} completed successfully")
                    
                except WorkflowPaused as e:
                    # Workflow paused for human review
                    state.status = WorkflowStatus.PAUSED
                    state.hitl_task_id = e.task_id
                    self.save_state(state)
                    logger.info(f"Workflow {workflow_id} paused for HITL: {e.task_id}")
                    raise
                    
                except Exception as e:
                    # Step failed
                    state.status = WorkflowStatus.FAILED
                    state.error = str(e)
                    state.failed_step = i
                    self.save_state(state)
                    logger.error(f"Step {i} failed: {e}")
                    raise
            
            # All steps completed
            state.status = WorkflowStatus.COMPLETED
            self.save_state(state)
            logger.info(f"Workflow {workflow_id} completed successfully")
            
            return state.step_results
            
        except WorkflowPaused:
            # Re-raise to notify caller
            raise
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
    
    async def _execute_step_with_retry(self, step: Callable, state: WorkflowState,
                                       max_retries: int = 3) -> Any:
        """Execute a step with retry logic"""
        retry_count = 0
        last_error = None
        
        # Get step metadata if available
        step_retry = getattr(step, '_retry', max_retries)
        step_timeout = getattr(step, '_timeout', 30)
        
        while retry_count < step_retry:
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    step(state.context, state.step_results),
                    timeout=step_timeout
                )
                return result
                
            except asyncio.TimeoutError:
                retry_count += 1
                last_error = "Timeout"
                logger.warning(f"Step timeout, retry {retry_count}/{step_retry}")
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                logger.warning(f"Step error: {e}, retry {retry_count}/{step_retry}")
                await asyncio.sleep(2 ** retry_count)
        
        # All retries exhausted
        raise Exception(f"Step failed after {step_retry} retries: {last_error}")
    
    async def resume_after_hitl(self, workflow_id: str, hitl_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resume workflow after human review
        
        Called when human approves/rejects a HITL task
        """
        state = self.load_state(workflow_id)
        if not state:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if state.status != WorkflowStatus.PAUSED:
            raise ValueError(f"Workflow {workflow_id} is not paused")
        
        # Add HITL result to context
        state.context['hitl_result'] = hitl_result
        state.status = WorkflowStatus.RUNNING
        state.hitl_task_id = None
        self.save_state(state)
        
        logger.info(f"Workflow {workflow_id} resumed after HITL")
        
        # Return to caller - workflow will be resumed by run()
        return {"status": "resumed", "workflow_id": workflow_id}
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current workflow status"""
        state = self.load_state(workflow_id)
        if not state:
            return None
        
        return {
            "workflow_id": state.workflow_id,
            "project_id": state.project_id,
            "skill_name": state.skill_name,
            "status": state.status.value,
            "current_step": state.current_step,
            "total_steps": state.total_steps,
            "progress": f"{state.current_step}/{state.total_steps}",
            "created_at": state.created_at,
            "updated_at": state.updated_at,
            "error": state.error,
            "hitl_task_id": state.hitl_task_id
        }
    
    def list_workflows(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all workflows, optionally filtered by project"""
        import os
        import glob
        
        workflows = []
        pattern = f"{self.storage_path}/*.json"
        
        for path in glob.glob(pattern):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    if project_id is None or data.get('project_id') == project_id:
                        workflows.append({
                            "workflow_id": data['workflow_id'],
                            "project_id": data['project_id'],
                            "skill_name": data['skill_name'],
                            "status": data['status'],
                            "progress": f"{data['current_step']}/{data['total_steps']}"
                        })
            except Exception as e:
                logger.error(f"Error reading {path}: {e}")
        
        return workflows
    
    def _generate_id(self, project_id: str, skill_name: str) -> str:
        """Generate unique workflow ID"""
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{project_id}:{skill_name}:{timestamp}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"wf-{skill_name.lower()}-{hash_value}"


class WorkflowPaused(Exception):
    """Exception raised when workflow is paused for human review"""
    def __init__(self, task_id: str, message: str = "Workflow paused for human review"):
        self.task_id = task_id
        self.message = message
        super().__init__(self.message)


def step(name: str = None, retry: int = 3, timeout: int = 30):
    """
    Decorator for workflow steps
    
    Usage:
        @step(name="fetch_data", retry=3, timeout=30)
        async def fetch_data(context, previous_results):
            # Step implementation
            return result
    """
    def decorator(func: Callable):
        func._step_name = name or func.__name__
        func._retry = retry
        func._timeout = timeout
        return func
    return decorator


# Example usage
if __name__ == "__main__":
    async def example():
        orchestrator = DurableOrchestrator(storage_path="/tmp/workflows")
        
        # Create workflow
        state = orchestrator.create_workflow(
            project_id="123",
            skill_name="IPp3_Carbon_Assessment",
            total_steps=5,
            context={"location": "NYC", "building_type": "Office"}
        )
        
        print(f"Created workflow: {state.workflow_id}")
        
        # Define steps
        @step(name="validate", retry=1)
        async def validate_inputs(context, previous):
            print("Validating inputs...")
            return {"valid": True}
        
        @step(name="fetch_data", retry=3, timeout=10)
        async def fetch_data(context, previous):
            print("Fetching data...")
            return {"data": "sample"}
        
        @step(name="calculate")
        async def calculate(context, previous):
            print("Calculating...")
            return {"result": 42}
        
        # Run workflow
        try:
            results = await orchestrator.run(
                state.workflow_id,
                [validate_inputs, fetch_data, calculate]
            )
            print(f"Results: {results}")
        except Exception as e:
            print(f"Workflow failed: {e}")
        
        # Check status
        status = orchestrator.get_workflow_status(state.workflow_id)
        print(f"Status: {status}")
    
    asyncio.run(example())
