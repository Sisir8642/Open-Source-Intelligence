from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.db.schemas.osint import SearchRequest, SearchOut, SearchSummary, ReportOut, ReportRequest
from app.services import search_service, report as report_service
from app.db.models.osint import Search, Finding

router = APIRouter(prefix="/searches", tags=["searches"])


@router.post("/", response_model=SearchOut, status_code=201)
async def create_search(
    payload: SearchRequest,
    db: AsyncSession = Depends(get_db),
):

    search = await search_service.create_search(db, payload)
    search = await search_service.execute_search(db, search)
    await db.commit()
    search = await search_service.get_search_by_id(db, search.id)
    return search


@router.get("/", response_model=List[SearchSummary])
async def list_searches(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """List past searches (search history)."""
    searches = await search_service.list_searches(db, limit)
    result = []
    for s in searches:
        result.append(SearchSummary(
            id=s.id,
            query=s.query,
            entity_type=s.entity_type,
            status=s.status,
            risk_level=s.risk_level,
            risk_score=s.risk_score,
            created_at=s.created_at,
            finding_count=len(s.findings) if hasattr(s, "findings") and s.findings else 0,
        ))
    return result


@router.get("/{search_id}", response_model=SearchOut)
async def get_search(
    search_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    search = await search_service.get_search_by_id(db, search_id)
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    return search


@router.post("/{search_id}/report", response_model=ReportOut)
async def generate_report(
    search_id: UUID,
    payload: ReportRequest,
    db: AsyncSession = Depends(get_db),
):
    search = await search_service.get_search_by_id(db, search_id)
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")

    findings = search.findings or []

    if payload.format == "markdown":
        content = report_service.generate_markdown(search, findings)
        report = await search_service.save_report(
            db, search_id, "markdown", content=content
        )
        await db.commit()
        return report

    elif payload.format == "pdf":
        file_path = report_service.generate_pdf(search, findings)
        content = f"/reports/{search_id}.pdf"  # public URL hint
        report = await search_service.save_report(
            db, search_id, "pdf", content=content, file_path=file_path
        )
        await db.commit()
        return report

    raise HTTPException(status_code=400, detail="Invalid format. Use 'markdown' or 'pdf'.")


@router.delete("/{search_id}", status_code=204)
async def delete_search(
    search_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    search = await search_service.get_search_by_id(db, search_id)
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    await db.delete(search)
    await db.commit()
