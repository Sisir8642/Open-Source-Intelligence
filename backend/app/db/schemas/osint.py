from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from app.db.models.osint import EntityType, RiskLevel, SearchStatus


# ── Request Schemas ──────────────────────────────────────────────
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500, description="Company or individual name")
    entity_type: EntityType = Field(..., description="'company' or 'individual'")


# ── Response Schemas ─────────────────────────────────────────────
class FindingOut(BaseModel):
    id: UUID
    adapter: str
    category: str
    title: str
    description: Optional[str]
    source_url: Optional[str]
    raw_data: Optional[Any]
    confidence: float
    risk_level: RiskLevel
    is_mock: bool
    fetched_at: datetime

    model_config = {"from_attributes": True}


class SearchOut(BaseModel):
    id: UUID
    query: str
    entity_type: EntityType
    status: SearchStatus
    risk_level: RiskLevel
    risk_score: float
    confidence_score: float
    summary: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    findings: List[FindingOut] = []

    model_config = {"from_attributes": True}


class SearchSummary(BaseModel):
    id: UUID
    query: str
    entity_type: EntityType
    status: SearchStatus
    risk_level: RiskLevel
    risk_score: float
    created_at: datetime
    finding_count: int = 0

    model_config = {"from_attributes": True}


class ReportOut(BaseModel):
    id: UUID
    search_id: UUID
    format: str
    content: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportRequest(BaseModel):
    format: str = Field("markdown", pattern="^(pdf|markdown)$")
