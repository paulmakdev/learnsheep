from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, Index
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class SubscriptionStatus(enum.Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"


class CancelEnumReason(enum.Enum):
    UNSPECIFIED = "unspecified"


class SubscriptionType(enum.Enum):
    NO_SUBSCRIPTION = "no-subscription"
    LEARNER = "learner"
    STUDENT = "student"


class BillingFrequency(enum.Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(
        Enum(SubscriptionStatus, name="subscription-status"),
        nullable=False,
        default=SubscriptionStatus.INACTIVE,
    )
    billing_frequency = Column(
        Enum(BillingFrequency, name="billing-frequency"), nullable=False
    )
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    recurring = Column(Boolean, nullable=False, default=False)
    start_day = Column(DateTime(timezone=True), server_default=func.now())
    cancel_day = Column(DateTime(timezone=True), default=None)
    cancel_reason = Column(String, nullable=True)
    # TODO: when growing larger and having more subscriptions, should be able to come up with common reasons
    cancel_enum_reason = Column(
        Enum(CancelEnumReason, name="cancel-reason"),
        default=CancelEnumReason.UNSPECIFIED,
    )

    __table_args__ = (Index("idx_user_id", "user_id"),)
