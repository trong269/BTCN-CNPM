from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date, Time
from sqlalchemy.orm import relationship
from backend.database import Base

class NhanVien(Base):
    __tablename__ = "NhanVien"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    luongtheogio = Column(Integer, nullable=False)
    sdt = Column(String(15), nullable=False)
    email = Column(String(255), nullable=False)

    # Relationships
    lich_lams = relationship("LichLam", back_populates="nhan_vien")
    don_xin_nghis = relationship("DonXinNghi", back_populates="nhan_vien")

class CaLam(Base):
    __tablename__ = "CaLam"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenca = Column(String(255), nullable=False)
    giobatdau = Column(Time(6), nullable=False)
    gioketthuc = Column(Time(6), nullable=False)
    hesoluong = Column(Float(10), nullable=False)
    phucap = Column(Integer, nullable=False)

    # Relationships
    lich_lams = relationship("LichLam", back_populates="ca_lam")

class LichLam(Base):
    __tablename__ = "LichLam"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ngaylam = Column(Date, nullable=False)
    NhanVienid = Column(Integer, ForeignKey("NhanVien.id"))
    CaLamid = Column(Integer, ForeignKey("CaLam.id"))

    # Relationships
    nhan_vien = relationship("NhanVien", back_populates="lich_lams")
    ca_lam = relationship("CaLam", back_populates="lich_lams")
    don_xin_nghis = relationship("DonXinNghi", back_populates="lich_lam")

class DonXinNghi(Base):
    __tablename__ = "DonXinNghi"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lydo = Column(String(255), nullable=False)
    trangthai = Column(String(255), nullable=False)
    ngaytao = Column(Date, nullable=False)
    NhanVienid = Column(Integer, ForeignKey("NhanVien.id"))
    LichLamid = Column(Integer, ForeignKey("LichLam.id"))

    # Relationships
    nhan_vien = relationship("NhanVien", back_populates="don_xin_nghis")
    lich_lam = relationship("LichLam", back_populates="don_xin_nghis")
