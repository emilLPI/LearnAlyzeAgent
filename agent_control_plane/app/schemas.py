from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .models import AutonomyMode, JobStatus, RiskLevel


class EmailCreate(BaseModel):
    tenant_id: str
    from_address: str
    subject: str
    body: str


class TaskCreateFromEmail(BaseModel):
    email_id: int


class TaskRead(BaseModel):
    id: int
    email_id: int | None
    tenant_id: str
    intent: str
    confidence: float
    risk: RiskLevel
    status: str
    why: str
    missing_fields: str | None
    created_at: datetime


class JobRead(BaseModel):
    id: int
    task_id: int | None
    tenant_id: str
    status: JobStatus
    source: str
    started_at: datetime
    updated_at: datetime


class ApprovalDecision(BaseModel):
    comment: str | None = None
    decided_by: str


class SettingsPayload(BaseModel):
    tenant_id: str
    autonomy_mode: AutonomyMode
    scopes: list[str]
    kill_switch: bool
    policy: dict[str, Any]
    outlook_connected: bool = False
    require_manual_learnalyze_login: bool = True


class DispatchRequest(BaseModel):
    action_id: str
    payload: dict[str, Any]
    on_behalf_of: str
    idempotency_key: str


class ManifestResponse(BaseModel):
    version: str
    pages: list[dict[str, Any]]
