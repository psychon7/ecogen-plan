"""FastAPI application entry point."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.middleware.audit import AuditLogMiddleware
from backend.routers import credits, dashboard, projects, reviews, skills
from shared.config import settings

logging.basicConfig(level=settings.log_level)

app = FastAPI(
    title="LEED v5 Automation Platform",
    version="0.1.0",
    description="Restate + OpenAI Agents SDK powered LEED credit automation",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditLogMiddleware)

# Routers
app.include_router(projects.router, prefix="/api")
app.include_router(credits.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(skills.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
