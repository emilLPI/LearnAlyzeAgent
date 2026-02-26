from __future__ import annotations

import json
from datetime import datetime

from sqlmodel import Session, select

from .models import (
    Approval,
    AuditLog,
    CapabilitySnapshot,
    EmailNormalized,
    Job,
    JobStatus,
    JobStep,
    RiskLevel,
    Settings,
    Task,
)


def classify_email(subject: str, body: str) -> tuple[str, str, float, RiskLevel]:
    text = f"{subject} {body}".lower()
    if "opret kunde" in text or "new customer" in text:
        return "create customer", "Detected customer onboarding keywords", 0.93, RiskLevel.low
    if "invoice" in text or "faktura" in text:
        return "invoice follow-up", "Detected invoicing workflow", 0.88, RiskLevel.medium
    if "delete" in text or "slet" in text:
        return "dangerous change", "Detected destructive intent", 0.81, RiskLevel.high
    return "needs triage", "No strong intent; route to inbox", 0.55, RiskLevel.low


def create_task_from_email(session: Session, email_id: int) -> Task:
    email = session.get(EmailNormalized, email_id)
    if not email:
        raise ValueError("email_not_found")

    intent, why, confidence, risk = classify_email(email.subject, email.body)
    missing_fields = None if confidence >= 0.7 else "customer_reference"

    task = Task(
        email_id=email.id,
        tenant_id=email.tenant_id,
        intent=intent,
        confidence=confidence,
        risk=risk,
        status="proposed",
        why=why,
        missing_fields=missing_fields,
    )
    session.add(task)
    email.status = "triaged"
    session.add(
        AuditLog(
            tenant_id=email.tenant_id,
            event_type="task_suggested",
            entity_id=str(email.id),
            payload_json=json.dumps({"intent": intent, "confidence": confidence}),
        )
    )
    session.commit()
    session.refresh(task)
    return task


def plan_job(session: Session, task: Task) -> Job:
    job = Job(task_id=task.id, tenant_id=task.tenant_id, status=JobStatus.planned)
    session.add(job)
    session.commit()
    session.refresh(job)

    step = JobStep(
        job_id=job.id,
        index=1,
        action_id=f"tasks.{task.intent.replace(' ', '_')}",
        backend="dispatch",
        input_json=json.dumps({"task_id": task.id, "intent": task.intent}),
        requires_approval=task.risk in {RiskLevel.medium, RiskLevel.high},
    )
    session.add(step)
    session.commit()
    session.refresh(step)

    if step.requires_approval:
        job.status = JobStatus.requires_approval
        session.add(Approval(job_step_id=step.id))
    else:
        job.status = JobStatus.executing

    session.add(
        AuditLog(
            tenant_id=task.tenant_id,
            event_type="job_planned",
            entity_id=str(job.id),
            payload_json=json.dumps({"task_id": task.id, "risk": task.risk.value}),
        )
    )
    job.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(job)
    return job


def latest_manifest(session: Session) -> CapabilitySnapshot | None:
    return session.exec(select(CapabilitySnapshot).order_by(CapabilitySnapshot.created_at.desc())).first()


def ensure_default_settings(session: Session, tenant_id: str) -> Settings:
    settings = session.exec(select(Settings).where(Settings.tenant_id == tenant_id)).first()
    if settings:
        return settings

    settings = Settings(tenant_id=tenant_id)
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings
