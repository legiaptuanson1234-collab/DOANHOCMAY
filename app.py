import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# CẤU HÌNH GIAO DIỆN TRANG WEB
# ==========================================
st.set_page_config(page_title="AI Dự Báo Bãi Đỗ Xe", page_icon="🚗", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🚗 HỆ THỐNG GIÁM SÁT & DỰ BÁO CHỖ ĐỖ XE THÔNG MINH</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Module: Quản lý bãi đỗ PARK_01 - PARK_05 | Phát triển bởi: Lê Giáp Tuấn Sơn (SV27)</h4>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# NẠP MÔ HÌNH VÀ DỮ LIỆU ĐÃ LƯU TỪ Ổ D
# ==========================================
@st.cache_resource
def load_assets():
    model = joblib.load(r'D:\TGMT\DOANHOCMAY\lgbm_pymoo_TH1.pkl')
    scaler_X = joblib.load(r'D:\TGMT\DOANHOCMAY\scaler_X.pkl')
    scaler_y = joblib.load(r'D:\TGMT\DOANHOCMAY\scaler_y.pkl')
    features = joblib.load(r'D:\TGMT\DOANHOCMAY\feature_cols.pkl')
    targets = joblib.load(r'D:\TGMT\DOANHOCMAY\target_cols.pkl')
    df_demo = pd.read_csv(r'D:\TGMT\DOANHOCMAY\demo_data.csv')
    return model, scaler_X, scaler_y, features, targets, df_demo

try:
    model, scaler_X, scaler_y, feature_cols, target_cols, df_demo = load_assets()
except Exception as e:
    st.error("⚠️ Không tìm thấy file dữ liệu tại D:\\TGMT\\DOANHOCMAY\\. Vui lòng kiểm tra lại!")
    st.stop()

# ==========================================
# THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2933/2933880.png", width=150)
st.sidebar.header("⚙️ BẢNG ĐIỀU KHIỂN")
menu = st.sidebar.radio("Chọn Chức Năng:", ["📊 Thống kê Dữ liệu & Điểm số", "🔮 Cảnh báo Thời gian thực (Live)"])

if menu == "📊 Thống kê Dữ liệu & Điểm số":
    st.header("1. Dữ liệu Đầu vào (Raw Data)")
    st.write("Bảng dữ liệu mô phỏng thu thập từ hệ thống cảm biến (10 dòng gần nhất):")
    
    # Tạo bản sao để làm đẹp tên cột hiển thị trên Web
    df_display = df_demo.tail(10).copy()
    df_display.columns = [col.replace('_available_spaces', '') for col in df_display.columns]
    
    # Ép bảng dãn hết chiều ngang giao diện
    st.dataframe(df_display, use_container_width=True)
    
    st.header("2. Hiệu suất AI (Đã tối ưu bằng Thuật toán Di truyền)")
    
    # Ép tỷ lệ cột: Cột 1 rộng hơn (1.5) để chữ không bao giờ bị cắt
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
    col1.metric("Thuật toán", "LGBM + Pymoo")
    col2.metric("Sai số MAE", "3.53 chỗ")
    col3.metric("Sai số RMSE", "4.63 chỗ")
    col4.metric("Độ tin cậy R²", "91.66 %")
    st.success("💡 Đánh giá: Mô hình xuất sắc, dự báo lệch trung bình chưa đến 4 chỗ đỗ xe. Hoàn toàn đủ tiêu chuẩn triển khai thực tế!")

elif menu == "🔮 Cảnh báo Thời gian thực (Live)":
    st.header("Radar Giám Sát Chỗ Trống Trong 30 Phút Tới")
    
    st.write("Mô phỏng nhập liệu thời gian thực. Hãy chọn một thời điểm để AI tính toán:")
    row_idx = st.slider("Chọn dòng dữ liệu để test:", 0, len(df_demo)-1, 95)
    
    sample_data = df_demo.iloc[[row_idx]]
    current_time = sample_data['timestamp'].values[0] if 'timestamp' in sample_data.columns else f"Mốc thời gian #{row_idx}"
    st.info(f"🕒 **Đang quét tại thời điểm:** {current_time}")
    
    if st.button("🚀 Kích Hoạt AI Dự Báo", use_container_width=True):
        with st.spinner('Siêu máy tính đang tính toán...'):
            # Đưa dữ liệu qua Scaler
            X_input = sample_data[feature_cols]
            X_scaled = scaler_X.transform(X_input)
            
            # AI đưa ra phán đoán
            y_pred_scaled = model.predict(X_scaled)
            y_pred_real = np.maximum(0, np.round(scaler_y.inverse_transform(y_pred_scaled)))[0]
            y_actual_real = sample_data[target_cols].values[0]
            
            # Giao diện Cảnh báo
            st.markdown("### 🚦 HỆ THỐNG CẢNH BÁO TRUNG TÂM")
            cols = st.columns(5)
            for i, park_name in enumerate(target_cols):
                pred_val = int(y_pred_real[i])
                actual_val = int(y_actual_real[i])
                
                with cols[i]:
                    st.markdown(f"**{park_name.replace('available_spaces_', '')}**")
                    st.metric(label="Chỗ trống 30p tới", value=f"{pred_val} chỗ", delta=f"Hiện tại: {actual_val} chỗ", delta_color="off")
                    
                    if pred_val <= 10:
                        st.error("🚨 Sắp Đầy! Đề xuất đóng rào.")
                    elif pred_val <= 30:
                        st.warning("⚠️ Đang đông. Cử bảo vệ phân luồng.")
                    else:
                        st.success("✅ Vắng vẻ. Tiếp tục đón khách.")
            
            # Vẽ biểu đồ So sánh Thực tế vs Dự báo (Đã sửa lỗi chữ đè nhau & dọn rác bộ nhớ)
            st.markdown("---")
            st.markdown("### 📈 Biểu đồ đối chiếu trực quan")
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Ép tên cột ngắn gọn để chống lỗi tràn chữ
            x_labels = ['PARK_01', 'PARK_02', 'PARK_03', 'PARK_04', 'PARK_05']
            x_pos = np.arange(len(x_labels))
            width = 0.35
            
            ax.bar(x_pos - width/2, y_actual_real, width, label='Hiện hành (Thực tế)', color='darkgray')
            ax.bar(x_pos + width/2, y_pred_real, width, label='30 Phút tới (AI Dự báo)', color='#3498DB')
            
            ax.set_ylabel('Số chỗ trống', fontsize=11)
            ax.set_title('Biến động Chỗ trống Bãi đỗ xe: Hiện hành vs Dự báo', fontsize=13, fontweight='bold', pad=15)
            ax.set_xticks(x_pos)
            
            ax.set_xticklabels(x_labels, fontsize=11, fontweight='bold')
            ax.legend(loc='upper right')
            
            st.pyplot(fig)
            plt.close(fig) # Lệnh then chốt giúp web không bị treo khi bấm nhiều lần