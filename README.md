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

