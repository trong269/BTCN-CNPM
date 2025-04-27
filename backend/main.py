from fastapi import FastAPI
from backend.router import donxinnghi, lichlam
from backend.database import Base, engine

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Quản lý nhân viên Part Time",
)

# Tạo các bảng trong cơ sở dữ liệu (nếu chưa tồn tại)
Base.metadata.create_all(bind=engine)

# Đăng ký các router
app.include_router(donxinnghi.router)
app.include_router(lichlam.router)

# Điểm bắt đầu của ứng dụng
@app.get("/")
def read_root():
    """
    Endpoint mặc định để kiểm tra ứng dụng.
    """
    return {"message": "Chào mừng đến với API Quản lý nhân viên!"}

