# LearnAlyzeAgent

Dette repo bruger en root `package.json`, så `npm install` i repo-roden virker.

## Fra repo-roden (Windows/PowerShell eller terminal)

```bash
npm install
npm run dev
```

Det starter ARX Control Plane UI fra workspace `agent_control_plane`.

## Alternativt direkte i app-mappen

```bash
cd agent_control_plane
npm install
npm run dev
```


Se også `read.md` for en kort fejlfindingsguide til `npm install`/`npm run dev`.

Tip: Når `npm run dev` viser `ARX UI available at http://localhost:5173`, så kører serveren korrekt.
Hold terminalen åben og åbn URL'en i din browser. Stop med `Ctrl + C`.


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

