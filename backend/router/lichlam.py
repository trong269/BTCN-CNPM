from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
import backend.schemas as schemas
from backend.database import get_db
from backend.utils import get_dslich_lam_by_nhanvien_id

router = APIRouter(
    prefix="/lichlam",
    tags=["LichLam"]
)

@router.get("/", response_model=List[schemas.LichLamPresent])
def get_all_lich_lam(nhanvien_id: int, db: Session = Depends(get_db)):
    """
    API để lấy toàn bộ lịch làm của một nhân viên, chỉ lấy lịch làm của ngày mai trở đi.
    """
    # Lấy danh sách lịch làm của nhân viên
    lich_lam_list = get_dslich_lam_by_nhanvien_id(db, nhanvien_id)
    return lich_lam_list