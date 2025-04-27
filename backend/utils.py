from sqlalchemy.orm import Session
from typing import List
import backend.models as models
import backend.schemas as schemas
from datetime import date, timedelta


def get_dsdon_xin_nghi_by_nhanvien_id(db: Session, nhanvien_id: int) -> List[schemas.DonXinNghiPresent]:
    """
    Lấy tất cả các đơn xin nghỉ phép của nhân viên có id = nhanvien_id.
    Chỉ trả về các trường ngaytao, lydo, và trangthai.

    Args:
        db (Session): Phiên làm việc với cơ sở dữ liệu.
        nhanvien_id (int): ID của nhân viên.

    Returns:
        List[DonXinNghi]: Danh sách các đơn xin nghỉ phép với các trường ngaytao, lydo, và trangthai.
    """
    # Truy vấn chỉ lấy các trường cần thiết
    don_xin_nghi_list = db.query(
        models.DonXinNghi.ngaytao,
        models.DonXinNghi.lydo,
        models.DonXinNghi.trangthai
    ).filter(
        models.DonXinNghi.NhanVienid == nhanvien_id
    ).order_by( models.DonXinNghi.ngaytao.desc()).all()

    # Chuyển đổi kết quả truy vấn thành danh sách schema DonXinNghi
    return [schemas.DonXinNghiPresent(ngaytao=don.ngaytao, lydo=don.lydo, trangthai= don.trangthai) for don in don_xin_nghi_list]

def check_don_xin_nghi_by_nhanvien_id_and_lich_lam_id(db: Session, nhanvien_id: int, lichlam_id: int) -> bool:
    """
    Kiểm tra xem đơn xin nghỉ đã tồn tại hay chưa.

    Args:
        db (Session): Phiên làm việc với cơ sở dữ liệu.
        nhanvien_id (int): ID của nhân viên.
        lichlam_id (int): ID của lịch làm việc.

    Returns:
        bool: True nếu đơn xin nghỉ đã tồn tại, False nếu không.
    """
    don_xin_nghi = db.query(models.DonXinNghi).filter(
        models.DonXinNghi.NhanVienid == nhanvien_id,
        models.DonXinNghi.LichLamid == lichlam_id
    ).first()
    return don_xin_nghi is not None

def get_dslich_lam_by_nhanvien_id(db: Session, nhanvien_id: int) -> List[schemas.LichLamPresent]:
    """
    Lấy tất cả các lịch làm việc của nhân viên có id = nhanvien_id, từ ngày mai trở đi.
    Chỉ trả về các trường ngaylam và tenca.

    Args:
        db (Session): Phiên làm việc với cơ sở dữ liệu.
        nhanvien_id (int): ID của nhân viên.

    Returns:
        List[LichLamPresent]: Danh sách các lịch làm việc từ ngày mai trở đi với ngaylam và tenca.
    """
    # Ngày mai
    tomorrow = date.today() + timedelta(days=1)

    # Truy vấn lịch làm việc từ ngày mai trở đi
    lich_lam_list = db.query(
        models.LichLam.id,
        models.LichLam.ngaylam,
        models.CaLam.tenca
    ).join(
        models.CaLam, models.LichLam.CaLamid == models.CaLam.id
    ).filter(
        models.LichLam.NhanVienid == nhanvien_id,
        models.LichLam.ngaylam >= tomorrow
    ).order_by(models.LichLam.ngaylam).all()

    # Chuyển đổi kết quả truy vấn thành danh sách LichLamPresent
    return [schemas.LichLamPresent( id= lich.id, ngaylam=lich.ngaylam, tenca=lich.tenca) for lich in lich_lam_list]

def create_don_xin_nghi(db: Session, don_xin_nghi: schemas.DonXinNghiCreate) -> None:
    """
    Tạo một đơn xin nghỉ phép mới.

    Args:
        db (Session): Phiên làm việc với cơ sở dữ liệu.
        don_xin_nghi (DonXinNghi): Đơn xin nghỉ phép mới.

    Returns:
        DonXinNghi: Đơn xin nghỉ phép đã được tạo.
    """
    db_don_xin_nghi = models.DonXinNghi(lydo=don_xin_nghi.lydo,
                                        trangthai=don_xin_nghi.trangthai,
                                        ngaytao=don_xin_nghi.ngaytao,
                                        NhanVienid=don_xin_nghi.NhanVienid,
                                        LichLamid=don_xin_nghi.LichLamid)
    db.add(db_don_xin_nghi)
    db.commit()
    db.refresh(db_don_xin_nghi)
