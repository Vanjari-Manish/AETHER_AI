from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db, check_health
from app.core.response import send_success
from app.config.settings import settings

router = APIRouter()

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
def health_check(db: Session = Depends(get_db)):
    db_health = check_health(db)
    
    health_data = {
        "status": "healthy" if db_health["status"] == "healthy" else "unhealthy",
        "service": "GPO API Gateway",
        "version": "1.3.0-ALPHA",
        "environment": settings.ENV,
        "database": db_health
    }
    return send_success(health_data)
