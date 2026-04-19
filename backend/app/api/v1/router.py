from fastapi import APIRouter
from app.api.v1.endpoints import searches, reports

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(searches.router)
api_router.include_router(reports.router)
