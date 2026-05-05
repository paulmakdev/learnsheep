from pydantic import BaseModel


class BasicInfoResponse(BaseModel):
    email: str
    role: str
    display_name: str
    created_at: str
