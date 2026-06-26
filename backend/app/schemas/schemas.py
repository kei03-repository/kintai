from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional


class AttendanceBase(BaseModel):
    date: date
    category1: Optional[str] = None
    category2: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    break_minutes: Optional[int] = Field(default=60)
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    category1: Optional[str] = None
    category2: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    break_minutes: Optional[int] = None
    notes: Optional[str] = None


class AttendanceInDBBase(AttendanceBase):
    id: int
    excel_file: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Attendance(AttendanceInDBBase):
    pass
