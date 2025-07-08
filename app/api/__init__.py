from fastapi import APIRouter
from app.api import organization, auth


api_router = APIRouter()
api_router.include_router(organization.router)
api_router.include_router(auth.router) 