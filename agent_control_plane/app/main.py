from __future__ import annotations

import json
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .db import create_db, get_session
from .logic import create_task_from_email, ensure_default_settings, latest_manifest, plan_job
from .models import Approval, AuditLog, CapabilitySnapshot, EmailNormalized, Job, JobStatus, Settings, Task
from .schemas import (
    ApprovalDecision,
    DispatchRequest,
    EmailCreate,
    ManifestResponse,
    SettingsPayload,
    TaskCreateFromEmail,
)


app = FastAPI(title="ARX Agent Control Plane API", version="0.1.0")
app.mount("/static", StaticFiles(directory="agent_control_plane/app/static"), name="static")


@app.get("/")
def webapp() -> FileResponse:
    return FileResponse("agent_control_plane/app/static/index.html")


@app.on_event("startup")
def on_startup() -> None:
    create_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/emails")
def get_emails(
    status: str = Query(default="new"),
    tenant_id: str | None = None,
    session: Session = Depends(get_session),
):
    query = select(EmailNormalized)
    if status:
        query = query.where(EmailNormalized.status == status)
    if tenant_id:
        query = query.where(EmailNormalized.tenant_id == tenant_id)
    return session.exec(query.order_by(EmailNormalized.created_at.desc())).all()


@app.post("/emails")
def create_email(payload: EmailCreate, session: Session = Depends(get_session)):
    email = EmailNormalized(**payload.model_dump())
    session.add(email)
    session.add(
        AuditLog(
            tenant_id=email.tenant_id,
            event_type="email_ingested",
            entity_id=None,
            payload_json=json.dumps(payload.model_dump()),
        )
    )
    session.commit()
    session.refresh(email)
    return email


@app.post("/tasks/from-email")
def create_task(payload: TaskCreateFromEmail, session: Session = Depends(get_session)):
    try:
        task = create_task_from_email(session, payload.email_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return task


@app.get("/tasks")
def get_tasks(status: str | None = None, session: Session = Depends(get_session)):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    return session.exec(query.order_by(Task.created_at.desc())).all()


@app.post("/jobs/plan/{task_id}")
def plan_from_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task_not_found")
    return plan_job(session, task)


@app.get("/jobs")
def get_jobs(status: JobStatus | None = None, session: Session = Depends(get_session)):
    query = select(Job)
    if status:
        query = query.where(Job.status == status)
    return session.exec(query.order_by(Job.started_at.desc())).all()


@app.get("/jobs/{job_id}")
def get_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job_not_found")
    return job


@app.post("/jobs/{job_id}/abort")
def abort_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job_not_found")
    job.status = JobStatus.aborted
    job.updated_at = datetime.utcnow()
    session.add(job)
    session.commit()
    return {"ok": True, "job_id": job_id, "status": job.status}


@app.post("/jobs/{job_id}/retry")
def retry_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job_not_found")
    job.status = JobStatus.executing
    job.updated_at = datetime.utcnow()
    session.add(job)
    session.commit()
    return {"ok": True, "job_id": job_id, "status": job.status}


@app.post("/approvals/{approval_id}/approve")
def approve(approval_id: int, payload: ApprovalDecision, session: Session = Depends(get_session)):
    approval = session.get(Approval, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="approval_not_found")
    approval.decision = "approved"
    approval.comment = payload.comment
    approval.decided_by = payload.decided_by
    session.add(approval)
    session.commit()
    return {"ok": True}


@app.post("/approvals/{approval_id}/reject")
def reject(approval_id: int, payload: ApprovalDecision, session: Session = Depends(get_session)):
    approval = session.get(Approval, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="approval_not_found")
    approval.decision = "rejected"
    approval.comment = payload.comment
    approval.decided_by = payload.decided_by
    session.add(approval)
    session.commit()
    return {"ok": True}


@app.get("/audit")
def get_audit(query: str | None = None, session: Session = Depends(get_session)):
    q = select(AuditLog)
    if query:
        q = q.where(AuditLog.payload_json.contains(query))
    return session.exec(q.order_by(AuditLog.created_at.desc())).all()


@app.get("/capabilities/latest", response_model=ManifestResponse)
def capabilities_latest(session: Session = Depends(get_session)):
    manifest = latest_manifest(session)
    if not manifest:
        return ManifestResponse(version="bootstrap", pages=[])
    return ManifestResponse(version=manifest.version, pages=json.loads(manifest.manifest_json)["pages"])


@app.post("/capabilities/rescan")
def capabilities_rescan(session: Session = Depends(get_session)):
    demo_manifest = {
        "version": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pages": [
            {
                "id": "customers",
                "route": "/customers",
                "title": "Kunder",
                "description": "Customer management",
                "actions": [
                    {
                        "id": "customers.create",
                        "label": "Opret kunde",
                        "risk": "low",
                        "required_permissions": ["customers:write"],
                        "inputs": [
                            {"name": "name", "label": "Navn", "type": "text", "required": True},
                            {"name": "cvr", "label": "CVR", "type": "text", "required": False},
                        ],
                        "ui_hooks": {"create_button": "[data-automation='customers-create']"},
                    }
                ],
            }
        ],
    }
    snapshot = CapabilitySnapshot(version=demo_manifest["version"], manifest_json=json.dumps(demo_manifest))
    session.add(snapshot)
    session.commit()
    return {"ok": True, "version": snapshot.version}


@app.get("/settings")
def get_settings(tenant_id: str, session: Session = Depends(get_session)):
    return ensure_default_settings(session, tenant_id)


@app.post("/settings")
def set_settings(payload: SettingsPayload, session: Session = Depends(get_session)):
    settings = session.exec(select(Settings).where(Settings.tenant_id == payload.tenant_id)).first()
    if not settings:
        settings = Settings(tenant_id=payload.tenant_id)

    settings.autonomy_mode = payload.autonomy_mode
    settings.scopes = ",".join(payload.scopes)
    settings.kill_switch = payload.kill_switch
    settings.policy_json = json.dumps(payload.policy)
    settings.outlook_connected = payload.outlook_connected
    settings.require_manual_learnalyze_login = payload.require_manual_learnalyze_login
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings


@app.get("/agent/manifest")
def agent_manifest(session: Session = Depends(get_session)):
    return capabilities_latest(session)


@app.post("/agent/dispatch")
def agent_dispatch(payload: DispatchRequest, session: Session = Depends(get_session)):
    session.add(
        AuditLog(
            tenant_id="shared",
            event_type="dispatch_called",
            payload_json=json.dumps(payload.model_dump()),
            entity_id=payload.action_id,
        )
    )
    session.commit()
    return {
        "ok": True,
        "action_id": payload.action_id,
        "idempotency_key": payload.idempotency_key,
        "performed_as": payload.on_behalf_of,
    }
