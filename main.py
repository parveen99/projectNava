import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.database import Base, master_engine

# create server
app = FastAPI(
    title="Organization Management API",
    description="REST API for managing organizations with dynamic databases",
    version="1.0.0"
)

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# handle versioning and routing
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"message": "Organization Management API is running!"}


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    Base.metadata.create_all(bind=master_engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

