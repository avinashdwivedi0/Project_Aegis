# Project Aegis

Project Aegis is an evidence-based, multi-agent software quality assessment platform.

## Local development

Backend:

```powershell
cd apps/api
poetry install
poetry run uvicorn app.main:app --reload
```

The backend health endpoint is available at `http://localhost:8000/api/v1/health`.

Frontend:

```powershell
cd apps/web
npm install
npm run dev
```
