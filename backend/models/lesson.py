from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, Integer
import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    s3_key = Column(String)
    subject_metadata = Column(JSONB)

class Module(Base):
    __tablename__ = 'modules'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    s3_key = Column(String)
    module_metadata = Column(JSONB)

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    s3_key = Column(String)
    lesson_metadata = Column(JSONB)

class ModuleLesson(Base):
    __tablename__ = "module_lessons"
    
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), primary_key=True)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), primary_key=True)
    order = Column(Integer)

class SubjectModule(Base):
    __tablename__ = "subject_modules"
    
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), primary_key=True)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), primary_key=True)
    order = Column(UUID(as_uuid=True))