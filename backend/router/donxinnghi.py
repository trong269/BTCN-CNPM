from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import backend.schemas as schemas
import backend.models as models
from backend.database import get_db
from backend.utils import get_dsdon_xin_nghi_by_nhanvien_id, create_don_xin_nghi, check_don_xin_nghi_by_nhanvien_id_and_lich_lam_id

router = APIRouter(
    prefix="/donxinnghi",
    tags=["DonXinNghi"]
)

@router.get("/", response_model=List[schemas.DonXinNghiPresent])
def get_all_don_xin_nghi(nhanvien_id: int, db: Session = Depends(get_db)):
    """
    API để lấy toàn bộ đơn xin nghỉ của một nhân viên.
    """
    don_xin_nghi_list = get_dsdon_xin_nghi_by_nhanvien_id(db, nhanvien_id)
    return don_xin_nghi_list

@router.post("/")
def create_new_don_xin_nghi(don_xin_nghi: schemas.DonXinNghiCreate, db: Session = Depends(get_db)):
    """
    API để tạo một đơn xin nghỉ mới.
    """
    try:
        create_don_xin_nghi(db, don_xin_nghi)
        return {"success": True, "message": "Đơn xin nghỉ đã được tạo thành công."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/check")
def check_don_xin_nghi(nhanvien_id: int, lichlam_id: int, db: Session = Depends(get_db)):
    """
    API để kiểm tra xem đơn xin nghỉ đã tồn tại hay chưa.
    """
    ok = check_don_xin_nghi_by_nhanvien_id_and_lich_lam_id(db, nhanvien_id, lichlam_id)
    
    if ok:
        return {"exists": True}
    else:
        return {"exists": False}