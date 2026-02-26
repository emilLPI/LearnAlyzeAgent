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
