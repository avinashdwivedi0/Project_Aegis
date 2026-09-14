from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.routers.analysis import router as analysis_router
from app.api.routers.auth import router as auth_router
from app.api.routers.findings import router as findings_router
from app.api.routers.projects import router as projects_router
from app.api.routers.recommendations import router as recommendations_router
from app.api.routers.reports import router as reports_router
from app.db.session import engine

app = FastAPI(title="Project Aegis API", version="0.1.0")


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(findings_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException) -> dict:
    return {"success": False, "error": {"message": exception.detail}}


@app.get("/")
async def root() -> dict[str, object]:
    return {"success": True, "data": {"name": "Project Aegis API", "docs": "/docs"}}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)


@app.get("/api/v1/health")
async def health() -> dict[str, object]:
    return {"success": True, "data": {"status": "ok"}}
