"""
OSINT Search Service
Orchestrates: adapters → analysis → database persistence
"""
from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.adapters.orchestrator import run_all_adapters
from app.adapters.base import AdapterFinding
from app.services.analysis import analyse
from app.db.models.osint import Search, Finding, Report, SearchStatus, RiskLevel as DBRiskLevel
from app.db.schemas.osint import SearchRequest


async def create_search(db: AsyncSession, payload: SearchRequest) -> Search:
    """Create a new search record in DB with 'running' status."""
    search = Search(
        query=payload.query,
        entity_type=payload.entity_type,
        status=SearchStatus.running,
    )
    db.add(search)
    await db.flush()
    return search


async def execute_search(db: AsyncSession, search: Search) -> Search:
    """Run all adapters, analyse results, persist findings, update search record."""
    try:
        raw_findings: List[AdapterFinding] = await run_all_adapters(
            search.query, search.entity_type.value
        )

        analysis = analyse(search.query, raw_findings)

        for f in analysis["findings"]:
            db_finding = Finding(
                search_id=search.id,
                adapter=f.adapter,
                category=f.category.value,
                title=f.title,
                description=f.description,
                source_url=f.source_url,
                raw_data=f.raw_data if isinstance(f.raw_data, dict) else None,
                confidence=f.confidence,
                risk_level=DBRiskLevel(f.risk_level.value),
                is_mock=f.is_mock,
                fetched_at=f.fetched_at,
            )
            db.add(db_finding)

        search.status = SearchStatus.completed
        search.risk_score = analysis["risk_score"]
        search.risk_level = DBRiskLevel(analysis["risk_level"].value)
        search.confidence_score = analysis["confidence_score"]
        search.summary = analysis["summary"]
        search.completed_at = datetime.utcnow()

        await db.flush()
    except Exception as exc:
        search.status = SearchStatus.failed
        search.summary = f"Search failed: {exc}"
        await db.flush()

    return search


async def get_search_by_id(db: AsyncSession, search_id: UUID) -> Search | None:
    result = await db.execute(
        select(Search)
        .options(selectinload(Search.findings))
        .where(Search.id == search_id)
    )
    return result.scalar_one_or_none()


async def list_searches(db: AsyncSession, limit: int = 50) -> List[Search]:
    result = await db.execute(
        select(Search).order_by(Search.created_at.desc()).limit(limit)
    )
    return result.scalars().all()


async def save_report(
    db: AsyncSession,
    search_id: UUID,
    fmt: str,
    content: str | None = None,
    file_path: str | None = None,
) -> Report:
    report = Report(
        search_id=search_id,
        format=fmt,
        content=content,
        file_path=file_path,
    )
    db.add(report)
    await db.flush()
    return report
