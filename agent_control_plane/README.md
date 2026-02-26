# ARX Agent Control Plane (MVP)

Dette er en kørende MVP-backend, der implementerer kerne-delene af den specificerede ARX Agent Control Plane:

- Email ingestion og triage (`/emails`, `/tasks/from-email`)
- Planning/job orchestration (`/jobs`, `/jobs/plan/{task_id}`)
- Approvals (`/approvals/{id}/approve|reject`)
- Audit stream (`/audit`)
- Capability self-discovery (`/capabilities/latest`, `/capabilities/rescan`, `/agent/manifest`)
- Generic action dispatch gateway (`/agent/dispatch`)
- Tenant settings for autonomy/scopes/policies + kill switch (`/settings`)

## Vigtig forretningsregel implementeret

Platform-login til LearnAlyze holdes **manuelt** på brugersiden (`require_manual_learnalyze_login=true` som default), mens Outlook-forbindelse kan sættes i settings (`outlook_connected=true`).

## Kør lokalt

```bash
cd agent_control_plane
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```

## Bemærkninger

- Persistence er SQLite for MVP.
- Manifest-rescan bruger en demo-generator; i produktion erstattes med pull fra webappens capability manifest.
- Dispatch-endpointet er bevidst generisk/stabilt for self-discovery designet.
