# ARX Agent Control Plane (MVP Webapp)

Nu kan du både:

1. Køre UI med npm.
2. Åbne og se LearnAlyze-vinduet direkte fra control plane UI.
3. Se et tydeligt "what the agent learned" overblik (capability insights).

## Kør webapp med npm

### Fra repo-roden (fix for ENOENT/package.json)

Hvis du står i repo-roden (som i din PowerShell fejl), kan du nu køre direkte:

```bash
npm install
npm run dev
```

Dette bruger root `package.json` og starter UI-workspace automatisk.

### Direkte i app-mappen

```bash
cd agent_control_plane
npm install
npm run dev
```

Åbn derefter: `http://127.0.0.1:5173`

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

## LearnAlyze login og credentials

- I UI findes en **LearnAlyze Login Window** sektion.
- LearnAlyze embeds ikke længere i iframe (for at undgå browser-fejlsiden), fordi target-sitet blokerer framing via sikkerhedsheaders.
- Du åbner i stedet `https://app-eu-learnalyze.azurewebsites.net/` i nyt vindue/tab direkte fra UI.
- Du kan gemme **email** i browser session storage som login-hjælp (password gemmes ikke).
- Kravet fastholdes: LearnAlyze login er stadig manuelt (`require_manual_learnalyze_login=true`).

## Agent learning/selv-opdagelse

UI viser nu en dedikeret "How the agent works + what it learned" sektion baseret på:

- `GET /capabilities/insights` (snapshot count, learned pages/actions, recent versions)
- `GET /capabilities/latest` (seneste manifest)

## API (udsnit)

- `GET/POST /emails`
- `POST /tasks/from-email`
- `POST /jobs/plan/{task_id}`
- `GET /jobs`, `POST /jobs/{id}/abort`, `POST /jobs/{id}/retry`
- `POST /approvals/{id}/approve|reject`
- `GET /audit`
- `GET /capabilities/latest`, `POST /capabilities/rescan`, `GET /capabilities/insights`
- `GET/POST /settings`
- `GET /agent/manifest`, `POST /agent/dispatch`


## AI integration (where to set it up)

Set AI integration in the **backend environment** (the terminal where you start FastAPI):

```bash
export AI_API_KEY="<your-key>"
export AI_PROVIDER="openai-compatible"
export AI_BASE_URL="https://api.openai.com/v1"
export AI_MODEL="gpt-4o-mini"
python -m uvicorn app.main:app --reload
```

PowerShell example:

```powershell
$env:AI_API_KEY = "<your-key>"
$env:AI_PROVIDER = "openai-compatible"
$env:AI_BASE_URL = "https://api.openai.com/v1"
$env:AI_MODEL = "gpt-4o-mini"
python -m uvicorn app.main:app --reload
```

Then open the UI and use **AI Integration Setup** → **Refresh AI Status**.

- API endpoint: `GET /ai/integration/status`
- Behavior: if `AI_API_KEY` is set, email triage tries AI classification first; if unavailable, it safely falls back to local rule-based classification.


## SSL browser error on localhost (ERR_SSL_PROTOCOL_ERROR)

If your browser shows `ERR_SSL_PROTOCOL_ERROR`, you most likely opened `https://localhost:...`.
This project runs on plain HTTP locally by default.

Use:

- `http://localhost:5173` for npm UI server
- `http://127.0.0.1:8000` for FastAPI server

Do **not** use `https://` unless you have explicitly configured local TLS certificates.



## Run fully functional dashboard (UI + API together)

Use one command to start both backend and UI:

```bash
npm run dev:full
```

Then open: `http://localhost:5173` (HTTP, not HTTPS).

## Test

```bash
pytest -q
```

## Bemærkninger

- Persistence er SQLite for MVP.
- Manifest-rescan bruger en demo-generator; i produktion erstattes med pull fra webappens capability manifest.
- Dispatch-endpointet er bevidst generisk/stabilt for self-discovery designet.
