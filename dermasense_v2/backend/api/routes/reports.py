from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from core.security import current_patient_id
from models.report import ReportRequest
from services.report_service import generate_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("")
@router.post("/", include_in_schema=False)
async def create_report(request: ReportRequest, patient_id: str = Depends(current_patient_id)):
    """Returns a PDF for the caller's own session. Patients can only ever get their own data."""
    pdf = await generate_report(patient_id, request.session_id)
    if pdf is None:
        raise HTTPException(404, "Patient not found")
    return Response(pdf, media_type="application/pdf",
                    headers={"Content-Disposition": 'attachment; filename="dermasense-report.pdf"'})
