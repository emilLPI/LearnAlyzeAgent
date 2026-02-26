# ARX Agent Control Plane (MVP Webapp)

Dette er nu en **kørende webapp** (ikke kun API), så du kan åbne den i browseren og styre flowet:

- Inbox (emails → tasks)
- Jobs (plan/retry/abort)
- Capabilities (rescan/latest)
- Settings (Outlook connect + manuel LearnAlyze login-regel)

## Vigtig forretningsregel implementeret

Platform-login til LearnAlyze holdes **manuelt** på brugersiden (`require_manual_learnalyze_login=true`), mens Outlook-forbindelse kan sættes i settings (`outlook_connected=true`).

## Kør lokalt

```bash
cd agent_control_plane
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Åbn derefter i browser:

- Webapp UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## API (udsnit)

- `GET/POST /emails`
- `POST /tasks/from-email`
- `POST /jobs/plan/{task_id}`
- `GET /jobs`, `POST /jobs/{id}/abort`, `POST /jobs/{id}/retry`
- `POST /approvals/{id}/approve|reject`
- `GET /audit`
- `GET /capabilities/latest`, `POST /capabilities/rescan`
- `GET/POST /settings`
- `GET /agent/manifest`, `POST /agent/dispatch`

## Test

```bash
pytest -q
```
