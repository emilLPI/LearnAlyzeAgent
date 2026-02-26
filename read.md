# read.md

Quick start for running LearnAlyzeAgent from the repository root.

## 1) Install dependencies

```bash
npm install
```

## 2) Start the web app

```bash
npm run dev
```

This command forwards to the `agent_control_plane` workspace and starts the static UI server.
When you see `ARX UI available at http://localhost:5173`, that means the server is running correctly (the terminal stays open by design).

Open this URL in your browser:

- <http://localhost:5173>

Stop the server with `Ctrl + C`.

## 3) Run backend for live agent API

The browser UI calls API endpoints such as `/jobs` and `/capabilities`. Start FastAPI in a second terminal:

```bash
cd agent_control_plane
python -m uvicorn app.main:app --reload
```

The npm UI server now proxies API requests to `http://127.0.0.1:8000` by default.

## If you get a package.json conflict / ENOENT

If your terminal says it cannot find `package.json`, make sure you are in the repo root (the folder that contains this file, `README.md`, and `package.json`):

```bash
pwd
# or on PowerShell:
Get-Location
```

Then run:

```bash
npm install
npm run dev
```

## Full backend option (single server)

If you prefer running only FastAPI (no npm static server), use:

```bash
cd agent_control_plane
python -m uvicorn app.main:app --reload
```

Open: <http://127.0.0.1:8000>
