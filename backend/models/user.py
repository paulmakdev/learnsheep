from sqlalchemy import Column, String, DateTime, Enum, Boolean
import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Role(enum.Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    PARENT = 'parent'
    LOCAL_ADMIN = 'local-admin'
    ADMIN = 'admin'

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    anonymous_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_salted_password = Column(String, nullable=False)
    role = Column(Enum(Role, name='role'), nullable=False, default='student')
    display_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_source = Column(String)
    gdpr_consent_at = Column(DateTime(timezone=True), nullable=True)
    data_deletion_requested_at = Column(DateTime(timezone=True), nullable=True)
    

