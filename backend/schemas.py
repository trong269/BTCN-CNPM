from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

# Schema cho NhanVien
class NhanVienBase(BaseModel):
    username: str
    email: str
    sdt: str
    luongtheogio: int

class NhanVienCreate(NhanVienBase):
    password: str

class NhanVien(NhanVienBase):
    id: int

    class Config:
        orm_mode = True

# Schema cho CaLam
class CaLamBase(BaseModel):
    tenca: str
    giobatdau: time
    gioketthuc: time
    hesoluong: float
    phucap: int

class CaLamCreate(CaLamBase):
    pass

class CaLam(CaLamBase):
    id: int

    class Config:
        orm_mode = True

# Schema cho LichLam
class LichLamBase(BaseModel):
    ngaylam: date
    NhanVienid: int
    CaLamid: int

class LichLamCreate(LichLamBase):
    pass

class LichLamPresent(BaseModel):
    id: int
    ngaylam: date
    tenca: str

class LichLam(LichLamBase):
    id: int

    class Config:
        orm_mode = True

# Schema cho DonXinNghi
class DonXinNghiBase(BaseModel):
    lydo: str
    trangthai: str
    ngaytao: date
    NhanVienid: int
    LichLamid: int

class DonXinNghiCreate(DonXinNghiBase):
    pass

class DonXinNghiPresent(BaseModel):
    ngaytao: date
    lydo: str
    trangthai: str

class DonXinNghi(DonXinNghiBase):
    id: int

    class Config:
        orm_mode = True