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


## AI integration

Set this in the FastAPI terminal before startup:

```bash
export AI_API_KEY="<your-key>"
export AI_MODEL="gpt-4o-mini"
python -m uvicorn app.main:app --reload
```

Check status from browser UI under **AI Integration Setup** or call `GET /ai/integration/status`.


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

