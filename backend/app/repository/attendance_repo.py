from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.models import Attendance
from ..schemas.schemas import AttendanceCreate, AttendanceUpdate


def _to_payload(schema_obj) -> dict:
    if hasattr(schema_obj, "model_dump"):
        return schema_obj.model_dump()
    return schema_obj.dict()


def _save_and_refresh(db: Session, attendance: Attendance) -> Attendance:
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def _first_day_of_next_month(year: int, month: int) -> date:
    next_year = year + (month // 12)
    next_month = (month % 12) + 1
    return date(next_year, next_month, 1)


def get_attendance_by_date(db: Session, target_date: date) -> Optional[Attendance]:
    return db.query(Attendance).filter(Attendance.date == target_date).first()


def list_attendances_by_month(db: Session, year: int, month: int) -> List[Attendance]:
    first_day = date(year, month, 1)
    first_day_next_month = _first_day_of_next_month(year, month)
    return (
        db.query(Attendance)
        .filter(Attendance.date >= first_day)
        .filter(Attendance.date < first_day_next_month)
        .order_by(Attendance.date)
        .all()
    )


def create_attendance(db: Session, attendance_in: AttendanceCreate) -> Attendance:
    attendance = Attendance(**_to_payload(attendance_in))
    return _save_and_refresh(db, attendance)


def update_attendance(db: Session, attendance: Attendance, updates: AttendanceUpdate) -> Attendance:
    update_payload = _to_payload(updates)
    for field, value in update_payload.items():
        setattr(attendance, field, value)
    return _save_and_refresh(db, attendance)


def upsert_attendance(db: Session, attendance_in: AttendanceCreate) -> Attendance:
    record = get_attendance_by_date(db, attendance_in.date)
    if record:
        updates = AttendanceUpdate(**_to_payload(attendance_in))
        return update_attendance(db, record, updates)
    return create_attendance(db, attendance_in)
