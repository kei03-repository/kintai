from fastapi import FastAPI

from .db import engine
from .models.models import Base
from .router.attendance import router as attendance_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="勤怠管理アプリ")
app.include_router(attendance_router)
