from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import os

from app.db.session import get_db
from app.db.models.osint import Report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{report_id}/download")
async def download_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Download a previously generated PDF report."""
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.format == "markdown":
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(
            content=report.content or "",
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="osint-report-{report_id}.md"'},
        )

    if report.format == "pdf" and report.file_path and os.path.exists(report.file_path):
        return FileResponse(
            path=report.file_path,
            media_type="application/pdf",
            filename=f"osint-report-{report_id}.pdf",
        )

    raise HTTPException(status_code=404, detail="Report file not found")
