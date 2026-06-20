# 🚗 HỆ THỐNG GIÁM SÁT & DỰ BÁO CHỖ ĐỖ XE THÔNG MINH (PARK_01 - PARK_05)

## 📌 Giới thiệu Đề tài
Đồ án giải quyết bài toán dự báo chuỗi thời gian: **Dự đoán số chỗ đỗ còn trống sau 30 phút cho 5 bãi đỗ xe (PARK_01 đến PARK_05)**.
Mục tiêu là tối ưu hóa việc quản lý bãi đỗ, giảm thời gian tìm kiếm chỗ đỗ của người dùng và hỗ trợ hệ thống cảnh báo phân luồng tự động.

* **Thực hiện:** [Tên của bạn] (Mã SV: [Mã Sinh Viên của bạn])
* **Mô hình chính:** Thuật toán LightGBM kết hợp Thuật toán Di truyền (Pymoo) để tự động hóa việc tinh chỉnh siêu tham số.
* **Kỹ thuật đánh giá & Giải thích:** Áp dụng Rolling Window (Walk-Forward Validation) để kiểm định độ ổn định và sử dụng thư viện SHAP để giải thích quyết định của mô hình.
* **Giao diện:** Ứng dụng Web trực quan được xây dựng bằng Streamlit.

---

## 📊 Kết Quả Đánh Giá Mô Hình (Sau Tối Ưu)
Mô hình LightGBM tối ưu đạt hiệu năng xuất sắc trên tập dữ liệu kiểm thử:
* **MAE (Sai số tuyệt đối trung bình):** 3.53 chỗ đỗ
* **RMSE (Sai số căn phương trung bình):** 4.63 chỗ đỗ
* **R² Score (Độ tin cậy):** 91.66%

---

## 📂 Cấu Trúc Mã Nguồn
```text
└── DOANHOCMAY/
    ├── DAHM.ipynb          # Notebook chứa toàn bộ quy trình: tiền xử lý, huấn luyện, tối ưu Pymoo và phân tích SHAP.
    ├── app.py              # Mã nguồn giao diện Web Dashboard (Streamlit).
    ├── demo_data.csv       # Bộ dữ liệu mẫu (100 chu kỳ gần nhất) dùng để mô phỏng thực tế.
    ├── lgbm_pymoo_TH1.pkl  # File mô hình LightGBM đã được huấn luyện tối ưu.
    ├── scaler_X.pkl        # File chuẩn hóa dữ liệu đầu vào.
    ├── scaler_y.pkl        # File chuẩn hóa dữ liệu đầu ra.
    ├── feature_cols.pkl    # Danh sách các biến đầu vào.
    └── target_cols.pkl     # Danh sách các biến mục tiêu (5 bãi đỗ).