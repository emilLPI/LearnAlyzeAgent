# ARX Agent Control Plane (MVP Webapp)

Nu kan du køre UI direkte via **npm** i terminalen.

## Kør webapp med npm

```bash
cd agent_control_plane
npm install
npm run dev
```

Åbn derefter: `http://127.0.0.1:5173`

> NPM-varianten server UI (`app/static`) som frontend-preview.

## Kør fuld backend + webapp via FastAPI

```bash
cd agent_control_plane
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Åbn derefter:

- Webapp UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## Vigtig forretningsregel implementeret

LearnAlyze login holdes manuelt (`require_manual_learnalyze_login=true`), mens Outlook connection kan aktiveres (`outlook_connected=true`).

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
