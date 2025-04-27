import requests
import pandas as pd
from datetime import date

# Địa chỉ gốc của FastAPI backend (thay đổi nếu cần)
BACKEND_URL = "http://127.0.0.1:8000"

# ----- Hàm gọi API thực tế -----

def get_lich_lam_viec_available_api(nhanvien_id: int):
    """Lấy danh sách lịch làm việc có thể nghỉ từ backend FastAPI"""
    try:
        response = requests.get(f"{BACKEND_URL}/lichlam/", params={"nhanvien_id": nhanvien_id}, timeout=5)
        response.raise_for_status()
        lich_lam_list = response.json()  # API trả về danh sách lịch làm việc
        return lich_lam_list
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API lấy lịch làm việc: {e}")
        return []  # Trả về danh sách rỗng nếu có lỗi

def get_danh_sach_don_api(nhanvien_id: int):
    """Lấy danh sách đơn xin nghỉ từ backend FastAPI"""
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(f"{BACKEND_URL}/donxinnghi/", params={"nhanvien_id": nhanvien_id}, timeout=5)
        response.raise_for_status()
        data_list = response.json()  # API trả về danh sách đơn dưới dạng JSON

        # Nếu không có dữ liệu, trả về DataFrame rỗng
        if not data_list:
            return pd.DataFrame(columns=['Ngày tạo', 'Ngày xin nghỉ', 'Ca xin nghỉ', 'Lý do', 'Trạng thái'])

        # Chuyển đổi dữ liệu thành DataFrame
        processed_data = []
        for item in data_list:
            processed_data.append({
                "Ngày tạo": item.get("ngaytao"),
                "Ngày xin nghỉ": item.get("ngayxinnghi"),
                "Ca xin nghỉ": item.get("caxinnghi"),
                "Lý do": item.get("lydo"),
                "Trạng thái": "Đã duyệt" if item.get("trangthai") else "Chưa duyệt"
            })

        # Tạo DataFrame từ danh sách đã xử lý
        df = pd.DataFrame(processed_data)

        # Định dạng cột "Ngày tạo" và "Ngày xin nghỉ" thành kiểu ngày tháng
        if "Ngày tạo" in df.columns:
            df["Ngày tạo"] = pd.to_datetime(df["Ngày tạo"], errors="coerce").dt.strftime('%d/%m/%Y')
        if "Ngày xin nghỉ" in df.columns:
            df["Ngày xin nghỉ"] = pd.to_datetime(df["Ngày xin nghỉ"], errors="coerce").dt.strftime('%d/%m/%Y')

        return df

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API lấy danh sách đơn: {e}")
        # Trả về DataFrame rỗng nếu có lỗi
        return pd.DataFrame(columns=['Ngày tạo', 'Ngày xin nghỉ', 'Ca xin nghỉ', 'Lý do', 'Trạng thái'])

def check_don_xin_nghi_api(nhanvien_id: int, lichlam_id: int):
    """Kiểm tra xem đơn xin nghỉ đã tồn tại hay chưa"""
    try:
        response = requests.get(f"{BACKEND_URL}/donxinnghi/check", params={"nhanvien_id": nhanvien_id, "lichlam_id": lichlam_id}, timeout=5)
        response.raise_for_status()
        return response.json()  # API trả về {"exists": True/False}
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API kiểm tra đơn: {e}")
        return {"exists": False}  # Trả về False nếu có lỗi

def submit_don_xin_nghi_api(ly_do: str, nhanvien_id: int, lichlam_id: int):
    """Gửi đơn xin nghỉ lên backend FastAPI"""
    payload = {
        "lydo": ly_do,
        "trangthai": "đang chờ",  # Mặc định trạng thái là "Chưa duyệt"
        "ngaytao": date.today().isoformat(),
        "NhanVienid": nhanvien_id,
        "LichLamid": lichlam_id
    }
    try:
        response = requests.post(f"{BACKEND_URL}/donxinnghi/", json=payload, timeout=10)
        response.raise_for_status()
        return response.json()  # API trả về {"success": True/False, "message": "..."}
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API gửi đơn: {e}")
        return {"success": False, "message": f"Lỗi kết nối backend: {e}"}