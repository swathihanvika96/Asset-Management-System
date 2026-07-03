from fastapi import FastAPI

from app.core.database import Base, engine

# Import models
from app.models.user import User
from app.models.asset import Asset
from app.models.allocation import Allocation

# Import routers
from app.routes.auth import router as auth_router
from app.routes.asset import router as asset_router
from app.routes.allocation import router as allocation_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Asset Management System",
    description="Backend API for Asset Management using FastAPI",
    version="1.0.0"
)

# Include Routers
app.include_router(auth_router)
app.include_router(asset_router)
app.include_router(allocation_router)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Asset Management System API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "OK",
        "message": "Application is running successfully."
    }