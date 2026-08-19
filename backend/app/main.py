from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.dependencies import engine
from app.api import users, auth   # ← add auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="AI Prompt Studio API",
    description="Full-stack tool for managing, versioning and testing LLM prompts",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth.router)          # ← Authentication routes
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Prompt Studio API",
        "docs": "/docs",
        "version": "0.1.0",
    }