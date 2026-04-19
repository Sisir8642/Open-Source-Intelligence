import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float, JSON, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.session import Base


class EntityType(str, enum.Enum):
    company = "company"
    individual = "individual"


class RiskLevel(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
    unknown = "unknown"


class SearchStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Search(Base):
    __tablename__ = "searches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    entity_type: Mapped[EntityType] = mapped_column(SAEnum(EntityType), nullable=False)
    status: Mapped[SearchStatus] = mapped_column(SAEnum(SearchStatus), default=SearchStatus.pending)
    risk_level: Mapped[RiskLevel] = mapped_column(SAEnum(RiskLevel), default=RiskLevel.unknown)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    findings: Mapped[list["Finding"]] = relationship("Finding", back_populates="search", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship("Report", back_populates="search", cascade="all, delete-orphan")


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("searches.id"), nullable=False, index=True)
    adapter: Mapped[str] = mapped_column(String(100), nullable=False)      
    category: Mapped[str] = mapped_column(String(50), nullable=False)     
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)            
    risk_level: Mapped[RiskLevel] = mapped_column(SAEnum(RiskLevel), default=RiskLevel.unknown)
    is_mock: Mapped[bool] = mapped_column(default=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    search: Mapped["Search"] = relationship("Search", back_populates="findings")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("searches.id"), nullable=False)
    format: Mapped[str] = mapped_column(String(20), nullable=False)        
    file_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    search: Mapped["Search"] = relationship("Search", back_populates="reports")
