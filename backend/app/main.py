from fastapi import FastAPI
from app.api import users  # Example router import

app = FastAPI(title="AI Prompt Studio API")

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "Welcome to AI Prompt Studio API"}
