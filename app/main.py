import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routers import users, daily_logs, entries, activity, insights, auth
from app.seeds.seed_runner import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    if os.getenv("SEED_DB", "false").lower() == "true":
        seed_database()
    
    yield
    
    # on shutdown
    pass

app = FastAPI(
    title="Lifestyle Tracker API",
    description="Track daily activities, mood, and get AI-powered insights",
    version="0.1.0",
    lifespan=lifespan 
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in PROD
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(daily_logs.router)
app.include_router(entries.router)
app.include_router(activity.router)
app.include_router(insights.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    """API root endpoint."""
    return {
        "message": "Welcome to the Lifestyle Tracker API",
        "documentation": "/docs",
        "version": "0.1.0"
    }