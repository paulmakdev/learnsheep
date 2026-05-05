from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.me import BasicInfoResponse
from app.services.me_service import get_basic_user_info
from app.core.info import get_current_user

router = APIRouter(prefix="/me", tags=["personal", "me"])


@router.get("/info", response_model=BasicInfoResponse, status_code=200)
def user_info(
    current_user=Depends(get_current_user),
):
    try:
        return get_basic_user_info(current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
