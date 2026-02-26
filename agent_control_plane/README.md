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

## Test

```bash
pytest -q
```

## Bemærkninger

- Persistence er SQLite for MVP.
- Manifest-rescan bruger en demo-generator; i produktion erstattes med pull fra webappens capability manifest.
- Dispatch-endpointet er bevidst generisk/stabilt for self-discovery designet.
