from app.models.user import User
from app.schemas.me import BasicInfoResponse


def get_basic_user_info(current_user: User) -> BasicInfoResponse:
    return {
        "email": current_user.email,
        "role": current_user.role,
        "display_name": current_user.display_name,
        "created_at": current_user.created_at.isoformat(),
    }
