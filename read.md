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

## Full backend option

If you want API + UI from FastAPI instead of the static npm flow:

```bash
cd agent_control_plane
python -m uvicorn app.main:app --reload
```

Open: <http://127.0.0.1:8000>
