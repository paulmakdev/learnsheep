from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.stat import OutboundProgressResponse
from app.services.stat_service import get_ordered_progress
from app.core.database import get_db
from app.core.info import get_current_user

router = APIRouter(prefix="/stat", tags=["stat"])


@router.get("/progress", response_model=OutboundProgressResponse, status_code=200)
def get_progress(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return get_ordered_progress(db, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
