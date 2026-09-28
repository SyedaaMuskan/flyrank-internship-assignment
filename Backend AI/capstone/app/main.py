from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.routers import (
    auth,
    submissions,
    tenants,
    widgets,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FlyRank Capstone API",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(tenants.router)
app.include_router(widgets.router)
app.include_router(submissions.router)


@app.get("/")
def root():
    return {
        "message": "FlyRank Capstone API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }