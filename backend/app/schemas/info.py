from pydantic import BaseModel
from typing import Optional


class DeviceInfo(BaseModel):
    browser: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    device: Optional[str] = None
