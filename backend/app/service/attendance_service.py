from typing import List

from sqlalchemy.orm import Session

from ..repository.attendance_repo import (
    list_attendances_by_month,
    upsert_attendance,
)
from ..schemas.schemas import AttendanceCreate, Attendance
from ..utils.excel_utils import export_attendance_to_excel


def save_attendance(db: Session, attendance_in: AttendanceCreate) -> Attendance:
    return upsert_attendance(db, attendance_in)


def get_monthly_attendances(db: Session, year: int, month: int) -> List[Attendance]:
    return list_attendances_by_month(db, year, month)


def export_monthly_excel(
    db: Session,
    year: int,
    month: int,
    template_path: str,
    output_dir: str,
) -> str:
    attendances = get_monthly_attendances(db, year, month)
    output_path = export_attendance_to_excel(
        attendances=attendances,
        year=year,
        month=month,
        template_path=template_path,
        output_dir=output_dir,
    )
    return output_path
