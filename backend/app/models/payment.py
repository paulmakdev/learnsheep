from sqlalchemy import Column, String, DateTime, Enum, Boolean, Index, Integer, ForeignKey, Text, Index
import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base



class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey('subscriptions.id'), default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    failure_reason = Column(Text, nullable=True)
    provider = Column(String(50), nullable=False)
    provider_payment_id = Column(String(255), unique=True, nullable=True)
    provider_invoice_id = Column(String(255), unique=True, nullable=True)
    invoice_url = Column(Text, nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('ix_payments_user_id', 'user_id'),
        Index('ix_payments_subscription_id', 'subscription_id'),
    )
