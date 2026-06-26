from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime
from sqlalchemy.sql import func
from ..db import Base


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    category1 = Column(String(100), nullable=True)
    category2 = Column(String(100), nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    break_minutes = Column(Integer, nullable=False, default=60)
    notes = Column(Text, nullable=True)
    excel_file = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
