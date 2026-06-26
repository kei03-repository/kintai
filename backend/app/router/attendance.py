from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..configs import OUTPUT_DIR, TEMPLATE_SOURCE
from ..schemas.schemas import Attendance, AttendanceCreate
from ..service.attendance_service import (
    export_monthly_excel,
    get_monthly_attendances,
    save_attendance,
)

router = APIRouter(prefix="/api")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/attendances", response_model=Attendance)
def create_attendance(
    attendance_in: AttendanceCreate,
    db: Session = Depends(get_db),
) -> Attendance:
    return save_attendance(db, attendance_in)


@router.get("/attendances", response_model=List[Attendance])
def read_attendances(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
) -> List[Attendance]:
    return get_monthly_attendances(db, year, month)


@router.post("/attendances/export")
def export_attendances(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
):
    output_path = export_monthly_excel(
        db=db,
        year=year,
        month=month,
        template_path=TEMPLATE_SOURCE,
        output_dir=str(OUTPUT_DIR),
    )
    if not Path(output_path).exists():
        raise HTTPException(status_code=500, detail="Excel file could not be generated")
    return FileResponse(
        path=output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=Path(output_path).name,
    )
