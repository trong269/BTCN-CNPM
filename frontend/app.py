import streamlit as st
import pandas as pd
from datetime import date


nhanvien_id = 1  # giả sử với nhân viên có id = 1 

# Import các hàm tiện ích từ utils.py
from utils import get_danh_sach_don_api as get_danh_sach_don
from utils import get_lich_lam_viec_available_api as get_lich_lam_viec_available
from utils import submit_don_xin_nghi_api as submit_don_xin_nghi
from utils import check_don_xin_nghi_api as check_don_xin_nghi

# --- Khởi tạo Session State ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'main'

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None
if 'ly_do' not in st.session_state:
    st.session_state.ly_do = ""

# --- Định nghĩa các hàm render cho từng View ---

def render_main_view():
    """Hiển thị giao diện chính"""
    st.title("🏠 Trang Chủ - Hệ Thống phân công chấm công nhân viên part time")
    
    if st.button("Đơn xin nghỉ", type="primary"):
        st.session_state.current_view = 'list_requests'
        st.rerun()

def render_list_requests_view():
    """Hiển thị danh sách đơn nghỉ và nút tạo đơn"""
    st.title("📄 Quản Lý Đơn Xin Nghỉ")

    if st.button("➕ Tạo đơn", type="primary"):
        st.session_state.selected_date = None
        st.session_state.ly_do = ""
        st.session_state.current_view = 'create_form'
        st.rerun()

    st.markdown("---")
    st.subheader("Danh sách đơn đã tạo")

    df_don_nghi = get_danh_sach_don(nhanvien_id=nhanvien_id)  # Thay `1` bằng ID nhân viên thực tế
    if df_don_nghi.empty:
        st.info("Chưa có đơn xin nghỉ nào được tạo.")
    else:
        df_display = df_don_nghi.copy()
        if 'NgayTao' in df_display.columns:
            try:
                df_display['NgayTao'] = pd.to_datetime(df_display['NgayTao'])
                df_display['NgayTao'] = df_display['NgayTao'].dt.strftime('%d/%m/%Y')
            except Exception as e:
                st.warning(f"Không thể định dạng ngày: {e}")

        st.dataframe(df_display, use_container_width=True)

    st.markdown("---")
    if st.button("⬅️ Quay lại trang chủ"):
        st.session_state.current_view = 'main'
        st.rerun()

def render_create_form_view():
    """Hiển thị form tạo đơn mới"""
    st.title("📝 Tạo Đơn Xin Nghỉ Mới")

    with st.form("create_leave_request_form", clear_on_submit=False):
        st.subheader("1. Chọn lịch xin nghỉ")
        lichlam = get_lich_lam_viec_available(nhanvien_id=nhanvien_id)  # Thay `1` bằng ID nhân viên thực tế
        if not lichlam:
            st.error("Không thể tải danh sách ngày làm việc. Không thể tạo đơn.")
            if st.form_submit_button("Hủy bỏ"):
                st.session_state.current_view = 'list_requests'
                st.rerun()
            return

        lich_options = {f'{lich['ngaylam']}  ({lich['tenca']})': int(lich['id']) for lich in lichlam}
        selected_lich_str = st.selectbox(
            "Chọn lịch bạn muốn xin nghỉ:",
            options=lich_options.keys(),
            key='form_select_date'
        )
        selected_lich_id = lich_options.get(selected_lich_str) if selected_lich_str else None
        exists_don = check_don_xin_nghi(nhanvien_id=nhanvien_id, lichlam_id=selected_lich_id)['exists']

        st.subheader("2. Nhập lý do")
        ly_do = st.text_area(
            "Nhập lý do chi tiết:",
            height=100,
            placeholder="Ví dụ: Nghỉ ốm, Có việc gia đình đột xuất...",
            key='form_ly_do'
        )

        st.markdown("---")

        submitted = st.form_submit_button("💾 Lưu đơn", type="primary")
        cancelled = st.form_submit_button("❌ Hủy bỏ")

        if cancelled:
            st.info("Đã hủy thao tác tạo đơn.")
            st.session_state.current_view = 'list_requests'
            st.rerun()

        if submitted:
            if not selected_lich_id:
                st.warning("Vui lòng chọn ngày nghỉ.")
            if exists_don:
                st.warning("Đã tồn tại đơn xin nghỉ cho lịch làm này. Vui lòng chọn lịch khác.")
            elif not ly_do or not ly_do.strip():
                st.warning("Vui lòng nhập lý do xin nghỉ.")
            else:
                with st.spinner('Đang gửi đơn...'):
                    result = submit_don_xin_nghi(ly_do.strip(), nhanvien_id=nhanvien_id, lichlam_id= selected_lich_id)  # Thay `1` bằng ID lịch làm thực tế

                if result.get("success"):
                    st.success(result.get("message", "Gửi đơn thành công!"))
                    st.balloons()
                    st.session_state.current_view = 'list_requests'
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(result.get("message", "Gửi đơn thất bại. Vui lòng thử lại."))

# --- Logic chính để chọn View cần render ---
if st.session_state.current_view == 'main':
    render_main_view()
elif st.session_state.current_view == 'list_requests':
    render_list_requests_view()
elif st.session_state.current_view == 'create_form':
    render_create_form_view()
else:
    st.session_state.current_view = 'main'
    st.rerun()