"""
Human-in-the-Loop (HITL) System for LEED Credit Automation

Manages human review checkpoints in automated workflows.
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HITLStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    EXPIRED = "expired"


@dataclass
class HITLTask:
    """Human review task"""
    id: str
    workflow_id: str
    project_id: str
    skill_name: str
    step_name: str
    assignee_role: str
    assignee_email: Optional[str]
    status: HITLStatus
    document_path: str
    checklist: List[str]
    instructions: str
    comments: Optional[str]
    rejection_reason: Optional[str]
    return_to_step: Optional[int]
    created_at: str
    assigned_at: Optional[str]
    completed_at: Optional[str]
    sla_hours: int
    expires_at: str
    metadata: Dict[str, Any]


class HITLManager:
    """
    Manages human review tasks and notifications
    """
    
    def __init__(self, storage_path: str = "/data/hitl", notification_service=None):
        self.storage_path = storage_path
        self.notification_service = notification_service or NotificationService()
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory exists"""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _task_path(self, task_id: str) -> str:
        """Get path to task file"""
        return f"{self.storage_path}/{task_id}.json"
    
    def _generate_task_id(self, workflow_id: str, step_name: str) -> str:
        """Generate unique task ID"""
        import hashlib
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{workflow_id}:{step_name}:{timestamp}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"hitl-{hash_value}"
    
    async def create_task(
        self,
        workflow_id: str,
        project_id: str,
        skill_name: str,
        step_name: str,
        assignee_role: str,
        document_path: str,
        checklist: List[str],
        instructions: str,
        sla_hours: int = 24,
        metadata: Dict[str, Any] = None
    ) -> HITLTask:
        """
        Create a new human review task
        
        This pauses the workflow and notifies the assignee
        """
        task_id = self._generate_task_id(workflow_id, step_name)
        
        expires_at = datetime.utcnow() + timedelta(hours=sla_hours)
        
        # Get assignee email from project data
        assignee_email = await self._get_assignee_email(project_id, assignee_role)
        
        task = HITLTask(
            id=task_id,
            workflow_id=workflow_id,
            project_id=project_id,
            skill_name=skill_name,
            step_name=step_name,
            assignee_role=assignee_role,
            assignee_email=assignee_email,
            status=HITLStatus.PENDING,
            document_path=document_path,
            checklist=checklist,
            instructions=instructions,
            comments=None,
            rejection_reason=None,
            return_to_step=None,
            created_at=datetime.utcnow().isoformat(),
            assigned_at=None,
            completed_at=None,
            sla_hours=sla_hours,
            expires_at=expires_at.isoformat(),
            metadata=metadata or {}
        )
        
        # Save task
        self._save_task(task)
        
        # Send notification
        await self._notify_assignee(task)
        
        logger.info(f"Created HITL task {task_id} for {skill_name}/{step_name}")
        
        return task
    
    def _save_task(self, task: HITLTask):
        """Save task to storage"""
        with open(self._task_path(task.id), 'w') as f:
            json.dump(asdict(task), f, indent=2, default=str)
    
    def load_task(self, task_id: str) -> Optional[HITLTask]:
        """Load task from storage"""
        try:
            with open(self._task_path(task_id), 'r') as f:
                data = json.load(f)
                return HITLTask(**data)
        except FileNotFoundError:
            return None
    
    async def _get_assignee_email(self, project_id: str, role: str) -> Optional[str]:
        """Get assignee email from project data"""
        # In production, query database
        # For now, return placeholder
        role_emails = {
            "leed_consultant": "consultant@example.com",
            "energy_modeler": "modeler@example.com",
            "project_manager": "pm@example.com",
            "gis_analyst": "gis@example.com"
        }
        return role_emails.get(role)
    
    async def _notify_assignee(self, task: HITLTask):
        """Send notification to assignee"""
        if not task.assignee_email:
            logger.warning(f"No email for assignee role {task.assignee_role}")
            return
        
        subject = f"[LEED Platform] Review Required: {task.skill_name}"
        
        body = f"""
Hello,

You have been assigned a review task for LEED credit automation.

Project: {task.project_id}
Credit: {task.skill_name}
Step: {task.step_name}
SLA: {task.sla_hours} hours

Instructions:
{task.instructions}

Review Checklist:
{"".join(f"- [ ] {item}" for item in task.checklist)}

Document: {task.document_path}

Review Link: https://platform.leed.ai/review/{task.id}

Please complete this review within {task.sla_hours} hours.

Thank you,
LEED Automation Platform
        """
        
        await self.notification_service.send_email(
            to=task.assignee_email,
            subject=subject,
            body=body
        )
        
        logger.info(f"Sent notification to {task.assignee_email}")
    
    async def approve(
        self,
        task_id: str,
        reviewer_email: str,
        comments: str = None,
        checklist_results: Dict[str, bool] = None
    ) -> HITLTask:
        """
        Approve a review task
        
        This resumes the workflow
        """
        task = self.load_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.status not in [HITLStatus.PENDING, HITLStatus.ASSIGNED, HITLStatus.IN_REVIEW]:
            raise ValueError(f"Task {task_id} cannot be approved (status: {task.status})")
        
        task.status = HITLStatus.APPROVED
        task.comments = comments
        task.completed_at = datetime.utcnow().isoformat()
        task.metadata['checklist_results'] = checklist_results
        task.metadata['reviewer_email'] = reviewer_email
        
        self._save_task(task)
        
        # Notify workflow system
        await self._notify_workflow_resume(task)
        
        logger.info(f"Task {task_id} approved by {reviewer_email}")
        
        return task
    
    async def reject(
        self,
        task_id: str,
        reviewer_email: str,
        rejection_reason: str,
        return_to_step: int = None,
        comments: str = None
    ) -> HITLTask:
        """
        Reject a review task
        
        This returns the workflow to a previous step
        """
        task = self.load_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.status not in [HITLStatus.PENDING, HITLStatus.ASSIGNED, HITLStatus.IN_REVIEW]:
            raise ValueError(f"Task {task_id} cannot be rejected (status: {task.status})")
        
        task.status = HITLStatus.REJECTED
        task.rejection_reason = rejection_reason
        task.return_to_step = return_to_step
        task.comments = comments
        task.completed_at = datetime.utcnow().isoformat()
        task.metadata['reviewer_email'] = reviewer_email
        
        self._save_task(task)
        
        # Notify workflow system
        await self._notify_workflow_return(task)
        
        logger.info(f"Task {task_id} rejected by {reviewer_email}, return to step {return_to_step}")
        
        return task
    
    async def _notify_workflow_resume(self, task: HITLTask):
        """Notify workflow system to resume"""
        # In production, call workflow API or publish event
        logger.info(f"Notifying workflow {task.workflow_id} to resume")
    
    async def _notify_workflow_return(self, task: HITLTask):
        """Notify workflow system to return to step"""
        logger.info(f"Notifying workflow {task.workflow_id} to return to step {task.return_to_step}")
    
    async def check_expired_tasks(self) -> List[HITLTask]:
        """Check for expired tasks and escalate"""
        import glob
        import os
        
        expired = []
        now = datetime.utcnow()
        
        for path in glob.glob(f"{self.storage_path}/*.json"):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    
                if data['status'] in [HITLStatus.PENDING.value, HITLStatus.ASSIGNED.value]:
                    expires_at = datetime.fromisoformat(data['expires_at'])
                    if now > expires_at:
                        task = HITLTask(**data)
                        await self._escalate_task(task)
                        expired.append(task)
            except Exception as e:
                logger.error(f"Error checking task {path}: {e}")
        
        return expired
    
    async def _escalate_task(self, task: HITLTask):
        """Escalate an expired task"""
        task.status = HITLStatus.ESCALATED
        self._save_task(task)
        
        # Notify project manager
        await self.notification_service.send_email(
            to="pm@example.com",
            subject=f"[ESCALATION] HITL task expired: {task.skill_name}",
            body=f"Task {task.id} has exceeded SLA of {task.sla_hours} hours."
        )
        
        logger.warning(f"Escalated expired task {task.id}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        task = self.load_task(task_id)
        if not task:
            return None
        
        return {
            "id": task.id,
            "status": task.status.value,
            "skill_name": task.skill_name,
            "step_name": task.step_name,
            "assignee_role": task.assignee_role,
            "created_at": task.created_at,
            "expires_at": task.expires_at,
            "completed_at": task.completed_at
        }
    
    def list_tasks(
        self,
        project_id: str = None,
        status: HITLStatus = None,
        assignee_role: str = None
    ) -> List[Dict[str, Any]]:
        """List tasks with optional filters"""
        import glob
        
        tasks = []
        
        for path in glob.glob(f"{self.storage_path}/*.json"):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                
                # Apply filters
                if project_id and data.get('project_id') != project_id:
                    continue
                if status and data.get('status') != status.value:
                    continue
                if assignee_role and data.get('assignee_role') != assignee_role:
                    continue
                
                tasks.append({
                    "id": data['id'],
                    "status": data['status'],
                    "skill_name": data['skill_name'],
                    "step_name": data['step_name'],
                    "assignee_role": data['assignee_role'],
                    "created_at": data['created_at'],
                    "expires_at": data['expires_at']
                })
            except Exception as e:
                logger.error(f"Error reading task {path}: {e}")
        
        return tasks


class NotificationService:
    """Placeholder notification service"""
    
    async def send_email(self, to: str, subject: str, body: str):
        """Send email notification"""
        logger.info(f"[EMAIL] To: {to}, Subject: {subject}")
        # In production, integrate with SendGrid, AWS SES, etc.
    
    async def send_slack(self, channel: str, message: str):
        """Send Slack notification"""
        logger.info(f"[SLACK] Channel: {channel}, Message: {message}")
        # In production, integrate with Slack API


# Decorator for HITL checkpoints
def hitl_checkpoint(
    name: str = None,
    assignee: str = "leed_consultant",
    sla_hours: int = 24,
    instructions: str = "Please review and approve"
):
    """
    Decorator for HITL checkpoint steps
    
    Usage:
        @hitl_checkpoint(
            name="human_review",
            assignee="leed_consultant",
            sla_hours=24,
            instructions="Review calculations and approve"
        )
        async def human_review(context, previous_results):
            # This will pause workflow and create HITL task
            pass
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            # This is called when the step executes
            # In practice, the workflow engine handles HITL
            return await func(*args, **kwargs)
        
        wrapper._hitl_checkpoint = True
        wrapper._hitl_name = name or func.__name__
        wrapper._hitl_assignee = assignee
        wrapper._hitl_sla = sla_hours
        wrapper._hitl_instructions = instructions
        
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    async def example():
        hitl = HITLManager(storage_path="/tmp/hitl")
        
        # Create task
        task = await hitl.create_task(
            workflow_id="wf-123",
            project_id="proj-456",
            skill_name="IPp3_Carbon_Assessment",
            step_name="human_review",
            assignee_role="leed_consultant",
            document_path="/docs/carbon_report.pdf",
            checklist=[
                "Energy model inputs verified",
                "Material quantities accurate",
                "Calculations reasonable"
            ],
            instructions="Please review the carbon assessment report and verify all calculations.",
            sla_hours=24
        )
        
        print(f"Created HITL task: {task.id}")
        
        # Simulate approval
        approved_task = await hitl.approve(
            task_id=task.id,
            reviewer_email="consultant@example.com",
            comments="Looks good, approved for submission"
        )
        
        print(f"Task approved: {approved_task.status}")
    
    asyncio.run(example())
