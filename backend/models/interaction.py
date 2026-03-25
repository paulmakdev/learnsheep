from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, Integer, Index
import enum
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class InteractionLog(Base):
    __tablename__ = 'interactions'

    id              = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # Who
    user_id         = Column(UUID, ForeignKey('users.id'), nullable=True)  # null if anonymous
    session_id      = Column(UUID, nullable=False)   # groups events within a visit
    anonymous_id    = Column(UUID, nullable=False)   # persistent even before login
    
    # What
    event_type      = Column(String, nullable=False)  # 'page_view', 'click', 'form_submit'
    event_category  = Column(String)                  # 'navigation', 'content', 'commerce'
    
    # Where
    page_url        = Column(String)
    page_path       = Column(String)                  # just /products/123, no domain
    referrer_url    = Column(String)
    
    # Context
    properties      = Column(JSONB)                   # event-specific payload
    
    # Device / environment
    ip_address      = Column(INET)
    user_agent      = Column(String)
    device_type     = Column(String)                  # 'mobile', 'desktop', 'tablet'
    browser         = Column(String)
    os              = Column(String)
    screen_width    = Column(Integer)
    screen_height   = Column(Integer)
    
    # Timing
    created_at      = Column(DateTime(timezone=True), default=func.now())
    client_ts       = Column(DateTime(timezone=True), nullable=True)             # timestamp from the browser
    server_ts       = Column(DateTime(timezone=True), default=func.now())  # when server received it

    __table_args__ = (
        # Used to analyze an individual user's path through the website
        Index("idx_user_session", "user_id", "session_id"),
    )