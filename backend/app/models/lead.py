"""Lead and related models."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.enums import (
    Intent,
    LeadStatus,
    LeadTemperature,
    PropertyType,
    Timeline,
    TransactionType,
)


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True
    )

    intent: Mapped[Intent] = mapped_column(
        Enum(Intent, name="intent_enum"), nullable=False, default=Intent.OTHER
    )
    transaction_type: Mapped[TransactionType | None] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum"), nullable=True
    )
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, name="lead_status_enum"),
        nullable=False,
        default=LeadStatus.NEW,
        index=True,
    )
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    temperature: Mapped[LeadTemperature | None] = mapped_column(
        Enum(LeadTemperature, name="lead_temperature_enum"), nullable=True, index=True
    )
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="leads")
    property_requirement: Mapped["PropertyRequirement | None"] = relationship(
        "PropertyRequirement",
        back_populates="lead",
        uselist=False,
        cascade="all, delete-orphan",
    )
    qualifications: Mapped[list["LeadQualification"]] = relationship(
        "LeadQualification", back_populates="lead", cascade="all, delete-orphan"
    )
    assignments: Mapped[list["LeadAssignment"]] = relationship(
        "LeadAssignment", back_populates="lead", cascade="all, delete-orphan"
    )
    status_history: Mapped[list["LeadStatusHistory"]] = relationship(
        "LeadStatusHistory", back_populates="lead", cascade="all, delete-orphan"
    )
    follow_ups: Mapped[list["FollowUp"]] = relationship(
        "FollowUp", back_populates="lead", cascade="all, delete-orphan"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="lead"
    )

    def __repr__(self) -> str:
        return f"<Lead id={self.id} status={self.status} score={self.score}>"


class PropertyRequirement(Base):
    __tablename__ = "property_requirements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    property_type: Mapped[PropertyType | None] = mapped_column(
        Enum(PropertyType, name="property_type_enum"), nullable=True
    )
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    budget_min: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    budget_max: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="NGN")
    additional_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    timeline: Mapped[Timeline | None] = mapped_column(
        Enum(Timeline, name="timeline_enum"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    lead: Mapped["Lead"] = relationship("Lead", back_populates="property_requirement")


class LeadQualification(Base):
    __tablename__ = "lead_qualifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature: Mapped[LeadTemperature] = mapped_column(
        Enum(LeadTemperature, name="qualification_temperature_enum"), nullable=False
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    qualified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    lead: Mapped["Lead"] = relationship("Lead", back_populates="qualifications")


class SalesRep(Base):
    __tablename__ = "sales_reps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    assignments: Mapped[list["LeadAssignment"]] = relationship(
        "LeadAssignment", back_populates="sales_rep"
    )
    follow_ups: Mapped[list["FollowUp"]] = relationship(
        "FollowUp", back_populates="sales_rep"
    )


class LeadAssignment(Base):
    __tablename__ = "lead_assignments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sales_rep_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sales_reps.id", ondelete="RESTRICT"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="assignments")
    sales_rep: Mapped["SalesRep"] = relationship("SalesRep", back_populates="assignments")


class LeadStatusHistory(Base):
    __tablename__ = "lead_status_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )

    old_status: Mapped[LeadStatus | None] = mapped_column(
        Enum(LeadStatus, name="history_old_status_enum"), nullable=True
    )
    new_status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, name="history_new_status_enum"), nullable=False
    )
    changed_by: Mapped[str] = mapped_column(String(50), nullable=False)  # SYSTEM / user id / etc.
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    lead: Mapped["Lead"] = relationship("Lead", back_populates="status_history")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sales_rep_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sales_reps.id", ondelete="SET NULL"), nullable=True
    )

    follow_up_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="PENDING", index=True
    )  # PENDING / COMPLETED / CANCELLED / OVERDUE

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    lead: Mapped["Lead"] = relationship("Lead", back_populates="follow_ups")
    sales_rep: Mapped["SalesRep | None"] = relationship(
        "SalesRep", back_populates="follow_ups"
    )
