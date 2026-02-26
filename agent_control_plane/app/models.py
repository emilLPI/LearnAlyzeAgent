from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class JobStatus(str, Enum):
    pending = "pending"
    planned = "planned"
    requires_approval = "requires_approval"
    executing = "executing"
    succeeded = "succeeded"
    failed = "failed"
    aborted = "aborted"


class AutonomyMode(str, Enum):
    off = "OFF"
    supervised = "SUPERVISED"
    autonomous = "AUTONOMOUS"


class CapabilitySnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version: str
    manifest_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EmailNormalized(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str
    from_address: str
    subject: str
    body: str
    status: str = "new"
    classification: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email_id: Optional[int] = Field(default=None, foreign_key="emailnormalized.id")
    tenant_id: str
    intent: str
    confidence: float
    risk: RiskLevel = RiskLevel.low
    status: str = "proposed"
    why: str
    missing_fields: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    tenant_id: str
    status: JobStatus = JobStatus.pending
    source: str = "email"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class JobStep(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    index: int
    action_id: str
    backend: str
    input_json: str
    output_json: Optional[str] = None
    status: str = "pending"
    requires_approval: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Approval(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_step_id: int = Field(foreign_key="jobstep.id")
    decision: Optional[str] = None
    comment: Optional[str] = None
    decided_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str
    event_type: str
    entity_id: Optional[str] = None
    payload_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Settings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str
    autonomy_mode: AutonomyMode = AutonomyMode.off
    scopes: str = "Customers,Projects,Invoices,Emails,Support"
    kill_switch: bool = False
    policy_json: str = (
        '{"no_delete_without_approval":true,"max_bulk_updates":100,'
        '"max_monetary_change_pct":10,"email_after_hours":false}'
    )
    outlook_connected: bool = False
    require_manual_learnalyze_login: bool = True
